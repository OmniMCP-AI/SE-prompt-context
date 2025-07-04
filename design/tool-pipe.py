import asyncio
from typing import Any, Dict, List, Optional, Protocol
from dataclasses import dataclass
from abc import ABC, abstractmethod
import json

@dataclass
class PipelineData:
    """Standard data format flowing through the pipeline - like stdin/stdout"""
    content: Any
    metadata: Dict[str, Any]
    task_id: str
    user_context: str

class ToolFilter(ABC):
    """Base filter class - each tool acts like a Unix filter"""
    
    def __init__(self, name: str):
        self.name = name
    
    @abstractmethod
    async def process(self, input_data: PipelineData) -> PipelineData:
        """Process input and return output - like reading stdin and writing stdout"""
        pass
    
    def should_process(self, input_data: PipelineData) -> bool:
        """Determine if this filter should process the data - like conditional execution"""
        return True

class MCPToolFilter(ToolFilter):
    """Wrapper for MCP tools to work as pipeline filters"""
    
    def __init__(self, tool_name: str, mcp_tool_function):
        super().__init__(tool_name)
        self.mcp_tool = mcp_tool_function
    
    async def process(self, input_data: PipelineData) -> PipelineData:
        # Call the actual MCP tool
        result = await self.mcp_tool(input_data.content)
        
        # Save to DB (your requirement)
        await self.save_to_db(input_data.task_id, self.name, result)
        
        # Return new pipeline data
        return PipelineData(
            content=result,
            metadata={**input_data.metadata, f"{self.name}_processed": True},
            task_id=input_data.task_id,
            user_context=input_data.user_context
        )
    
    async def save_to_db(self, task_id: str, tool_name: str, result: Any):
        # Your DB save logic here
        print(f"Saving {tool_name} result for task {task_id}")

class ConversionFilter(ToolFilter):
    """Smart converter filter - your crypto address to symbol example"""
    
    def __init__(self, search_best_tool_func):
        super().__init__("converter")
        self.search_best_tool = search_best_tool_func
    
    def should_process(self, input_data: PipelineData) -> bool:
        # Check if conversion is needed
        return self.needs_conversion(input_data.content)
    
    async def process(self, input_data: PipelineData) -> PipelineData:
        # Find best conversion tool
        conversion_tool = await self.search_best_tool(
            input_schema=self.get_schema(input_data.content),
            user_context=input_data.user_context
        )
        
        if conversion_tool:
            converted_content = await conversion_tool(input_data.content)
            return PipelineData(
                content=converted_content,
                metadata={**input_data.metadata, "converted": True, "converter": conversion_tool.name},
                task_id=input_data.task_id,
                user_context=input_data.user_context
            )
        
        return input_data  # Pass through if no conversion needed
    
    def needs_conversion(self, content: Any) -> bool:
        # Simple heuristic - check if content looks like crypto addresses
        if isinstance(content, str) and len(content) == 42 and content.startswith('0x'):
            return True
        if isinstance(content, dict) and any('address' in str(k).lower() for k in content.keys()):
            return True
        return False
    
    def get_schema(self, content: Any) -> Dict:
        # Extract schema information for search_best_tool
        return {"type": type(content).__name__, "sample": str(content)[:100]}

class ToolPipeline:
    """Unix-style pipeline for tool chaining"""
    
    def __init__(self):
        self.filters: List[ToolFilter] = []
    
    def add_filter(self, tool_filter: ToolFilter) -> 'ToolPipeline':
        """Add filter to pipeline - like | in Unix"""
        self.filters.append(tool_filter)
        return self
    
    def pipe(self, tool_filter: ToolFilter) -> 'ToolPipeline':
        """Alias for add_filter - more Unix-like"""
        return self.add_filter(tool_filter)
    
    async def execute(self, initial_data: PipelineData) -> PipelineData:
        """Execute the pipeline - data flows through each filter"""
        current_data = initial_data
        
        for filter_tool in self.filters:
            if filter_tool.should_process(current_data):
                print(f"Processing through {filter_tool.name}...")
                current_data = await filter_tool.process(current_data)
            else:
                print(f"Skipping {filter_tool.name} (conditions not met)")
        
        return current_data

class PipelineBuilder:
    """Factory for common pipeline patterns"""
    
    @staticmethod
    def create_crypto_pipeline(search_best_tool_func, mcp_tools: Dict[str, Any]) -> ToolPipeline:
        """Create a pipeline for crypto data processing"""
        return (ToolPipeline()
                .pipe(MCPToolFilter("fetch_token_data", mcp_tools["fetch_token_data"]))
                .pipe(ConversionFilter(search_best_tool_func))
                .pipe(MCPToolFilter("format_output", mcp_tools["format_output"])))
    
    @staticmethod
    def create_generic_pipeline(tool_configs: List[Dict]) -> ToolPipeline:
        """Create pipeline from configuration"""
        pipeline = ToolPipeline()
        
        for config in tool_configs:
            if config["type"] == "mcp_tool":
                pipeline.pipe(MCPToolFilter(config["name"], config["function"]))
            elif config["type"] == "converter":
                pipeline.pipe(ConversionFilter(config["search_function"]))
        
        return pipeline

# Usage Example
async def example_usage():
    """Example of how to use the pipeline system"""
    
    # Mock functions for demonstration
    async def mock_fetch_token_data(input_data):
        return {"address": "0x1234...abcd", "balance": 1000}
    
    async def mock_search_best_tool(input_schema, user_context):
        # Mock conversion tool that converts address to symbol
        async def address_to_symbol_converter(data):
            if isinstance(data, dict) and "address" in data:
                data["symbol"] = "ETH"  # Mock conversion
            return data
        return address_to_symbol_converter
    
    async def mock_format_output(input_data):
        return f"Token: {input_data.get('symbol', 'Unknown')} | Balance: {input_data.get('balance', 0)}"
    
    # Create MCP tools dictionary
    mcp_tools = {
        "fetch_token_data": mock_fetch_token_data,
        "format_output": mock_format_output
    }
    
    # Build pipeline
    pipeline = PipelineBuilder.create_crypto_pipeline(
        search_best_tool_func=mock_search_best_tool,
        mcp_tools=mcp_tools
    )
    
    # Create initial pipeline data
    initial_data = PipelineData(
        content="0x1234567890abcdef1234567890abcdef12345678",
        metadata={},
        task_id="task_001",
        user_context="User wants crypto token information"
    )
    
    # Execute pipeline
    result = await pipeline.execute(initial_data)
    
    print(f"Final result: {result.content}")
    print(f"Metadata: {result.metadata}")

# Alternative: One-liner pipeline creation (very Unix-like)
def create_simple_pipeline(tools):
    """Create pipeline with Unix-like syntax"""
    pipeline = ToolPipeline()
    for tool in tools:
        pipeline.pipe(tool)
    return pipeline

# Even simpler usage:
async def simple_example():
    # tool1 | converter | tool2
    pipeline = (ToolPipeline()
               .pipe(MCPToolFilter("tool1", lambda x: {"processed": x}))
               .pipe(ConversionFilter(lambda schema, context: None))  # Mock
               .pipe(MCPToolFilter("tool2", lambda x: f"Final: {x}")))
    
    data = PipelineData("input", {}, "task1", "user query")
    result = await pipeline.execute(data)
    return result

if __name__ == "__main__":
    asyncio.run(example_usage())
    