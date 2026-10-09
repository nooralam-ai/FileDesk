"""
FileDesk - a small Streamlit app to create, read, update and delete text files.
Run with:  streamlit run app.py
"""
from datetime import datetime
from pathlib import Path

import streamlit as st

# ---------- Setup ----------
WORKSPACE = Path("workspace")
WORKSPACE.mkdir(exist_ok=True)

st.set_page_config(page_title="FileDesk", page_icon="🗂️", layout="wide")

st.markdown(
    """
<style>
@import url('https://fonts.googleapis.com/css2?family=Bricolage+Grotesque:wght@500;700;800&family=IBM+Plex+Sans:wght@400;500;600&display=swap');

:root {
    --ink: #12343B;
    --teal: #0F6B6F;
    --teal-soft: #DCEFEE;
    --amber: #E8A33D;
    --paper: #F2F6F7;
    --line: #D3E0E2;
}
html, body, [class*="css"], .stMarkdown, .stTextInput, .stTextArea, button {
    font-family: 'IBM Plex Sans', sans-serif;
}
.stApp { background: var(--paper); }
#MainMenu, footer, header { visibility: hidden; }
.block-container { padding-top: 2rem; max-width: 1100px; }

/* Hero */
.hero {
    background: linear-gradient(135deg, #12343B 0%, #0F6B6F 100%);
    border-radius: 20px;
    padding: 2.2rem 2.4rem;
    color: #fff;
    margin-bottom: 1.4rem;
    border-bottom: 5px solid var(--amber);
}
.hero h1 {
    font-family: 'Bricolage Grotesque', sans-serif;
    font-weight: 800;
    font-size: 2.8rem;
    margin: 0;
    color: #fff;
    letter-spacing: -0.02em;
}
.hero p { margin: .4rem 0 0; color: #CFE6E6; font-size: 1.05rem; }

/* Stat tiles */
.stat {
    background: #fff;
    border: 1px solid var(--line);
    border-radius: 14px;
    padding: 1rem 1.2rem;
}
.stat .num {
    font-family: 'Bricolage Grotesque', sans-serif;
    font-size: 1.9rem; font-weight: 700; color: var(--ink);
}
.stat .lbl { color: #5B7377; font-size: .9rem; }

/* Tabs */
.stTabs [data-baseweb="tab-list"] { gap: 6px; border-bottom: 1px solid var(--line); }
.stTabs [data-baseweb="tab"] {
    font-family: 'Bricolage Grotesque', sans-serif;
    font-weight: 700; font-size: 1.02rem; color: #5B7377;
    padding: .6rem 1.1rem; border-radius: 10px 10px 0 0;
}
.stTabs [aria-selected="true"] { color: var(--teal); background: var(--teal-soft); }
.stTabs [data-baseweb="tab-highlight"] { background: var(--teal); }

/* Buttons */
.stButton > button, .stFormSubmitButton > button, .stDownloadButton > button {
    background: var(--teal); color: #fff; border: none; border-radius: 10px;
    font-weight: 600; padding: .55rem 1.3rem;
}
.stButton > button:hover, .stFormSubmitButton > button:hover { background: var(--ink); color: #fff; }
.stButton > button:focus-visible { outline: 3px solid var(--amber); }

/* Sidebar */
section[data-testid="stSidebar"] { background: #fff; border-right: 1px solid var(--line); }
.file-row {
    display: flex; justify-content: space-between; align-items: center;
    padding: .5rem .7rem; border-radius: 8px; margin-bottom: 4px;
    background: var(--paper); font-size: .92rem; color: var(--ink);
}
.file-row small { color: #5B7377; }
.empty { color: #5B7377; font-size: .95rem; padding: .6rem 0; }
</style>
""",
    unsafe_allow_html=True,
)


# ---------- Helpers ----------
def safe_path(name: str):
    """Keep every file inside the workspace folder (blocks ../ tricks)."""
    clean = Path(name.strip()).name
    return WORKSPACE / clean if clean else None


def list_files():
    return sorted([p for p in WORKSPACE.iterdir() if p.is_file()], key=lambda p: p.name.lower())


def fmt_size(n: int) -> str:
    for unit in ("B", "KB", "MB"):
        if n < 1024:
            return f"{n:.0f} {unit}" if unit == "B" else f"{n:.1f} {unit}"
        n /= 1024
    return f"{n:.1f} GB"


def flash(kind: str, msg: str):
    st.session_state["flash"] = (kind, msg)
    st.rerun()


# ---------- Hero ----------
st.markdown(
    """
<div class="hero">
  <h1>FileDesk</h1>
  <p>Create, read, update and delete text files from one clean screen.</p>
</div>
""",
    unsafe_allow_html=True,
)

if "flash" in st.session_state:
    kind, msg = st.session_state.pop("flash")
    getattr(st, kind)(msg)

files = list_files()
total = sum(p.stat().st_size for p in files)
latest = max((p.stat().st_mtime for p in files), default=None)

c1, c2, c3 = st.columns(3)
for col, num, lbl in [
    (c1, len(files), "Files in workspace"),
    (c2, fmt_size(total), "Total size"),
    (c3, datetime.fromtimestamp(latest).strftime("%d %b, %H:%M") if latest else "-", "Last change"),
]:
    col.markdown(f'<div class="stat"><div class="num">{num}</div><div class="lbl">{lbl}</div></div>', unsafe_allow_html=True)

st.write("")

# ---------- Sidebar: file explorer ----------
with st.sidebar:
    st.markdown("### Your files")
    if files:
        for p in files:
            st.markdown(
                f'<div class="file-row"><span>📄 {p.name}</span><small>{fmt_size(p.stat().st_size)}</small></div>',
                unsafe_allow_html=True,
            )
    else:
        st.markdown('<div class="empty">No files yet. Create your first one in the Create tab.</div>', unsafe_allow_html=True)
    st.caption("Files are stored in the local `workspace/` folder.")

# ---------- Tabs ----------
tab_create, tab_read, tab_update, tab_delete = st.tabs(["Create", "Read", "Update", "Delete"])

# CREATE
with tab_create:
    with st.form("create_form", clear_on_submit=True):
        name = st.text_input("File name", placeholder="notes.txt")
        data = st.text_area("Content", height=220, placeholder="Write something...")
        if st.form_submit_button("Create file"):
            path = safe_path(name)
            if path is None:
                st.error("Enter a file name.")
            elif path.exists():
                st.error(f"`{path.name}` already exists. Pick another name or use the Update tab.")
            else:
                path.write_text(data, encoding="utf-8")
                flash("success", f"Created `{path.name}`.")

# READ
with tab_read:
    if not files:
        st.markdown('<div class="empty">Nothing to read yet. Create a file first.</div>', unsafe_allow_html=True)
    else:
        choice = st.selectbox("Choose a file", [p.name for p in files], key="read_choice")
        path = WORKSPACE / choice
        content = path.read_text(encoding="utf-8", errors="replace")
        st.caption(f"{fmt_size(path.stat().st_size)} · modified {datetime.fromtimestamp(path.stat().st_mtime):%d %b %Y, %H:%M}")
        if content:
            st.code(content, language=None, wrap_lines=True)
        else:
            st.info("This file is empty.")
        st.download_button("Download file", content, file_name=choice)

# UPDATE
with tab_update:
    if not files:
        st.markdown('<div class="empty">Nothing to update yet. Create a file first.</div>', unsafe_allow_html=True)
    else:
        choice = st.selectbox("Choose a file", [p.name for p in files], key="update_choice")
        path = WORKSPACE / choice
        action = st.radio("What do you want to do?", ["Rename", "Append", "Overwrite"], horizontal=True)

        if action == "Rename":
            new_name = st.text_input("New file name", key="rename_input")
            if st.button("Rename file"):
                new_path = safe_path(new_name)
                if new_path is None:
                    st.error("Enter a new file name.")
                elif new_path.exists():
                    st.error(f"`{new_path.name}` already exists.")
                else:
                    path.rename(new_path)
                    flash("success", f"Renamed `{choice}` to `{new_path.name}`.")

        elif action == "Append":
            extra = st.text_area("Text to add at the end", height=140, key="append_input")
            if st.button("Append text"):
                if not extra:
                    st.error("Write the text you want to add.")
                else:
                    with open(path, "a", encoding="utf-8") as fs:
                        fs.write("\n" + extra)
                    flash("success", f"Added text to `{choice}`.")

        else:
            current = path.read_text(encoding="utf-8", errors="replace")
            new_data = st.text_area("New content (replaces everything)", value=current, height=220, key=f"over_{choice}")
            if st.button("Overwrite file"):
                path.write_text(new_data, encoding="utf-8")
                flash("success", f"Overwrote `{choice}`.")

# DELETE
with tab_delete:
    if not files:
        st.markdown('<div class="empty">Nothing to delete.</div>', unsafe_allow_html=True)
    else:
        choice = st.selectbox("Choose a file", [p.name for p in files], key="delete_choice")
        sure = st.checkbox(f"Delete `{choice}` permanently. This can't be undone.")
        if st.button("Delete file", disabled=not sure):
            (WORKSPACE / choice).unlink()
            flash("success", f"Deleted `{choice}`.")