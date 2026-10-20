#!/usr/bin/env python3
"""
MarkItDown TUI - Convert anything to Markdown.
"""

import subprocess
import sys
from pathlib import Path

from textual.app import App, ComposeResult
from textual.containers import Horizontal, Vertical
from textual.widgets import Header, Footer, Static, Button, Label, Input
from textual.binding import Binding


def get_downloads_folder():
    home = Path.home()
    downloads = home / "Downloads"
    if not downloads.exists():
        downloads.mkdir(parents=True, exist_ok=True)
    return downloads


class MarkItDownApp(App):
    CSS = """
    Screen { background: $background; }
    #title-bar {
        height: 3;
        content-align: center middle;
        background: $accent;
        color: $text;
        text-style: bold;
    }
    #subtitle {
        height: 2;
        content-align: center middle;
        color: $text-muted;
        background: $surface;
    }
    #main { padding: 1 2; height: 1fr; }
    #path-label { margin-top: 1; color: $text-muted; text-style: bold; }
    #btn-row { height: 3; margin-top: 1; align: center middle; }
    #btn-convert { background: $accent; color: $text; margin-right: 2; min-width: 18; }
    #status {
        height: 8;
        border: solid $panel;
        padding: 1 2;
        background: $surface;
        margin-top: 1;
        color: $text;
    }
    """

    BINDINGS = [
        Binding("ctrl+q", "quit", "Quit"),
        Binding("f1", "action_clear", "Clear"),
    ]

    def compose(self) -> ComposeResult:
        yield Header(show_clock=True)
        yield Static("MarkItDown TUI — Convert any file to Markdown", id="title-bar")
        yield Static("PDF · DOCX · XLSX · PPTX · Images · HTML · CSV · JSON · XML", id="subtitle")
        with Vertical(id="main"):
            yield Label("File Path:", id="path-label")
            yield Input(placeholder=r"Paste file path here e.g. C:\Users\You\file.pdf", id="path-input")
            with Horizontal(id="btn-row"):
                yield Button("⚡ Convert", id="btn-convert", variant="primary")
                yield Button("Clear", id="btn-clear")
            yield Static("Ready. Paste a file path and hit Convert.", id="status")
        yield Footer()

    def set_status(self, text: str):
        self.query_one("#status", Static).update(text)

    def on_button_pressed(self, event: Button.Pressed):
        if event.button.id == "btn-convert":
            self.do_convert()
        elif event.button.id == "btn-clear":
            self.action_clear()

    def on_input_submitted(self, event: Input.Submitted):
        self.do_convert()

    def do_convert(self):
        raw_path = self.query_one("#path-input", Input).value.strip().strip('"').strip("'")

        if not raw_path:
            self.set_status("ERROR: No path entered.")
            return

        file_path = Path(raw_path)
        if not file_path.exists():
            self.set_status(f"ERROR: File not found:\n{raw_path}")
            return

        self.set_status(f"Converting: {file_path.name} ...\n(this may take a moment)")

        try:
            from markitdown import MarkItDown
        except ImportError:
            self.set_status("markitdown not found. Installing...\nRun: pip install markitdown[pdf]")
            return

        try:
            md = MarkItDown()
            result = md.convert(str(file_path))
            content = result.text_content

            downloads = get_downloads_folder()
            out_name = file_path.stem + ".md"
            out_path = downloads / out_name

            counter = 1
            while out_path.exists():
                out_path = downloads / f"{file_path.stem}_{counter}.md"
                counter += 1

            out_path.write_text(content, encoding="utf-8")
            self.set_status(f"DONE!\nSaved to: {out_path}\nCharacters: {len(content):,}")

        except Exception as e:
            self.set_status(f"ERROR: {e}")

    def action_clear(self):
        self.query_one("#path-input", Input).value = ""
        self.set_status("Cleared. Ready for next file.")


if __name__ == "__main__":
    app = MarkItDownApp()
    app.run()