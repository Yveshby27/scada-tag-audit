"""PyInstaller top-level entry: invokes the packaged CLI as if via `python -m scada_tag_audit`."""

from scada_tag_audit.cli import main

if __name__ == "__main__":
    main()
