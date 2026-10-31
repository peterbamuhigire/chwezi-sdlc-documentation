# Templates

## reference.docx

This directory must contain `reference.docx` — a styled Microsoft Word document
used by Pandoc as the style reference for all generated `.docx` output.

### Setup (one-time, per consultant machine)

1. Create or obtain a Word document with your organisation's styles defined:
   - **Heading 1, 2, 3** — document section headings
   - **Normal** — body text (font, size, line spacing)
   - **Table** — table style
   - **Code** — monospace for code blocks
   - **Title, Subtitle** — cover page styles

2. Save it as `templates/reference.docx` in this repository root

3. `templates/reference.docx` is gitignored — each consultant uses their own
   branded template. When the file is absent, `scripts/build-doc.sh` generates a
   temporary default style template, which needs the `docs` extra (`python-docx`).

### Gitignore Note

`reference.docx` is excluded from git (binary file, org-specific branding).
Only `templates/README.md` is committed.

### Pandoc Reference Doc Documentation

https://pandoc.org/MANUAL.html#option--reference-doc
