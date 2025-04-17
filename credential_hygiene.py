"""
8. Continuous Auditing & Credential Hygiene (Agent Card, AuthenticationInfo)
Mitigates: Supply Chain Attack, Credential Theft
MAESTRO Layers: 4 (Deployment & Infrastructure), 6 (Security & Compliance)
"""
from common.types import AuthenticationInfo
import os

def rotate_a2a_token():
    os.environ["A2A_TOKEN"] = "new_secret_token"
    return AuthenticationInfo(schemes=["bearer"], credentials="new_secret_token")

# Example usage:
if __name__ == "__main__":
    new_auth = rotate_a2a_token()
