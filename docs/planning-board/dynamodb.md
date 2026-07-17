No need to be afraid of it — DynamoDB just has a different mental model than SQL, and once the core ideas click it's actually simpler than relational DBs in a lot of ways. Let me build it up from scratch, using your actual VPC/subnet case as the running example.

## The core idea: it's a key-value store, not a table with rows

Forget "tables with columns" for a second. Think of DynamoDB as a giant dictionary/hashmap that AWS manages for you. You put items in, you get items out, by key. That's it at the core.

## The two keys that matter: Partition Key and Sort Key

Every table has a **Partition Key** (required) and optionally a **Sort Key**. Together they're the item's unique identity.

- **Partition Key (PK)** — determines *which physical partition* your data lives on. Items with the same PK live together.
- **Sort Key (SK)** — orders items *within* a partition key group, and lets you have multiple items sharing a PK.

For your subnets table:
```
PK: vpc_id        SK: subnet_id
vpc-001           subnet-aaa
vpc-001           subnet-bbb
vpc-002           subnet-ccc
```
All subnets belonging to `vpc-001` share the same PK. This is the whole trick — it's not a "join," it's just "things with the same partition key are physically grouped together," so asking for them is fast and cheap.

## The two ways to read data

This is the part that trips people up coming from SQL, because there's no `SELECT * WHERE anything`.

1. **GetItem** — "give me the exact item with PK=X and SK=Y." Fastest, cheapest, most common operation.
2. **Query** — "give me all items with PK=X" (optionally narrowed by SK). This is how you get "all subnets in vpc-001" — `Query` where `vpc_id = 'vpc-001'`.
3. **Scan** — "look at every single item in the table." Slow, expensive, avoid in real code. Fine for a one-off debug check, not for application logic.

There's no `Query` across arbitrary attributes unless that attribute is a key — which is why **you design the table around your access patterns first**, not around "what fields does a VPC have." Ask yourself: "how will I ever look this data up?" then build keys for those lookups.

## GSIs: how you query by something other than the PK

What if you need `GET /subnets/{subnet_id}` directly, without knowing which VPC it's in? You add a **Global Secondary Index (GSI)** — basically a second PK/SK arrangement over the same data, maintained automatically by DynamoDB.

```
Base table:  PK=vpc_id,    SK=subnet_id
GSI:         PK=subnet_id
```
Now you can `Query` the GSI directly by `subnet_id` when that's all you have.

## Putting it together for your project

**`vpcs` table**
```
PK: vpc_id
attributes: cidr_block, name, created_at, ...
```
- `GET /vpcs/{vpc_id}` → `GetItem(PK=vpc_id)`
- `GET /vpcs` → `Scan` (fine here — you're listing everything, and PoC-scale VPC counts are tiny)

**`subnets` table**
```
PK: vpc_id     SK: subnet_id
attributes: cidr_block, name, ...
GSI "subnet_id_index": PK = subnet_id
```
- `GET /vpcs/{vpc_id}/subnets` → `Query(PK=vpc_id)` — this is your "join," it's just a query
- `GET /subnets/{subnet_id}` → `Query` the GSI on `subnet_id`
- `GET /subnets` → `Scan`
- `POST /vpcs/{vpc_id}/subnets` → `PutItem` with `PK=vpc_id, SK=subnet_id`

No third table needed — the relationship *is* the key structure.

## A few things that remove most of the fear once you know them

- **No schema enforcement on non-key attributes.** You don't declare "columns" in Terraform beyond the key attributes. Each item can technically have different attributes (be disciplined about this anyway, but DynamoDB won't stop you).
- **Everything is idempotent by key.** `PutItem` with the same PK+SK overwrites — no separate "insert vs update" ceremony like SQL.
- **Costs are pay-per-request** in on-demand mode (which I'd pick for a PoC) — you're billed per read/write, not for idle capacity. This is where the "cheap for PoC" property actually comes from.
- **There is genuinely no way to do a flexible ad-hoc query later** without either a GSI designed in advance or falling back to `Scan` + filter (works, just not efficient at scale — totally fine for a PoC's data volumes).

Want me to write the actual `aws_dynamodb_table` Terraform for both tables (with the GSI), or first show you what the boto3 code in `aws_vpc_controller.py`/`aws_subnet_controller.py` looks like for `PutItem`/`Query`/`GetItem` against this schema?