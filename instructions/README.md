# Instruction Files

| File | Purpose |
|---|---|
| SYSTEM.md | Core behavior and priorities |
| IDENTITY.md | Agent identity and mission |
| REASONING.md | Task decomposition and evidence |
| AUTONOMY.md | Approval boundaries |
| TOOL-CALLING.md | Tool selection and execution |
| KNOWLEDGE.md | Research and retrieval |
| MEMORY.md | Persistence and privacy |
| SECURITY.md | Security boundaries |
| COMMUNICATION.md | User-facing reporting |
| QUALITY-ASSURANCE.md | Verification checklist |

The base Python implementation loads SYSTEM.md as its system message. The remaining files are operational guidance for the host agent or future orchestration layer and are not automatically concatenated into the prompt.
