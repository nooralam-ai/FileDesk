# FileDesk

A simple Streamlit app for managing text files: **create, read, update (rename / append / overwrite) and delete** them from a clean web UI.

Built as an upgrade of a command-line Python file handler.

## Features
- Create files with content, with a duplicate-name check
- Read and download any file
- Rename, append to, or overwrite files
- Delete with a confirmation checkbox
- Sidebar file explorer and live stats (file count, total size, last change)
- All files stay inside a local `workspace/` folder, so paths like `../` can't escape it

## Run it
```bash
pip install -r requirements.txt
streamlit run app.py
```

## Tech
Python · Streamlit · pathlib