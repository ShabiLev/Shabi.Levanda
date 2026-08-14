from __future__ import annotations

import contextlib
import http.server
import os
import socket
import threading
from pathlib import Path

import pytest


ROOT = Path(__file__).resolve().parents[1]


class QuietHandler(http.server.SimpleHTTPRequestHandler):
    def log_message(self, format: str, *args: object) -> None:
        return


@pytest.fixture(scope="session")
def portfolio_base_url():
    configured_url = os.getenv("PORTFOLIO_BASE_URL")
    if configured_url:
        yield configured_url.rstrip("/")
        return

    with contextlib.closing(socket.socket()) as probe:
        probe.bind(("127.0.0.1", 0))
        port = probe.getsockname()[1]

    handler = lambda *args, **kwargs: QuietHandler(*args, directory=str(ROOT), **kwargs)
    server = http.server.ThreadingHTTPServer(("127.0.0.1", port), handler)
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    try:
        yield f"http://127.0.0.1:{port}"
    finally:
        server.shutdown()
        thread.join(timeout=5)
        server.server_close()


@pytest.fixture
def loaded_page(page, portfolio_base_url: str):
    page.goto(portfolio_base_url, wait_until="networkidle")
    return page
