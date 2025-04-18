"""
Mitigation Example 5: Schema Validation (A2A + Google GenAI + CrewAI)
Validates message schemas using Pydantic and CrewAI.
"""
from samples.python.common.types import Message, TextPart
from pydantic import ValidationError
from crewai import Agent, Crew, LLM, Task
from crewai.process import Process
from dotenv import load_dotenv
import os
from google import genai
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("schema_validation")

def get_api_key():
    load_dotenv()
    return os.getenv("GOOGLE_API_KEY")

def validate_message_schema(data: dict) -> Message:
    try:
        return Message(**data)
    except ValidationError as e:
        raise ValueError(f"Schema validation error: {e}")

class SchemaValidationAgent:
    def __init__(self):
        self.llm = LLM(model="gemini/gemini-2.0-flash", api_key=get_api_key())
        self.agent = Agent(
            role="Schema Validator",
            goal="Validate message schemas before processing.",
            backstory="You are a security agent that checks all messages for schema compliance.",
            verbose=False,
            allow_delegation=False,
            tools=[],
            llm=self.llm,
        )
        self.task = Task(
            description="Validate the schema of the message.",
            expected_output="A valid Message object or an error if schema is invalid.",
            agent=self.agent,
        )
        self.crew = Crew(
            agents=[self.agent],
            tasks=[self.task],
            process=Process.sequential,
            verbose=False,
        )
    def validate(self, data):
        try:
            msg = validate_message_schema(data)
            logger.info("Schema validated: %s", msg)
            return msg
        except Exception as e:
            logger.error("Schema validation failed: %s", e)
            return str(e)

def test_schema_validation_agent():
    agent = SchemaValidationAgent()
    valid = {"role": "user", "parts": [{"type": "text", "text": "hi"}]}
    assert isinstance(agent.validate(valid), Message)
    invalid = {"role": "user", "parts": [{"type": "text"}]}
    result = agent.validate(invalid)
    assert "Schema validation error" in result

if __name__ == "__main__":
    test_schema_validation_agent()
    print("Schema validation (A2A + GenAI + CrewAI) example ran successfully.")
