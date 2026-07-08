# Sequence Diagram (`sequenceDiagram`)

## Notation

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

Evidence block contents: participants, messages, branches, and returns with `file:line` citations.

- Participants are modules or services, not individual functions. Functions travel in message labels.
- Represent branches with `alt` / `opt` / `loop` blocks.
- Use `-->>` (dotted arrows) for returns and error responses.

## Trace Completion

- Every `alt` shows every arm found by the trace.
- Every edge, including `alt` arms, returns, and error responses, has a line in the trace record.
