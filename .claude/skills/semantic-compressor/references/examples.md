# Compression Examples

## Skill Description Examples

### Example 1: Document Processing Skill
```
BEFORE (89 tokens):
"This skill provides comprehensive document creation, editing, and analysis
capabilities with full support for tracked changes, comments, formatting
preservation, and text extraction. Use this skill when Claude needs to work
with professional documents in .docx format for any of the following tasks:
creating new documents from scratch, modifying or editing existing content,
working with tracked changes and revision history, or adding comments and
annotations to documents."

AFTER (24 tokens):
"Word (.docx) handler: create/edit/analyze. Features: tracked changes,
comments, formatting. TRIGGERS: document, docx, Word, report, edit document"

Ratio: 3.7:1
```

### Example 2: Data Analysis Skill
```
BEFORE (67 tokens):
"This skill enables users to perform data analysis tasks including reading
CSV and Excel files, performing statistical calculations, creating
visualizations, and generating reports. It should be triggered when users
ask about analyzing data, creating charts, or working with spreadsheets."

AFTER (19 tokens):
"Data analysis: CSV/Excel → stats/viz/reports.
TRIGGERS: analyze data, chart, spreadsheet, statistics, plot"

Ratio: 3.5:1
```

## Context Compression Examples

### Example 1: Multi-turn Development Conversation
```
BEFORE (312 tokens):
User: "Hi there! I'm working on a new project and could use some help."
Assistant: "Of course! I'd be happy to help. What kind of project are you working on?"
User: "I'm building a web app for managing tasks. Something like Todoist but simpler."
Assistant: "Great idea! What tech stack are you thinking about using?"
User: "I was thinking maybe React for the frontend, but I'm not sure about the backend.
       What do you recommend?"
Assistant: "For a task management app, you have several good options. Node.js with
            Express is popular and JavaScript throughout. Python with FastAPI is
            another great choice if you prefer Python. Django is more full-featured."
User: "Let's go with FastAPI since I know Python better."
Assistant: "Excellent choice! FastAPI is fast, has great documentation, and auto-generates
            API docs. Should we start with the data models?"
User: "Yes, but I also need user authentication. Can we use JWT?"
Assistant: "Absolutely! JWT is perfect for this. We'll need to set up password hashing too."

AFTER (52 tokens) - DICE format:
[GOAL] Build task management web app (Todoist-simple)
[STATE] Stack decided: React frontend + FastAPI backend
[CONSTRAINT] User knows Python > JS; needs auth
[DECISION] JWT for auth, FastAPI for backend
[NEXT] Design data models, then implement JWT auth

Ratio: 6:1
```

### Example 2: Debugging Session
```
BEFORE (198 tokens):
User: "My API is returning 500 errors sometimes"
Assistant: "Let me help debug. Can you share the error logs?"
User: "Here's the traceback: [long traceback]"
Assistant: "I see a database connection error. Are you using connection pooling?"
User: "Not sure, let me check... no, I'm creating a new connection each request"
Assistant: "That's likely the issue. Under load, you're exhausting connections."
User: "How do I fix it?"
Assistant: "Use SQLAlchemy's connection pool. Set pool_size=5, max_overflow=10"
User: "That fixed it! But now I'm seeing slow queries"
Assistant: "Let's add query logging to identify the slow ones"

AFTER (41 tokens) - DICE format:
[GOAL] Fix API 500 errors
[STATE] Root cause: DB connection exhaustion (no pooling)
[FIXED] Added SQLAlchemy pool (size=5, overflow=10)
[NEW_ISSUE] Slow queries identified
[NEXT] Add query logging, optimize slow queries

Ratio: 4.8:1
```

## Output Compression Examples

### Example 1: Code Review Analysis
```
BEFORE (L2 - 180 tokens):
"The code review identified several issues. First, there's a potential SQL
injection vulnerability in the user search function where user input is
directly concatenated into the query string. Second, the error handling is
inconsistent - some functions return None on error while others raise
exceptions. Third, there's significant code duplication in the authentication
middleware that could be refactored. Fourth, several functions exceed 50 lines
and should be broken down. Finally, test coverage is only at 45% with no tests
for edge cases. Priority should be fixing the SQL injection immediately, then
standardizing error handling, then addressing code quality issues."

L1 (48 tokens):
"Critical: SQL injection in user_search (fix NOW)
High: Inconsistent error handling (None vs exceptions)
Medium: Auth middleware duplication, long functions
Low: 45% test coverage, no edge case tests
Action: SQLi fix → error standardization → refactor"

L0 (12 tokens):
"CRITICAL: Fix SQL injection in user_search immediately"

Ratios: L2→L1 = 3.75:1, L2→L0 = 15:1
```

### Example 2: Research Summary
```
BEFORE (L2 - 156 tokens):
"Analysis of three database options for the project. PostgreSQL offers strong
ACID compliance, excellent JSON support, and the team has existing expertise.
Cost estimate $200/month on RDS. MongoDB provides flexible schema and
horizontal scaling but lacks transaction support needed for financial data.
Cost estimate $180/month. MySQL is cost-effective at $120/month but has weaker
JSON support and the team would need training. Recommendation: PostgreSQL
despite higher cost due to transaction requirements and team familiarity.
The JSON column support will handle our semi-structured metadata needs."

L1 (38 tokens):
"DB comparison:
- PostgreSQL: ACID ✓, JSON ✓, team exp ✓, $200/mo → RECOMMENDED
- MongoDB: flexible but no ACID ×, $180/mo
- MySQL: cheap $120/mo but weak JSON, needs training"

L0 (9 tokens):
"Use PostgreSQL: ACID + JSON + team expertise"

Ratios: L2→L1 = 4.1:1, L2→L0 = 17.3:1
```

## Code Compression Examples

### Signature-Only Mode
```python
# BEFORE (142 tokens)
class UserService:
    def __init__(self, db: Database, cache: Redis):
        self.db = db
        self.cache = cache
        self.logger = logging.getLogger(__name__)

    def get_user(self, user_id: str) -> Optional[User]:
        """Fetch user by ID, checking cache first."""
        cached = self.cache.get(f"user:{user_id}")
        if cached:
            return User.from_json(cached)
        user = self.db.query(User).filter_by(id=user_id).first()
        if user:
            self.cache.set(f"user:{user_id}", user.to_json(), ex=3600)
        return user

    def create_user(self, email: str, name: str) -> User:
        """Create new user with email validation."""
        if not self._validate_email(email):
            raise ValueError("Invalid email")
        user = User(email=email, name=name)
        self.db.add(user)
        self.db.commit()
        return user

# AFTER (38 tokens)
class UserService:
    def __init__(self, db: Database, cache: Redis): ...
    def get_user(self, user_id: str) -> Optional[User]: ...
    def create_user(self, email: str, name: str) -> User: ...

Ratio: 3.7:1
```

### Interface + Docstring Mode
```python
# AFTER (52 tokens) - preserves intent
class UserService:
    """User CRUD with Redis caching."""
    def __init__(self, db: Database, cache: Redis): ...
    def get_user(self, user_id: str) -> Optional[User]:
        """Fetch user, cache-first (1hr TTL)."""
    def create_user(self, email: str, name: str) -> User:
        """Create user with email validation."""

Ratio: 2.7:1 (more context preserved)
```

## Document Compression Examples

### ToC Mode
```
BEFORE: 3200-word API documentation

AFTER (67 tokens):
# API Documentation Summary
1. Auth - JWT bearer tokens, 1hr expiry
2. Users - CRUD endpoints, pagination supported
3. Tasks - Create/update/delete, bulk operations available
4. Webhooks - Event subscriptions, retry policy 3x
5. Rate Limits - 1000 req/hr per API key
6. Errors - Standard HTTP codes, error_code in body
```

### Entity-Relation Mode
```yaml
# BEFORE: 2500-word system architecture doc

# AFTER (45 tokens):
entities:
  services: [api-gateway, user-svc, task-svc, notification-svc]
  data: [PostgreSQL, Redis, S3]
  infra: [K8s, ALB, CloudWatch]
flow:
  request → gateway → service → db
  async: service → queue → notification
deps:
  user-svc → PostgreSQL, Redis
  task-svc → PostgreSQL, S3
```
