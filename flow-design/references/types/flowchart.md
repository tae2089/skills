# Flowchart (`flowchart`)

Collection rules below apply to traced diagrams only. For proposed diagrams, use the syntax and notation examples only.

```mermaid
flowchart TD
    A["Receive request<br/>api/order.go"] --> B{"Body valid?"}
    B -- no --> E["400 response"]
    B -- yes --> C{"Stock available?"}
    C -- no --> F["409 response"]
    C -- yes --> D["Insert order<br/>repo/order.go"]
    D --> G["201 response"]
```

Evidence when asked: list nodes, edges, and branch arms with `file:line` citations.

- Decision nodes `{}` correspond 1:1 with conditions in the trace record.
- Default direction is `TD`; use `LR` when the flow is long and shallow.
- Every leaf must be a terminal from the trace (response, commit, publish, exit). Do not leave dangling actions.
