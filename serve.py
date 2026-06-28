#!/usr/bin/env python3
"""Serve the BBM Textual TUI over the web for the Replit preview pane."""
import os

from textual_serve.server import Server

PORT = int(os.environ.get("PORT", "5000"))

if __name__ == "__main__":
    src_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "src")
    os.environ["PYTHONPATH"] = src_path + os.pathsep + os.environ.get("PYTHONPATH", "")

    server = Server(
        command="python -m bbm",
        host="0.0.0.0",
        port=PORT,
        title="BBM — Bitbucket Repository Manager",
    )
    server.serve()
