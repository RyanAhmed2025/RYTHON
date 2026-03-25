"""
╔══════════════════════════════════════════════════════════════════════════════╗
║            RYTHON — Python Webview App Template                              ║
║            by Ryan Ahmed  ·  Copyright © 2025 RYAN                          ║
╚══════════════════════════════════════════════════════════════════════════════╝

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
WINDOW / UI FEATURES
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  • Frameless window          pywebview + Flask on 127.0.0.1:5000
  • Edge resize handles       8 px invisible strips → WinAPI SendMessage hit-test
  • Title-bar drag            mousedown → WinAPI SetWindowPos loop (daemon thread)
  • Snap shortcuts            Alt+←  left-half   |  Alt+→  right-half
                              Alt+↓  centered    |  Alt+↑  maximize ↔ restore
  • Double-click title bar    maximize / restore cycle (WinAPI ShowWindow)
  • Traffic-light buttons     minimize  ·  close
  • Left pill                 4 fixed + 3 hover-revealed icon buttons
  • Right pill                3 hover (incl. theme toggle) + 3 fixed + traffic lights
  • Unibar overlay            Alt+S  |  double-click title  →  //commands
  • Center title pill         app name + rolling status line
  • Collapsible sidebars      ArrowLeft / ArrowRight (when not in a text input)
  • Sidebar border fade       vertical borders blend seamlessly into title bar
  • macOS-style dialog        showDialog(msg, icon?)  ·  showInputDialog(msg, def?)
  • Dark / Light theme        persisted to localStorage

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
FULLSTACK VIBECODING GUIDE
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

── PROJECT LAYOUT  (recommended when growing beyond one file) ─────────────────

  rython/
  ├── app.py              ← Flask backend (this file — keep lean)
  ├── database.py         ← DB init, get_conn(), migrations (extract when >2 tables)
  ├── models.py           ← Pure-Python data classes / business logic
  ├── routes/             ← Flask blueprints (split when >10 endpoints)
  │   ├── __init__.py
  │   └── items.py        ←  @items_bp.route('/api/items', ...)
  ├── static/             ← Assets if you split HTML out of Python
  │   ├── app.js
  │   ├── style.css
  │   └── icons/
  ├── templates/          ← Jinja2 HTML (alternative to the inline HTML string)
  │   └── index.html
  ├── rython.db           ← SQLite file — auto-created at startup; add to .gitignore
  ├── .env                ← Secrets / config — NEVER commit to git
  ├── .gitignore          ← .env  *.db  __pycache__/  dist/  *.spec
  └── requirements.txt    ←  pip freeze > requirements.txt

# ── DATABASE  (SQLite · stdlib · zero install) ─────────────────────────────────
#
#   import sqlite3, os
#   DB = os.path.join(os.path.dirname(__file__), 'rython.db')
#
#   def get_conn():
#       conn = sqlite3.connect(DB)
#       conn.row_factory = sqlite3.Row   # dict-like: row['col']
#       return conn


# RULES:
#   ✓  Parameterised queries only:  cursor.execute("SELECT * FROM t WHERE id=?", (id,))
#   ✗  Never f-string SQL  →  SQL injection vector
#   ✓  Commit after writes; close connections promptly
#   ✓  For relational complexity, swap sqlite3 for SQLAlchemy:
#         pip install flask-sqlalchemy  →  define Model classes in models.py
── FLASK CRUD SKELETON ────────────────────────────────────────────────────────

  @app.route('/api/items',             methods=['GET'])    # list / query
  @app.route('/api/items',             methods=['POST'])   # create
  @app.route('/api/items/<int:item_id>', methods=['GET'])  # read one
  @app.route('/api/items/<int:item_id>', methods=['PUT'])  # update
  @app.route('/api/items/<int:item_id>', methods=['DELETE'])# delete

  Always return jsonify({...}).  pywebview's JS fetch expects JSON.
  Use appropriate HTTP status codes:  201 Created, 404 Not Found, 400 Bad Request.

── JS FETCH PATTERN (in <script> block) ───────────────────────────────────────

  // CREATE
  const data = await fetch('/api/items', {
      method : 'POST',
      headers: { 'Content-Type': 'application/json' },
      body   : JSON.stringify({ title: 'Hello' })
  }).then(r => r.json());

  // READ LIST
  const items = await fetch('/api/items').then(r => r.json());

  // UPDATE
  await fetch(`/api/items/${id}`, {
      method : 'PUT',
      headers: { 'Content-Type': 'application/json' },
      body   : JSON.stringify({ title: 'Updated' })
  });

  // DELETE — always show showDialog() confirmation first!
  const ok = await showDialog('Delete this item?', 'delete');
  if (ok) await fetch(`/api/items/${id}`, { method: 'DELETE' });

── PYWEBVIEW JS API  (window.pywebview.api.<method>) ──────────────────────────

  • Add methods to WindowApi class below
  • All args / returns must be JSON-serialisable (str, int, list, dict, None)
  • Long operations → spawn a threading.Thread so the UI thread stays free
  • File / folder dialogs, clipboard, OS notifications → live here, not in Flask
  • Never block the WindowApi method body for more than ~50 ms

── ENVIRONMENT & SECRETS ──────────────────────────────────────────────────────

  pip install python-dotenv
  from dotenv import load_dotenv; load_dotenv()
  SECRET = os.environ.get('MY_SECRET', 'dev-fallback')

  .env example:
    MY_SECRET=abc123
    DB_PATH=/custom/path/rython.db

── PACKAGING TO EXE  (Windows) ────────────────────────────────────────────────

  pip install pyinstaller
  pyinstaller --noconsole --onefile --name RYTHON app.py
    --add-data "static;static"    ← bundle extra assets
    --icon=icon.ico               ← window / taskbar icon
  The EXE embeds Flask + pywebview + Chromium in a single file.

── REQUIREMENTS.TXT ───────────────────────────────────────────────────────────

  flask
  pywebview
  # python-dotenv       ← env / secrets
  # flask-sqlalchemy    ← ORM for larger schemas
  # pillow              ← image processing
  # reportlab           ← PDF export
"""

import os, sys, threading
import webview
from flask import Flask, jsonify, request

# ── Flask app ──────────────────────────────────────────────────────────────
app = Flask(__name__)

# ── DATABASE SETUP ─────────────────────────────────────────────────────────
# PLACEHOLDER: uncomment and expand to wire up SQLite.
#
# import sqlite3
# DB = os.path.join(os.path.dirname(__file__), 'rython.db')
#
# def get_conn():
#     conn = sqlite3.connect(DB)
#     conn.row_factory = sqlite3.Row
#     return conn
#
# def init_db():
#     conn = get_conn()
#     conn.executescript("""
#         CREATE TABLE IF NOT EXISTS items (
#             id      INTEGER PRIMARY KEY AUTOINCREMENT,
#             title   TEXT    NOT NULL,
#             body    TEXT    DEFAULT '',
#             created TIMESTAMP DEFAULT CURRENT_TIMESTAMP
#         );
#     """)
#     conn.commit(); conn.close()
#
# init_db()   ← call before app.run()

# ── FLASK ROUTES ───────────────────────────────────────────────────────────
# PLACEHOLDER: replace with your own CRUD routes.
# Pattern: GET list · POST create · GET/PUT/DELETE by id
#
# @app.route('/api/items', methods=['GET'])
# def list_items():
#     conn = get_conn()
#     rows = conn.execute('SELECT * FROM items ORDER BY id DESC').fetchall()
#     conn.close()
#     return jsonify([dict(r) for r in rows])
#
# @app.route('/api/items', methods=['POST'])
# def create_item():
#     data = request.json
#     conn = get_conn()
#     cur  = conn.execute('INSERT INTO items (title, body) VALUES (?,?)',
#                         (data['title'], data.get('body', '')))
#     conn.commit(); conn.close()
#     return jsonify({'id': cur.lastrowid, 'status': 'created'}), 201
#
# @app.route('/api/items/<int:item_id>', methods=['GET','PUT','DELETE'])
# def item_ops(item_id):
#     conn = get_conn()
#     if request.method == 'GET':
#         row = conn.execute('SELECT * FROM items WHERE id=?',(item_id,)).fetchone()
#         conn.close()
#         return jsonify(dict(row)) if row else ({}, 404)
#     if request.method == 'PUT':
#         d = request.json
#         conn.execute('UPDATE items SET title=?,body=? WHERE id=?',
#                      (d['title'], d.get('body',''), item_id))
#         conn.commit(); conn.close()
#         return jsonify({'status': 'updated'})
#     # DELETE
#     conn.execute('DELETE FROM items WHERE id=?', (item_id,))
#     conn.commit(); conn.close()
#     return jsonify({'status': 'deleted'})

@app.route('/')
def index():
    return HTML

# ── HTML / CSS / JS ─────────────────────────────────────────────────────────
HTML = r"""
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>RYTHON</title>
<link rel="stylesheet"
      href="https://fonts.googleapis.com/css2?family=Material+Symbols+Outlined:opsz,wght,FILL,GRAD@20..48,100..700,0,1"/>
<link href="https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;700&family=Inter:wght@400;500;600&display=swap"
      rel="stylesheet">
<style>
/* ═══════════════════════════════════════════════════════
   DESIGN TOKENS  —  dark default, light override below
═══════════════════════════════════════════════════════ */
:root {
  --bg-body:          #050505;
  --bg-sidebar:       #050505;
  --bg-editor:        #050505;
  --bg-pill:          #1a1a1a;
  --bg-pill-hover:    #252525;

  --accent:           #00f2ff;
  --text-content:     #e0e0e0;
  --text-secondary:   #00f2ff;
  --text-muted:       #808080;
  --text-title:       #00f2ff;

  --border-light:     #1f1f1f;
  --border-focus:     #00f2ff;
  --scrollbar-thumb:  #333;

  --traffic-red:    #ff5f57;
  --traffic-yellow: #febc2e;
  --traffic-green:  #28c840;

  --tl-close-fill:  #00d2df;
  --tl-close-ring:  rgba(0,242,255,.18);
  --tl-min-fill:    transparent;
  --tl-min-ring:    rgba(0,242,255,.72);
  --tl-cluster-bg:  rgba(0,242,255,.05);
  --tl-cluster-ring:rgba(0,242,255,.12);
  --tl-cluster-hbg: rgba(0,242,255,.08);
  --tl-cluster-hrg: rgba(0,242,255,.18);

  --dialog-bg:         rgba(26,26,26,.97);
  --dialog-text:       #fff;
  --dialog-cancel-bg:  #2a2a2a;
  --dialog-cancel-txt: #aaa;
  --dialog-ok-bg:      #00f2ff;
  --dialog-ok-txt:     #000;

  --font-mono: 'JetBrains Mono', monospace;
  --font-ui:   'Inter', sans-serif;
}

[data-theme="light"] {
  --bg-body:          #f5f5f5;
  --bg-sidebar:       #eaeaea;
  --bg-editor:        #ffffff;
  --bg-pill:          #ffffff;
  --bg-pill-hover:    #f0f0f0;

  --accent:           #008b8b;
  --text-content:     #111111;
  --text-secondary:   #008b8b;
  --text-muted:       #666666;
  --text-title:       #555555;

  --border-light:     #cccccc;

  --tl-close-fill:  #b7bcc5;  --tl-close-ring: rgba(135,143,156,.26);
  --tl-min-fill:    transparent; --tl-min-ring: rgba(158,167,179,.85);
  --tl-cluster-bg:  rgba(185,191,201,.18); --tl-cluster-ring: rgba(154,162,173,.22);
  --tl-cluster-hbg: rgba(185,191,201,.26); --tl-cluster-hrg: rgba(154,162,173,.30);

  --dialog-bg:         rgba(248,248,248,.98);
  --dialog-text:       #111;
  --dialog-cancel-bg:  #e2e2e2;
  --dialog-cancel-txt: #444;
  --dialog-ok-bg:      #111;
  --dialog-ok-txt:     #fff;
}

/* ═══════════════════════════════════════════════════════
   RESET
═══════════════════════════════════════════════════════ */
*, *::before, *::after { box-sizing: border-box; outline: none; }
::selection { background: #00f2ff; color: #000; }

body {
  margin: 0; padding: 0; height: 100vh; overflow: hidden;
  background: transparent;
  font-family: var(--font-ui);
  color: var(--accent);
  user-select: none;
}

::-webkit-scrollbar        { width: 8px; background: transparent; }
::-webkit-scrollbar-thumb  { background: transparent; border-radius: 4px; transition: background .3s; }
*:hover::-webkit-scrollbar-thumb { background: var(--scrollbar-thumb); }

/* ── app shell ─────────────────────────────────────── */
.app-shell {
  display: flex; flex-direction: column; height: 100%;
  background: var(--bg-body);
  transition: background .3s,
              transform .26s cubic-bezier(.22,1,.36,1),
              filter .26s cubic-bezier(.22,1,.36,1),
              opacity .22s,
              border-radius .26s cubic-bezier(.22,1,.36,1);
  transform-origin: 50% 0%;
  will-change: transform, filter, opacity;
}
.app-shell.maximized   { border-radius: 0; }
.app-shell.win-resizing {
  transform: scale(.986);
  filter: saturate(.94) brightness(1.03);
  opacity: .985;
}

/* ═══════════════════════════════════════════════════════
   RESIZE HANDLES  —  8 px invisible edges, always on top
═══════════════════════════════════════════════════════ */
.rh { position: fixed; z-index: 10000; pointer-events: auto; }
.rh-top    { top:0;    left:0; width:100%; height:8px; cursor:n-resize; }
.rh-left   { top:0;    left:0; width:8px;  height:100%; cursor:w-resize; }
.rh-right  { top:0;   right:0; width:8px;  height:100%; cursor:e-resize; }
.rh-bottom { bottom:0; left:0; width:100%; height:8px; cursor:s-resize; }

/* ═══════════════════════════════════════════════════════
   TITLE BAR
═══════════════════════════════════════════════════════ */
.title-bar {
  height: 56px;
  background: var(--bg-body);
  display: flex; align-items: center; justify-content: space-between;
  padding: 8px 16px 0 16px;
  -webkit-app-region: no-drag;
  z-index: 1000; position: relative; flex-shrink: 0;
}
#titleDragZone {
  position: absolute; inset: 0; z-index: 0;
  cursor: grab; -webkit-app-region: no-drag;
}
#titleDragZone:active { cursor: grabbing; }

@media (max-width: 1000px) {
  .pill-hidden { display: none !important; }
  .center-pill { width: 140px !important; }
  .title-bar   { padding: 8px 8px 0 8px; }
}

/* ── pill ─────────────────────────────────────────── */
.pill {
  display: inline-flex; align-items: center;
  background: var(--bg-pill); border-radius: 50px;
  padding: 3px; height: 46px;
  border: 1px solid var(--border-light);
  -webkit-app-region: no-drag;
  overflow: hidden; z-index: 20; position: relative;
  box-shadow: 0 4px 12px rgba(0,0,0,.1);
  transition: border-color .3s;
  margin-top: -8px;
}
.title-bar > .pill:first-of-type { transform: translateX(-7px); }
.title-bar > .pill:last-of-type  { transform: translateX( 7px); }

.pill-fixed  { display: flex; align-items: center; }
.pill-hidden { max-width: 0; opacity: 0; overflow: hidden;
               transition: all .5s cubic-bezier(.25,1,.5,1); }
@media (min-width: 1001px) {
  .pill:hover .pill-hidden { max-width: 450px; opacity: 1; margin: 0 4px; }
}

/* ── icon button ────────────────────────────────────── */
.icon-btn {
  background: transparent; border: none; color: var(--accent);
  width: 40px; height: 40px; border-radius: 50%;
  display: flex; align-items: center; justify-content: center;
  padding: 0; cursor: pointer; flex-shrink: 0; position: relative;
  transition: background .2s, transform .2s;
}
.icon-btn:hover { background: var(--bg-pill-hover); transform: scale(1.1); }
.icon-btn span  { font-size: 24px; }
.icon-btn.active { color: var(--traffic-green); }

/* ── traffic lights ─────────────────────────────────── */
.traffic-lights {
  display: flex; gap: 8px;
  padding: 4px 10px 4px 12px; margin-left: 2px;
  border-left: 1px solid var(--border-light);
  height: 40px; align-items: center;
  border-radius: 999px;
  background: var(--tl-cluster-bg);
  box-shadow: inset 0 0 0 1px var(--tl-cluster-ring);
  transition: background .24s, box-shadow .24s;
}
.tl-btn {
  width: 24px; height: 24px; border-radius: 50%; border: none;
  cursor: pointer; background: transparent;
  display: flex; align-items: center; justify-content: center;
  padding: 0; position: relative; flex-shrink: 0;
  -webkit-app-region: no-drag;
  transition: transform .24s cubic-bezier(.22,1,.36,1);
}
.tl-btn::before {
  content: ''; width: 16px; height: 16px; border-radius: 50%;
  background: var(--tl-idle, var(--bg-pill-hover));
  box-shadow: inset 0 0 0 1px var(--tl-ring, transparent);
  transition: transform .24s cubic-bezier(.22,1,.36,1),
              background .24s, box-shadow .24s, opacity .24s;
}
.traffic-lights:not(:hover) .tl-btn         { transform: scale(.92); }
.traffic-lights:not(:hover) .tl-btn::before { transform: scale(.94); }
.traffic-lights:hover {
  background: var(--tl-cluster-hbg);
  box-shadow: inset 0 0 0 1px var(--tl-cluster-hrg), 0 4px 16px rgba(0,0,0,.08);
}
.traffic-lights:hover .tl-btn {
  transform: translateY(-1px) scale(1);
}
.traffic-lights:hover .tl-btn::before {
  transform: scale(1.14);
  box-shadow: inset 0 0 0 1px var(--tl-active-ring, transparent),
              0 4px 12px rgba(0,0,0,.18);
}
.traffic-lights:hover .tl-close::before { background: var(--tl-active); }
.traffic-lights:hover .tl-min::before   { background: var(--tl-active); }
.tl-close {
  --tl-idle: var(--tl-close-fill); --tl-active: var(--traffic-red);
  --tl-ring: var(--tl-close-ring); --tl-active-ring: rgba(255,95,87,.42);
}
.tl-min {
  --tl-idle: var(--tl-min-fill);   --tl-active: var(--traffic-yellow);
  --tl-ring: var(--tl-min-ring);   --tl-active-ring: rgba(254,188,46,.34);
}

/* ── center pill ─────────────────────────────────────── */
.center-pill {
  position: absolute; left: 50%; transform: translateX(-50%);
  width: 250px; display: flex; flex-direction: column;
  align-items: center; justify-content: center;
  height: 68px; z-index: 10;
  -webkit-app-region: no-drag; pointer-events: auto;
  transition: width .3s;
}
.app-title {
  font-family: var(--font-mono); font-weight: 700; font-size: 15px;
  letter-spacing: 1px; color: var(--text-title); text-transform: uppercase;
  cursor: pointer; padding: 4px 8px; -webkit-app-region: no-drag;
}
.app-status { font-size: 11px; color: var(--text-secondary); margin-top: -2px; }
[data-theme="light"] .app-status { color: #808080; }

/* ── unibar overlay ─────────────────────────────────── */
.unibar {
  position: absolute; display: none;
  top: 0; left: 0; right: 0; height: 56px;
  background: var(--bg-body);
  z-index: 2000; align-items: center; justify-content: center;
  -webkit-app-region: no-drag; pointer-events: auto;
  border-bottom: 1px solid var(--border-light);
}
.unibar-input {
  width: 50%; height: 40px;
  background: var(--bg-editor);
  border: 1px solid var(--accent); border-radius: 8px;
  padding: 0 16px; color: var(--accent);
  font-family: var(--font-mono); font-size: 14px;
}

/* ═══════════════════════════════════════════════════════
   WORKSPACE
═══════════════════════════════════════════════════════ */
.workspace {
  display: flex; flex: 1; overflow: hidden; position: relative;
}

/*
   ── TOP BORDER BLEND ──────────────────────────────────
   The workspace sits immediately below the title bar.
   Sidebar vertical borders are replaced by pseudo-elements
   that fade from transparent → solid over the first 40 px,
   removing the hard T-junction against the title bar.
*/
.workspace::before {
  /* thin gradient veil that covers the very top of the workspace,
     blending any border-start artefacts into the title-bar bg */
  content: ''; pointer-events: none;
  position: absolute; top: 0; left: 0; right: 0;
  height: 28px;
  background: linear-gradient(to bottom, var(--bg-body) 0%, transparent 100%);
  z-index: 9;   /* above sidebar borders, below content */
}

/* ── left sidebar ─────────────────────────────────── */
.sidebar-left {
  width: 240px; flex-shrink: 0;
  background: var(--bg-sidebar);
  /* border-right replaced by ::after gradient pseudo-element */
  display: flex; flex-direction: column; position: relative;
  transition: margin-left .3s cubic-bezier(.4,0,.2,1);
  z-index: 10;
}
.sidebar-left.collapsed { margin-left: -240px; }

/* fade-in right border from the top */
.sidebar-left::after {
  content: ''; pointer-events: none;
  position: absolute; top: 0; right: 0;
  width: 1px; height: 100%;
  background: linear-gradient(
    to bottom,
    transparent 0%,
    var(--border-light) 40px,
    var(--border-light) 100%
  );
  z-index: 2;
}

/* ── right sidebar ────────────────────────────────── */
.sidebar-right {
  width: 240px; flex-shrink: 0;
  background: var(--bg-sidebar);
  /* border-left replaced by ::before gradient pseudo-element */
  display: flex; flex-direction: column; position: relative;
  transition: margin-right .3s cubic-bezier(.4,0,.2,1);
  z-index: 10;
}
.sidebar-right.collapsed { margin-right: -240px; }

/* fade-in left border from the top */
.sidebar-right::before {
  content: ''; pointer-events: none;
  position: absolute; top: 0; left: 0;
  width: 1px; height: 100%;
  background: linear-gradient(
    to bottom,
    transparent 0%,
    var(--border-light) 40px,
    var(--border-light) 100%
  );
  z-index: 2;
}

/* shared sidebar chrome */
.sidebar-header {
  padding: 13.5px 12px;
  font-size: 12px; font-weight: 700; letter-spacing: 1.2px;
  color: var(--accent); text-transform: uppercase;
  font-family: var(--font-mono);
  display: flex; justify-content: space-between; align-items: center;
  border-bottom: 1px solid var(--border-light);
}
.sidebar-body {
  flex: 1; overflow-y: auto; padding: 12px;
  color: var(--text-muted); font-size: 12px;
  font-family: var(--font-mono); line-height: 1.6;
}

/* ── main content area ────────────────────────────── */
.main-area {
  flex: 1; min-width: 0;
  background: var(--bg-editor);
  display: flex; flex-direction: column;
  align-items: center; justify-content: center;
  position: relative; z-index: 1; overflow: hidden;
}

/* ── centered heading ─────────────────────────────── */
.main-heading {
  text-align: center; user-select: text;
  padding: 0 32px;
}
.main-heading h1 {
  font-family: var(--font-mono);
  font-size: clamp(28px, 4.5vw, 48px);
  font-weight: 700; letter-spacing: 4px;
  color: var(--accent); margin: 0 0 10px;
  text-transform: uppercase;
}
.main-heading .subtitle {
  font-size: 13px; color: var(--text-muted);
  font-family: var(--font-ui); margin: 0 0 20px;
  line-height: 1.6; letter-spacing: .3px;
}
.main-heading .copyright {
  font-size: 10px; color: var(--text-muted);
  letter-spacing: .5px; opacity: .45;
  font-family: var(--font-mono);
}

/* ── placeholder hint cards ───────────────────────── */
.ph-grid {
  display: flex; flex-wrap: wrap; gap: 8px;
  justify-content: center; margin-top: 28px;
}
.ph-card {
  border: 1px dashed var(--border-light);
  border-radius: 8px; padding: 9px 18px;
  font-size: 11px; color: var(--text-muted);
  font-family: var(--font-mono); letter-spacing: .5px;
  opacity: .5; transition: border-color .2s, opacity .2s;
}
.ph-card:hover { border-color: var(--accent); opacity: 1; }

/*
════════════════════════════════════════════════════════
OPTIONAL — WRITER / NOTEPAD PANE
────────────────────────────────────────────────────────
Uncomment the CSS block below and swap out the .main-area
contents with the writer HTML snippet (commented further
down in the HTML) to add a full notepad-like editor.

.writer-pane {
  display: flex; flex-direction: column;
  width: 100%; height: 100%; overflow-y: auto;
  padding: 48px 64px 200px 64px;   ← Apple Notes style
  box-sizing: border-box;
  max-width: 860px;                ← optional line-length cap
  margin: 0 auto;                  ← centre on ultrawide
  user-select: text;
}
.writer-title {
  background: transparent; border: none; outline: none;
  font-family: var(--font-mono); font-size: 24px; font-weight: 700;
  color: var(--text-title); width: 100%; margin-bottom: 20px;
  letter-spacing: 1px;
}
.writer-title::placeholder { color: var(--text-muted); opacity: .4; }
.writer-body {
  flex: 1; outline: none;
  font-family: var(--font-mono); font-size: 15px;
  line-height: 1.75; color: var(--text-content);
  white-space: pre-wrap; word-wrap: break-word; overflow-wrap: anywhere;
}
.writer-body:empty::before {
  content: attr(data-placeholder);
  color: var(--text-muted); pointer-events: none; opacity: .35;
}
════════════════════════════════════════════════════════
*/

/* ═══════════════════════════════════════════════════════
   STATUS BAR
═══════════════════════════════════════════════════════ */
.status-bar {
  height: 26px; background: var(--bg-body);
  border-top: 1px solid var(--border-light);
  display: flex; align-items: center; justify-content: space-between;
  padding: 0 16px; flex-shrink: 0;
  font-size: 11px; color: var(--text-secondary);
  font-family: var(--font-mono);
}

/* ═══════════════════════════════════════════════════════
   macOS-STYLE DIALOG
   — icon  ·  message  ·  Cancel  ·  Confirm
   — used by showDialog() and showInputDialog()
═══════════════════════════════════════════════════════ */
.dialog-overlay {
  position: fixed; inset: 0;
  background: rgba(0,0,0,.45); backdrop-filter: blur(6px);
  z-index: 5000; display: none;
  align-items: flex-start; justify-content: center;
  padding-top: 100px; opacity: 0; transition: opacity .3s;
}
.dialog-overlay.visible { opacity: 1; }

.dialog-box {
  background: var(--dialog-bg);
  width: 320px; padding: 24px 20px 20px;
  border-radius: 14px;
  border: 1px solid rgba(255,255,255,.06);
  box-shadow: 0 20px 60px rgba(0,0,0,.55), 0 4px 16px rgba(0,0,0,.3);
  display: flex; flex-direction: column; align-items: center; text-align: center;
  transform: scale(.88);
  transition: transform .32s cubic-bezier(.34,1.56,.64,1);
}
.dialog-overlay.visible .dialog-box { transform: scale(1); }

/* icon */
.dialog-icon {
  font-size: 38px; margin-bottom: 10px;
  color: var(--accent);
  display: flex; align-items: center; justify-content: center;
}
.dialog-icon span { font-size: 38px; }

/* message */
.dialog-msg {
  font-size: 13px; color: var(--dialog-text);
  margin-bottom: 20px; font-family: var(--font-ui);
  line-height: 1.5; width: 100%;
}

/* buttons row */
.dialog-actions { display: flex; width: 100%; gap: 8px; }
.dialog-btn {
  flex: 1; padding: 9px 8px; border: none; border-radius: 8px;
  font-size: 12px; font-weight: 600; cursor: pointer;
  transition: filter .15s, transform .1s;
  font-family: var(--font-ui);
}
.dialog-btn:hover  { filter: brightness(1.12); }
.dialog-btn:active { transform: scale(.97); }
.dialog-btn:focus  { outline: 2px solid var(--border-focus); outline-offset: 2px; }
.btn-cancel  { background: var(--dialog-cancel-bg);  color: var(--dialog-cancel-txt); }
.btn-confirm { background: var(--dialog-ok-bg);      color: var(--dialog-ok-txt);     }
</style>
</head>

<body data-theme="dark">

<!-- ── resize handles ──────────────────────────────────────────────── -->
<div class="rh rh-top"    onmousedown="WinApi.startDrag('top')"></div>
<div class="rh rh-left"   onmousedown="WinApi.startDrag('left')"></div>
<div class="rh rh-right"  onmousedown="WinApi.startDrag('right')"></div>
<div class="rh rh-bottom" onmousedown="WinApi.startDrag('bottom')"></div>

<div class="app-shell" id="appShell">

  <!-- ════════════════════════════════════════════════════
       TITLE BAR
  ════════════════════════════════════════════════════ -->
  <div class="title-bar" id="titleBar">

    <div id="titleDragZone"></div>

    <!-- UNIBAR OVERLAY -->
    <div class="unibar" id="unibar" onclick="closeUnibar(event)"
         onmousedown="event.stopPropagation()">
      <input class="unibar-input" id="unibarInput"
             placeholder="Alt+S to search…  or  //command">
    </div>

    <!-- ── LEFT PILL ──────────────────────────────────────── -->
    <div class="pill" onmousedown="event.stopPropagation()">
      <div class="pill-fixed">
        <!-- PLACEHOLDER: open file / folder dialog via WinApi.openFileDialog() -->
        <button class="icon-btn" title="Open" onclick="setStatus('Open — connect to WinApi.openFileDialog()')">
          <span class="material-symbols-outlined">folder</span>
        </button>
        <!-- PLACEHOLDER: trigger a save via POST /api/items -->
        <button class="icon-btn" title="Save" onclick="setStatus('Save — wire to your POST /api/items route')">
          <span class="material-symbols-outlined">save</span>
        </button>
        <!-- sidebar toggle (wired) -->
        <button class="icon-btn" title="Toggle Left Sidebar"
                onclick="toggleSidebar('left')">
          <span class="material-symbols-outlined">menu</span>
        </button>
        <!-- Action D — shows macOS confirmation dialog (demo) -->
        <button class="icon-btn" title="Action D (demo dialog)"
                onclick="confirmActionD()">
          <span class="material-symbols-outlined">add</span>
        </button>
      </div>
      <div class="pill-hidden">
        <!-- PLACEHOLDER: wire to your action log / history panel -->
        <button class="icon-btn" title="History" onclick="setStatus('History — PLACEHOLDER')">
          <span class="material-symbols-outlined">timeline</span>
        </button>
        <!-- PLACEHOLDER: open a grid / list view of your data -->
        <button class="icon-btn" title="Grid View" onclick="setStatus('Grid View — PLACEHOLDER')">
          <span class="material-symbols-outlined">grid_view</span>
        </button>
        <!-- PLACEHOLDER: toggle a canvas / visual layer -->
        <button class="icon-btn" title="Canvas" onclick="setStatus('Canvas — PLACEHOLDER')">
          <span class="material-symbols-outlined">draw</span>
        </button>
      </div>
    </div>

    <!-- ── CENTER TITLE PILL ─────────────────────────────── -->
    <div class="center-pill" id="centerPill">
      <div class="app-title"
           ondblclick="event.stopPropagation(); openUnibar()">RYTHON</div>
      <div class="app-status" id="statusMsg">Ready</div>
    </div>

    <!-- ── RIGHT PILL ─────────────────────────────────────── -->
    <div class="pill" onmousedown="event.stopPropagation()">
      <div class="pill-hidden">
        <!-- PLACEHOLDER: any hidden action -->
        <button class="icon-btn" title="Action H" onclick="setStatus('Action H — PLACEHOLDER')">
          <span class="material-symbols-outlined">star</span>
        </button>
        <!-- Theme toggle — dark ↔ light  (was Action I) -->
        <button class="icon-btn" id="btnTheme" title="Toggle Theme"
                onclick="toggleTheme()">
          <span class="material-symbols-outlined">contrast</span>
        </button>
        <!-- PLACEHOLDER: open a settings panel / overlay -->
        <button class="icon-btn" title="Settings" onclick="setStatus('Settings — PLACEHOLDER')">
          <span class="material-symbols-outlined">settings</span>
        </button>
      </div>
      <div class="pill-fixed">
        <!-- sidebar toggle (wired) -->
        <button class="icon-btn" title="Toggle Right Sidebar"
                onclick="toggleSidebar('right')">
          <span class="material-symbols-outlined">content_paste</span>
        </button>
        <!-- PLACEHOLDER: wire to an export / share flow -->
        <button class="icon-btn" title="Export" onclick="setStatus('Export — PLACEHOLDER')">
          <span class="material-symbols-outlined">ios_share</span>
        </button>
        <div class="traffic-lights">
          <button class="tl-btn tl-min"   onclick="WinApi.minimize()"></button>
          <button class="tl-btn tl-close" onclick="WinApi.close()"></button>
        </div>
      </div>
    </div>

  </div><!-- /title-bar -->

  <!-- ════════════════════════════════════════════════════
       WORKSPACE
  ════════════════════════════════════════════════════ -->
  <div class="workspace">

    <!-- LEFT SIDEBAR -->
    <div class="sidebar-left collapsed" id="sidebarLeft">
      <div class="sidebar-header">
        LEFT PANEL
        <!-- PLACEHOLDER: add header icon buttons here -->
      </div>
      <div class="sidebar-body">
        <!--
          PLACEHOLDER: left sidebar content.
          Examples: notes list, file tree, entity browser.
          Fetch data from GET /api/items and render here.
        -->
      </div>
    </div>

    <!-- MAIN CONTENT AREA -->
    <div class="main-area" id="mainArea">

      <!--
        ══ OPTIONAL WRITER / NOTEPAD PANE ═══════════════════
        To enable a notepad layout:
          1. Uncomment the CSS  .writer-pane  block above.
          2. Replace the .main-heading block below with:

        <div class="writer-pane" id="writerPane">
          <input  class="writer-title" id="writerTitle"
                  placeholder="Title…">
          <div    class="writer-body"  id="writerBody"
                  contenteditable="true"
                  data-placeholder="Start writing…"></div>
        </div>

          3. Hook writerTitle / writerBody to POST /api/items
             on input  (debounce ~800 ms) or on Ctrl+S.
        ════════════════════════════════════════════════════ -->

      <!-- DEFAULT: centred heading -->
      <div class="main-heading">
        <h1>RYTHON</h1>
        <p class="subtitle">
          Python Webview App Template &nbsp;&middot;&nbsp; by Ryan Ahmed
        </p>
        <p class="copyright">Copyright &copy; 2025 RYAN &nbsp;&middot;&nbsp; All rights reserved</p>

        <div class="ph-grid">
          <!-- PLACEHOLDER: replace with your real UI modules -->
          <div class="ph-card">#PLACEHOLDER &nbsp; main content area</div>
          <div class="ph-card">#PLACEHOLDER &nbsp; data layer / routes</div>
          <div class="ph-card">#PLACEHOLDER &nbsp; sidebar panels</div>
        </div>
      </div>

    </div><!-- /main-area -->

    <!-- RIGHT SIDEBAR -->
    <div class="sidebar-right collapsed" id="sidebarRight">
      <div class="sidebar-header">
        RIGHT PANEL
        <!-- PLACEHOLDER: add header icon buttons here -->
      </div>
      <div class="sidebar-body">
        <!--
          PLACEHOLDER: right sidebar content.
          Examples: clipboard history, properties inspector,
          action log, AI assistant panel.
        -->
      </div>
    </div>

  </div><!-- /workspace -->

  <!-- STATUS BAR -->
  <div class="status-bar">
    <!-- PLACEHOLDER: left info (word count, cursor pos, DB status…) -->
    <span id="statusLeft">RYTHON v1.0</span>
    <!-- live clock (wired) -->
    <span id="statusRight">--:--</span>
  </div>

</div><!-- /app-shell -->

<!-- ════════════════════════════════════════════════════════
     macOS-STYLE DIALOG
     — always Cancel on the left, Confirm on the right
     — icon is set dynamically by showDialog(msg, icon)
════════════════════════════════════════════════════════ -->
<div class="dialog-overlay" id="dlgOverlay">
  <div class="dialog-box">
    <div class="dialog-icon" id="dlgIcon">
      <span class="material-symbols-outlined">help</span>
    </div>
    <div class="dialog-msg" id="dlgMsg">Message</div>
    <div class="dialog-actions">
      <button class="dialog-btn btn-cancel"  id="dlgCancel">Cancel</button>
      <button class="dialog-btn btn-confirm" id="dlgConfirm">Confirm</button>
    </div>
  </div>
</div>

<script>
"use strict";
/* ─── state ─────────────────────────────────────────────── */
let isDark       = true;
let isMaximized  = false;
let isTitleMaxed = false;
let snapBusy     = false;
let _dlgResolver = null;

/* ─── window API proxy ───────────────────────────────────── */
const WinApi = {
  close()    { window.pywebview?.api.close_window(); },
  minimize() { window.pywebview?.api.minimize_window(); },
  startDrag(m){ window.pywebview?.api.start_drag(m); },
  /* PLACEHOLDER: expose more WindowApi methods as needed */
};

/* ═══════════════════════════════════════════════════════════
   THEME
═══════════════════════════════════════════════════════════ */
function toggleTheme() {
  isDark = !isDark;
  const t = isDark ? 'dark' : 'light';
  document.body.setAttribute('data-theme', t);
  localStorage.setItem('rython_theme', t);
  setStatus(isDark ? 'Dark mode' : 'Light mode');
}

/* ═══════════════════════════════════════════════════════════
   STATUS / CLOCK
═══════════════════════════════════════════════════════════ */
function setStatus(msg) {
  const el = document.getElementById('statusMsg');
  el.textContent = msg;
  clearTimeout(setStatus._t);
  setStatus._t = setTimeout(() => { el.textContent = 'Ready'; }, 3000);
}

function _tick() {
  document.getElementById('statusRight').textContent =
    new Intl.DateTimeFormat(navigator.language,
      { hour: '2-digit', minute: '2-digit', hour12: false }
    ).format(new Date());
}
setInterval(_tick, 1000);
_tick();

/* ═══════════════════════════════════════════════════════════
   SIDEBARS
═══════════════════════════════════════════════════════════ */
function toggleSidebar(side) {
  const id = side === 'left' ? 'sidebarLeft' : 'sidebarRight';
  document.getElementById(id).classList.toggle('collapsed');
  /* PLACEHOLDER: fire any load callback after uncollapsing */
}

/* ═══════════════════════════════════════════════════════════
   UNIBAR
═══════════════════════════════════════════════════════════ */
function openUnibar() {
  document.getElementById('unibar').style.display = 'flex';
  const cp = document.getElementById('centerPill');
  cp.style.opacity = '0'; cp.style.pointerEvents = 'none';
  document.getElementById('unibarInput').focus();
}
function closeUnibar(e) {
  if (!e || e.target.id === 'unibar') {
    document.getElementById('unibar').style.display = 'none';
    const cp = document.getElementById('centerPill');
    cp.style.opacity = '1'; cp.style.pointerEvents = 'auto';
  }
}
function _handleUnibarKey(e) {
  if (e.key === 'Escape') { closeUnibar(); return; }
  if (e.key !== 'Enter')  return;
  const val = e.target.value.trim();
  if (!val) return;
  if (val.startsWith('//')) {
    const cmd = val.slice(2).toLowerCase();
    /* PLACEHOLDER: register //commands here */
    if      (cmd === 'theme') toggleTheme();
    else if (cmd === 'left')  toggleSidebar('left');
    else if (cmd === 'right') toggleSidebar('right');
    else setStatus(`Unknown: //${cmd}`);
  } else {
    /* PLACEHOLDER: implement search / command routing */
    setStatus(`Search: "${val}"`);
  }
  e.target.value = '';
  closeUnibar();
}

/* ═══════════════════════════════════════════════════════════
   macOS-STYLE DIALOG
   showDialog(msg, icon='help')       → Promise<bool>
   showInputDialog(msg, def='', icon) → Promise<string|null>
═══════════════════════════════════════════════════════════ */
function _openDlg(icon = 'help') {
  document.getElementById('dlgIcon').innerHTML =
    `<span class="material-symbols-outlined">${icon}</span>`;
  const ov = document.getElementById('dlgOverlay');
  ov.style.display = 'flex';
  requestAnimationFrame(() => ov.classList.add('visible'));
  return ov;
}
function _closeDlg() {
  const ov = document.getElementById('dlgOverlay');
  ov.classList.remove('visible');
  setTimeout(() => { ov.style.display = 'none'; }, 320);
}

function showDialog(msg, icon = 'help') {
  document.getElementById('dlgMsg').textContent = msg;
  _openDlg(icon);
  document.getElementById('dlgConfirm').focus();
  return new Promise(resolve => {
    _dlgResolver = ok => { _closeDlg(); resolve(ok); };
    document.getElementById('dlgConfirm').onclick = () => _dlgResolver(true);
    document.getElementById('dlgCancel').onclick  = () => _dlgResolver(false);
  });
}

function showInputDialog(msg, defVal = '', icon = 'edit') {
  document.getElementById('dlgMsg').innerHTML =
    `${msg}<br><br>
     <input id="_dlgInput" value="${defVal}"
       style="width:100%;padding:9px 10px;
              background:var(--bg-pill);color:var(--accent);
              border:1px solid var(--border-light);border-radius:8px;
              font-family:var(--font-mono);font-size:13px;outline:none;">`;
  _openDlg(icon);
  const inp = document.getElementById('_dlgInput');
  inp.focus(); inp.select();
  return new Promise(resolve => {
    const done = ok => {
      const v = ok ? (document.getElementById('_dlgInput')?.value ?? '') : null;
      _closeDlg(); resolve(v);
    };
    document.getElementById('dlgConfirm').onclick = () => done(true);
    document.getElementById('dlgCancel').onclick  = () => done(false);
    inp.addEventListener('keydown', e => { if (e.key === 'Enter') done(true); });
  });
}

function _handleDlgKeys(e) {
  if (document.getElementById('dlgOverlay').style.display !== 'flex') return;
  if (e.key === 'Enter')  { document.activeElement.click(); return; }
  if (e.key === 'Escape') { _dlgResolver?.(false); return; }
  if (e.key === 'ArrowLeft' || e.key === 'ArrowRight') {
    const ok = document.getElementById('dlgConfirm');
    const cl = document.getElementById('dlgCancel');
    (document.activeElement === ok ? cl : ok).focus();
  }
}

/* ── Action D demo ────────────────────────────────────────── */
async function confirmActionD() {
  const ok = await showDialog(
    'Proceed with Action D?\nThis will demonstrate the macOS-style confirmation dialog.',
    'info'
  );
  setStatus(ok ? 'Action D confirmed ✓' : 'Action D cancelled');
  /* PLACEHOLDER: replace with your actual action (e.g. create a DB record) */
}

/* ═══════════════════════════════════════════════════════════
   TITLE-BAR DRAG
═══════════════════════════════════════════════════════════ */
function initTitleBarDrag() {
  const zone = document.getElementById('titleDragZone');

  zone.addEventListener('mousedown', async (e) => {
    if (e.button !== 0) return;
    if (document.getElementById('unibar').style.display === 'flex') return;
    e.preventDefault();

    if (isTitleMaxed) {
      const sx = e.clientX, sy = e.clientY;
      let fired = false;
      const clean = () => {
        window.removeEventListener('mousemove', mv, true);
        window.removeEventListener('mouseup',   mu, true);
      };
      const mu = () => clean();
      const mv = async (me) => {
        if (fired) return;
        if (Math.abs(me.clientX-sx) < 6 && Math.abs(me.clientY-sy) < 6) return;
        fired = true; clean();
        await safeMaximize();
        setTimeout(() => window.pywebview?.api.start_drag('move'), 0);
      };
      window.addEventListener('mousemove', mv, true);
      window.addEventListener('mouseup',   mu, true);
      return;
    }
    window.pywebview?.api.start_drag('move');
  });

  zone.addEventListener('dblclick', (e) => {
    e.preventDefault(); e.stopPropagation();
    cycleTitleBarState();
  });

  window.addEventListener('mouseup', () => window.pywebview?.api.end_drag?.());
}

/* ═══════════════════════════════════════════════════════════
   SNAP / MAXIMIZE / RESTORE
═══════════════════════════════════════════════════════════ */
async function _getArea(mon = false) {
  const a = await (mon
    ? window.pywebview?.api.get_monitor_bounds?.()
    : window.pywebview?.api.get_work_area?.());
  if (a?.width) return a;
  const dpr = window.devicePixelRatio || 1;
  return mon
    ? { left: Math.round((window.screen.left||0)*dpr),
        top:  Math.round((window.screen.top||0)*dpr),
        width: Math.round(window.screen.width*dpr),
        height:Math.round(window.screen.height*dpr) }
    : { left: Math.round((window.screen.availLeft||0)*dpr),
        top:  Math.round((window.screen.availTop||0)*dpr),
        width: Math.round(window.screen.availWidth*dpr),
        height:Math.round(window.screen.availHeight*dpr) };
}

async function _applySnap(x, y, w, h, useMon = false) {
  if (snapBusy) return;
  snapBusy = true;
  try { return await window.pywebview?.api.snap_window(x, y, w, h, useMon, true); }
  finally { snapBusy = false; }
}

async function safeMaximize() {
  const {left:l,top:t,width:w,height:h} = await _getArea(true);
  await _applySnap(l, t, w, h, true);
  isMaximized = true; isTitleMaxed = false;
}
async function safeRestore() {
  const {left:l,top:t,width:w,height:h} = await _getArea(false);
  const tw = Math.min(1600, w), th = Math.min(980, h);
  await _applySnap(l + Math.floor((w-tw)/2), t + Math.floor((h-th)/2), tw, th);
  isMaximized = false; isTitleMaxed = false;
}

async function performSnap(action) {
  if (snapBusy) return;
  const mon  = await _getArea(true);
  const work = await _getArea(false);
  const { left:l, top:t, width:w, height:h } = mon;
  let tx, ty, tw, th, useMon = true;
  switch (action) {
    case 'left':  tw = Math.floor(w/2);  th = h; tx = l;            ty = t; break;
    case 'right': tw = w-Math.floor(w/2);th = h; tx = l+Math.floor(w/2); ty = t; break;
    default:      /* center */
      tw = Math.min(1600, work.width); th = Math.min(980, work.height);
      tx = work.left + Math.floor((work.width-tw)/2);
      ty = work.top  + Math.floor((work.height-th)/2);
      useMon = false;
  }
  await _applySnap(tx, ty, tw, th, useMon);
  isMaximized = false; isTitleMaxed = false;
}

function cycleSnapState()    { if (!snapBusy) (isMaximized ? safeRestore() : safeMaximize()); }
function cycleTitleBarState(){ if (!snapBusy)  window.pywebview?.api.maximize_toggle(); }

/* called from Python after ShowWindow */
function updateWindowState(s) {
  document.getElementById('appShell').classList.toggle('maximized', s === 'maximized');
  isTitleMaxed = s === 'maximized'; if (isTitleMaxed) isMaximized = false;
}

/* ═══════════════════════════════════════════════════════════
   KEYBOARD SHORTCUTS
═══════════════════════════════════════════════════════════ */
document.addEventListener('keydown', e => {
  /* dialog intercept — highest priority */
  if (document.getElementById('dlgOverlay').style.display === 'flex') {
    _handleDlgKeys(e); return;
  }
  /* unibar */
  if (e.altKey && e.key === 's') { e.preventDefault(); openUnibar(); return; }
  /* snap */
  if (e.altKey && e.key === 'ArrowLeft')  { performSnap('left');   return; }
  if (e.altKey && e.key === 'ArrowRight') { performSnap('right');  return; }
  if (e.altKey && e.key === 'ArrowDown')  { performSnap('center'); return; }
  if (e.altKey && e.key === 'ArrowUp')    { cycleSnapState();      return; }
  /* sidebar arrows (only when not typing) */
  const inInput = document.activeElement?.isContentEditable ||
                  ['INPUT','TEXTAREA'].includes(document.activeElement?.tagName);
  if (!inInput) {
    if (e.key === 'ArrowLeft')  toggleSidebar('left');
    if (e.key === 'ArrowRight') toggleSidebar('right');
  }
  if (e.key === 'Escape') closeUnibar();
  /* PLACEHOLDER: add more shortcuts here */
});

/* auto-collapse sidebars on narrow windows */
window.addEventListener('resize', () => {
  if (window.innerWidth < 1000) {
    document.getElementById('sidebarLeft').classList.add('collapsed');
    document.getElementById('sidebarRight').classList.add('collapsed');
  }
});

/* ═══════════════════════════════════════════════════════════
   BOOT
═══════════════════════════════════════════════════════════ */
document.addEventListener('DOMContentLoaded', () => {
  const saved = localStorage.getItem('rython_theme');
  if (saved) { isDark = saved === 'dark'; document.body.setAttribute('data-theme', saved); }

  initTitleBarDrag();
  document.getElementById('unibarInput').addEventListener('keydown', _handleUnibarKey);

  /* PLACEHOLDER: call your startup data fetch here, e.g.
       fetch('/api/items').then(r=>r.json()).then(renderItems);
  */
});

/* ══════════════════════════════════════════════════════════
   PLACEHOLDER — JS FETCH HELPERS (copy-paste snippets)
   ─────────────────────────────────────────────────────────
   async function apiGet(path)        { return fetch(path).then(r=>r.json()); }
   async function apiPost(path, body) {
     return fetch(path, { method:'POST',
                          headers:{'Content-Type':'application/json'},
                          body: JSON.stringify(body) }).then(r=>r.json());
   }
   async function apiPut(path, body)  { ... same as POST with method:'PUT' }
   async function apiDel(path)        {
     const ok = await showDialog('Delete?', 'delete');
     if (ok) return fetch(path, { method:'DELETE' }).then(r=>r.json());
   }
═══════════════════════════════════════════════════════════ */
</script>
</body>
</html>
"""

# ── Window API ──────────────────────────────────────────────────────────────
class WindowApi:
    """
    Methods here become  window.pywebview.api.<method>()  in JS.
    Keep methods fast (<50 ms).  Spawn threads for anything heavier.
    PLACEHOLDER: add your own OS-level methods below the built-ins.
    """
    def __init__(self):
        self.window      = None
        self.state       = 'windowed'
        self._hwnd       = None
        self._dragging   = False
        self._base_style = None

    # ── built-in controls ────────────────────────────────────────────────────
    def close_window(self):
        self.window.destroy(); sys.exit()

    def minimize_window(self):
        self.window.minimize()

    def maximize_toggle(self):
        if self.state == 'windowed':
            self.window.maximize(); self.state = 'maximized'
        else:
            self.window.restore();  self.state = 'windowed'
        self.window.evaluate_js(f"updateWindowState('{self.state}')")

    # ── snap / resize ────────────────────────────────────────────────────────
    def snap_window(self, x, y, width, height,
                    use_monitor_bounds=False, clamp_to_target=True):
        import ctypes
        from ctypes import wintypes
        hwnd = self._find_hwnd()
        if not hwnd: return None

        target = (self.get_monitor_bounds(int(x), int(y))
                  if use_monitor_bounds else self.get_work_area(int(x), int(y)))
        if not target:
            target = (self.get_monitor_bounds() if use_monitor_bounds
                      else self.get_work_area())

        x, y, width, height = int(x), int(y), int(width), int(height)
        if target and clamp_to_target:
            width  = min(width,  target['width'])
            height = min(height, target['height'])
            x = max(target['left'], min(x, target['left'] + target['width']  - width))
            y = max(target['top'],  min(y, target['top']  + target['height'] - height))

        SW_RESTORE = 9
        if ctypes.windll.user32.IsZoomed(hwnd) or self.state == 'maximized':
            ctypes.windll.user32.ShowWindow(hwnd, SW_RESTORE)
            self.state = 'windowed'
        if self._base_style is not None:
            ctypes.windll.user32.SetWindowLongW(hwnd, -16, self._base_style)
        ctypes.windll.user32.SetWindowPos(
            hwnd, None, x, y, width, height,
            0x0004 | 0x0010 | 0x0020)   # NOZORDER | NOACTIVATE | FRAMECHANGED

        r = wintypes.RECT()
        ctypes.windll.user32.GetWindowRect(hwnd, ctypes.byref(r))
        return {'left': r.left, 'top': r.top,
                'width': r.right-r.left, 'height': r.bottom-r.top}

    def get_work_area(self, x=None, y=None):
        return self._mon_rect(x, y, work=True)

    def get_monitor_bounds(self, x=None, y=None):
        return self._mon_rect(x, y, work=False)

    def _mon_rect(self, x=None, y=None, work=True):
        import ctypes
        from ctypes import wintypes
        mon = None
        if x is not None and y is not None:
            mon = ctypes.windll.user32.MonitorFromPoint(
                wintypes.POINT(int(x), int(y)), 2)
        if not mon:
            hwnd = self._find_hwnd()
            if hwnd: mon = ctypes.windll.user32.MonitorFromWindow(hwnd, 2)
        if not mon: return None

        class MI(ctypes.Structure):
            _fields_ = [('cbSize', ctypes.c_ulong),
                        ('rcMonitor', wintypes.RECT),
                        ('rcWork',    wintypes.RECT),
                        ('dwFlags',   ctypes.c_ulong)]
        mi = MI(); mi.cbSize = ctypes.sizeof(MI)
        if not ctypes.windll.user32.GetMonitorInfoW(mon, ctypes.byref(mi)):
            return None
        r = mi.rcWork if work else mi.rcMonitor
        return {'left': r.left, 'top': r.top,
                'width': r.right-r.left, 'height': r.bottom-r.top}

    # ── drag ─────────────────────────────────────────────────────────────────
    def start_drag(self, mode):
        import threading, time, ctypes
        from ctypes import wintypes
        hwnd = self._find_hwnd()
        if not hwnd: return
        if mode != 'move':
            hmap = {'left':10,'right':11,'top':12,'bottom':15,
                    'topleft':13,'topright':14,'bottomleft':16,'bottomright':17}
            s = ctypes.windll.user32.GetWindowLongW(hwnd, -16)
            ctypes.windll.user32.SetWindowLongW(hwnd, -16, s|0x00C00000|0x00040000)
            ctypes.windll.user32.ReleaseCapture()
            ctypes.windll.user32.SendMessageW(hwnd, 0xA1, hmap.get(mode, 2), 0)
            return
        pt = wintypes.POINT(); ctypes.windll.user32.GetCursorPos(ctypes.byref(pt))
        rc = wintypes.RECT();  ctypes.windll.user32.GetWindowRect(hwnd, ctypes.byref(rc))
        ox, oy = pt.x - rc.left, pt.y - rc.top
        self._dragging = True
        def _loop():
            F = 0x0001|0x0004|0x0010
            while self._dragging:
                if not (ctypes.windll.user32.GetAsyncKeyState(0x01) & 0x8000):
                    self._dragging = False; break
                c = wintypes.POINT(); ctypes.windll.user32.GetCursorPos(ctypes.byref(c))
                ctypes.windll.user32.SetWindowPos(hwnd, None, c.x-ox, c.y-oy, 0, 0, F)
                time.sleep(0.005)
        threading.Thread(target=_loop, daemon=True).start()

    def end_drag(self): self._dragging = False

    # ── file dialogs ─────────────────────────────────────────────────────────
    def select_folder(self):
        """PLACEHOLDER: called from JS via window.pywebview.api.select_folder()"""
        r = self.window.create_file_dialog(webview.FOLDER_DIALOG)
        return r[0] if r else None

    def open_file_dialog(self, file_types=None):
        """
        PLACEHOLDER: extend file_types for your app's accepted formats.
        Returns {'filename': str, 'content': str} or None.
        """
        types = file_types or ('Text Files (*.txt;*.md)', 'All files (*.*)')
        r = self.window.create_file_dialog(
            webview.OPEN_DIALOG, allow_multiple=False, file_types=types)
        if not r: return None
        try:
            with open(r[0], encoding='utf-8') as f:
                return {'filename': os.path.basename(r[0]), 'content': f.read()}
        except Exception: return None

    # ── PLACEHOLDER: add your own OS methods here ─────────────────────────────
    # def read_clipboard(self):   ...
    # def write_clipboard(self, text): ...
    # def show_notification(self, title, msg): ...

    # ── hwnd cache ────────────────────────────────────────────────────────────
    def _find_hwnd(self):
        if self._hwnd: return self._hwnd
        import ctypes
        h = ctypes.windll.user32.FindWindowW(None, 'RYTHON')
        if h:
            self._hwnd = h
            if self._base_style is None:
                self._base_style = ctypes.windll.user32.GetWindowLongW(h, -16)
        return h

# ── entry point ──────────────────────────────────────────────────────────────
def on_loaded(window):
    api.window = window

if __name__ == '__main__':
    # PLACEHOLDER: call init_db() here if you have a database setup
    threading.Thread(
        target=app.run,
        kwargs={'port': 5000, 'use_reloader': False},
        daemon=True
    ).start()

    api = WindowApi()
    window = webview.create_window(
        'RYTHON',
        'http://127.0.0.1:5000',
        width=1100, height=750,
        frameless=True,
        easy_drag=False,
        background_color='#050505',
        js_api=api
    )
    window.events.loaded += lambda: on_loaded(window)
    webview.start(debug=False)
