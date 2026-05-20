#!/usr/bin/env python3
"""Minimal CLI todo manager with JSON storage."""
import json, sys, os
from datetime import datetime

DB = os.path.expanduser("~/.todos.json")

def load():
    if not os.path.exists(DB): return []
    with open(DB) as f: return json.load(f)

def save(todos):
    with open(DB, "w") as f: json.dump(todos, f, indent=2)

def cmd_add(text):
    todos = load()
    todos.append({"id": len(todos)+1, "text": text, "done": False, "created": datetime.now().isoformat()})
    save(todos)
    print(f"✅ Added: {text}")

def cmd_list():
    todos = load()
    if not todos: print("No todos yet."); return
    for t in todos:
        status = "✓" if t["done"] else "○"
        print(f"  [{status}] {t['id']}. {t['text']}")

def cmd_done(idx):
    todos = load()
    for t in todos:
        if t["id"] == idx: t["done"] = True; save(todos); print(f"✓ Done: {t['text']}"); return
    print("Not found.")

def cmd_remove(idx):
    todos = load()
    todos = [t for t in todos if t["id"] != idx]
    save(todos)
    print(f"🗑 Removed #{idx}")

if __name__ == "__main__":
    args = sys.argv[1:]
    if not args: cmd_list(); sys.exit()
    if args[0] == "add" and len(args) > 1: cmd_add(" ".join(args[1:]))
    elif args[0] == "list": cmd_list()
    elif args[0] == "done" and len(args) > 1: cmd_done(int(args[1]))
    elif args[0] == "remove" and len(args) > 1: cmd_remove(int(args[1]))
    else: print("Usage: todo.py [add|list|done|remove] [args]")
