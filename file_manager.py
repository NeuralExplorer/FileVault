import streamlit as st
from pathlib import Path
import os
import time

# ── Page config ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="FileVault",
    page_icon="🗂️",
    layout="centered",
)

# ── Custom CSS ────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@300;400;500;600;700&family=JetBrains+Mono:wght@400;500&display=swap');

/* ── Reset & Base ── */
html, body, [class*="css"] {
    font-family: 'Space Grotesk', sans-serif;
}

.stApp {
    background: #0a0a0f;
    color: #e8e8f0;
}

/* ── Header ── */
.vault-header {
    text-align: center;
    padding: 3rem 0 1.5rem;
}
.vault-logo {
    font-size: 3.2rem;
    font-weight: 700;
    letter-spacing: -2px;
    background: linear-gradient(135deg, #7c6af7 0%, #a78bfa 50%, #c4b5fd 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    line-height: 1;
}
.vault-tagline {
    font-size: 0.85rem;
    font-weight: 400;
    letter-spacing: 0.25em;
    text-transform: uppercase;
    color: #6b6b80;
    margin-top: 0.4rem;
}

/* ── Operation pills ── */
.op-grid {
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 0.75rem;
    margin: 2rem 0;
}
.op-pill {
    background: #14141e;
    border: 1px solid #1e1e2e;
    border-radius: 12px;
    padding: 1rem 0.5rem;
    text-align: center;
    cursor: pointer;
    transition: all 0.2s ease;
}
.op-pill:hover {
    border-color: #7c6af7;
    background: #18182a;
}
.op-pill.active {
    border-color: #7c6af7;
    background: linear-gradient(135deg, #1a1535, #20183c);
    box-shadow: 0 0 20px rgba(124, 106, 247, 0.15);
}
.op-icon { font-size: 1.5rem; }
.op-label {
    font-size: 0.7rem;
    font-weight: 600;
    letter-spacing: 0.08em;
    text-transform: uppercase;
    color: #8888a0;
    margin-top: 0.35rem;
}

/* ── Card ── */
.card {
    background: #14141e;
    border: 1px solid #1e1e2e;
    border-radius: 16px;
    padding: 1.75rem 2rem;
    margin-bottom: 1rem;
}
.card-title {
    font-size: 1rem;
    font-weight: 600;
    color: #c4b5fd;
    letter-spacing: 0.02em;
    margin-bottom: 1.25rem;
    display: flex;
    align-items: center;
    gap: 0.5rem;
}

/* ── Streamlit widget overrides ── */
div[data-testid="stTextInput"] input,
div[data-testid="stTextArea"] textarea,
div[data-testid="stSelectbox"] select {
    background: #0f0f18 !important;
    border: 1px solid #2a2a3e !important;
    border-radius: 10px !important;
    color: #e8e8f0 !important;
    font-family: 'JetBrains Mono', monospace !important;
    font-size: 0.875rem !important;
}
div[data-testid="stTextInput"] input:focus,
div[data-testid="stTextArea"] textarea:focus {
    border-color: #7c6af7 !important;
    box-shadow: 0 0 0 2px rgba(124, 106, 247, 0.2) !important;
}

div[data-testid="stTextInput"] label,
div[data-testid="stTextArea"] label,
div[data-testid="stSelectbox"] label {
    color: #8888a0 !important;
    font-size: 0.8rem !important;
    font-weight: 500 !important;
    letter-spacing: 0.06em !important;
    text-transform: uppercase !important;
}

/* ── Primary button ── */
div[data-testid="stButton"] button[kind="primary"] {
    background: linear-gradient(135deg, #7c6af7, #a78bfa) !important;
    border: none !important;
    border-radius: 10px !important;
    color: white !important;
    font-family: 'Space Grotesk', sans-serif !important;
    font-weight: 600 !important;
    font-size: 0.875rem !important;
    letter-spacing: 0.04em !important;
    padding: 0.6rem 1.5rem !important;
    transition: all 0.2s !important;
    width: 100% !important;
}
div[data-testid="stButton"] button[kind="primary"]:hover {
    transform: translateY(-1px) !important;
    box-shadow: 0 4px 20px rgba(124, 106, 247, 0.4) !important;
}

/* ── Secondary button ── */
div[data-testid="stButton"] button[kind="secondary"] {
    background: transparent !important;
    border: 1px solid #2a2a3e !important;
    border-radius: 10px !important;
    color: #8888a0 !important;
    font-family: 'Space Grotesk', sans-serif !important;
    font-weight: 500 !important;
    font-size: 0.875rem !important;
    width: 100% !important;
    transition: all 0.2s !important;
}
div[data-testid="stButton"] button[kind="secondary"]:hover {
    border-color: #7c6af7 !important;
    color: #c4b5fd !important;
}

/* ── Alerts ── */
div[data-testid="stSuccess"] {
    background: #0d1f17 !important;
    border: 1px solid #1a4731 !important;
    border-radius: 10px !important;
    color: #4ade80 !important;
}
div[data-testid="stError"] {
    background: #1f0d0d !important;
    border: 1px solid #471a1a !important;
    border-radius: 10px !important;
    color: #f87171 !important;
}
div[data-testid="stInfo"] {
    background: #0d1220 !important;
    border: 1px solid #1a2a4a !important;
    border-radius: 10px !important;
    color: #93c5fd !important;
}
div[data-testid="stWarning"] {
    background: #1f1800 !important;
    border: 1px solid #473d00 !important;
    border-radius: 10px !important;
    color: #fbbf24 !important;
}

/* ── File content box ── */
.file-content-box {
    background: #0f0f18;
    border: 1px solid #2a2a3e;
    border-radius: 10px;
    padding: 1.25rem;
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.82rem;
    color: #a0a0c0;
    line-height: 1.7;
    white-space: pre-wrap;
    word-break: break-all;
    max-height: 280px;
    overflow-y: auto;
}
.file-content-box::-webkit-scrollbar { width: 4px; }
.file-content-box::-webkit-scrollbar-track { background: transparent; }
.file-content-box::-webkit-scrollbar-thumb { background: #3a3a5e; border-radius: 4px; }

/* ── File meta pill ── */
.file-meta {
    display: inline-flex;
    align-items: center;
    gap: 0.4rem;
    background: #1a1a2e;
    border: 1px solid #2a2a4e;
    border-radius: 6px;
    padding: 0.25rem 0.65rem;
    font-size: 0.75rem;
    font-family: 'JetBrains Mono', monospace;
    color: #8888a0;
    margin-bottom: 1rem;
}

/* ── Divider ── */
.section-divider {
    height: 1px;
    background: linear-gradient(90deg, transparent, #2a2a3e, transparent);
    margin: 1.25rem 0;
}

/* ── Radio hack (hidden, replaced by JS-free tabs) ── */
div[data-testid="stRadio"] {
    display: none !important;
}

/* ── Footer ── */
.vault-footer {
    text-align: center;
    padding: 2.5rem 0 1rem;
    color: #3a3a55;
    font-size: 0.75rem;
    letter-spacing: 0.08em;
}
</style>
""", unsafe_allow_html=True)

# ── Helpers ──────────────────────────────────────────────────────────────────
SAFE_DIR = Path("filevault_workspace")
SAFE_DIR.mkdir(exist_ok=True)

def safe_path(name: str) -> Path:
    """Resolve path strictly inside workspace."""
    p = (SAFE_DIR / name).resolve()
    if SAFE_DIR.resolve() not in p.parents and p != SAFE_DIR.resolve():
        return None
    return p

def human_size(path: Path) -> str:
    b = path.stat().st_size
    return f"{b} B" if b < 1024 else f"{b/1024:.1f} KB"

def list_workspace_files():
    return sorted(SAFE_DIR.glob("*"))

# ── Session state ─────────────────────────────────────────────────────────────
if "op" not in st.session_state:
    st.session_state.op = "Create"

# ── Header ───────────────────────────────────────────────────────────────────
st.markdown("""
<div class="vault-header">
    <div class="vault-logo">FileVault</div>
    <div class="vault-tagline">Terminal-grade file management · Built with Python</div>
</div>
""", unsafe_allow_html=True)

# ── Operation selector ────────────────────────────────────────────────────────
ops = {
    "Create":  ("✦", "Create"),
    "Read":    ("◈", "Read"),
    "Update":  ("⟳", "Update"),
    "Delete":  ("⌫", "Delete"),
}

cols = st.columns(4)
for i, (key, (icon, label)) in enumerate(ops.items()):
    with cols[i]:
        active_class = "active" if st.session_state.op == key else ""
        st.markdown(f"""
        <div class="op-pill {active_class}">
            <div class="op-icon">{icon}</div>
            <div class="op-label">{label}</div>
        </div>
        """, unsafe_allow_html=True)
        if st.button(label, key=f"btn_{key}", use_container_width=True):
            st.session_state.op = key
            st.rerun()

st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)
op = st.session_state.op

# ── Sidebar: workspace browser ────────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div style="font-size:0.7rem;font-weight:600;letter-spacing:0.15em;
                text-transform:uppercase;color:#5a5a75;margin-bottom:0.75rem;">
        Workspace
    </div>
    """, unsafe_allow_html=True)

    files = list_workspace_files()
    if not files:
        st.markdown('<div style="color:#4a4a60;font-size:0.8rem;">No files yet — create one!</div>',
                    unsafe_allow_html=True)
    else:
        for f in files:
            size = human_size(f)
            st.markdown(f"""
            <div style="background:#14141e;border:1px solid #1e1e2e;border-radius:8px;
                        padding:0.55rem 0.75rem;margin-bottom:0.4rem;display:flex;
                        justify-content:space-between;align-items:center;">
                <span style="font-family:'JetBrains Mono',monospace;font-size:0.78rem;
                             color:#c4b5fd;">{f.name}</span>
                <span style="font-size:0.68rem;color:#4a4a65;">{size}</span>
            </div>
            """, unsafe_allow_html=True)

    st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)
    st.markdown(f'<div style="color:#3a3a55;font-size:0.72rem;">{len(files)} file{"s" if len(files)!=1 else ""} · filevault_workspace/</div>',
                unsafe_allow_html=True)

# ── CREATE ────────────────────────────────────────────────────────────────────
if op == "Create":
    st.markdown("""
    <div class="card">
        <div class="card-title">✦ &nbsp;Create new file</div>
    </div>
    """, unsafe_allow_html=True)

    fname = st.text_input("File name", placeholder="notes.txt", key="create_name")
    fcontent = st.text_area("Content", placeholder="Start typing…", height=160, key="create_content")

    if st.button("Create file", type="primary"):
        if not fname.strip():
            st.error("File name cannot be empty.")
        else:
            path = safe_path(fname.strip())
            if path is None:
                st.error("Invalid file path.")
            elif path.exists():
                st.error(f"**{fname}** already exists. Use Update to modify it.")
            else:
                path.write_text(fcontent)
                st.success(f"**{fname}** created successfully! ({human_size(path)})")
                time.sleep(0.3)
                st.rerun()

# ── READ ──────────────────────────────────────────────────────────────────────
elif op == "Read":
    st.markdown("""
    <div class="card">
        <div class="card-title">◈ &nbsp;Read file</div>
    </div>
    """, unsafe_allow_html=True)

    files = list_workspace_files()
    if not files:
        st.info("No files in workspace yet. Create one first.")
    else:
        options = [f.name for f in files]
        fname = st.selectbox("Select file", options, key="read_name")

        if st.button("Read file", type="primary"):
            path = safe_path(fname)
            if path and path.exists():
                content = path.read_text()
                st.markdown(f'<div class="file-meta">📄 {fname} &nbsp;·&nbsp; {human_size(path)}</div>',
                            unsafe_allow_html=True)
                if content.strip():
                    st.markdown(f'<div class="file-content-box">{content}</div>',
                                unsafe_allow_html=True)
                else:
                    st.markdown('<div class="file-content-box" style="color:#4a4a65;font-style:italic;">(empty file)</div>',
                                unsafe_allow_html=True)
            else:
                st.error("File not found.")

# ── UPDATE ────────────────────────────────────────────────────────────────────
elif op == "Update":
    st.markdown("""
    <div class="card">
        <div class="card-title">⟳ &nbsp;Update file</div>
    </div>
    """, unsafe_allow_html=True)

    files = list_workspace_files()
    if not files:
        st.info("No files in workspace yet. Create one first.")
    else:
        options = [f.name for f in files]
        fname = st.selectbox("Select file to update", options, key="update_name")
        action = st.selectbox(
            "Operation",
            ["Rename", "Append content", "Overwrite content"],
            key="update_action"
        )

        if action == "Rename":
            new_name = st.text_input("New file name", placeholder="new-name.txt", key="rename_target")
            if st.button("Rename file", type="primary"):
                if not new_name.strip():
                    st.error("New name cannot be empty.")
                else:
                    src = safe_path(fname)
                    dst = safe_path(new_name.strip())
                    if dst is None:
                        st.error("Invalid file path.")
                    elif dst.exists():
                        st.error(f"**{new_name}** already exists.")
                    else:
                        src.rename(dst)
                        st.success(f"Renamed **{fname}** → **{new_name}**")
                        time.sleep(0.3)
                        st.rerun()

        elif action == "Append content":
            path = safe_path(fname)
            if path:
                current = path.read_text()
                if current.strip():
                    st.markdown(f'<div class="file-content-box" style="margin-bottom:0.75rem;">{current}</div>',
                                unsafe_allow_html=True)
            new_data = st.text_area("Text to append", height=120, key="append_data")
            if st.button("Append to file", type="primary"):
                if path and path.exists():
                    with open(path, "a") as f:
                        f.write("\n" + new_data)
                    st.success(f"Appended {len(new_data)} characters to **{fname}**")
                    time.sleep(0.3)
                    st.rerun()

        elif action == "Overwrite content":
            path = safe_path(fname)
            existing = path.read_text() if path and path.exists() else ""
            new_data = st.text_area("New content (replaces existing)", value=existing, height=160, key="overwrite_data")
            if st.button("Overwrite file", type="primary"):
                if path:
                    path.write_text(new_data)
                    st.success(f"**{fname}** overwritten ({human_size(path)})")
                    time.sleep(0.3)
                    st.rerun()

# ── DELETE ────────────────────────────────────────────────────────────────────
elif op == "Delete":
    st.markdown("""
    <div class="card">
        <div class="card-title">⌫ &nbsp;Delete file</div>
    </div>
    """, unsafe_allow_html=True)

    files = list_workspace_files()
    if not files:
        st.info("No files in workspace. Nothing to delete.")
    else:
        options = [f.name for f in files]
        fname = st.selectbox("Select file to delete", options, key="delete_name")
        path = safe_path(fname)

        if path and path.exists():
            size = human_size(path)
            content_preview = path.read_text()[:120]
            st.markdown(f'<div class="file-meta">📄 {fname} &nbsp;·&nbsp; {size}</div>',
                        unsafe_allow_html=True)
            if content_preview:
                st.markdown(f'<div class="file-content-box">{content_preview}{"…" if len(path.read_text()) > 120 else ""}</div>',
                            unsafe_allow_html=True)

        st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)
        st.warning(f"This will permanently delete **{fname}**. This cannot be undone.")

        confirm = st.checkbox("I understand this action is irreversible", key="delete_confirm")
        if st.button("Delete file", type="primary", disabled=not confirm):
            if path and path.exists():
                path.unlink()
                st.success(f"**{fname}** has been deleted.")
                time.sleep(0.3)
                st.rerun()
            else:
                st.error("File not found.")

# ── Footer ────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="vault-footer">
    FileVault &nbsp;·&nbsp; Built with Python + Streamlit &nbsp;·&nbsp; CRUD File Manager
</div>
""", unsafe_allow_html=True)
