import os
import json
import anthropic

### Load Claude
with open('./api_key.json', 'r', encoding="utf-8") as file:
    claude3haiku_api_key = json.load(file)['Claude']
    os.environ['ANTHROPIC_API_KEY'] = claude3haiku_api_key
    
client = anthropic.Anthropic()


def send_query(query:dict):
    """    
        Sends a query to the Claude model and returns the response.
        
        :param query: The query to send to the Claude model.
        :return: The response from the Claude model.
    """
    
    response = client.beta.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=10000,
        messages=query,
        betas=["files-api-2025-04-14"],
        # max_tokens=16000,
        # thinking={  #Extended Thinking
        #     "type": "enabled",
        #     "budget_tokens": 10000
        # },
    )

    for block in response.content:
        if block.type == "thinking":
            return block.thinking
        elif block.type == "text":
            return block.text
    return response.content



"""
HTTP errors from claude API
Our API follows a predictable HTTP error code format:

400 - invalid_request_error: There was an issue with the format or content of your request. We may also use this error type for other 4XX status codes not listed below.

401 - authentication_error: There’s an issue with your API key.

403 - permission_error: Your API key does not have permission to use the specified resource.

404 - not_found_error: The requested resource was not found.

413 - request_too_large: Request exceeds the maximum allowed number of bytes. The maximum request size is 32 MB for standard API endpoints.

429 - rate_limit_error: Your account has hit a rate limit.

500 - api_error: An unexpected error has occurred internal to Anthropic’s systems.

529 - overloaded_error: Anthropic’s API is temporarily overloaded.

Request size limits
The API enforces request size limits to ensure optimal performance:
Endpoint Type	Maximum Request Size
Messages API	32 MB
Token Counting API	32 MB
Batch API	256 MB
Files API	500 MB
If you exceed these limits, you’ll receive a 413 request_too_large error. The error is returned from Cloudflare before the request reaches Anthropic’s API servers.

Error shapes
Errors are always returned as JSON, with a top-level error object that always includes a type and message value. For example:
{
  "type": "error",
  "error": {
    "type": "not_found_error",
    "message": "The requested resource could not be found."
  }
}
"""

def process_response(response: str) -> dict:
    """
        Processes the response from the Claude model and returns it as a dictionary.
        
        :param response: The response string from the Claude model.
        :return: A dictionary containing the error status and the processed response.
    """
    
    if not response:
        return {"error": True, "message": "No response from Claude."}
    
    try:
        
        # Clean the response by removing any XML-like tags
        response = response.replace("<output>", "").replace("</output>", "").strip()
        response = json.loads(response)
        # Check Claude return error message in response
        if 'error' in response:
            return {"error": True, "api_error":True, "message": response['error']}
    
        if isinstance(response, list):
            data = []
            for item in response:
                if isinstance(item, str):
                    item = item.strip()
                    data.append(item)
            if len(data) == 0:
                return {"error": True, "api_error":False, "message": "No data found in the response."}
            else:
                return {"error": False, "api_error":False, "data": data}
        elif isinstance(response, dict):
            data = {}
            for key, value in response.items():
                if isinstance(value, list):
                    data[key] =  value
            if len(data) == 0:
                return {"error": True, "api_error":False, "message": "No data found in the response."}
            else:
                return {"error": False, "api_error":False, "data": data}
        else:
            return {"error": True, "api_error":False, "message": "Unexpected response format."}
    except json.JSONDecodeError:
        return {"error": True, "api_error":False, "message": "Failed to decode JSON response."}
