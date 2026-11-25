# Tool Registry

The Python registry exposes named tools with parameter schemas, risk levels, and async handlers. Unknown tools are rejected. The base implementation registers a restricted calculator and UTC clock. Add tools only through reviewed handlers; arbitrary shell execution is not exposed.
