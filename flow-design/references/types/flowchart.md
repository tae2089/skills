# Flowchart (`flowchart`)

## Notation

```mermaid
flowchart TD
    A["Receive request<br/>api/order.go"] --> B{"Body valid?"}
    B -- no --> E["400 response"]
    B -- yes --> C{"Stock available?"}
    C -- no --> F["409 response"]
    C -- yes --> D["Insert order<br/>repo/order.go"]
    D --> G["201 response"]
```

Evidence block contents: nodes, edges, and branch arms with `file:line` citations.

- Quote node labels that contain parentheses, brackets, or colons.

## Trace Completion

- Decision nodes `{}` correspond 1:1 with conditions in the trace record.
- Every leaf must be a terminal from the trace (response, commit, publish, exit). Do not leave dangling actions.
