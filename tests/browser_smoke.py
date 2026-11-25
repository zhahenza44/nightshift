#!/usr/bin/env python3
"""Rendered smoke check for the portfolio shell using Firefox WebDriver BiDi.

No third-party package is needed. The script serves the repository over HTTP,
opens a 390px iframe in headless Firefox, exercises the controls, and checks
layout, focus, and reduced-motion behavior.
"""

import base64
import http.server
import json
import os
import shutil
import socket
import struct
import subprocess
import sys
import tempfile
import time
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
HARNESS_PATH = "/__portfolio_browser_check__.html"
HARNESS = """<!doctype html>
<html lang="en">
<head><meta charset="utf-8"><title>Portfolio browser check</title></head>
<body>
<iframe id="frame" src="/index.html" style="width:390px;height:844px;border:0"></iframe>
</body>
</html>
"""

NORMAL_SCRIPT = r"""
new Promise((resolve) => {
  const frame = document.getElementById('frame');
  const checks = [];
  const check = (name, pass, detail) => checks.push({name, pass: Boolean(pass), detail});
  const run = () => {
    setTimeout(() => {
      const win = frame.contentWindow;
      const doc = win.document;
      const viewport = win.innerWidth;
      const scrollWidth = doc.documentElement.scrollWidth;
      check('390px iframe viewport', viewport === 390, String(viewport));
      check('no horizontal overflow', scrollWidth <= viewport, 'scrollWidth=' + scrollWidth);

      const overflowing = Array.from(doc.querySelectorAll('body *')).filter((el) => {
        const rect = el.getBoundingClientRect();
        const style = win.getComputedStyle(el);
        return rect.width > 0 && style.position !== 'fixed' &&
          (rect.right > viewport + 1 || rect.left < -1);
      }).map((el) => el.tagName.toLowerCase() + '.' + el.className);
      check('no element escapes viewport', overflowing.length === 0, overflowing.slice(0, 5).join(' | ') || 'none');

      const heroOpacity = Array.from(doc.querySelectorAll('.hero-copy > *'))
        .map((el) => win.getComputedStyle(el).opacity);
      check('hero copy visible after entrance', heroOpacity.every((value) => Number(value) === 1),
        heroOpacity.join(','));

      const cards = () => Array.from(doc.querySelectorAll('.project-card'))
        .filter((card) => !card.hidden).length;
      const pressed = (id) => doc.getElementById(id).getAttribute('aria-pressed');
      check('all cards visible initially', cards() === 6, 'visible=' + cards());

      doc.getElementById('filter-job1').click();
      check('AI filter shows one card', cards() === 1, 'visible=' + cards());
      check('AI filter pressed state', pressed('filter-job1') === 'true' && pressed('filter-all') === 'false',
        'all=' + pressed('filter-all') + ' job1=' + pressed('filter-job1'));

      doc.getElementById('filter-job2').click();
      check('Web filter shows five cards', cards() === 5, 'visible=' + cards());

      doc.getElementById('filter-all').click();
      check('All filter restores six cards', cards() === 6, 'visible=' + cards());

      const toggle = doc.getElementById('menu-toggle');
      const menu = doc.getElementById('mobile-menu');
      toggle.click();
      check('menu opens', toggle.getAttribute('aria-expanded') === 'true' && !menu.hasAttribute('inert'),
        'expanded=' + toggle.getAttribute('aria-expanded') + ' inert=' + menu.hasAttribute('inert'));
      check('menu label closes in English', toggle.getAttribute('aria-label') === 'Close menu',
        toggle.getAttribute('aria-label'));
      check('focus moves into menu', doc.activeElement === menu.querySelector('a'),
        doc.activeElement && doc.activeElement.textContent.trim());

      doc.dispatchEvent(new win.KeyboardEvent('keydown', {key: 'Escape', bubbles: true}));
      check('Escape closes menu', toggle.getAttribute('aria-expanded') === 'false' && menu.hasAttribute('inert'),
        'expanded=' + toggle.getAttribute('aria-expanded') + ' inert=' + menu.hasAttribute('inert'));
      check('focus returns to toggle', doc.activeElement === toggle, doc.activeElement && doc.activeElement.id);
      check('menu label opens in English', toggle.getAttribute('aria-label') === 'Open menu',
        toggle.getAttribute('aria-label'));

      const links = Array.from(doc.querySelectorAll('a'));
      links.forEach((link) => link.addEventListener('click', (event) => event.preventDefault(), true));
      links.forEach((link) => link.click());
      check('all links dispatch click', links.length === 22, 'links=' + links.length);

      [
        ['filter-all', 'All filter'],
        ['menu-toggle', 'Menu toggle'],
        ['filter-job1', 'AI filter'],
      ].forEach(([id, label]) => {
        const el = doc.getElementById(id);
        el.scrollIntoView({block: 'center'});
        el.focus();
        const style = win.getComputedStyle(el);
        check(label + ' has visible focus outline',
          style.outlineStyle !== 'none' && Number.parseFloat(style.outlineWidth) > 0,
          style.outlineStyle + ' ' + style.outlineWidth);
        const rect = el.getBoundingClientRect();
        check(label + ' focus target inside viewport',
          rect.left >= -1 && rect.right <= viewport + 1 && rect.top >= -1 && rect.bottom <= win.innerHeight + 1,
          'top=' + Math.round(rect.top) + ' bottom=' + Math.round(rect.bottom));
      });

      const cardLink = doc.querySelector('.card-link');
      cardLink.scrollIntoView({block: 'center'});
      cardLink.focus();
      const linkStyle = win.getComputedStyle(cardLink);
      check('card link has visible focus outline',
        linkStyle.outlineStyle !== 'none' && Number.parseFloat(linkStyle.outlineWidth) > 0,
        linkStyle.outlineStyle + ' ' + linkStyle.outlineWidth);

      resolve(checks);
    }, 1200);
  };
  if (frame.contentDocument && frame.contentDocument.readyState === 'complete') {
    run();
  } else {
    frame.addEventListener('load', run, {once: true});
  }
})
"""

REDUCED_SCRIPT = r"""
new Promise((resolve) => {
  const frame = document.getElementById('frame');
  const checks = [];
  const check = (name, pass, detail) => checks.push({name, pass: Boolean(pass), detail});
  const run = () => {
    setTimeout(() => {
      const win = frame.contentWindow;
      const doc = win.document;
      const nodes = Array.from(doc.querySelectorAll('.hero-copy > *, .btn, .card-link, .project-card'));
      const names = Array.from(new Set(nodes.map((el) => win.getComputedStyle(el).animationName)));
      check('reduced motion disables animations', names.every((name) => name === 'none'), names.join(','));
      const opacity = Array.from(doc.querySelectorAll('.hero-copy > *'))
        .map((el) => win.getComputedStyle(el).opacity);
      check('reduced motion keeps copy visible', opacity.every((value) => Number(value) === 1),
        opacity.join(','));
      resolve(checks);
    }, 100);
  };
  if (frame.contentDocument && frame.contentDocument.readyState === 'complete') {
    run();
  } else {
    frame.addEventListener('load', run, {once: true});
  }
})
"""


def free_port():
    with socket.socket() as sock:
        sock.bind(("127.0.0.1", 0))
        return sock.getsockname()[1]


class Handler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=str(ROOT), **kwargs)

    def do_GET(self):
        if self.path.split("?", 1)[0] == HARNESS_PATH:
            body = HARNESS.encode()
            self.send_response(200)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.send_header("Content-Length", str(len(body)))
            self.end_headers()
            self.wfile.write(body)
            return
        super().do_GET()

    def log_message(self, *args):
        pass


class WebSocket:
    def __init__(self, url, port):
        parsed = urllib.parse.urlparse(url)
        self.sock = socket.create_connection((parsed.hostname, parsed.port or port), timeout=30)
        self.sock.settimeout(30)
        key = base64.b64encode(os.urandom(16)).decode()
        request = (
            f"GET {parsed.path} HTTP/1.1\r\n"
            f"Host: {parsed.hostname}:{parsed.port or port}\r\n"
            "Upgrade: websocket\r\n"
            "Connection: Upgrade\r\n"
            f"Sec-WebSocket-Key: {key}\r\n"
            "Sec-WebSocket-Version: 13\r\n\r\n"
        )
        self.sock.sendall(request.encode())
        buffer = b""
        while b"\r\n\r\n" not in buffer:
            chunk = self.sock.recv(4096)
            if not chunk:
                raise RuntimeError("WebSocket handshake closed")
            buffer += chunk
        header, self.pending = buffer.split(b"\r\n\r\n", 1)
        if b"101" not in header.split(b"\r\n")[0]:
            raise RuntimeError("WebSocket handshake failed")
        self.next_id = 1

    def _recv_exact(self, count):
        while len(self.pending) < count:
            chunk = self.sock.recv(65536)
            if not chunk:
                raise RuntimeError("WebSocket closed")
            self.pending += chunk
        data, self.pending = self.pending[:count], self.pending[count:]
        return data

    def send(self, method, params=None):
        message = {"id": self.next_id, "method": method, "params": params or {}}
        payload = json.dumps(message).encode()
        header = bytes([0x81])
        length = len(payload)
        if length < 126:
            header += bytes([0x80 | length])
        elif length < 65536:
            header += bytes([0xFE]) + struct.pack("!H", length)
        else:
            header += bytes([0xFF]) + struct.pack("!Q", length)
        mask = os.urandom(4)
        masked = bytes(byte ^ mask[i % 4] for i, byte in enumerate(payload))
        self.sock.sendall(header + mask + masked)
        wanted = message["id"]
        self.next_id += 1
        while True:
            first, second = self._recv_exact(2)
            opcode = first & 0x0F
            length = second & 0x7F
            if length == 126:
                length = struct.unpack("!H", self._recv_exact(2))[0]
            elif length == 127:
                length = struct.unpack("!Q", self._recv_exact(8))[0]
            if second & 0x80:
                response_mask = self._recv_exact(4)
                data = bytes(byte ^ response_mask[i % 4] for i, byte in enumerate(self._recv_exact(length)))
            else:
                data = self._recv_exact(length)
            if opcode != 1:
                continue
            response = json.loads(data)
            if response.get("id") == wanted:
                if response.get("type") != "success":
                    raise RuntimeError(f"{method} failed: {json.dumps(response)}")
                return response.get("result", {})

    def close(self):
        self.sock.close()


def unwrap(value):
    if isinstance(value, dict):
        kind = value.get("type")
        if kind in ("string", "boolean", "number", "null"):
            return value.get("value")
        if kind == "object":
            return {key: unwrap(item) for key, item in value.get("value", [])}
        if kind == "array":
            return [unwrap(item) for item in value.get("value", [])]
    return value


def evaluate(client, context, expression):
    result = client.send("script.evaluate", {
        "expression": expression,
        "target": {"context": context},
        "awaitPromise": True,
        "returnByValue": True,
    })
    return unwrap(result.get("result", {}))


def wait_for_bidi(port):
    url = f"http://127.0.0.1:{port}/session"
    deadline = time.monotonic() + 30
    while time.monotonic() < deadline:
        try:
            urllib.request.urlopen(url, timeout=1)
        except urllib.error.HTTPError as error:
            if error.code == 400:
                return True
        except OSError:
            pass
        time.sleep(0.2)
    return False


def run_check(firefox, url, expression, reduced):
    """Run one expression in a fresh Firefox profile and return its checks."""
    profile = tempfile.mkdtemp(prefix="portfolio-firefox-")
    if reduced:
        (Path(profile) / "prefs.js").write_text(
            'user_pref("ui.prefersReducedMotion", 1);\n', encoding="utf-8")
    bidi_port = free_port()
    browser = subprocess.Popen([
        firefox, "--headless", "--no-remote", "--profile", profile,
        f"--remote-debugging-port={bidi_port}", f"--remote-allow-hosts=127.0.0.1",
        url,
    ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    try:
        if not wait_for_bidi(bidi_port):
            raise RuntimeError("Firefox BiDi endpoint did not start")
        client = WebSocket(f"ws://127.0.0.1:{bidi_port}/session", bidi_port)
        try:
            client.send("session.new", {"capabilities": {"alwaysMatch": {"browserName": "firefox"}}})
            tree = client.send("browsingContext.getTree", {})
            contexts = tree.get("contexts") or []
            if not contexts:
                raise RuntimeError("no browsing context")
            context = contexts[0]["context"]
            client.send("browsingContext.navigate", {"context": context, "url": url, "wait": "complete"})
            return evaluate(client, context, expression)
        finally:
            client.close()
    finally:
        browser.terminate()
        try:
            browser.wait(timeout=10)
        except subprocess.TimeoutExpired:
            browser.kill()
        shutil.rmtree(profile, ignore_errors=True)


def main():
    firefox = shutil.which("firefox")
    if not firefox:
        print("SKIP: firefox not installed")
        return 0

    http_port = free_port()
    server = http.server.ThreadingHTTPServer(("127.0.0.1", http_port), Handler)
    server_thread = __import__("threading").Thread(target=server.serve_forever, daemon=True)
    server_thread.start()
    url = f"http://127.0.0.1:{http_port}{HARNESS_PATH}"

    failed = 0
    try:
        checks = []
        for expression, reduced in ((NORMAL_SCRIPT, False), (REDUCED_SCRIPT, True)):
            checks += run_check(firefox, url, expression, reduced)
        for item in checks:
            status = "PASS" if item.get("pass") else "FAIL"
            if status == "FAIL":
                failed += 1
            print(f"CHECK {status} {item.get('name')} :: {item.get('detail')}")
        print(f"checks={len(checks)} failed={failed}")
    finally:
        server.shutdown()
        server.server_close()

    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
