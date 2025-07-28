# Intelligent Workflow Platform Frontend Requirements Document

## 1. Product Overview

### 1.1 Frontend Positioning
Build a conversational workflow planning and execution interface that allows users to describe needs through natural language and view task decomposition, execution progress, and final results in real-time.

### 1.2 Core Interaction Philosophy
- **Conversation-driven**: All functions start from conversation; users only need to describe needs.
- **Process transparency**: Let users clearly see how AI decomposes and executes tasks.
- **Progressive interaction**: From simple to complex, gradually guide users to complete complex tasks.
- **Intelligent guidance**: Reduce user onboarding barriers through preset questions and suggestions.

### 1.3 Key Design Principles (Based on Pokee Experience Optimization)
- **Lower onboarding barriers**: Homepage provides rich example questions for users to quickly experience product capabilities.
- **Flexible execution control**: Support both step-by-step confirmation and one-click execution modes.
- **Conversation history management**: Intelligently suggest new conversations to avoid long history affecting effectiveness.
- **Error recovery friendly**: Support single-step retry without restarting the entire process.

## 2. Overall Interface Architecture

### 2.1 Main Interface Layout
Adopt a three-column layout with a focus on user guidance optimization:

- **Left Navigation Bar**:
  - Chat Interface (current conversation)
  - My Tasks (my tasks)
  - Scheduled Workflows (scheduled workflows) - important function displayed separately
  - Tool Center (tool center)
  - Authorizations (authorization management) - independent management page
  - Settings (settings)

- **Middle Conversation Area**:
  - Homepage guidance area: display example questions and product capability introduction
  - Conversation History (conversation history)
  - User input box and send button
  - Real-time message display area
  - Intelligent suggestion area (new conversation prompts, etc.)

- **Right Execution Panel**:
  - Execution Steps (execution steps)
  - Task decomposition display (support collapse/expand)
  - Real-time progress tracking
  - Single-step operation control
  - Result preview area

### 2.2 Homepage Guidance Design
**Example Question Cards**: Display categorized example questions below the input box:
- 📊 Data Analysis: "Analyze my sales data and generate monthly report"
- 📰 Information Collection: "Collect latest AI industry trends and organize into weekly report"
- 📱 Social Media: "Help me create multi-platform content about product launch"
- 🔄 Automation: "Set up project progress reminders every Monday morning"

**Product Capability Display**:
- Concise feature introduction
- Success case showcase
- Quick start guide

### 2.3 Welcome Page Design
**Initial visit welcome interface**: When users first visit or click "start new conversation", display dedicated welcome page:

**Page Layout**:
- Left: Navigation menu (maintain consistency)
- Middle: Welcome content area (occupy main space)
- Right: Simplified feature introduction or hidden

**Middle welcome area content**: 
🎉 Welcome to Intelligent Workflow Platform  
✨ You can create these types of tasks:
- 📊 Data Analysis & Reports
  - Sales data analysis and visualization
  - User behavior analysis reports
  - Financial data monthly summaries
- 📰 Information Collection & Organization
  - Industry trend tracking
  - Competitor analysis reports
  - News information summaries
- 📱 Content Creation & Publishing
  - Social media content generation
  - Multi-platform content distribution
  - Brand marketing copy
- 🔄 Automated Workflows
  - Scheduled task scheduling
  - Data synchronization backup
  - Notification reminder settings

[Start Creating] [View Examples] [Watch Tutorial]

### 2.4 Playback Case Display Area
**Excellent case playback functionality**: Add Playback case display area below conversation input box:

**Case Card Design**: 
📺 Excellent Case Playback
- 🎬 "AI News Weekly Report Auto-Generation" Creator: @Product Manager Wang Duration: 8 minutes | Success Rate: 95% [▶️ Watch Playback] [🔄 Copy & Use]
- 🎬 "Competitor Price Monitoring Alert" Creator: @E-commerce Operations Lisa Duration: 5 minutes | Success Rate: 98% [▶️ Watch Playback] [🔄 Copy & Use]
- 🎬 "Social Media Content Batch Publishing" Creator: @Marketing Director Alex Duration: 12 minutes | Success Rate: 92% [▶️ Watch Playback] [🔄 Copy & Use]
  
[View More Cases] [Submit My Case]

**Playback functionality**:
- Simulate real conversation and execution process
- Display input/output for each step
- Users can pause, fast forward, rewind
- Support parameter modification based on playback
- One-click copy entire workflow to current conversation

### 2.5 Responsive Design Requirements
- **Desktop**: Three-column layout, minimum width 1200px
- **Tablet**: Left sidebar collapsible, minimum width 768px
- **Mobile**: Single-column layout, drawer navigation, minimum width 375px

## 3. Core Function Interface Design

### 3.1 Conversation Interaction Area

#### 3.1.1 Message Display Components
- **User Message Style**:
  - Right-aligned, light blue background
  - Rounded bubble design, maximum width 70%
  - Support text, file upload, image display
  - Show send time

- **System Message Style**:
  - Left-aligned, light gray background
  - System avatar + message content
  - Support rich text display (bold, links, lists)
  - Display AI role identifier

#### 3.1.2 Core Responsibilities of Conversation Phases
- **Requirement Analysis and Task Planning**:
  - Understand user's real needs
  - Formulate detailed execution plans
  - Predict required tools and authorization
  - Confirm task details with user

- **Authorization Requirement Communication**:
  - Pre-identify all necessary authorizations
  - Clearly explain purpose and scope of each authorization
  - Provide choice of authorization timing
  - Unified completion of authorization confirmation process

- **Task Confirmation and Initiation**:
  - Final plan confirmation
  - Execution parameter setting
  - Start execution process

#### 3.1.3 Execution Mode Selection
**Execution mode selection** (referencing Pokee's step-by-step design):
📋 I will complete this task for you in 3 steps:
- 🔍 Search AI agent-related news (past 7 days)
- 📱 Collect large model application updates
- 🎯 Organize multimodal AI technology breakthroughs

⏱️ Estimated duration: 8-10 minutes 🔐 Authorization needed: Google Search, Notion Save, Gmail Send

**Authorization method**:
- ○ Complete authorization now (recommended) - uninterrupted execution process
- ○ Authorize during execution - flexible control, authorize when needed

**Execution method**:
- ○ Step-by-step confirmation (Step by Step) - each step requires your confirmation
- ○ One-click execution (Run All) - skip confirmation and execute directly

[Start Execution] [Modify Requirements]

#### 3.1.4 Intelligent Suggestion Mechanism
**Conversation History Management**: When conversation becomes too long, system proactively suggests:
💡 Tip: Current conversation history is long, may affect execution effectiveness  
Suggestion: [Start New Conversation] [Continue Current Conversation]

**Workflow Save Suggestion**: After successful task completion:
✅ Task Complete! This workflow executed well 💾 Save as scheduled task? [Set Scheduled Execution] [Save as Template] [Don't Save for Now]

#### 3.1.5 Special Message Types
- **Task Planning Message**: 
  📋 I will complete this task for you in 3 steps:
  - 🔍 Search AI agent-related news (past 7 days)
  - 📱 Collect large model application updates
  - 🎯 Organize multimodal AI technology breakthroughs
  - ⏱️ Estimated duration: 8-10 minutes 🛠 Tools needed: Google Search, Notion Save, Email Send
  [Start Execution] [Modify Requirements]

- **Authorization Request Message**: 
  ⚠️ Need your authorization to continue: 
  - Google Search API: Get latest news 
  - Notion API: Save report to your workspace 
  - Gmail API: Send report to team
  [One-click Authorization] [View Detailed Permissions]

- **Execution Complete Message**: 
  ✅ Task Complete! 
  📊 Collected 26 articles, covering: 
  - AI agent products: 12 articles 
  - Large model applications: 8 articles 
  - Multimodal technology: 6 articles
  📝 Generated 4000-word professional report 
  📧 Report sent to your email 
  🔗 [View Complete Report] [Save as Template] [Set Scheduled Task]

### 3.2 Execution Steps Panel

#### 3.2.1 Core Responsibilities of Right Panel
**Pure execution-oriented design**:
- Focus on task execution process display and control
- Real-time display of execution status and progress
- Provide execution-level operations and adjustments
- Handle exceptions and decisions during execution

#### 3.2.2 Step List Design
**Step Status Display**:
- ⏳ Waiting: Gray circle, step name in gray
- 🔄 Executing: Blue spinning animation, step name in blue
- ✅ Completed: Green checkmark, step name in green
- ❌ Failed: Red X, step name in red
- ⚠️ Needs Confirmation: Yellow exclamation mark, waiting for user action
- 🔐 Waiting for Authorization: Orange lock icon, needs user authorization (dynamic authorization mode)

**Step Control Buttons**: Display action buttons on the right side of each step:
- [▶️ Execute] - Start executing current step
- [🔄 Retry] - Re-execute failed step
- [⏸️ Pause] - Pause current execution
- [📋 Details] - View detailed information
- [✅ Confirm] - Confirm step results (step-by-step mode)
- [🔐 Authorize] - Handle dynamic authorization requests

#### 3.2.3 Step Detail Display
**Collapsible detail area**:
- ✅ 1. Search AI agent-related news [🔄 Retry] [📋 Details]
  └── 📥 Input: (click to expand) Keywords: AI agents, intelligent agents Time range: past 7 days 
  └── 📤 Output: (click to expand) 12 news articles 
  - OpenAI Agent Framework 2.0 release 
  - Anthropic intelligent agent new features 
  - Microsoft Copilot enterprise version upgrade 
  View complete list (5 items)

- 🔐 2. Save report to Notion [🔐 Authorize] [⏭️ Skip]
  └── ⚠️ Authorization status: (dynamic authorization mode) Need Notion write permission 
  Permission scope: specified workspace pages 
  [Authorize Now] [Modify Permissions] [Skip This Step]

#### 3.2.4 Execution Mode Support
- **Step-by-Step Mode**:
  - Each step pauses after completion, waiting for user confirmation
  - Display "waiting for confirmation" status
  - User can view results and decide to continue or modify

- **Run All Mode**:
  - Execute all steps continuously
  - Only pause for errors, user authorization needs, or confirmations
  - Real-time progress display; user can pause anytime

- **Dynamic Authorization Handling**:
  - When steps need authorization, handle in right panel
  - Don't interrupt overall execution flow
  - Provide skip options to maintain process flexibility

### 3.3 Authorization Management Design Logic

#### 3.3.1 Hybrid Authorization Strategy
**Core Design Philosophy**: User experience-first hybrid authorization mode
- **Authorization Timing Choice**:
  - Pre-authorization (recommended): Complete all necessary authorizations during conversation phase to ensure uninterrupted execution
  - Dynamic authorization (flexible): Handle unexpected authorization needs or user-chosen delayed authorization during execution

#### 3.3.2 Pre-authorization Flow in Conversation
**Authorization Requirement Prediction Display**:
🤖 I will complete the "AI Weekly Report Generation" task for you  
📋 Task Plan:
- 🔍 Search latest AI news (Google Search)
- 📝 Organize and analyze content (AI processing)
- 📄 Generate weekly report document (Notion save)
- 📧 Send email notification (Gmail send)

🔐 Need following authorizations: 
- Google Search API: Get latest AI news content 
- Notion API: Save weekly report to your workspace 
- Gmail API: Send weekly report email to team

**Authorization method**:
- ○ Complete authorization now (recommended) - uninterrupted execution 
- ○ Authorize during execution - flexible control, authorize when needed

[Authorize All Now] [Authorize During Execution] [Modify Requirements]

#### 3.3.3 Dynamic Authorization Handling During Execution
**Authorization scenarios during execution**: When user chooses "authorize during execution" or unexpected authorization needs arise:

**Authorization status in right execution panel**:
- 🔄 2. Save weekly report to Notion ⚠️ Waiting for authorization: Need Notion write permission
  - 📋 Permission description: 
    - Access permission: specific pages in specified workspace 
    - Operation permission: create and edit documents 
    - Data scope: only content related to this task
  [🔐 Authorize Now] [⏭️ Skip This Step] [📝 Modify Permission Scope]

#### 3.3.4 Unified Authorization Management Page
**Independent authorization center** (supporting both authorization modes):
- Display all authorized and pending tools
- Support batch authorization management
- Provide authorization history and usage statistics
- Fine-grained permission scope control

**Authorization Status Display**:
- 🔍 Google Search API Status: ✅ Authorized (pre-authorization) 
  - Authorization time: 2024-01-15 14:30 
  - Usage frequency: 12 times this month 
  [Manage Permissions] [Revoke Authorization]

- 📝 Notion API Status: ⏳ Pending Authorization (authorize during execution) 
  - Expected use: AI weekly report task 
  - Permission scope: specified page write access 
  [Authorize Now] [View Details]

### 3.4 Task Execution Confirmation Interface

#### 3.4.1 Pre-execution Confirmation
**Confirmation Information Display**:
📋 About to execute operations: 
- 📄 Generate 4000-word professional AI weekly report 
- 📧 Send report summary email to team@company.com 
- 🔗 Generate public sharing link 
- 📱 Create WeChat push message

📊 Report Overview: 
- 26 news articles covering AI agents, large model applications, multimodal AI 
- Identified 5 major events and 8 technology breakthroughs 
- Includes 3 data visualization charts 
- Provides next 3 months trend predictions

[Confirm Execution] [Modify Settings] [Preview Report] [Cancel]

#### 3.4.2 Execution Result Display
**Result Summary Cards**:
- Task completion status
- Key metrics display
- Generated content preview
- Follow-up action options

### 3.4 Scheduled Task Management Interface

#### 3.4.1 Scheduled Task List
**Scheduled Workflows page** (referencing Pokee's independent management):
- Calendar view and list view switching
- Real-time task status updates
- Execution history record viewing
- Centralized task management operations

**Task Card Design**:
📊 AI Weekly Report Generation 
- ⏰ Every Monday 09:00 execution 
- 📈 Success rate: 95% (19/20) 
- 📅 Next execution: 2024-01-22 09:00 
- Status: ✅ Running 
- Recent execution: 2024-01-15 09:00 - Success 
[Execute Now] [Modify Settings] [Pause] [View Details]

#### 3.4.2 Task Creation Optimization
**Create scheduled tasks from successful conversations**:
- Directly provide "set scheduled" option after conversation completion
- Pre-fill task parameters and configuration
- Intelligently suggest execution frequency
- One-click create scheduled task

#### 3.4.3 Task Status Monitoring
**Real-time Status Updates**:
- Real-time progress display for executing tasks
- Highlight failed tasks and provide solutions
- Display key metrics for successful tasks
- Support task execution history viewing

### 3.6 Tool Center Interface

#### 3.6.1 Tool Category Display
**Tool Category Cards**:
- 🔍 Search Tools (12 items) Google Search, Bing Search, Academic Search...
- 📄 Document Tools (8 items) Notion, Google Docs, Word Processing...
- 📧 Communication Tools (6 items) Gmail, Slack, WeChat Push...
- 📊 Data Tools (15 items) Excel Processing, Database Query, Chart Generation...

#### 3.6.2 Tool Detail Page
**Tool Information Display**:
- Tool name and icon
- Feature description and use cases
- Authorization status and permission description
- Usage statistics and success rate
- Related workflow templates

## 4. Interaction Detail Design

### 4.1 Loading and Waiting States

#### 4.1.1 Thinking State
**AI Thinking Animation**:
- Three bouncing dots animation
- "Understanding your requirements..." text prompt
- Estimated processing time display

#### 4.1.2 Execution State
**Task Execution Animation**:
- Step-level progress bars
- Real-time status update text
- Cancellable operation buttons

### 4.2 Error Handling and Recovery Mechanisms

#### 4.2.1 Single-step Retry Functionality
**Intelligent Error Handling** (referencing Pokee's single-step retry):
❌ Step 2 execution failed 
- 🔍 Google Search API call timeout 
- Cause: Network connection unstable

**Suggested solutions**:
- Retry current step 
- Switch to backup search engine 
- Adjust search parameters
[🔄 Retry] [🔀 Switch Tool] [⏭️ Skip This Step]

#### 4.2.2 Execution State Persistence
**Task State Persistence**:
- Automatically save state after each step completion
- Can continue from breakpoint after failure
- No need to restart entire process
- Support task pause and resume

#### 4.2.3 User Confirmation Mechanism
**Critical Operation Confirmation**: When tasks involve publishing content or important operations:
⚠️ About to execute important operation
- 📤 Will publish content to following platforms: 
  - Twitter: Post product update tweet 
  - LinkedIn: Publish company news 
  - WeChat Official Account: Publish technical article

**Content Preview**: Title: "AI Technology Breakthrough: Our New Product Launch" 
Content: [Display content summary]
[📝 Edit Content] [✅ Confirm Publishing] [❌ Cancel Operation]

### 4.3 Mobile Adaptation

#### 4.3.1 Mobile Layout
**Single-column Layout Design**:
- Top title bar + hamburger menu
- Main content area
- Bottom input bar fixed

**Drawer Navigation**:
- Left slide-out
