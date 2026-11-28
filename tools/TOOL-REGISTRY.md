# Tool Registry

The Python registry exposes named tools with JSON Schema parameter definitions, risk levels, and synchronous or asynchronous handlers. It validates each argument object against its registered schema before requesting approval or dispatching the handler. Unknown tools and malformed arguments are rejected.

The base implementation registers a restricted calculator and UTC clock. Add tools only through reviewed handlers; arbitrary shell execution is not exposed. Keep schemas narrow, set `additionalProperties: false` where appropriate, and classify risk conservatively.
