import os
from google.adk.agents import LlmAgent
from google.adk.models import Gemini
from google.genai.types import HttpRetryOptions
from typing import List

from google.adk.agents.remote_a2a_agent import RemoteA2aAgent
import sys
from google.adk.apps.app import App

from .adk_utils import LabExUtils

RETRY_OPTIONS = HttpRetryOptions(initial_delay=1, max_delay=3, attempts=30)
plugins = [LabExUtils()]

# Agents
illustration_agent = RemoteA2aAgent(
    name="illustration_agent",
    description="Agent that generates illustrations.",
    agent_card=(
        "illustration-agent-card.json"
    ),
)

root_agent = LlmAgent(
    model=Gemini(model=os.getenv("MODEL"), retry_options=RETRY_OPTIONS),
    name='slide_content_agent',
    description='An agent that writes content for slide decks.',
    instruction="""
        A user will ask you to create content for a slide to communicate an idea.
        Write a short headline about this idea.
        Write 1-2 sentences of body text about this idea.
        Share these with the user.
        Then transfer to the 'illustration_agent' to generate an illustration related to this idea.
        """,
	# Add the sub_agents parameter below
    sub_agents=[illustration_agent]
)

app = App(
    name="slide_content_agent",
    root_agent=root_agent,
    plugins=plugins
)