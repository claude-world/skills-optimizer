# Compression Strategies

## 1. Skill Description Compression

### Trigger-Preserve Algorithm
```
1. EXTRACT trigger words (file extensions, action verbs, domain terms)
2. REMOVE filler: "This skill", "helps you", "allows users to", "Use when"
3. CONVERT sentences → keyword lists with separators
4. MERGE synonyms: "create/make/generate" → "create"
5. VALIDATE: ensure all original triggers still present
```

### Compression Patterns
| Pattern | Before | After |
|---------|--------|-------|
| Passive → Active | "can be used to edit" | "edit" |
| Verbose trigger | "Use this when working with" | "For:" |
| Redundant category | "file types including .pdf, .docx" | ".pdf/.docx" |
| Feature list | "supports X, Y, and Z" | "X/Y/Z" |

## 2. DICE Context Compression

### Drop Rules
- Greetings: "Hi", "Hello", "Thanks"
- Acknowledgments: "Got it", "Sure", "I understand"
- Failed attempts: keep only final working approach
- Repetition: keep first mention only
- Meta-commentary: "Let me think...", "I'll try..."

### Implicit Conversion
```
EXPLICIT: "The user said they want to build a REST API"
IMPLICIT: goal=REST_API

EXPLICIT: "User prefers Python over JavaScript"
IMPLICIT: lang=Python

EXPLICIT: "They mentioned it needs to be fast"
IMPLICIT: constraint=perf
```

### Consolidation Templates
```
Multi-turn decision:
  U: "Should we use React?"
  A: "React or Vue both work"
  U: "Let's go with React"
  → decision: framework=React

Error-recovery:
  A: [tried X, failed]
  A: [tried Y, failed]
  A: [tried Z, worked]
  → approach=Z (X,Y failed)
```

### Extraction Schema
```yaml
facts:
  - type: requirement|decision|constraint|blocker
    key: short_identifier
    value: compressed_value
    confidence: high|medium|low
```

## 3. Hierarchical Output Compression

### L0 Ultra (<15 tokens)
Single actionable insight or decision.
```
Input: [500 word analysis of database options]
L0: "Use PostgreSQL: best fit for ACID + JSON needs"
```

### L1 Brief (<50 tokens)
Key findings as terse list.
```
L1: "DB choice: PostgreSQL
    - ACID compliance ✓
    - JSON support ✓
    - Team expertise ✓
    - Cost: ~$200/mo"
```

### L2 Standard (<200 tokens)
Structured summary with context.
```
L2: "## Recommendation: PostgreSQL

Selected over MongoDB (lacks ACID) and MySQL (weaker JSON).

Key factors:
1. Transaction requirements → need ACID
2. Semi-structured data → need JSON columns
3. Team has Postgres experience

Trade-off: Higher ops complexity vs. flexibility.

Next: provision RDS instance, est. $200/mo"
```

## 4. Code Compression Modes

### Signature-Only
```python
# BEFORE
def calculate_total(items: List[Item], tax_rate: float = 0.1) -> float:
    """Calculate total price including tax."""
    subtotal = sum(item.price * item.quantity for item in items)
    return subtotal * (1 + tax_rate)

# AFTER (signature-only)
def calculate_total(items: List[Item], tax_rate: float = 0.1) -> float: ...
```

### Interface Mode
```python
# Extract public API only
class OrderService:
    def create_order(self, items: List[Item]) -> Order: ...
    def get_order(self, order_id: str) -> Optional[Order]: ...
    def cancel_order(self, order_id: str) -> bool: ...
    # Private methods omitted
```

### Delta Mode
```diff
# Only changes + minimal context
class OrderService:
    # ... unchanged ...
+   def refund_order(self, order_id: str, reason: str) -> Refund:
+       """New: process refund for order."""
+       ...
    # ... unchanged ...
```

## 5. Document Compression Modes

### ToC Mode
```
# Original: 5000 word technical spec
# Compressed:
1. Overview - System handles real-time event processing
2. Architecture - Kafka + Flink pipeline
3. Data Model - Event schema with 12 fields
4. API - REST endpoints for ingestion/query
5. Deployment - K8s with auto-scaling
6. Monitoring - Prometheus + Grafana dashboards
```

### Entity Mode
```yaml
entities:
  systems: [Kafka, Flink, PostgreSQL, Redis]
  actions: [ingest, process, store, query]
  constraints: [<100ms latency, 10k events/sec]
  stakeholders: [data-team, platform-team]
relations:
  - Kafka → Flink: stream
  - Flink → PostgreSQL: persist
  - Redis: cache layer
```

## 6. Compression Quality Metrics

### Information Retention Score
```
IRS = (key_facts_after / key_facts_before) * 100

Target:
- Skill descriptions: IRS > 95%
- Context handoff: IRS > 85%
- Report summaries: IRS > 80%
```

### Actionability Score
```
AS = actionable_items_preserved / actionable_items_original

All compression should maintain AS = 100%
(Never lose action items in compression)
```
