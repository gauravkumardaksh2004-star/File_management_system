import streamlit as st
import streamlit.components.v1 as components
from pathlib import Path

st.set_page_config(page_title="FileForge", layout="wide")

BASE_DIR = Path(__file__).parent

html = (BASE_DIR / "index.html").read_text(encoding="utf-8")
css = (BASE_DIR / "style.css").read_text(encoding="utf-8")
js = (BASE_DIR / "script.js").read_text(encoding="utf-8")

# components.html renders in an isolated iframe with no access to your
# other files on disk, so the external <link>/<script> references need
# to be inlined directly into the HTML before we hand it off.
html = html.replace(
    '<link rel="stylesheet" href="style.css">',
    f"<style>{css}</style>",
)
html = html.replace(
    '<script src="script.js"></script>',
    f"<script>{js}</script>",
)

components.html(html, height=950, scrolling=True)