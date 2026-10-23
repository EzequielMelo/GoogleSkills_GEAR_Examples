import os
from dotenv import load_dotenv
import sys
from google.adk.agents import LlmAgent
from google.adk.apps.app import App

# Add the parent directory to sys.path to allow importing from adk_utils
# Get the absolute path of the directory containing agent.py
current_dir = os.path.dirname(os.path.abspath(__file__))
# Get the parent directory (adk_mcp_tools)
parent_dir = os.path.dirname(current_dir)

# Insert it at the beginning of the path list
if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)

# Debug: Print the path so you can see it in the terminal logs
print(f"DEBUG: Searching for modules in: {parent_dir}")

from google.adk.tools.mcp_tool.mcp_toolset import MCPToolset, \
                StreamableHTTPConnectionParams
from google.genai import types
from adk_utils.plugins import LabExUtils
from google.adk.models import Gemini
from google.genai.types import HttpRetryOptions

load_dotenv()

import google.auth
from google.auth import impersonated_credentials
from google.auth.transport.requests import Request

PROJECT_ID = os.environ["GOOGLE_CLOUD_PROJECT"]

# The Maps MCP server requires an OAuth token with the Maps scope.
# Your Cloud Shell credentials mint short-lived tokens for the lab's
# maps-mcp-agent service account, which carry that scope.
maps_credentials = impersonated_credentials.Credentials(
    source_credentials=google.auth.default()[0],
    target_principal=f"maps-mcp-agent@{PROJECT_ID}.iam.gserviceaccount.com",
    target_scopes=[
        "https://www.googleapis.com/auth/cloud-platform",
        "https://www.googleapis.com/auth/maps-platform.mapstools",
    ],
)

def maps_auth_headers(context):
    """Returns fresh auth headers for each call to the Maps MCP server."""
    if not maps_credentials.valid:
        maps_credentials.refresh(Request())
    return {
        "Authorization": f"Bearer {maps_credentials.token}",
        "x-goog-user-project": PROJECT_ID,
    }

# Retry options help avoid the occasional error from popular models
# receiving too many requests at once.
RETRY_OPTIONS = types.HttpRetryOptions(initial_delay=1, max_delay=3, attempts=30)
plugins = [LabExUtils()]

root_agent = LlmAgent(
    # name: A unique name for the agent.
    name='maps_assistant_agent',
    # description: A short description of the agent's purpose, so
    # other agents in a multi-agent system know when to call it.
    description="Use google maps to find directions.",
    # model: The LLM model that the agent will use:
    model=Gemini(model=os.getenv("MODEL"), retry_options=RETRY_OPTIONS),
     # instruction: Instructions (or the prompt) for the agent.
    instruction="""
        Help the user with mapping, directions, and finding places
        using Google Maps tools.
    """,
    # tools: functions to enhance the model's capabilities.
    # Add the MCPToolset below:
    tools=[
    MCPToolset(
        connection_params=StreamableHTTPConnectionParams(
            url="https://mapstools.googleapis.com/mcp",
            timeout=15,
        ),
        header_provider=maps_auth_headers,
    )
],

)

app = App(
    name="google_maps_mcp_agent",
    root_agent=root_agent,
    plugins=plugins
)
# UNCOMMENT THE LINE BELOW TO TEST FAILOVER:
### Is there a way to add something here for testing purpose.