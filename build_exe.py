#!/usr/bin/env python3
"""
build_exe.py — Run this once to create markitdown-tui.exe
Requires: pip install pyinstaller
"""

import subprocess
import sys
import os
from pathlib import Path

def main():
    print("🔧 Checking PyInstaller...")
    try:
        import PyInstaller
        print(f"   PyInstaller {PyInstaller.__version__} found.")
    except ImportError:
        print("   Installing PyInstaller...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "pyinstaller"])
        print("   Done.")

    script = Path(__file__).parent / "app.py"
    print(f"\n📦 Building EXE from: {script}")

    cmd = [
        sys.executable, "-m", "PyInstaller",
        "--onefile",                    # Single exe
        "--name", "markitdown-tui",     # Output name
        "--console",                    # Keep terminal (required for Textual TUI)
        "--clean",
        str(script)
    ]

    print(f"   Running: {' '.join(cmd)}\n")
    result = subprocess.run(cmd)

    if result.returncode == 0:
        dist = Path("dist") / "markitdown-tui.exe"
        if not dist.exists():
            dist = Path("dist") / "markitdown-tui"  # Linux/Mac fallback
        print(f"\n✅ Build complete!")
        print(f"   EXE location: {dist.resolve()}")
        print(f"\n💡 Copy markitdown-tui.exe anywhere and run it — no Python needed.")
    else:
        print("\n❌ Build failed. Check the output above.")

if __name__ == "__main__":
    main()
