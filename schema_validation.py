"""
5. Schema Validation (A2A Messages, Artifacts)
Mitigates: Message Schema Violation, Task Replay
MAESTRO Layers: 2 (Data Operations), 3 (Agent Frameworks)
"""
from common.types import Message, TextPart
from pydantic import ValidationError

def validate_message_schema(message: Message):
    """Validate that a Message conforms to the A2A schema using pydantic."""
    try:
        message.model_validate(message.model_dump())
    except ValidationError as e:
        raise ValueError(f"Schema validation failed: {e}")

# Example usage:
if __name__ == "__main__":
    msg = Message(role="user", parts=[TextPart(text="Test")])
    validate_message_schema(msg)
