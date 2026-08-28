import streamlit as st
from pathlib import Path
from datetime import datetime

# ----------------------------------------------------------------------------
# Config
# ----------------------------------------------------------------------------
st.set_page_config(
    page_title="FileVault | File Manager",
    page_icon="🗂️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# All operations are sandboxed inside this workspace folder for safety —
# no arbitrary path traversal on the host filesystem.
WORKSPACE = Path("workspace")
WORKSPACE.mkdir(exist_ok=True)


def safe_path(filename: str) -> Path:
    """Resolve a user-supplied filename inside the workspace only."""
    candidate = (WORKSPACE / filename).resolve()
    if WORKSPACE.resolve() not in candidate.parents and candidate != WORKSPACE.resolve():
        raise ValueError("Invalid file name.")
    return candidate


def human_size(num_bytes: int) -> str:
    for unit in ["B", "KB", "MB", "GB"]:
        if num_bytes < 1024:
            return f"{num_bytes:.0f} {unit}"
        num_bytes /= 1024
    return f"{num_bytes:.1f} TB"


# ----------------------------------------------------------------------------
# Styling
# ----------------------------------------------------------------------------
st.markdown(
    """
    <style>
    .main-title {
        font-size: 2.4rem;
        font-weight: 800;
        margin-bottom: 0;
        background: linear-gradient(90deg, #6366f1, #8b5cf6, #ec4899);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    .subtitle {
        color: #9ca3af;
        font-size: 1rem;
        margin-top: 0;
        margin-bottom: 1.5rem;
    }
    .stButton>button {
        border-radius: 10px;
        font-weight: 600;
        padding: 0.5rem 1.2rem;
        transition: all 0.15s ease-in-out;
    }
    .stButton>button:hover {
        transform: translateY(-1px);
        box-shadow: 0 4px 12px rgba(99, 102, 241, 0.25);
    }
    div[data-testid="stMetric"] {
        background-color: rgba(99, 102, 241, 0.08);
        border-radius: 12px;
        padding: 12px;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# ----------------------------------------------------------------------------
# Header
# ----------------------------------------------------------------------------
st.markdown('<p class="main-title">🗂️ FileVault</p>', unsafe_allow_html=True)
st.markdown(
    '<p class="subtitle">A clean, safe, all-in-one file manager — Create · Read · Update · Delete</p>',
    unsafe_allow_html=True,
)

# ----------------------------------------------------------------------------
# Sidebar — navigation + live file browser
# ----------------------------------------------------------------------------
with st.sidebar:
    st.header("Navigation")
    page = st.radio(
        "Choose an operation",
        ["🏠 Dashboard", "📄 Create", "👁️ Read", "✏️ Update", "🗑️ Delete"],
        label_visibility="collapsed",
    )

    st.divider()
    st.subheader("📁 Workspace files")
    files = sorted(WORKSPACE.glob("*"))
    if files:
        for f in files:
            if f.is_file():
                st.caption(f"📄 {f.name}  ·  {human_size(f.stat().st_size)}")
    else:
        st.caption("No files yet — create one to get started!")

    st.divider()
    st.caption("All operations are sandboxed inside a local `workspace/` folder.")

# ----------------------------------------------------------------------------
# Dashboard
# ----------------------------------------------------------------------------
if page == "🏠 Dashboard":
    col1, col2, col3 = st.columns(3)
    total_files = len([f for f in files if f.is_file()])
    total_size = sum(f.stat().st_size for f in files if f.is_file())
    last_modified = (
        datetime.fromtimestamp(max(f.stat().st_mtime for f in files)).strftime("%b %d, %H:%M")
        if files
        else "—"
    )
    col1.metric("Total files", total_files)
    col2.metric("Total size", human_size(total_size))
    col3.metric("Last modified", last_modified)

    st.divider()
    st.subheader("How it works")
    c1, c2, c3, c4 = st.columns(4)
    with c1:
        st.markdown("**📄 Create**")
        st.caption("Spin up a new file, optionally with initial content.")
    with c2:
        st.markdown("**👁️ Read**")
        st.caption("Preview any file's contents and download it.")
    with c3:
        st.markdown("**✏️ Update**")
        st.caption("Rename, append to, or overwrite an existing file.")
    with c4:
        st.markdown("**🗑️ Delete**")
        st.caption("Remove a file permanently (with confirmation).")

    if files:
        st.divider()
        st.subheader("Files at a glance")
        st.table(
            {
                "Name": [f.name for f in files if f.is_file()],
                "Size": [human_size(f.stat().st_size) for f in files if f.is_file()],
                "Last modified": [
                    datetime.fromtimestamp(f.stat().st_mtime).strftime("%Y-%m-%d %H:%M")
                    for f in files
                    if f.is_file()
                ],
            }
        )

# ----------------------------------------------------------------------------
# Create
# ----------------------------------------------------------------------------
elif page == "📄 Create":
    st.subheader("Create a new file")
    with st.form("create_form", clear_on_submit=False):
        name = st.text_input("File name", placeholder="e.g. notes.txt")
        content = st.text_area("Initial content (optional)", height=150)
        submitted = st.form_submit_button("Create file", type="primary")

    if submitted:
        if not name.strip():
            st.error("Please enter a file name.")
        else:
            try:
                path = safe_path(name.strip())
                if path.exists():
                    st.warning(f"⚠️ `{path.name}` already exists. Choose a different name or use **Update**.")
                else:
                    path.write_text(content)
                    st.success(f"✅ File `{path.name}` created successfully!")
                    st.balloons()
            except Exception as err:
                st.error(f"Something went wrong: {err}")

# ----------------------------------------------------------------------------
# Read
# ----------------------------------------------------------------------------
elif page == "👁️ Read":
    st.subheader("Read a file")
    existing = [f.name for f in files if f.is_file()]
    if not existing:
        st.info("No files in the workspace yet. Create one first!")
    else:
        name = st.selectbox("Choose a file", existing)
        if st.button("Read file", type="primary"):
            try:
                path = safe_path(name)
                content = path.read_text()
                st.success(f"Showing contents of `{path.name}`")
                st.code(content or "(empty file)", language=None)
                st.download_button(
                    "⬇️ Download this file",
                    data=content,
                    file_name=path.name,
                )
            except Exception as err:
                st.error(f"Something went wrong: {err}")

# ----------------------------------------------------------------------------
# Update
# ----------------------------------------------------------------------------
elif page == "✏️ Update":
    st.subheader("Update a file")
    mode = st.radio(
        "What would you like to do?",
        ["Rename", "Append content", "Overwrite content"],
        horizontal=True,
    )
    existing = [f.name for f in files if f.is_file()]

    if not existing:
        st.info("No files in the workspace yet. Create one first!")
    else:
        name = st.selectbox("Choose a file", existing)

        if mode == "Rename":
            new_name = st.text_input("New file name")
            if st.button("Rename", type="primary"):
                try:
                    old_path = safe_path(name)
                    new_path = safe_path(new_name.strip())
                    if not new_name.strip():
                        st.error("Please enter a new name.")
                    elif new_path.exists():
                        st.warning(f"⚠️ `{new_path.name}` already exists.")
                    else:
                        old_path.rename(new_path)
                        st.success(f"✅ Renamed `{old_path.name}` → `{new_path.name}`")
                except Exception as err:
                    st.error(f"Something went wrong: {err}")

        elif mode == "Append content":
            data = st.text_area("Content to append", height=120)
            if st.button("Append", type="primary"):
                try:
                    path = safe_path(name)
                    with open(path, "a") as fs:
                        fs.write("\n" + data)
                    st.success(f"✅ Content appended to `{path.name}`")
                except Exception as err:
                    st.error(f"Something went wrong: {err}")

        elif mode == "Overwrite content":
            data = st.text_area("New content (replaces everything)", height=150)
            confirm = st.checkbox("I understand this will erase the current content.")
            if st.button("Overwrite", type="primary", disabled=not confirm):
                try:
                    path = safe_path(name)
                    path.write_text(data)
                    st.success(f"✅ `{path.name}` overwritten successfully")
                except Exception as err:
                    st.error(f"Something went wrong: {err}")

# ----------------------------------------------------------------------------
# Delete
# ----------------------------------------------------------------------------
elif page == "🗑️ Delete":
    st.subheader("Delete a file")
    existing = [f.name for f in files if f.is_file()]
    if not existing:
        st.info("No files in the workspace yet.")
    else:
        name = st.selectbox("Choose a file to delete", existing)
        confirm = st.checkbox(f"I'm sure I want to permanently delete `{name}`")
        if st.button("Delete file", type="primary", disabled=not confirm):
            try:
                path = safe_path(name)
                path.unlink()
                st.success(f"🗑️ `{path.name}` deleted successfully")
                st.rerun()
            except Exception as err:
                st.error(f"Something went wrong: {err}")

# ----------------------------------------------------------------------------
# Footer
# ----------------------------------------------------------------------------
st.divider()
st.caption("Built with ❤️ using Python & Streamlit")