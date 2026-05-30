# Local Claude Code AI Agent Clone

A lightweight, local command-line implementation of an AI developer agent. This assistant utilizes LLM function calling via the OpenAI SDK wrapper (configured for OpenRouter) to autonomously read files, write source code, and interact directly with a localized sub-shell environment.

---

## 🛠 Features & Tool Matrix

The agent is equipped with three structural capabilities declared to the model schema:

| Tool Name | Parameters | Action |
| :--- | :--- | :--- |
| **`Read`** | `file_path` | Inspects workspace contents and streams text back to the agent thread context. |
| **`Write`** | `file_path`, `content` | Dynamically writes or rewrites source file assets locally. |
| **`Bash`** | `command` | Executes native sub-shell terminal workflows relative to the project directory. |

---

## 🏗 Core Execution Architecture

The script implements a robust **Agent Loop** that continually handles OpenAI-compatible tool calling messages. When the engine requests system access via HTTP RESTful API cycles, the runtime catches the payload, sequences the task executions, appends structural tool results, and continues running until all tasks are complete:

The assistant orchestrates loops using an ongoing state assessment iteration. As long as the model flags technical demands utilizing local tools (`chat.choices[0].message.tool_calls`), the runtime captures parameters, executes operational requests, stacks context strings, and updates the chat pipeline:

```python
while (chat.choices[0].message.tool_calls):
    payload = chat.choices[0].message
    message.append(payload.model_dump())

    for tool_call in payload.tool_calls:
        result = "Error: Tool not recognized"
        
        # 1. READ INTERACTION
        if tool_call.function.name == "Read":
            # Target path extraction and reading implementation...
            
        # 2. WRITE INTERACTION
        if tool_call.function.name == "Write":
            # Disk stream serialization logic...

        # 3. SHELL INTERACTION
        if tool_call.function.name == "Bash":
            args_dict = json.loads(tool_call.function.arguments)
            command = args_dict["command"]
            target_path = "."
            
            # Contextually bound execution
            res = subprocess.run(command, cwd=target_path, shell=True, capture_output=True, text=True)
            result = res.stdout if res.returncode == 0 else res.stderr
        
        # Append the safe serializable string output to avoid execution crashes
        message.append({
            "role": "tool",
            "tool_call_id": tool_call.id,
            "content": result
        })
    
    # Re-verify task evaluation tracking
    chat = client.chat.completions.create(...)# Local Claude Code AI Agent Clone
```

A lightweight, local command-line implementation of an AI developer agent. This assistant utilizes LLM function calling via the OpenAI SDK wrapper (configured for OpenRouter) to autonomously read files, write source code, and interact directly with a localized sub-shell environment.

---

## 🛠 Features & Tool Matrix

The agent is equipped with three structural capabilities declared to the model schema:

| Tool Name | Parameters | Action |
| :--- | :--- | :--- |
| **`Read`** | `file_path` | Inspects workspace contents and streams text back to the agent thread context. |
| **`Write`** | `file_path`, `content` | Dynamically writes or rewrites source file assets locally. |
| **`Bash`** | `command` | Executes native sub-shell terminal workflows relative to the project directory. |

---

## 🏗 Core Execution Architecture

The assistant orchestrates loops using an ongoing state assessment iteration. As long as the model flags technical demands utilizing local tools (`chat.choices[0].message.tool_calls`), the runtime captures parameters, executes operational requests, stacks context strings, and updates the chat pipeline:

```python
while (chat.choices[0].message.tool_calls):
    payload = chat.choices[0].message
    message.append(payload.model_dump())

    for tool_call in payload.tool_calls:
        result = "Error: Tool not recognized"
        
        # 1. READ INTERACTION
        if tool_call.function.name == "Read":
            # Target path extraction and reading implementation...
            
        # 2. WRITE INTERACTION
        if tool_call.function.name == "Write":
            # Disk stream serialization logic...

        # 3. SHELL INTERACTION
        if tool_call.function.name == "Bash":
            args_dict = json.loads(tool_call.function.arguments)
            command = args_dict["command"]
            target_path = "."
            
            # Contextually bound execution
            res = subprocess.run(command, cwd=target_path, shell=True, capture_output=True, text=True)
            result = res.stdout if res.returncode == 0 else res.stderr
        
        # Append the safe serializable string output to avoid execution crashes
        message.append({
            "role": "tool",
            "tool_call_id": tool_call.id,
            "content": result
        })
    
    # Re-verify task evaluation tracking
    chat = client.chat.completions.create(...)

    🚀 Setup & Execution
1. Environment Configurations
The program parses required access parameters from your operational environment profile. Ensure your platform authentication parameters are mapped out prior to launch:
# On Windows PowerShell
$env:OPENROUTER_API_KEY="your_openrouter_api_key_here"

# On Linux/macOS
export OPENROUTER_API_KEY="your_openrouter_api_key_here"

2. Local Execution
Launch the orchestration cycle from your workspace directory passing a design parameter instruction using the -p flag:
python app/main.py -p "Check if there's a file called server.py. If not, create it and print a hello world."