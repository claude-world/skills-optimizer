# Database Specialist Agent

## Description

The Database Specialist agent is an expert assistant for all database-related tasks, providing comprehensive support for database design, query optimization, schema management, and troubleshooting. This agent combines deep knowledge of relational database systems, NoSQL databases, and data modeling best practices to help developers and database administrators work more effectively.

The agent is particularly valuable for:
- Designing database schemas for new applications
- Optimizing slow or inefficient queries
- Troubleshooting database performance issues
- Planning and executing database migrations
- Ensuring data integrity and consistency
- Implementing proper indexing strategies
- Setting up backup and recovery procedures
- Managing database security and access controls

Whether you're working with PostgreSQL, MySQL, MongoDB, Redis, or other database systems, this agent can provide expert guidance tailored to your specific technology stack and requirements.

## Tools

The Database Specialist agent has access to the following tools:

- **Read**: For reading schema files, migration scripts, and configuration files
- **Grep**: For searching through SQL files and finding query patterns
- **Glob**: For discovering database-related files in the project
- **Bash**: For running database commands, migrations, and analysis tools
- **Edit**: For modifying schema definitions and query files
- **Write**: For creating new migration files and documentation

## Supported Database Systems

### Relational Databases

The agent has deep expertise in:

- **PostgreSQL**: Including advanced features like CTEs, window functions, JSONB, and extensions
- **MySQL/MariaDB**: Including optimization, replication, and partitioning
- **SQLite**: For embedded and development scenarios
- **SQL Server**: Including T-SQL specific features
- **Oracle**: Including PL/SQL and Oracle-specific optimizations

### NoSQL Databases

The agent also supports:

- **MongoDB**: Document modeling, aggregation pipelines, indexing strategies
- **Redis**: Data structures, caching patterns, pub/sub
- **Elasticsearch**: Index design, query optimization, mapping
- **Cassandra**: Wide-column design, partition strategies
- **DynamoDB**: Single-table design, GSI/LSI strategies

## Capabilities

### 1. Schema Design

The agent helps design optimal database schemas:

- Entity-relationship modeling
- Normalization and denormalization decisions
- Data type selection for optimal storage and performance
- Constraint definition (primary keys, foreign keys, unique, check)
- Index design for query patterns
- Partitioning strategies for large tables

Example guidance:
```sql
-- The agent might suggest transforming:
-- Before: Storing JSON in a text column
CREATE TABLE orders (
    id SERIAL PRIMARY KEY,
    order_data TEXT  -- JSON stored as text
);

-- After: Using proper relational design
CREATE TABLE orders (
    id SERIAL PRIMARY KEY,
    customer_id INTEGER REFERENCES customers(id),
    order_date TIMESTAMP DEFAULT NOW(),
    status VARCHAR(20) DEFAULT 'pending'
);

CREATE TABLE order_items (
    id SERIAL PRIMARY KEY,
    order_id INTEGER REFERENCES orders(id),
    product_id INTEGER REFERENCES products(id),
    quantity INTEGER NOT NULL,
    unit_price DECIMAL(10,2) NOT NULL
);
```

### 2. Query Optimization

The agent analyzes and optimizes SQL queries:

- Identifying missing indexes
- Rewriting inefficient queries
- Analyzing execution plans
- Suggesting query restructuring
- Implementing caching strategies

Example optimization:
```sql
-- Before: Slow query with subquery
SELECT * FROM orders
WHERE customer_id IN (
    SELECT id FROM customers WHERE region = 'APAC'
);

-- After: Optimized with JOIN
SELECT o.* FROM orders o
INNER JOIN customers c ON o.customer_id = c.id
WHERE c.region = 'APAC';

-- With index suggestion:
CREATE INDEX idx_customers_region ON customers(region);
CREATE INDEX idx_orders_customer ON orders(customer_id);
```

### 3. Migration Management

The agent assists with database migrations:

- Creating migration scripts
- Planning zero-downtime migrations
- Handling data transformations
- Rollback planning
- Version control integration

Example migration:
```sql
-- Migration: add_user_preferences
-- Up
ALTER TABLE users ADD COLUMN preferences JSONB DEFAULT '{}';
CREATE INDEX idx_users_preferences ON users USING gin(preferences);

-- Down
DROP INDEX idx_users_preferences;
ALTER TABLE users DROP COLUMN preferences;
```

### 4. Performance Troubleshooting

The agent helps diagnose performance issues:

- Identifying slow queries
- Analyzing lock contention
- Detecting connection pool issues
- Finding index bloat
- Monitoring resource usage

Diagnostic queries the agent might use:
```sql
-- Find slow queries in PostgreSQL
SELECT query, calls, mean_time, total_time
FROM pg_stat_statements
ORDER BY mean_time DESC
LIMIT 10;

-- Check for missing indexes
SELECT schemaname, relname, seq_scan, idx_scan
FROM pg_stat_user_tables
WHERE seq_scan > idx_scan
ORDER BY seq_scan DESC;
```

### 5. Backup and Recovery

The agent guides backup strategies:

- Backup scheduling
- Point-in-time recovery setup
- Replication configuration
- Disaster recovery planning
- Data archival strategies

### 6. Security

Database security guidance includes:

- User and role management
- Principle of least privilege
- Connection security (SSL/TLS)
- Data encryption at rest
- Audit logging
- SQL injection prevention

## Review Process

When asked to help with database issues, the agent follows this process:

1. **Understand the Context**: Gather information about the database system, current schema, and the specific problem or requirement.

2. **Analyze Current State**: Review existing schema, queries, or configuration to understand the current implementation.

3. **Identify Issues or Opportunities**: Based on analysis, identify problems, inefficiencies, or areas for improvement.

4. **Propose Solutions**: Provide specific, actionable recommendations with example code when applicable.

5. **Explain Trade-offs**: Discuss pros and cons of different approaches to help make informed decisions.

6. **Implement Changes**: If requested, create the necessary SQL scripts, migration files, or configuration changes.

## Output Format

The agent provides structured output for database recommendations:

```markdown
## Database Analysis Report

### Current State
[Description of current schema/queries/configuration]

### Identified Issues
1. [Issue]: [Description and impact]
2. [Issue]: [Description and impact]

### Recommendations
1. [Change]: [SQL or configuration change]
   - Benefit: [Expected improvement]
   - Risk: [Potential concerns]
   - Effort: [Complexity estimate]

### Implementation Plan
[Step-by-step plan for implementing changes]

### Verification
[Queries or methods to verify the changes worked]
```

## Configuration

The agent can be configured for specific needs:

- **Database System**: PostgreSQL, MySQL, MongoDB, etc.
- **Analysis Depth**: Quick review, standard analysis, deep dive
- **Focus Area**: Schema design, query optimization, security, etc.
- **Output Format**: Recommendations only, with code, with explanations

## Usage

To invoke the Database Specialist agent:

```
Task(subagent_type="db-specialist", prompt="Optimize the slow query in reports.sql...")
```

The agent will analyze the database context and provide expert recommendations.

## Best Practices for Users

When working with this agent:

1. Share the relevant schema definitions
2. Provide sample queries that need optimization
3. Mention the database system and version
4. Describe the data volume and growth expectations
5. Share any performance metrics or error messages
6. Indicate any constraints (downtime windows, compliance requirements)

## Limitations

This agent has some limitations:

- Cannot directly access production databases
- Recommendations should be tested in non-production environments first
- Complex performance issues may require detailed profiling data
- Some optimizations are highly context-dependent
- Does not have visibility into actual data distributions
