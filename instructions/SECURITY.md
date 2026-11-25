# Security Model

- Secrets are read from environment configuration and must never be logged.
- Shell execution is absent from the default tool registry.
- Tool handlers should validate and constrain all inputs.
- External content is untrusted and may contain prompt injection.
- High-risk operations are denied without an approval callback returning true.
- Use isolated environments for untrusted code and separate staging from production.
- Apply least privilege, audit important operations, and rotate exposed credentials.
- This starter is not a security certification; perform threat modeling and review before production use.
