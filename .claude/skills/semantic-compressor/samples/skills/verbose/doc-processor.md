---
name: doc-processor
description: |
  This comprehensive skill provides advanced document processing capabilities that allow Claude
  to work with various document formats including Word documents, PDF files, and plain text files.
  The skill enables users to perform a wide range of operations such as creating new documents
  from scratch, editing existing documents, extracting text content, converting between different
  formats, and analyzing document structure.

  Key features include:
  - Full support for Microsoft Word (.docx) format with formatting preservation
  - PDF text extraction and basic manipulation capabilities
  - Tracked changes and revision history management
  - Comment insertion and annotation features
  - Table creation and manipulation
  - Image embedding support
  - Template-based document generation

  Use this skill when Claude needs to help users with any document-related tasks, including but
  not limited to: writing reports, creating memos, editing contracts, extracting information from
  PDFs, or generating standardized documents from templates. The skill is particularly useful for
  business and professional document workflows where formatting and consistency are important.
---

# Document Processor Skill

This skill provides comprehensive document processing capabilities for working with various document formats.

## Overview

The Document Processor skill is designed to help users work with documents in a variety of formats. It provides a complete set of tools for creating, editing, and analyzing documents while maintaining proper formatting and structure.

## Supported Formats

The following document formats are fully supported by this skill:

| Format | Extension | Capabilities |
|--------|-----------|--------------|
| Microsoft Word | .docx | Full read/write with formatting |
| PDF | .pdf | Read and text extraction |
| Plain Text | .txt | Full read/write |
| Rich Text | .rtf | Basic read/write support |
| Markdown | .md | Full read/write with conversion |

## Features

### Document Creation

You can create new documents from scratch using this skill. The skill supports:

1. **Blank Document Creation**: Start with an empty document and add content
2. **Template-Based Creation**: Use predefined templates for common document types
3. **Conversion Creation**: Create documents by converting from other formats

### Document Editing

The skill provides comprehensive editing capabilities:

- **Text Editing**: Add, modify, or remove text content
- **Formatting**: Apply fonts, styles, colors, and alignment
- **Structural Editing**: Work with headings, lists, tables
- **Track Changes**: Enable revision tracking for collaborative editing
- **Comments**: Add inline comments and annotations

### Document Analysis

Analyze documents to extract useful information:

- **Text Extraction**: Get plain text content from any supported format
- **Structure Analysis**: Identify headings, sections, and document hierarchy
- **Statistics**: Word count, page count, reading time estimates
- **Content Search**: Find specific text or patterns within documents

### Format Conversion

Convert documents between different formats:

- Word to PDF
- PDF to Word (with OCR if needed)
- Markdown to Word/PDF
- Any format to plain text

## Usage

### Basic Commands

```
/doc-processor create --type docx --template report
/doc-processor edit <file_path> --track-changes
/doc-processor extract <file_path> --format text
/doc-processor convert <input_file> --to pdf
```

### Examples

#### Creating a Report

To create a new report document, use the following approach:

```
/doc-processor create report
```

This will create a new Word document with standard report formatting including title page, table of contents placeholder, and section headers.

#### Editing with Track Changes

When you need to edit a document while preserving the change history:

```
/doc-processor edit contract.docx --track-changes --comment "Updated clause 3.2"
```

#### Extracting Text from PDF

To get the text content from a PDF file:

```
/doc-processor extract invoice.pdf --format text --preserve-layout
```

## Best Practices

When working with documents using this skill, follow these best practices:

1. **Always Backup**: Before making changes to important documents, create a backup
2. **Use Track Changes**: For collaborative work, enable track changes to maintain history
3. **Check Formatting**: After conversion, verify that formatting was preserved correctly
4. **Consider File Size**: Large documents with many images may take longer to process

## Limitations

Please be aware of the following limitations:

- Complex PDF layouts may not convert perfectly to editable formats
- Some advanced Word features (macros, embedded objects) may not be fully supported
- Very large documents (>50MB) may experience slower processing times
- Encrypted or password-protected documents require the password to access

## Error Handling

If you encounter errors while using this skill:

1. Check that the file path is correct and the file exists
2. Verify that you have proper permissions to access the file
3. Ensure the file is not corrupted or in an unsupported format
4. For conversion errors, try a simpler target format first

## See Also

- [Template Gallery](templates.md) - Browse available document templates
- [Format Guide](formats.md) - Detailed format support information
- [Troubleshooting](troubleshooting.md) - Common issues and solutions
