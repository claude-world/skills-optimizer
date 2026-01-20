# Contributing to Semantic Compressor

Thank you for your interest in contributing to Semantic Compressor!

## How to Contribute

### Adding New Sample Files

1. Add verbose file to `samples/*/verbose/`
2. Run `/semantic-compressor <file>` to compress
3. Pass all 5 phases (iterate if NEEDS_IMPROVEMENT)
4. Commit both versions

### File Naming

- Skills: `.claude/skills/semantic-compressor/samples/skills/`
- Agents: `.claude/skills/semantic-compressor/samples/agents/`
- Use descriptive names: `doc-processor.md`, `api-tester.md`

### Quality Requirements

All compressed files must:

- [ ] Pass Phase 4 LLM comparison
- [ ] Preserve 100% of triggers
- [ ] Preserve 100% of commands
- [ ] Preserve 100% of tools
- [ ] Achieve minimum 2:1 compression ratio

### Testing Your Changes

```bash
# Verify a single file
/semantic-compressor verify path/to/file.md

# Run full benchmark
/semantic-compressor benchmark
```

### Commit Messages

Follow conventional commits:

```
feat(samples): add new api-tester sample
fix(skill): improve compression rules for triggers
docs: update README with new examples
```

## Reporting Issues

When reporting bugs, please include:

1. The file you were trying to compress
2. Phase where the issue occurred
3. The comparison result (if applicable)
4. Expected vs actual behavior

## Code of Conduct

- Be respectful and constructive
- Focus on improving the tool
- Share knowledge and help others

## Questions?

Open an issue on GitHub or join the [Claude World Discord](https://discord.gg/claude-world).

---

Thank you for contributing!
