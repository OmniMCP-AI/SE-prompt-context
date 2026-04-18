I need to design prompt standard , which need to solve problem like: 
- what kind of component is needed
- which is essitical for the probelm 
- how each part is effect the system 

here is thte proposal:

agent
desc (=listtool)
prompt
    role
    plan
    template
    ui_url
    input
    output
    use case / examples
    … …
    mcp tools
    UI (HTML)

agent swarm
    <agent_swarm>
    <description/>
    <plan>
    </plan>
    <agent>
    </agent>
    <lead>
    </lead>
    </agent_swarm>

app
    <description/> (=listtool)
    <agent>
    </agent>
    <context/>
    <app data/>
    <config/>

other convention
    template
    <template>
    <variable/>
    </template>
    use agent/swarm/mcp
    @agent
    @agent_swarm
    @mcp_sever:tool (URI)
 

**you nned to refer this wordware docs:**

Wordware home pagelight logo

Search...
⌘K
Support
Get Started

Documentation
Try it Out
Join our Discord
Book a Demo
Talk to our Founders
Get Started
Tour
Publish and Deploy
API
Workflows
Recipes
Chatbot
Parsing a PDF
Tutorials
Nodes
Generation
Structured Generation
Mention
Triggers
Actions
Ask a Human
Input
Loop
Code execution
If-Else
Flow
Comment
Tool
Formatting
Nodes
If-Else
Let your WordApp make decisions

​
What does it do?
If-else nodes, as the name suggests, allow you to create conditional logic in your WordApp. This means you can make your WordApp do different things based on the content it’s generated so far, or the inputs it’s received.

If-else nodes give WordApps the ability to make decisions, and sit at the heart of the intelligence AI provides. With Wordware, you can trivially pass data back and forth between software and AI, leveraging whichever form of intelligence is best for each point of your workflow.

If Else First Pn

Did you know that WordApps are Turing complete? The combination of if-else nodes and loop nodes make WordApps capable of carrying out any computation a computer can!

​
How do I use it?
An if-else node is made up of a series of conditions, each with a corresponding action. When the node runs, it checks each condition in turn, running the nodes inside the first section where the condition is true.

To create an if-else node, type /if in the editor, and hit Enter. You’ll be prompted to fill in some details about the node, like its name, and the conditions and actions you want to include in the attributes editor.

If Else Second Pn

​
Conditions
Conditions are set in the attributes editor under the Expressions section, with each condition (IF) having two slots for inputs, and three ways to compare them. You can access the ways to compare by clicking =, you will then have the following three options :

If Else Comparison Pn

Comparison	How it works
Match	Checks if the two values are equal
Text	Checks if the first value contains the second value
Number	Compares two numeric inputs, with sub-options for the comparison operator (e.g. >, <)
You can add as many conditions as you like with the + Add Ifbutton below all the existing conditions. There’s also an ELSE condition, which runs if none of the other conditions are true.

​
Actions
Actions are set in the editor under the appropriate condition, allowing for generations, mentions, and any other node types to be run depending on which condition is true.

The if-else example above, for example, works as follows:

1
If

First, the IF condition checks if the @is_known_user mention is the text “true”. If so, the WordApp will run the nodes inside this section:

If One Pn

2
Else

Then, if the above condition is not met, the WordApp will run the nodes inside this section:

Else Two Pn

Code execution
Flow
website
discord
x
linkedin
Powered by Mintlify
On this page
What does it do?
How do I use it?
Conditions
Actions



Wordware home pagelight logo

Search...
⌘K
Support
Get Started

Documentation
Try it Out
Join our Discord
Book a Demo
Talk to our Founders
Get Started
Tour
Publish and Deploy
API
Workflows
Recipes
Chatbot
Parsing a PDF
Tutorials
Nodes
Generation
Structured Generation
Mention
Triggers
Actions
Ask a Human
Input
Loop
Code execution
If-Else
Flow
Comment
Tool
Formatting
Nodes
Input
Data for your WordApp to crunch


​
What does it do?
Inputs lets you pass data into your WordApp. You can use them to provide context for your AI models, or to give them something to work with.

When you run a WordApp, you will be asked to provide values for your output for this particular run. If you access your WordApp via API, you’ll need to provide these values in your request.

​
How do I use it?
Inputs live in the input bar, just above the start of your flow in the editor.

Inputs Live Pn

To add an input, you can:

Click the + New Input button in the input bar
Type /input in the editor and hit Enter
Type @ and a name for the new input in the editor, then hit +
​
Options
A number of options appear in the attributes editor when you create a new input. Here’s what they mean:

​
Label
The name of the input. You’ll need this later if you want to reference the input in your flow.

Inputs Live Pn

​
Description
A description of the input. This can be useful for keeping track of what each input is for, but is not required. It’s also not visible to the AI models in a generation.

Description Input Pn

​
Input Type
What values are allowed for this input. You can choose between:

Type Input Pn

Note: we currently only support the below input types, but more will be added in the future!

Input type	What it’s for
Text	A short word or phrase
Number	A numerical value
True/False	A true/false statement
Image	An image, helpful if you’re using AI models with vision capabilities, like GPT-4o
Audio	Upload a song, or a recording and use it in your prompt. This is helpful if you’re using AI models with audio capabilities, like Google Gemini.
PDF/Document file	Choose a sub file type between Document or Raw File. A file must be processed by a tool like Document Parser or File Content Extractor before it can be used in the prompt. See a full example in Parsing a PDF.
CSV/Text file	If you have a spreadsheet-type file, currently CSVs are supported but we will be adding support for additional file formats in the future
List	A list of any one of the other types in this table, including other lists!
Object	A grouped collection of other types, e.g. a “person” object might include a text-type name, a number-type age, and an image for their profile photo
Select	Allow the user to choose from a specific set of options you provide, e.g “house” or “apartment” for addresses
​
Outputs
While it’s not technically an output, the value of an input can be referenced in your flow the same as any other output.

Ask a Human
Loop
website
discord
x
linkedin
Powered by Mintlify
On this page
What does it do?
How do I use it?
Options
Label
Description
Input Type
Outputs
Input - Wordware




Wordware home pagelight logo

Search...
⌘K
Support
Get Started

Documentation
Try it Out
Join our Discord
Book a Demo
Talk to our Founders
Get Started
Tour
Publish and Deploy
API
Workflows
Recipes
Chatbot
Parsing a PDF
Tutorials
Nodes
Generation
Structured Generation
Mention
Triggers
Actions
Ask a Human
Input
Loop
Code execution
If-Else
Flow
Comment
Tool
Formatting
Nodes
Flow
Call another flow from inside your own


​
What does it do?
Flows let you call another flow from inside your own. This can be useful for breaking up your WordApp into smaller, composable parts, or for reusing common patterns across multiple WordApps. Flows also give you deeper control over the context window, as the contents produced in intermediate steps of a subflow are not visible to the AI model of the parent flow.

Flows in the Editor

​
How do I use it?
To create a flow, type /flow in the editor, and hit Enter. You’ll be prompted to select which flow you want to call from your existing flows, and then to provide the inputs for that flow.

Flows in the Sidebar
​
Options
When you create a flow, you’ll see a number of options in the sidebar. Here’s what they mean:

​
Flow
The flow you want to call. You can select from any of the flows in the current project.

​
Inputs
The inputs you want to pass to the flow. These can be any of the inputs available in the current flow, or a @mentions from the current flow.

​
Outputs
Flows output all the variables generated by the flow. These can be referenced in the parent flow using a @mention with the name of the flow, followed by a dot and the name of the variable.

If-Else
Comment
website
discord
x
linkedin
Powered by Mintlify
On this page
What does it do?
How do I use it?
Options
Flow
Inputs
Outputs
Flow - Wordware




