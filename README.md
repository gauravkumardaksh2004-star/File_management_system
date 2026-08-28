# File_management_system
CRUD OPEARTIONS
# FileForge

A console-style UI for basic file CRUD operations — create, read, update (rename / append / overwrite), and delete — built as a front-end companion to a Python file-handling script.

Runs entirely in the browser with an in-memory virtual filesystem (no backend, nothing touches your real disk), so it's safe to open directly or host as a static demo.

## Structure

```
fileforge/
├── index.html   # markup
├── style.css    # styling (dark console theme)
└── script.js    # CRUD logic + virtual filesystem + terminal log
```

## Run it

Just open `index.html` in a browser — no build step, no dependencies besides two Google Fonts loaded via CDN.

## Features

- **Create** — add a new file to the session
- **Read** — view a file's contents
- **Update** — rename, append to, or overwrite a file
- **Delete** — remove a file
- A live `session.log` terminal panel that echoes every operation, like a real shell session
