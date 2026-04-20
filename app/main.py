import argparse
import os
import sys
import json
import subprocess

from openai import OpenAI

API_KEY = os.getenv("OPENROUTER_API_KEY")
BASE_URL = os.getenv("OPENROUTER_BASE_URL", default="https://openrouter.ai/api/v1")


def main():
    p = argparse.ArgumentParser()
    p.add_argument("-p", required=True)
    args = p.parse_args()

    if not API_KEY:
        raise RuntimeError("OPENROUTER_API_KEY is not set")

    client = OpenAI(api_key=API_KEY, base_url=BASE_URL)

    # chat = client.chat.completions.create(
    #     model="anthropic/claude-haiku-4.5",
    #     messages=[{"role": "user", "content": args.p}],
    #     max_tokens=1000,
    #     tools=[{
    #         "type": "function",
    #         "function": {
    #             "name": "Read",
    #             "description": "Read and return the contents of a file",
    #             "parameters": {
    #             "type": "object",
    #             "properties": {
    #                 "file_path": {
    #                 "type": "string",
    #                 "description": "The path to the file to read"
    #                 }
    #             },
    #             "required": ["file_path"]
    #             }
    #         }
    #         }],
    # )


    # if not chat.choices or len(chat.choices) == 0:
    #     raise RuntimeError("no choices in response")

    # You can use print statements as follows for debugging, they'll be visible when running tests.
    print("Logs from your program will appear here!", file=sys.stderr)

    # TODO: Uncomment the following line to pass the first stage
    # This will show you the 'tool_calls' if the model decided to use the tool




    message=[{"role": "user", "content": args.p}]
    tool = [{
            "type": "function",
            "function": {
                "name": "Read",
                "description": "Read and return the contents of a file",
                "parameters": {
                "type": "object",
                "properties": {
                    "file_path": {
                    "type": "string",
                    "description": "The path to the file to read"
                    }
                },
                "required": ["file_path"]
                }
            }
            },{
                "type": "function",
                "function": {
                    "name": "Write",
                    "description": "Write content to a file",
                    "parameters": {
                    "type": "object",
                    "required": ["file_path", "content"],
                    "properties": {
                        "file_path": {
                        "type": "string",
                        "description": "The path of the file to write to"
                        },
                        "content": {
                        "type": "string",
                        "description": "The content to write to the file"
                        }
                    }
                    }
                }
                },{
                "type": "function",
                "function": {
                    "name": "Bash",
                    "description": "Execute a shell command",
                    "parameters": {
                    "type": "object",
                    "required": ["command"],
                    "properties": {
                        "command": {
                        "type": "string",
                        "description": "The command to execute"
                        }
                    }
                    }
                }
                }
            ]

    chat = client.chat.completions.create(
        model="anthropic/claude-haiku-4.5",
        messages=message,
        max_tokens=1000,
        tools=tool,
    )

    if not chat.choices or len(chat.choices) == 0:
        raise RuntimeError("no choices in response")


    while (chat.choices[0].message.tool_calls) :
        payload = chat.choices[0].message
        message.append(payload.model_dump())
        #if (chat.choices[0].message.content != None):
            #print(chat.choices[0].message.content)

        
        for tool_call in payload.tool_calls :
            result = "Error: Tool not recognized"
            if tool_call.function.name == "Read":
                args_string = tool_call.function.arguments
                args_dict = json.loads(args_string)
                file_path = args_dict["file_path"]
                result = "file not found"
                
                try:
                    with open(file_path, "r", encoding="utf-8") as file:
                        result = file.read()
                        
                except FileNotFoundError:
                    print(f"Error: The file {file_path} does not exist.", file=sys.stderr)
                except Exception as e:
                    print(f"An error occurred: {e}", file=sys.stderr)
            
            if tool_call.function.name == "Write":
                args_string = tool_call.function.arguments
                args_dict = json.loads(args_string)
                file_path = args_dict["file_path"]
                file_content = args_dict["content"]
                
                try:
                    with open(file_path, "w", encoding="utf-8") as file:
                        file.write(file_content)
                    result = f"Successfully wrote to {file_path}"
                        
                except Exception as e:
                    print(f"An error occurred: {e}", file=sys.stderr)
                    result = f"Error: Could not write to file. {str(e)}"

            if tool_call.function.name == "Bash":
                args_string = tool_call.function.arguments
                args_dict = json.loads(args_string)
                command = args_dict["command"]

                target_path="."
                
                result = subprocess.run(command, cwd=target_path, shell=True, capture_output=True, text=True)
                result = result.stdout if result.returncode == 0 else result.stderr
            
            message.append({
                "role": "tool",
                "tool_call_id": tool_call.id,
                "content": result
            })
        
        chat = client.chat.completions.create(
        model="anthropic/claude-haiku-4.5",
        messages=message,
        max_tokens=1000,
        tools=tool,
        )


    print(chat.choices[0].message.content)
        






    # print(chat)

    # if chat.choices[0].message.tool_calls:
    #     tool_call = chat.choices[0].message.tool_calls[0]
    
    #     if tool_call.function.name == "Read":
    #         args_string = tool_call.function.arguments
    #         args_dict = json.loads(args_string)
    #         file_path = args_dict["file_path"]
             
    #         try:
    #             with open(file_path, "r", encoding="utf-8") as file:
    #                 content = file.read()
    #                 # Print to stdout for the test runner to see
    #                 print(content)
    #         except FileNotFoundError:
    #             print(f"Error: The file {file_path} does not exist.", file=sys.stderr)
    #         except Exception as e:
    #             print(f"An error occurred: {e}", file=sys.stderr)
    # else:
    # # If no tool was called, show the text response
    #     print(chat.choices[0].message.content)

    
    


if __name__ == "__main__":
    main()
