#!/usr/bin/env python3
"""Rendered smoke check for the portfolio shell using Firefox WebDriver BiDi.

No third-party package is needed. The script serves the repository over HTTP,
opens 390px and 320px iframes in headless Firefox, exercises the controls, and
checks layout, focus, motion, and reduced-motion behavior.
"""

import base64
import http.server
import json
import os
import re
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
NARROW_PATH = "/__portfolio_browser_check__320.html"
HARNESS_TEMPLATE = """<!doctype html>
<html lang="en">
<head><meta charset="utf-8"><title>Portfolio browser check</title></head>
<body>
<iframe id="frame" src="/index.html" style="width:{width}px;height:844px;border:0"></iframe>
</body>
</html>
"""

NORMAL_SCRIPT = r"""
new Promise((resolve) => {
  const frame = document.getElementById('frame');
  const checks = [];
  const check = (name, pass, detail) => checks.push({name, pass: Boolean(pass), detail});
  const run = () => {
    const immediateWin = frame.contentWindow;
    const immediateDoc = immediateWin.document;
    const heroActions = immediateDoc.querySelector('.hero-actions');
    immediateDoc.querySelector('.hero-actions .btn--primary').focus();
    const immediateStyle = immediateWin.getComputedStyle(heroActions);
    checks.push({
      name: 'focused hero actions are visible immediately',
      pass: Number(immediateStyle.opacity) === 1 && immediateStyle.animationName === 'none',
      detail: 'opacity=' + immediateStyle.opacity + ' animation=' + immediateStyle.animationName
    });
    const firstHeroStyle = immediateWin.getComputedStyle(immediateDoc.querySelector('.hero-copy > *'));
    checks.push({
      name: 'hero entrance animation is applied',
      pass: firstHeroStyle.animationName === 'hero-in' && firstHeroStyle.animationDuration === '0.7s',
      detail: firstHeroStyle.animationName + ' ' + firstHeroStyle.animationDuration
    });
    setTimeout(() => {
      const win = frame.contentWindow;
      const doc = win.document;
      const viewport = win.innerWidth;
      const scrollWidth = doc.documentElement.scrollWidth;
      check('390px iframe viewport', viewport === 390, String(viewport));
      check('no horizontal overflow', scrollWidth <= viewport, 'scrollWidth=' + scrollWidth);

      const tickerRoot = doc.querySelector('.ticker');
      const orbRoot = doc.querySelector('.hero-orb');
      const inSubtree = (root, el) => Boolean(root) && el !== root && root.contains(el);
      const findEscapes = () => Array.from(doc.querySelectorAll('body *')).filter((el) => {
        if (el.ownerSVGElement && inSubtree(orbRoot, el)) return false;
        if (inSubtree(tickerRoot, el)) return false;
        const rect = el.getBoundingClientRect();
        const style = win.getComputedStyle(el);
        return rect.width > 0 && style.position !== 'fixed' &&
          (rect.right > viewport + 1 || rect.left < -1);
      }).map((el) => el.tagName.toLowerCase() + '.' + el.className);
      const overflowing = findEscapes();
      check('no element escapes viewport', overflowing.length === 0, overflowing.slice(0, 5).join(' | ') || 'none');

      const probeHost = doc.querySelector('.sr-only');
      const probe = doc.createElement('div');
      probe.className = 'overflow-probe';
      probe.style.position = 'absolute';
      probe.style.left = '-500px';
      probe.style.width = '10px';
      probe.style.height = '10px';
      probeHost.appendChild(probe);
      const probeFound = findEscapes().some((item) => item.includes('overflow-probe'));
      check('overflow scan catches escaped content inside clipped container', probeFound,
        probeFound ? 'flagged' : 'missed');
      probe.remove();

      const heroOpacity = Array.from(doc.querySelectorAll('.hero-copy > *'))
        .map((el) => win.getComputedStyle(el).opacity);
      check('hero copy visible after entrance', heroOpacity.every((value) => Number(value) === 1),
        heroOpacity.join(','));

      const orb = doc.querySelector('.orb-rings');
      const ticker = doc.querySelector('.ticker-track');
      check('orb loop is running', win.getComputedStyle(orb).animationName === 'orb-spin',
        win.getComputedStyle(orb).animationName);
      check('ticker loop is running', win.getComputedStyle(ticker).animationName === 'ticker-scroll',
        win.getComputedStyle(ticker).animationName);

      const introRect = doc.querySelector('.hero-intro').getBoundingClientRect();
      const actionsRect = doc.querySelector('.hero-actions').getBoundingClientRect();
      const actionGap = Math.round(actionsRect.top - introRect.bottom);
      check('Instagram action row sits close to intro', actionGap <= 16, 'gap=' + actionGap + 'px');

      const primaryRect = doc.querySelector('.btn--primary').getBoundingClientRect();
      const ghostRect = doc.querySelector('.btn--ghost').getBoundingClientRect();
      check('Instagram button aligns with View projects', primaryRect.top === ghostRect.top,
        'primary=' + Math.round(primaryRect.top) + ' ghost=' + Math.round(ghostRect.top));

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

      win.scrollTo({top: 200, behavior: 'instant'});
      win.dispatchEvent(new win.Event('scroll'));
      const widthBeforeFilter = Number.parseFloat(doc.getElementById('scroll-progress-bar').style.width);
      doc.getElementById('filter-job1').click();
      const filteredMax = doc.documentElement.scrollHeight - win.innerHeight;
      const expectedFiltered = filteredMax > 0
        ? Math.min(100, Math.max(0, win.scrollY / filteredMax * 100))
        : 0;
      const widthAfterFilter = Number.parseFloat(doc.getElementById('scroll-progress-bar').style.width);
      check('scroll progress follows filter height change',
        Math.abs(widthAfterFilter - expectedFiltered) < 1,
        'was=' + widthBeforeFilter.toFixed(2) + '% now=' + widthAfterFilter.toFixed(2) +
        '% expected=' + expectedFiltered.toFixed(2) + '%');
      doc.getElementById('filter-all').click();

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

      const motionToggle = doc.getElementById('motion-toggle');
      const toggleText = () => motionToggle.querySelector('.motion-toggle-label').textContent.trim();
      check('pause control starts English and unpaused',
        motionToggle.getAttribute('aria-label') === 'Pause motion' &&
        toggleText() === 'Pause motion' &&
        motionToggle.getAttribute('aria-pressed') === 'false',
        motionToggle.getAttribute('aria-label') + '/' + toggleText() + ' pressed=' + motionToggle.getAttribute('aria-pressed'));
      motionToggle.click();
      check('pause control keeps its name while pressed',
        motionToggle.getAttribute('aria-label') === 'Pause motion' && toggleText() === 'Pause motion',
        motionToggle.getAttribute('aria-label') + '/' + toggleText());
      check('pause control pauses both loops',
        doc.documentElement.classList.contains('motion-paused') &&
        motionToggle.getAttribute('aria-pressed') === 'true' &&
        win.getComputedStyle(orb).animationPlayState === 'paused' &&
        win.getComputedStyle(ticker).animationPlayState === 'paused',
        win.getComputedStyle(orb).animationPlayState + ' / ' + win.getComputedStyle(ticker).animationPlayState);
      motionToggle.click();
      check('pause control resumes both loops',
        !doc.documentElement.classList.contains('motion-paused') &&
        motionToggle.getAttribute('aria-pressed') === 'false' &&
        toggleText() === 'Pause motion' &&
        win.getComputedStyle(orb).animationPlayState === 'running' &&
        win.getComputedStyle(ticker).animationPlayState === 'running',
        win.getComputedStyle(orb).animationPlayState + ' / ' + win.getComputedStyle(ticker).animationPlayState);

      const magnetic = doc.querySelector('.btn--primary');
      const magneticRect = magnetic.getBoundingClientRect();
      magnetic.dispatchEvent(new win.PointerEvent('pointermove', {
        bubbles: true, pointerType: 'mouse',
        clientX: magneticRect.right - 1, clientY: magneticRect.top + 1
      }));
      const magX = Math.abs(Number.parseFloat(magnetic.style.getPropertyValue('--mag-x')) || 0);
      const magY = Math.abs(Number.parseFloat(magnetic.style.getPropertyValue('--mag-y')) || 0);
      check('magnetic offset responds and stays capped at 2px',
        magX >= 1.5 && magY >= 1.5 && magX <= 2.01 && magY <= 2.01,
        'x=' + magX.toFixed(2) + ' y=' + magY.toFixed(2));
      magnetic.dispatchEvent(new win.PointerEvent('pointerleave', {bubbles: true}));
      magnetic.focus();
      const focusMagX = magnetic.style.getPropertyValue('--mag-x');
      check('keyboard focus does not move button', focusMagX === '0px', focusMagX);

      const links = Array.from(doc.querySelectorAll('a'));
      let clicked = 0;
      links.forEach((link) => link.addEventListener('click', (event) => {
        event.preventDefault();
        clicked += 1;
      }, true));
      links.forEach((link) => link.click());
      check('all links dispatch click', clicked === links.length,
        'clicked=' + clicked + '/' + links.length);
      const hrefs = links.map((link) => link.getAttribute('href'));
      const required = [
        '#main', '#top', '#project-grid', '#contact',
        'https://instagram.com/zhahenzar',
        'https://github.com/zhahenza44',
        'mailto:zhahenza666@proton.me',
        'https://github.com/zhahenza44/otomasi-web',
        'demos/ai-lead-capture/dashboard/index.html',
        'demos/servis-ac/index.html',
        'demos/ruang-rapi/index.html',
        'demos/kedai-kopi/index.html',
        'demos/rental-mobil/index.html',
        'demos/nightshift/index.html'
      ];
      const missing = required.filter((href) => !hrefs.includes(href));
      check('all required link destinations present', missing.length === 0,
        missing.join(',') || 'all present');

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

      doc.getElementById('project-grid').scrollIntoView({block: 'center'});
      setTimeout(() => {
        const gridOpacity = Number(win.getComputedStyle(doc.getElementById('project-grid')).opacity);
        check('project grid reveal completes', gridOpacity === 1, 'opacity=' + gridOpacity);

        win.scrollTo({top: doc.documentElement.scrollHeight, behavior: 'instant'});
        win.dispatchEvent(new win.Event('scroll'));
        const progressWidth = Number.parseFloat(doc.getElementById('scroll-progress-bar').style.width);
        check('scroll progress reaches bottom', progressWidth >= 99, 'width=' + progressWidth + '%');
        resolve(checks);
      }, 700);
    }, 1200);
  };
  if (frame.contentDocument && frame.contentDocument.readyState === 'complete') {
    run();
  } else {
    frame.addEventListener('load', run, {once: true});
  }
})
"""

NARROW_SCRIPT = r"""
new Promise((resolve) => {
  const frame = document.getElementById('frame');
  const checks = [];
  const check = (name, pass, detail) => checks.push({name, pass: Boolean(pass), detail});
  const run = () => setTimeout(() => {
    const win = frame.contentWindow;
    const doc = win.document;
    check('320px iframe viewport', win.innerWidth === 320, String(win.innerWidth));
    check('320px has no horizontal overflow', doc.documentElement.scrollWidth <= 320,
      'scrollWidth=' + doc.documentElement.scrollWidth);
    for (const selector of ['.brand', '.motion-toggle', '#menu-toggle', '.btn--primary', '.btn--ghost']) {
      const rect = doc.querySelector(selector).getBoundingClientRect();
      check(selector + ' fits 320px',
        rect.left >= -1 && rect.right <= 321 && rect.height >= 44,
        Math.round(rect.left) + '..' + Math.round(rect.right) + ' h=' + Math.round(rect.height));
    }
    resolve(checks);
  }, 1200);
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
      const nodes = Array.from(doc.querySelectorAll(
        '.hero-copy > *, .btn, .card-link, .project-card, .orb-rings, .ticker-track, .project-grid'
      ));
      const names = Array.from(new Set(nodes.map((el) => win.getComputedStyle(el).animationName)));
      check('reduced motion disables animations', names.every((name) => name === 'none'), names.join(','));
      const opacity = Array.from(doc.querySelectorAll('.hero-copy > *'))
        .map((el) => win.getComputedStyle(el).opacity);
      check('reduced motion keeps copy visible', opacity.every((value) => Number(value) === 1),
        opacity.join(','));
      check('reduced motion hides pause control',
        win.getComputedStyle(doc.getElementById('motion-toggle')).display === 'none',
        win.getComputedStyle(doc.getElementById('motion-toggle')).display);
      const gridOpacity = Number(win.getComputedStyle(doc.getElementById('project-grid')).opacity);
      check('reduced motion keeps project grid visible', gridOpacity === 1, 'opacity=' + gridOpacity);
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
        match = re.fullmatch(r"/__portfolio_browser_check__(\d*)\.html", self.path.split("?", 1)[0])
        if match:
            width = int(match.group(1) or 390)
            body = HARNESS_TEMPLATE.format(width=width).encode()
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
        self.events = []

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
            if response.get("method"):
                self.events.append(response)

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
            client.send("session.subscribe", {"events": ["log.entryAdded"]})
            tree = client.send("browsingContext.getTree", {})
            contexts = tree.get("contexts") or []
            if not contexts:
                raise RuntimeError("no browsing context")
            context = contexts[0]["context"]
            client.send("browsingContext.navigate", {"context": context, "url": url, "wait": "complete"})
            result = evaluate(client, context, expression)
            errors = [
                event for event in client.events
                if event.get("method") == "log.entryAdded"
                and event.get("params", {}).get("level") == "error"
            ]
            if isinstance(result, list):
                result = result + [{
                    "name": "no console errors",
                    "pass": not errors,
                    "detail": str(len(errors)) + " errors",
                }]
            return result
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
        print("FAIL: firefox not installed")
        return 1

    http_port = free_port()
    server = http.server.ThreadingHTTPServer(("127.0.0.1", http_port), Handler)
    server_thread = __import__("threading").Thread(target=server.serve_forever, daemon=True)
    server_thread.start()
    url = f"http://127.0.0.1:{http_port}{HARNESS_PATH}"
    narrow_url = f"http://127.0.0.1:{http_port}{NARROW_PATH}"

    failed = 0
    try:
        checks = []
        for check_url, expression, reduced in (
            (url, NORMAL_SCRIPT, False),
            (narrow_url, NARROW_SCRIPT, False),
            (url, REDUCED_SCRIPT, True),
        ):
            result = run_check(firefox, check_url, expression, reduced)
            if not isinstance(result, list) or not result:
                failed += 1
                print(f"CHECK FAIL harness returned no checks :: {check_url}")
                continue
            checks += result
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
