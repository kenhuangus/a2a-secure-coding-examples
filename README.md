# Secure Coding Practices for A2A Applications

This repository provides reference code snippets of secure coding patterns for [Google A2A](https://github.com/google/A2A) applications, following the [Maestro](https://cloudsecurityalliance.org/blog/2025/02/06/agentic-ai-threat-modeling-framework-maestro) framework. Each example demonstrates how to mitigate common security threats in multi-agent systems. The code snippets are organized by security topic and can be used as a starting point for your own implementation.

> **Disclaimer:**
> These examples are provided for educational and reference purposes only. **No warranty is provided. The code is not fully tested and is not intended for use in production systems.** Each file demonstrates a security pattern or mitigation technique, but may require adaptation and further testing for your specific environment.

## Secure Coding Examples

### Original Examples

1. **Input Validation & Sanitization** ([input_validation.py](https://github.com/kenhuangus/a2a-secure-coding-examples/blob/master/input_validation.py))
    - Prevents message schema violations and prompt injection by validating and sanitizing message parts.
2. **Output Verification & Content Filtering** ([output_verification.py](https://github.com/kenhuangus/a2a-secure-coding-examples/blob/master/output_verification.py))
    - Filters artifacts to prevent leaking sensitive or forbidden content.
3. **Strong Authentication & Authorization** ([authentication_authorization.py](https://github.com/kenhuangus/a2a-secure-coding-examples/blob/master/authentication_authorization.py))
    - Uses JWT and environment-based credentials to ensure agent identity and secure operations.
4. **Rate Limiting & Monitoring** ([rate_limiting.py](https://github.com/kenhuangus/a2a-secure-coding-examples/blob/master/rate_limiting.py))
    - Enforces rate limits to protect against DoS and abuse.
5. **Schema Validation** ([schema_validation.py](https://github.com/kenhuangus/a2a-secure-coding-examples/blob/master/schema_validation.py))
    - Validates message schemas using Pydantic.
6. **Secure State & Cache Management** ([secure_cache.py](https://github.com/kenhuangus/a2a-secure-coding-examples/blob/master/secure_cache.py))
    - Demonstrates secure, thread-safe cache usage for artifacts and credentials.
7. **Logging & Observability** ([logging_observability.py](https://github.com/kenhuangus/a2a-secure-coding-examples/blob/master/logging_observability.py))
    - Provides safe logging practices to prevent log injection and improve auditability.
8. **Continuous Auditing & Credential Hygiene** ([credential_hygiene.py](https://github.com/kenhuangus/a2a-secure-coding-examples/blob/master/credential_hygiene.py))
    - Shows how to rotate credentials and maintain secure authentication info.

### CrewAI + GenAI Secure Examples

The following examples are now located in the **root directory** of the repository and demonstrate the same mitigations using CrewAI constructs and Google GenAI:

1. **Input Validation & Sanitization** ([input_validation_a2a_crew.py](https://github.com/kenhuangus/a2a-secure-coding-examples/blob/master/input_validation_a2a_crew.py))
2. **Output Verification & Content Filtering** ([output_verification_a2a_crew.py](https://github.com/kenhuangus/a2a-secure-coding-examples/blob/master/output_verification_a2a_crew.py))
3. **Strong Authentication & Authorization** ([authentication_authorization_a2a_crew.py](https://github.com/kenhuangus/a2a-secure-coding-examples/blob/master/authentication_authorization_a2a_crew.py))
4. **Rate Limiting & Monitoring** ([rate_limiting_a2a_crew.py](https://github.com/kenhuangus/a2a-secure-coding-examples/blob/master/rate_limiting_a2a_crew.py))
5. **Schema Validation** ([schema_validation_a2a_crew.py](https://github.com/kenhuangus/a2a-secure-coding-examples/blob/master/schema_validation_a2a_crew.py))
6. **Secure State & Cache Management** ([secure_cache_a2a_crew.py](https://github.com/kenhuangus/a2a-secure-coding-examples/blob/master/secure_cache_a2a_crew.py))
7. **Logging & Observability** ([logging_observability_a2a_crew.py](https://github.com/kenhuangus/a2a-secure-coding-examples/blob/master/logging_observability_a2a_crew.py))
8. **Continuous Auditing & Credential Hygiene** ([credential_hygiene_a2a_crew.py](https://github.com/kenhuangus/a2a-secure-coding-examples/blob/master/credential_hygiene_a2a_crew.py))

Each file contains an example usage. **Adapt these patterns to your own A2A systems for improved security.**
