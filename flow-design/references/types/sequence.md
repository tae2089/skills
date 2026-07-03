# Sequence Diagram (`sequenceDiagram`)

Collection rules below apply to traced diagrams only. For proposed diagrams, use the syntax and notation examples only.

```mermaid
sequenceDiagram
    participant H as OrderHandler<br/>(api/order.go)
    participant S as OrderService<br/>(service/order.go)
    participant R as OrderRepo<br/>(repo/order.go)
    H->>S: CreateOrder(req)
    S->>S: validate(req)
    alt validation fails
        S-->>H: 400 InvalidArgument
    else ok
        S->>R: Insert(order)
        R-->>S: id
        S-->>H: 201 {id}
    end
```

Evidence when asked: list participants, messages, branches, and returns with `file:line` citations.

- Participants are modules or services, not individual functions. Functions travel in message labels.
- Represent branches from the trace record with `alt` / `opt` / `loop` blocks. Every `alt` shows every arm found by the trace.
- Use `-->>` (dotted arrows) for returns and error responses. Every edge, including `alt` arms, returns, and error responses, has a line in the trace record.
