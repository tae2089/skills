# Pseudocode Format

## Notation

- Line numbers: `P1`, `P2`, ... so scenarios, reviews, and diagrams can refer to lines.
- One action per line: one validation, one call, one write, or one return. Split compound lines.
- Branches use explicit `IF` / `ELSE` arms with indentation; loops use `FOR EACH` / `WHILE`. Every `IF` accounts for every arm. A guard clause (`IF cond -> early exit`) counts the fall-through as the other arm. Non-guard branches need an explicit `ELSE`.
- Existing-code integration points go at the end of the line in brackets: `[api/order.go:58]`. Lines without brackets are new logic.
- Mark side effects with a leading verb: `WRITE`, fallible external/IO `CALL`, `PUBLISH`. Each needs an explicit failure arm. Local pure/helper calls do not need failure arms.
- Failure arms state observable results (status code, error type, event). Do not write "handle error".

## Example

Work unit: partial refund for a paid order. Criteria: only `Paid` orders can be refunded; amount <= remaining; every refund records a ledger entry; payment gateway failure must not contaminate the ledger.

```text
P1  receive POST /orders/{id}/refund (amount)          [api/order.go:24]
P2  load order by id                                   [repo/order.go:31]
P3  IF order not found -> return 404
P4  IF order.status != Paid -> return 409 "not refundable"
P5  IF amount <= 0 OR amount > order.remaining -> return 422
P6  begin transaction                                  [repo/tx.go:12]
P7  WRITE ledger entry (order id, -amount)
P8    IF write fails -> rollback, return 500
P9  CALL payment gateway refund(amount)                [pay/gateway.go:88]
P10   IF gateway fails or times out -> rollback, return 502
P11 update order.remaining -= amount
P12 commit transaction
P13   IF commit fails -> return 500 (gateway refund now orphaned - flag for reconciliation)
P14 PUBLISH refund event                               [events/refund.go:9]
P15   IF publish fails -> log and continue (event is not part of the contract)
P16 return 200 {remaining}
```

Use `scenario-extraction.md` when scenario format and coverage rules are needed.

## Completeness Check

Scan the block and confirm each item exists or is intentionally absent:

- All inputs are validated at the boundary (`P3`-`P5` pattern); cover empty, missing, and out-of-range values.
- Authorization/permission is checked if the operation requires it.
- Every `WRITE` / fallible external/IO `CALL` / `PUBLISH` has a failure arm with an observable result.
- Ordering risk is explicit: what happens when an earlier side effect succeeds and a later step fails (`P13` pattern).
- Concurrency: if two calls can race on the same data, say who wins.
- Every acceptance criterion for the work unit maps to at least one line; list unmapped criteria as gaps.
