---
name: doc-processor
description: |
  Document CRUD for .docx/.pdf/.txt/.rtf/.md. Features: tracked changes, comments, tables, images, templates, conversion.
  TRIGGERS: document, docx, pdf, Word, report, memo, create report, edit document, track changes, extract text, convert
---

# Document Processor

Create, edit, analyze, convert documents. Supports .docx/.pdf/.txt/.rtf/.md with tables and images.

## Formats

| Format | Capabilities |
|--------|-------------|
| .docx | Full read/write, formatting |
| .pdf | Read, text extraction |
| .txt/.md | Full read/write |

## Commands

```bash
/doc-processor create --type docx --template report
/doc-processor edit <file> --track-changes
/doc-processor extract <file> --format text
/doc-processor convert <file> --to pdf
```

## Features

- **Create**: Blank, template-based, or from conversion
- **Edit**: Text, formatting, headings, tables, track changes, comments
- **Analyze**: Text extraction, structure, word count, search
- **Convert**: docx↔pdf, md→docx/pdf, any→txt

## Limits

- Complex PDF layouts may not convert perfectly
- Max file size: 50MB
- Encrypted files require password
