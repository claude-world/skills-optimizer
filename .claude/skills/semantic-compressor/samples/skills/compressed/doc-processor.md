---
name: doc-processor
description: |
  Document creation/editing/analysis/conversion for Microsoft Word (.docx), PDF (.pdf), plain text (.txt), Rich Text (.rtf), and Markdown (.md), preserving formatting and structure.
  Features: templates, tracked changes/revision history, comments/annotations, tables, images, text extraction, statistics, search, OCR-assisted conversion.
  TRIGGERS: document, Word document, PDF, plain text, Rich Text, Markdown, writing reports, creating memos, editing contracts, extracting information from PDFs, standardized documents, templates, business documents, professional document workflows
---

# Document Processor

## Formats

| Format | Capability |
|---|---|
| Microsoft Word `.docx` | Full read/write with formatting |
| PDF `.pdf` | Read, text extraction, basic manipulation |
| Plain Text `.txt` | Full read/write |
| Rich Text `.rtf` | Basic read/write |
| Markdown `.md` | Full read/write with conversion |

## Features

1. Create blank, template-based, or converted documents.
2. Edit text; fonts/styles/colors/alignment; headings/lists/tables; tracked changes; inline comments/annotations.
3. Extract text from every supported format; identify headings/sections/hierarchy; calculate word/page counts and reading-time estimates; search text/patterns.
4. Convert Word→PDF, PDF→Word with OCR when needed, Markdown→Word/PDF, or any supported format→plain text.

## Commands

```text
/doc-processor create --type docx --template report
/doc-processor edit <file_path> --track-changes
/doc-processor extract <file_path> --format text
/doc-processor convert <input_file> --to pdf
/doc-processor create report
/doc-processor edit contract.docx --track-changes --comment "Updated clause 3.2"
/doc-processor extract invoice.pdf --format text --preserve-layout
```

`/doc-processor create report` creates a Word document with standard report formatting: a title page, table of contents placeholder, and section headers.

## Safety, limits, and recovery

- Back up important documents before editing; use tracked changes for collaboration; verify formatting after conversion; expect image-heavy files to take longer.
- Complex PDF layouts may convert imperfectly. Advanced Word macros/embedded objects may be unsupported. Files `>50MB` may be slower. Encrypted/password-protected files require the password.
- On error, verify the path exists, permissions allow access, the file is uncorrupted and supported, then retry conversion with a simpler target format.

References: templates `templates.md`, formats `formats.md`, troubleshooting `troubleshooting.md`.
