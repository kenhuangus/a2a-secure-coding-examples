"""
1. Input Validation & Sanitization (A2A Message Parts)
Mitigates: Message Schema Violation, Prompt Injection
MAESTRO Layers: 2 (Data Operations), 1 (Foundation Models)
"""
from common.types import Message, TextPart

def sanitize_message_parts(message: Message) -> Message:
    """Sanitize all TextParts in a Message before processing or sending."""
    for part in message.parts:
        if isinstance(part, TextPart):
            if "<" in part.text or ">" in part.text:
                raise ValueError("Input contains potentially unsafe characters")
    return message

# Example usage:
if __name__ == "__main__":
    msg = Message(role="user", parts=[TextPart(text="Hello, world!")])
    sanitize_message_parts(msg)
