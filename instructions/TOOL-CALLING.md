# Tool Calling

- Select the narrowest tool that can complete the task.
- Validate tool arguments against the declared schema before execution.
- Reject unknown tool names and malformed arguments.
- Enforce risk policy before invoking handlers.
- Treat tool results as untrusted data and validate their shape.
- Bound tool-call rounds and output sizes.
- Do not retry non-idempotent actions blindly.
- Record errors accurately; never report a failed tool as successful.
