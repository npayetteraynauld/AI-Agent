import os
import sys
import argparse
from system_prompt import system_prompt
from functions.func_schemas import schema_get_files_info, schema_get_file_content, schema_run_python_file, schema_write_file
from functions.call_function import call_function
from dotenv import load_dotenv
from google import genai
from google.genai import types


load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")
client = genai.Client(api_key=api_key)

available_functions = types.Tool(
    function_declarations=[
        schema_get_files_info,
        schema_get_file_content,
        schema_run_python_file,
        schema_write_file,
    ]
)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("prompt", help="The user prompt")
    parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
    args = parser.parse_args()

    prompt = args.prompt
    if len(prompt) == 0:
        print("No prompt provided")
        sys.exit(1)

    messages = [
        types.Content(role="user", parts=[types.Part(text=prompt)]),
    ]

    response = client.models.generate_content(
        model = "gemini-2.0-flash-001", 
        contents = messages,
        config = types.GenerateContentConfig(
            tools = [available_functions],
            system_instruction=system_prompt
        )
    )

    if args.verbose == False:
        if response.function_calls and len(response.function_calls) > 0:
            for function_call_part in response.function_calls:
                print(f"Calling function: {function_call_part.name}({function_call_part.args})")
        elif response.text:
            print(response.text)
        return

    prompt_token_count = response.usage_metadata.prompt_token_count
    response_token_count = response.usage_metadata.candidates_token_count
    
    print(f"User prompt: {prompt}")
    print()
    if response.function_calls and len(response.function_calls) > 0:
        for function_call_part in response.function_calls:
            print(f"Calling function: {function_call_part.name}({function_call_part.args})")
    elif response.text:
        print(response.text)
    print()
    print(f"Prompt tokens: {prompt_token_count}")
    print(f"Response tokens: {response_token_count}")


if __name__ == "__main__":
    main()
