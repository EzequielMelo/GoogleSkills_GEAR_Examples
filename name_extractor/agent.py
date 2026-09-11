from google.adk.agents.llm_agent import Agent

root_agent = Agent(
    model="gemini-3.5-flash",
    name="name_extractor",
    instruction="Extract the person's name from the message. Return ONLY the name, nothing else.",
    output_key="user_name",
)
