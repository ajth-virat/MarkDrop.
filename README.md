# MarkItDown TUI

Drop in a file path, get a Markdown file back. That's the whole app.


## Just want to use it?

1. Download `markitdown-tui.exe` from the Releases page. https://github.com/ajth-virat/MarkDrop/releases/latest
2. Double-click it. A terminal window opens.
3. Paste the full path to a file (quotes are fine) and press Enter.
4. Your `.md` file is in your Downloads folder.

No Python needed. Windows only for now. The exe is around 160 MB because it carries everything inside it, so the first launch can take a few seconds.

## What it converts

PDF, DOCX, XLSX, PPTX, HTML, CSV, JSON, XML and images. The conversion itself is done by Microsoft's [MarkItDown](https://github.com/microsoft/markitdown). This project is a small Textual interface around it.

Scanned PDFs and photos of text won't give you much, since there's no OCR.

## Run from source

    pip install textual "markitdown[pdf]"
    python app.py

Needs Python 3.10+. Quit with Ctrl+Q.

## Build the exe yourself

    pip install pyinstaller
    python build_exe.py

The result lands in `dist/markitdown-tui.exe`.

## Limits

- One file at a time.
- Output always goes to Downloads. If a name is taken, you get `name_1.md`, `name_2.md`.
