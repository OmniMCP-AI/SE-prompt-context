import asyncio
from typing import Any, Dict, List, Optional, Callable
from dataclasses import dataclass
import json
from autogen import ConversableAgent, UserProxyAgent, GroupChat, GroupChatManager
from autogen.agentchat.contrib.gpt_assistant_agent import GPTAssistantAgent

# Reuse the pipeline classes from previous artifact
from tool_pipeline import PipelineData, ToolFilter, MCPToolFilter, ConversionFilter, ToolPipeline

class AutoGenPipelineAgent(ConversableAgent):
    """AutoGen agent that executes tool pipelines"""
    
    def __init__(
        self,
        name: str,
        pipeline: ToolPipeline,
        system_message: str = "You are a pipeline execution agent.",
        **kwargs
    ):
        super().__init__(
            name=name,
            system_message=system_message,
            **kwargs
        )
        self.pipeline = pipeline
        self.execution_history = []
        
        # Register the pipeline execution as a function
        self.register_function(
            function_map={
                "execute_pipeline": self._execute_pipeline_wrapper
            }
        )
    
    async def _execute_pipeline_wrapper(
        self,
        user_input: str,
        task_id: str,
        user_context: str = "",
        metadata: Dict = None
    ) -> Dict[str, Any]:
        """Wrapper to execute pipeline and return results in AutoGen format"""
        
        initial_data = PipelineData(
            content=user_input,
            metadata=metadata or {},
            task_id=task_id,
            user_context=user_context
        )
        
        try:
            result = await self.pipeline.execute(initial_data)
            
            # Store execution history
            self.execution_history.append({
                "task_id": task_id,
                "input": user_input,
                "output": result.content,
                "metadata": result.metadata
            })
            
            return {
                "success": True,
                "result": result.content,
                "metadata": result.metadata,
                "task_id": task_id
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "task_id": task_id
            }

class PipelineCoordinatorAgent(ConversableAgent):
    """Coordinates multiple pipeline agents and manages tool chaining decisions"""
    
    def __init__(
        self,
        name: str = "pipeline_coordinator",
        pipeline_agents: Dict[str, AutoGenPipelineAgent] = None,
        **kwargs
    ):
        system_message = """You are a pipeline coordinator. Your job is to:
        1. Analyze user requests and determine which pipeline(s) to use
        2. Execute pipelines in the correct order
        3. Handle results and coordinate between different pipeline agents
        4. Provide final formatted responses to users
        
        Available functions:
        - route_to_pipeline: Route user request to appropriate pipeline
        - execute_sequential_pipelines: Execute multiple pipelines in sequence
        """
        
        super().__init__(
            name=name,
            system_message=system_message,
            **kwargs
        )
        
        self.pipeline_agents = pipeline_agents or {}
        
        # Register coordination functions
        self.register_function(
            function_map={
                "route_to_pipeline": self._route_to_pipeline,
                "execute_sequential_pipelines": self._execute_sequential_pipelines,
                "get_pipeline_capabilities": self._get_pipeline_capabilities
            }
        )
    
    def add_pipeline_agent(self, agent_name: str, agent: AutoGenPipelineAgent):
        """Add a pipeline agent to coordination"""
        self.pipeline_agents[agent_name] = agent
    
    async def _route_to_pipeline(
        self,
        user_request: str,
        task_id: str,
        preferred_pipeline: str = None
    ) -> Dict[str, Any]:
        """Route user request to appropriate pipeline agent"""
        
        if preferred_pipeline and preferred_pipeline in self.pipeline_agents:
            agent = self.pipeline_agents[preferred_pipeline]
            return await agent._execute_pipeline_wrapper(
                user_input=user_request,
                task_id=task_id,
                user_context=user_request
            )
        
        # Simple routing logic - can be enhanced with ML
        if any(keyword in user_request.lower() for keyword in ['crypto', 'token', 'address', 'symbol']):
            if 'crypto_pipeline' in self.pipeline_agents:
                agent = self.pipeline_agents['crypto_pipeline']
                return await agent._execute_pipeline_wrapper(
                    user_input=user_request,
                    task_id=task_id,
                    user_context=user_request
                )
        
        # Default to first available pipeline
        if self.pipeline_agents:
            first_agent = next(iter(self.pipeline_agents.values()))
            return await first_agent._execute_pipeline_wrapper(
                user_input=user_request,
                task_id=task_id,
                user_context=user_request
            )
        
        return {"success": False, "error": "No suitable pipeline found"}
    
    async def _execute_sequential_pipelines(
        self,
        user_request: str,
        task_id: str,
        pipeline_sequence: List[str]
    ) -> Dict[str, Any]:
        """Execute multiple pipelines in sequence - output of one becomes input of next"""
        
        current_input = user_request
        results = []
        
        for pipeline_name in pipeline_sequence:
            if pipeline_name not in self.pipeline_agents:
                return {"success": False, "error": f"Pipeline {pipeline_name} not found"}
            
            agent = self.pipeline_agents[pipeline_name]
            result = await agent._execute_pipeline_wrapper(
                user_input=current_input,
                task_id=f"{task_id}_{pipeline_name}",
                user_context=user_request
            )
            
            if not result.get("success", False):
                return result  # Return error immediately
            
            results.append(result)
            current_input = result["result"]  # Chain the output
        
        return {
            "success": True,
            "final_result": current_input,
            "pipeline_results": results,
            "task_id": task_id
        }
    
    def _get_pipeline_capabilities(self) -> Dict[str, List[str]]:
        """Return available pipelines and their capabilities"""
        capabilities = {}
        for name, agent in self.pipeline_agents.items():
            # Extract filter names from pipeline
            filter_names = [f.name for f in agent.pipeline.filters]
            capabilities[name] = filter_names
        return capabilities

class AutoGenPipelineFactory:
    """Factory to create AutoGen-compatible pipeline agents"""
    
    @staticmethod
    def create_crypto_pipeline_agent(
        search_best_tool_func: Callable,
        mcp_tools: Dict[str, Callable],
        llm_config: Dict = None
    ) -> AutoGenPipelineAgent:
        """Create crypto-specific pipeline agent"""
        
        # Build the pipeline
        pipeline = (ToolPipeline()
                   .pipe(MCPToolFilter("fetch_crypto_data", mcp_tools.get("fetch_crypto_data")))
                   .pipe(ConversionFilter(search_best_tool_func))
                   .pipe(MCPToolFilter("format_crypto_output", mcp_tools.get("format_crypto_output"))))
        
        return AutoGenPipelineAgent(
            name="crypto_pipeline_agent",
            pipeline=pipeline,
            system_message="I execute crypto data processing pipelines. I can fetch token data, convert addresses to symbols, and format outputs.",
            llm_config=llm_config
        )
    
    @staticmethod
    def create_generic_pipeline_agent(
        name: str,
        filters: List[ToolFilter],
        system_message: str = None,
        llm_config: Dict = None
    ) -> AutoGenPipelineAgent:
        """Create generic pipeline agent from filters"""
        
        pipeline = ToolPipeline()
        for filter_obj in filters:
            pipeline.pipe(filter_obj)
        
        return AutoGenPipelineAgent(
            name=name,
            pipeline=pipeline,
            system_message=system_message or f"I execute {name} pipelines.",
            llm_config=llm_config
        )

class AutoGenPipelineSystem:
    """Complete system integrating pipelines with AutoGen"""
    
    def __init__(self, llm_config: Dict = None):
        self.llm_config = llm_config or {"model": "gpt-4"}
        self.coordinator = PipelineCoordinatorAgent(llm_config=self.llm_config)
        self.user_proxy = UserProxyAgent(
            name="user",
            human_input_mode="NEVER",
            code_execution_config=False
        )
        
    def add_pipeline(
        self,
        name: str,
        pipeline_agent: AutoGenPipelineAgent
    ):
        """Add a pipeline agent to the system"""
        self.coordinator.add_pipeline_agent(name, pipeline_agent)
    
    async def process_request(
        self,
        user_request: str,
        task_id: str = None,
        pipeline_name: str = None
    ) -> Dict[str, Any]:
        """Process user request through appropriate pipeline"""
        
        if task_id is None:
            task_id = f"task_{hash(user_request) % 10000}"
        
        # Route to specific pipeline or let coordinator decide
        return await self.coordinator._route_to_pipeline(
            user_request=user_request,
            task_id=task_id,
            preferred_pipeline=pipeline_name
        )
    
    def create_group_chat(self, additional_agents: List[ConversableAgent] = None) -> GroupChatManager:
        """Create AutoGen group chat with pipeline agents"""
        
        agents = [self.user_proxy, self.coordinator]
        agents.extend(self.coordinator.pipeline_agents.values())
        
        if additional_agents:
            agents.extend(additional_agents)
        
        group_chat = GroupChat(
            agents=agents,
            messages=[],
            max_round=10
        )
        
        return GroupChatManager(
            groupchat=group_chat,
            llm_config=self.llm_config
        )

# Usage Example
async def example_autogen_integration():
    """Example of how to use the pipeline system with AutoGen"""
    
    # Mock MCP tools
    async def mock_fetch_crypto_data(input_data):
        return {"address": input_data, "balance": 1000, "name": "Unknown Token"}
    
    async def mock_format_crypto_output(input_data):
        return f"Token: {input_data.get('symbol', input_data.get('name', 'Unknown'))} | Balance: {input_data.get('balance', 0)}"
    
    async def mock_search_best_tool(input_schema, user_context):
        async def address_to_symbol_converter(data):
            if isinstance(data, dict) and any('address' in str(k).lower() for k in data.keys()):
                data["symbol"] = "ETH"  # Mock conversion
            return data
        return address_to_symbol_converter
    
    # Setup
    llm_config = {"model": "gpt-4"}
    mcp_tools = {
        "fetch_crypto_data": mock_fetch_crypto_data,
        "format_crypto_output": mock_format_crypto_output
    }
    
    # Create pipeline system
    pipeline_system = AutoGenPipelineSystem(llm_config=llm_config)
    
    # Create and add crypto pipeline
    crypto_agent = AutoGenPipelineFactory.create_crypto_pipeline_agent(
        search_best_tool_func=mock_search_best_tool,
        mcp_tools=mcp_tools,
        llm_config=llm_config
    )
    
    pipeline_system.add_pipeline("crypto_pipeline", crypto_agent)
    
    # Process a request
    result = await pipeline_system.process_request(
        user_request="Get information for crypto address 0x1234567890abcdef1234567890abcdef12345678",
        task_id="crypto_001"
    )
    
    print("Pipeline Result:", result)
    
    # You can also use it in AutoGen group chat
    group_chat_manager = pipeline_system.create_group_chat()
    
    return result

# Integration with existing AutoGen agents
def integrate_with_existing_autogen_setup(existing_agents: List[ConversableAgent]):
    """Show how to integrate pipeline system with existing AutoGen setup"""
    
    # Create pipeline system
    pipeline_system = AutoGenPipelineSystem()
    
    # Add your pipeline agents
    # ... (create your specific pipeline agents)
    
    # Create group chat with existing agents + pipeline agents
    all_agents = existing_agents + [pipeline_system.coordinator] + list(pipeline_system.coordinator.pipeline_agents.values())
    
    group_chat = GroupChat(
        agents=all_agents,
        messages=[],
        max_round=20
    )
    
    return GroupChatManager(groupchat=group_chat, llm_config={"model": "gpt-4"})

if __name__ == "__main__":
    asyncio.run(example_autogen_integration())