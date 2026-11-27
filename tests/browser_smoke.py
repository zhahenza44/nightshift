#!/usr/bin/env python3
"""Rendered smoke check for the NightShift landing page using Firefox WebDriver BiDi.

No third-party package is needed. The script serves the repository over HTTP,
opens 390px, 320px, and 1366px iframes in headless Firefox, exercises the
controls, and checks layout, focus, motion, and reduced-motion behavior.
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
WIDE_PATH = "/__portfolio_browser_check__1366.html"
HARNESS_TEMPLATE = """<!doctype html>
<html lang="en">
<head><meta charset="utf-8"><title>NightShift browser check</title></head>
<body>
<iframe id="frame" src="/index.html?noboot" style="width:{width}px;height:844px;border:0"></iframe>
</body>
</html>
"""

NORMAL_SCRIPT_A = r"""
new Promise((resolve) => {
  const frame = document.getElementById('frame');
  const checks = [];
  const check = (name, pass, detail) => checks.push({name, pass: Boolean(pass), detail});
  const wait = (ms) => new Promise((done) => setTimeout(done, ms));
  (async () => {
    try {
      if (!(frame.contentDocument && frame.contentDocument.readyState === 'complete')) {
        await new Promise((done) => frame.addEventListener('load', done, {once: true}));
      }
      await wait(2400);

      const win = frame.contentWindow;
      const doc = win.document;
      const viewport = win.innerWidth;
      check('390px iframe viewport', viewport === 390, String(viewport));
      check('no horizontal overflow', doc.documentElement.scrollWidth <= viewport,
        'scrollWidth=' + doc.documentElement.scrollWidth);

      const boot = doc.getElementById('boot');
      check('boot overlay finished or removed', !boot || boot.classList.contains('is-done'),
        boot ? boot.className : 'removed');
      check('document marked ready', doc.documentElement.classList.contains('is-ready'),
        doc.documentElement.className);

      const heroLabel = doc.querySelector('.hero-title').getAttribute('aria-label');
      check('hero copy is English', heroLabel === 'Webs that cannot be ignored.', heroLabel);
      const heroWords = Array.from(doc.querySelectorAll('.hero-title .title-inner'))
        .map((el) => el.textContent.trim()).join(' ');
      check('hero headline words translated', heroWords === 'WEBS THAT CANNOT BE IGNORED.', heroWords);

      const heroOpacity = ['.hero-copy', '.hero-stats', '.hero-foot']
        .map((selector) => Number(win.getComputedStyle(doc.querySelector(selector)).opacity));
      check('hero entrance copies visible', heroOpacity.every((value) => value === 1),
        heroOpacity.join(','));
      const titleOffsets = Array.from(doc.querySelectorAll('.title-inner')).map((el) => {
        const matrix = new DOMMatrixReadOnly(win.getComputedStyle(el).transform);
        return Math.round(matrix.m42);
      });
      check('hero title lines settle', titleOffsets.every((value) => Math.abs(value) < 1),
        titleOffsets.join(','));

      const orbRoot = doc.querySelector('.hero-orb');
      const scopedRoots = [
        orbRoot,
        doc.querySelector('.ticker'),
        doc.querySelector('.hero'),
        doc.querySelector('.footer-marquee'),
      ];
      const inSubtree = (root, el) => Boolean(root) && el !== root && root.contains(el);
      const findEscapes = () => Array.from(doc.querySelectorAll('body *')).filter((el) => {
        if (scopedRoots.some((root) => el === root || inSubtree(root, el))) return false;
        const rect = el.getBoundingClientRect();
        const style = win.getComputedStyle(el);
        return rect.width > 0 && style.position !== 'fixed' &&
          (rect.right > viewport + 1 || rect.left < -1);
      }).map((el) => el.tagName.toLowerCase() + '.' + el.className);
      const overflowing = findEscapes();
      check('no element escapes viewport', overflowing.length === 0,
        overflowing.slice(0, 5).join(' | ') || 'none');

      const probeHost = doc.createElement('div');
      probeHost.style.cssText = 'position:relative;overflow:hidden;width:100px;height:10px;';
      doc.body.appendChild(probeHost);
      const probe = doc.createElement('div');
      probe.className = 'overflow-probe';
      probe.style.cssText = 'position:absolute;left:-500px;width:10px;height:10px;';
      probeHost.appendChild(probe);
      const probeFound = findEscapes().some((item) => item.includes('overflow-probe'));
      check('overflow scan catches escaped content inside clipped container', probeFound,
        probeFound ? 'flagged' : 'missed');
      probeHost.remove();

      const animationName = (selector) => win.getComputedStyle(doc.querySelector(selector)).animationName;
      check('orb loop is running', animationName('.orb-copy') === 'orb-spin',
        animationName('.orb-copy'));
      check('ticker loop is running', animationName('.ticker-track') === 'ticker',
        animationName('.ticker-track'));
      check('footer marquee is running', animationName('.footer-marquee div') === 'footer-marquee',
        animationName('.footer-marquee div'));
      check('hero rings drift', animationName('.hero-rings') === 'rings-drift',
        animationName('.hero-rings'));

      const earlyBar = doc.getElementById('scroll-progress');
      win.scrollTo({top: 200, behavior: 'instant'});
      win.dispatchEvent(new win.Event('scroll'));
      let progress = 0;
      const earlyDeadline = Date.now() + 1000;
      while (Date.now() < earlyDeadline) {
        progress = Number.parseFloat(earlyBar.style.width);
        if (progress > 0) break;
        await wait(20);
      }
      check('scroll progress responds to scrolling', progress > 0 && progress < 100,
        'width=' + progress + '%');

      doc.getElementById('process-list').scrollIntoView({block: 'center', behavior: 'instant'});
      win.dispatchEvent(new win.Event('scroll'));
      await wait(200);
      const fill = Number.parseFloat(doc.getElementById('process-fill').style.height);
      check('process fill advances', fill > 0, 'height=' + fill + '%');
      const activeSteps = doc.querySelectorAll('.process-step.is-active').length;
      check('process steps activate on scroll', activeSteps >= 1, 'active=' + activeSteps);
      const stepNumbers = Array.from(doc.querySelectorAll('.step-no'))
        .map((el) => el.textContent.trim()).join(',');
      check('process step numbers are roman', stepNumbers === 'I,II,III,IV,V', stepNumbers);

      const menuButton = doc.getElementById('menu-btn');
      const menu = doc.getElementById('mobile-menu');
      menuButton.click();
      check('menu opens',
        menuButton.getAttribute('aria-expanded') === 'true' &&
        menu.getAttribute('aria-hidden') === 'false' && !menu.inert,
        'expanded=' + menuButton.getAttribute('aria-expanded') + ' hidden=' + menu.getAttribute('aria-hidden'));
      check('menu label closes in English', menuButton.getAttribute('aria-label') === 'Close menu',
        menuButton.getAttribute('aria-label'));
      await wait(220);
      check('focus moves into menu', doc.activeElement === menu.querySelector('a'),
        doc.activeElement && doc.activeElement.textContent.trim());
      doc.dispatchEvent(new win.KeyboardEvent('keydown', {key: 'Escape', bubbles: true}));
      check('Escape closes menu',
        menuButton.getAttribute('aria-expanded') === 'false' &&
        menu.getAttribute('aria-hidden') === 'true' && menu.inert,
        'expanded=' + menuButton.getAttribute('aria-expanded') + ' hidden=' + menu.getAttribute('aria-hidden'));
      check('focus returns to menu button', doc.activeElement === menuButton,
        doc.activeElement && doc.activeElement.id);
      check('menu label opens in English', menuButton.getAttribute('aria-label') === 'Open menu',
        menuButton.getAttribute('aria-label'));

      const projectButton = doc.querySelector('[data-open-project="hypermart"]');
      projectButton.scrollIntoView({block: 'center'});
      projectButton.click();
      const dialog = doc.getElementById('project-dialog');
      check('case file dialog opens', dialog.open, String(dialog.open));
      const dialogText = doc.getElementById('dialog-content').textContent;
      check('dialog case copy is English',
        dialogText.includes('CASE FILE 01 / E-COMMERCE') && dialogText.includes('Challenge') &&
        dialogText.includes('Approach') && dialogText.includes('YEAR'),
        dialogText.slice(0, 90).replace(/\s+/g, ' '));
      check('dialog note discloses fictional case',
        dialogText.includes('fictional case study for portfolio use'),
        dialogText.includes('fictional case study for portfolio use') ? 'present' : 'missing');
      resolve(checks);
    } catch (error) {
      resolve([{name: 'normal pass opens dialog', pass: false,
        detail: String((error && error.stack) || error)}]);
    }
  })();
})
"""

NORMAL_SCRIPT_B = r"""
new Promise((resolve) => {
  const checks = [];
  const check = (name, pass, detail) => checks.push({name, pass: Boolean(pass), detail});
  const wait = (ms) => new Promise((done) => setTimeout(done, ms));
  (async () => {
    try {
      await wait(80);
      const doc = document;
      const win = window;
      const viewport = win.innerWidth;
      const dialog = doc.getElementById('project-dialog');
      check('Escape closes case file dialog', !dialog.open, String(dialog.open));
      check('focus returns to case file button',
        doc.activeElement === doc.querySelector('[data-open-project="hypermart"]'),
        (doc.activeElement && doc.activeElement.dataset.openProject) || '');

      const contactMain = doc.querySelector('.contact-main');
      const mailActions = contactMain ? Array.from(contactMain.querySelectorAll('a[href^="mailto:"]')) : [];
      const sendMessage = doc.getElementById('send-message');
      const githubAction = doc.querySelector('.contact-actions a[href="https://github.com/zhahenza44/otomasi-web"]');
      check('send message opens Instagram DM in a new tab',
        Boolean(sendMessage) &&
          sendMessage.getAttribute('href') === 'https://ig.me/m/zhahenzar' &&
          sendMessage.getAttribute('target') === '_blank' &&
          (sendMessage.getAttribute('rel') || '').includes('noopener') &&
          sendMessage.querySelector('span').textContent === 'Send message',
        sendMessage ? sendMessage.outerHTML : 'missing link');
      check('email link row is gone',
        Boolean(contactMain) && !doc.querySelector('.contact-links') &&
          mailActions.length === 1 &&
          mailActions[0].querySelector('span').textContent === 'Email',
        'mailto=' + mailActions.length + ' textLinks=' + doc.querySelectorAll('.contact-links').length);
      check('github is a box beside send message',
        Boolean(githubAction) && Boolean(sendMessage) &&
          githubAction.closest('.contact-actions') === sendMessage.closest('.contact-actions') &&
          githubAction.classList.contains('btn') &&
          githubAction.getAttribute('target') === '_blank' &&
          (githubAction.getAttribute('rel') || '').includes('noopener') &&
          githubAction.querySelector('span').textContent === 'GITHUB' &&
          (sendMessage.compareDocumentPosition(githubAction) & win.Node.DOCUMENT_POSITION_FOLLOWING) > 0,
        githubAction ? githubAction.outerHTML : 'missing link');

      const magnetic = doc.querySelector('.hero-actions .btn--primary');
      magnetic.scrollIntoView({block: 'center', behavior: 'instant'});
      const magneticRect = magnetic.getBoundingClientRect();
      magnetic.dispatchEvent(new win.MouseEvent('mousemove', {
        bubbles: true, clientX: magneticRect.right - 1, clientY: magneticRect.top + 1,
      }));
      const magneticTransform = magnetic.style.transform;
      const magneticCoordinates = magneticTransform.slice(
        magneticTransform.indexOf('(') + 1,
        magneticTransform.lastIndexOf(')'),
      );
      const magneticValues = (magneticCoordinates.match(/-?\d+(?:\.\d+)?/g) || []).map(Number);
      check('magnetic button responds to mouse movement',
        magneticValues.length >= 2 && (Math.abs(magneticValues[0]) > 0 || Math.abs(magneticValues[1]) > 0),
        magneticTransform || 'none');
      check('magnetic offset stays capped',
        Math.abs(magneticValues[0]) <= 9.01 && Math.abs(magneticValues[1]) <= 7.01,
        magneticTransform || 'none');
      magnetic.dispatchEvent(new win.MouseEvent('mouseleave', {bubbles: true}));
      check('magnetic button resets', magnetic.style.transform === 'translate3d(0px, 0px, 0px)',
        magnetic.style.transform);

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

      const cvSection = doc.querySelector('section#cv');
      const sectionIds = Array.from(doc.querySelectorAll('section')).map((section) => section.id);
      check('cv section follows manifesto',
        Boolean(cvSection) && sectionIds.indexOf('studio') < sectionIds.indexOf('cv') &&
          sectionIds.indexOf('cv') < sectionIds.indexOf('work'), sectionIds.join(','));
      check('section ids are merged',
        sectionIds.join(',') === 'top,studio,cv,work,process,contact', sectionIds.join(','));
      const workSection = doc.querySelector('section#work');
      check('combined work section keeps both content blocks',
        Boolean(workSection) && workSection.querySelectorAll('.project-card').length === 3 &&
          workSection.querySelectorAll('.service-card').length === 4,
        'projects=' + (workSection ? workSection.querySelectorAll('.project-card').length : 'missing') +
          ' services=' + (workSection ? workSection.querySelectorAll('.service-card').length : 'missing'));
      const servicesBlock390 = doc.querySelector('.services-block');
      const workStyle390 = win.getComputedStyle(workSection);
      const afterCapabilities390 = servicesBlock390
        ? Math.round(workSection.getBoundingClientRect().bottom - servicesBlock390.getBoundingClientRect().bottom) : -1;
      check('work bottom padding stays compact at 390px',
        workStyle390.paddingBottom === '32px' && afterCapabilities390 >= 31 && afterCapabilities390 <= 33,
        'padding=' + workStyle390.paddingBottom + ' gap=' + afterCapabilities390);
      check('services nav anchor is gone', doc.querySelectorAll('a[href="#services"]').length === 0,
        'anchors=' + doc.querySelectorAll('a[href="#services"]').length);
      const githubLink = doc.querySelector('.contact-actions a[href="https://github.com/zhahenza44/otomasi-web"]');
      check('github label stays GITHUB in the action row',
        Boolean(githubLink) && githubLink.textContent.trim().startsWith('GITHUB') &&
          !doc.querySelector('.contact-links'),
        githubLink ? githubLink.textContent.trim() : 'missing link');
      const bodyText = doc.body.textContent;
      check('location is Surabaya',
        bodyText.includes('Surabaya, ID') && bodyText.includes('surabaya, id') &&
          !bodyText.includes('Jakarta') && !bodyText.includes('JKT'),
        'Surabaya=' + bodyText.includes('Surabaya, ID') + ' lower=' + bodyText.includes('surabaya, id'));
      const statLabels = Array.from(doc.querySelectorAll('.hero-stats dt'))
        .map((el) => el.textContent.trim());
      const statValues = Array.from(doc.querySelectorAll('.hero-stats dd'))
        .map((el) => el.textContent.trim());
      check('hero stats match owner update',
        statLabels.join(',') === 'Projects,Response' && statValues.join(',') === '1,<24h',
        statLabels.join(',') + ' :: ' + statValues.join(','));
      const cvText = cvSection ? cvSection.textContent.replace(/\s+/g, ' ').trim() : '';
      check('cv identity is visible',
        cvText.includes('Alan Nawa') && cvText.includes('Web & AI Automation'),
        cvText.slice(0, 120) || 'missing');
      const footerNote = doc.querySelector('.demo-note');
      check('contact demo note removed',
        !footerNote && !bodyText.includes('names, metrics, email, and phone number are fictional'),
        footerNote ? footerNote.textContent.trim() : 'removed');
      const contactSection = doc.querySelector('section#contact.section.contact');
      const contactPanel = doc.querySelector('.contact-panel');
      const siteFooter = doc.querySelector('.site-footer');
      const lastProcessStep = doc.querySelector('#process .process-step:last-of-type');
      const contactStyle = contactSection ? win.getComputedStyle(contactSection) : null;
      const footerStyle = siteFooter ? win.getComputedStyle(siteFooter) : null;
      check('contact section drops vertical padding',
        Boolean(contactStyle) && contactStyle.paddingTop === '0px' && contactStyle.paddingBottom === '0px',
        contactStyle ? 'top=' + contactStyle.paddingTop + ' bottom=' + contactStyle.paddingBottom : 'missing section');
      const abovePanel = contactPanel && lastProcessStep
        ? Math.round(contactPanel.getBoundingClientRect().top - lastProcessStep.getBoundingClientRect().bottom) : -1;
      check('contact panel follows last process step without extra gap', abovePanel >= 0 && abovePanel <= 1,
        'above=' + abovePanel);
      const belowPanel = contactPanel && siteFooter
        ? Math.round(siteFooter.getBoundingClientRect().top - contactPanel.getBoundingClientRect().bottom) : -1;
      check('contact panel sits flush with footer',
        Boolean(footerStyle) && footerStyle.marginTop === '0px' && belowPanel >= 0 && belowPanel <= 1,
        'marginTop=' + (footerStyle ? footerStyle.marginTop : 'missing') + ' below=' + belowPanel);
      check('cv note separates real CV from fictional case files',
        cvText.includes('This section is my real CV') && cvText.includes('fictional'),
        cvText.includes('This section is my real CV') ? 'cv note present' : 'cv note missing');
      const cvNav = doc.querySelectorAll('a[href="#cv"]');
      check('CV nav anchor reaches the CV section', cvNav.length === 2, 'anchors=' + cvNav.length);
      const cvContactParts = [
        'instagram.com/zhahenzar', 'github.com/zhahenza44', 'mailto:zhahenza666@proton.me',
      ];
      check('three CV contact links present',
        cvContactParts.every((part) => hrefs.some((href) => href && href.includes(part))),
        cvContactParts.filter((part) => !hrefs.some((href) => href && href.includes(part)))
          .join(',') || 'all present');
      const cvVisibleAnchors = Array.from(doc.querySelectorAll('.cv-demo-list a'));
      check('CV demo links are visible',
        cvVisibleAnchors.length === 6 && cvVisibleAnchors.every((link) => {
          const rect = link.getBoundingClientRect();
          return rect.width > 0 && rect.height > 0;
        }), 'visible=' + cvVisibleAnchors.filter((link) => {
          const rect = link.getBoundingClientRect();
          return rect.width > 0 && rect.height > 0;
        }).length + '/6');

      const required = [
        '#main', '#top', '#studio', '#cv', '#work', '#process', '#contact',
        'https://github.com/zhahenza44/otomasi-web',
        'https://ig.me/m/zhahenzar',
        'demos/ai-lead-capture/dashboard/index.html', 'demos/servis-ac/index.html',
        'demos/ruang-rapi/index.html', 'demos/kedai-kopi/index.html',
        'demos/rental-mobil/index.html', 'demos/nightshift/index.html',
        'https://instagram.com/zhahenzar', 'https://github.com/zhahenza44',
        'mailto:zhahenza666@proton.me',
      ];
      const missing = required.filter((href) => !hrefs.includes(href));
      check('required hrefs present', missing.length === 0, missing.join(',') || 'all present');
      const staleHrefs = hrefs.filter((href) => href && (href.includes('nightshift.studio') || href.includes('wa.me')));
      check('no fictional email or WhatsApp link remains', staleHrefs.length === 0,
        staleHrefs.join(',') || 'none');
      const demoHrefs = required.filter((href) => href && href.startsWith('demos/'));
      const demoLinks = Array.from(doc.querySelectorAll('a[href^="demos/"]'));
      const badDemoLinks = demoLinks.filter((link) => link.getAttribute('target') !== '_blank' ||
        !(link.getAttribute('rel') || '').includes('noopener') ||
        !demoHrefs.includes(link.getAttribute('href')));
      check('six CV demo links open in a new tab',
        demoLinks.length === 6 && badDemoLinks.length === 0,
        'links=' + demoLinks.length + ' bad=' + badDemoLinks.length);

      for (const [selector, label] of [
        ['#menu-btn', 'menu button'],
        ['.hero-actions .btn--primary', 'primary action'],
        ['[data-open-project="hypermart"]', 'case file button'],
        ['#send-message', 'send message button'],
      ]) {
        const el = doc.querySelector(selector);
        if (!el) {
          check(label + ' exists', false, 'missing ' + selector);
          continue;
        }
        el.scrollIntoView({block: 'center', behavior: 'instant'});
        el.focus();
        const style = win.getComputedStyle(el);
        check(label + ' has visible focus outline',
          style.outlineStyle !== 'none' && Number.parseFloat(style.outlineWidth) > 0,
          style.outlineStyle + ' ' + style.outlineWidth);
        const rect = el.getBoundingClientRect();
        check(label + ' focus target inside viewport',
          rect.left >= -1 && rect.right <= viewport + 1,
          Math.round(rect.left) + '..' + Math.round(rect.right));
      }

      const progressBar = doc.getElementById('scroll-progress');
      win.scrollTo({top: doc.documentElement.scrollHeight, behavior: 'instant'});
      win.dispatchEvent(new win.Event('scroll'));
      let bottomProgress = 0;
      const progressDeadline = Date.now() + 1000;
      while (Date.now() < progressDeadline) {
        bottomProgress = Number.parseFloat(progressBar.style.width);
        if (bottomProgress >= 99) break;
        await wait(20);
      }
      check('footer progress reaches bottom', bottomProgress >= 99, 'width=' + bottomProgress + '%');
      const footerText = doc.querySelector('.site-footer').textContent.replace(/\s+/g, ' ').trim();
      check('fictional studio footer label removed', !footerText.includes('DEMO CONCEPT / FICTIONAL STUDIO'),
        footerText.slice(0, 80));
      check('footer keeps English copy and back to top',
        footerText.includes('NIGHT//SHIFT') && footerText.includes('BACK TO TOP'),
        footerText.slice(0, 80));

      resolve(checks);
    } catch (error) {
      resolve([{name: 'normal pass continues after Escape', pass: false,
        detail: String((error && error.stack) || error)}]);
    }
  })();
})
"""

NARROW_SCRIPT = r"""
new Promise((resolve) => {
  const frame = document.getElementById('frame');
  const checks = [];
  const check = (name, pass, detail) => checks.push({name, pass: Boolean(pass), detail});
  const wait = (ms) => new Promise((done) => setTimeout(done, ms));
  (async () => {
    try {
      if (!(frame.contentDocument && frame.contentDocument.readyState === 'complete')) {
        await new Promise((done) => frame.addEventListener('load', done, {once: true}));
      }
      await wait(2400);
      const win = frame.contentWindow;
      const doc = win.document;
      check('320px iframe viewport', win.innerWidth === 320, String(win.innerWidth));
      check('320px has no horizontal overflow', doc.documentElement.scrollWidth <= 320,
        'scrollWidth=' + doc.documentElement.scrollWidth);
      const servicesBlock = doc.querySelector('.services-block');
      const blockRect = servicesBlock ? servicesBlock.getBoundingClientRect() : null;
      check('combined section fits 320px',
        Boolean(blockRect) && blockRect.left >= -1 && blockRect.right <= 321,
        blockRect ? Math.round(blockRect.left) + '..' + Math.round(blockRect.right) : 'missing');
      const cvBlocks = [doc.querySelector('.cv-grid'), doc.querySelector('.cv-demo-list')];
      check('cv section fits 320px', cvBlocks.every(Boolean) && cvBlocks.every((el) => {
        const rect = el.getBoundingClientRect();
        return rect.left >= -1 && rect.right <= 321;
      }), cvBlocks.filter(Boolean).map((el) => {
        const rect = el.getBoundingClientRect();
        return Math.round(rect.left) + '..' + Math.round(rect.right);
      }).join(' | ') || 'missing');
      for (const selector of [
        '.brand', '#menu-btn', '.hero-actions .btn--primary', '.hero-actions .btn--ghost',
        '#send-message', '.contact-actions .btn--primary',
      ]) {
        const el = doc.querySelector(selector);
        if (!el) {
          check(selector + ' exists at 320px', false, 'missing ' + selector);
          continue;
        }
        const rect = el.getBoundingClientRect();
        check(selector + ' fits 320px and meets 24px tap target',
          rect.left >= -1 && rect.right <= 321 && rect.width >= 24 && rect.height >= 24,
          Math.round(rect.left) + '..' + Math.round(rect.right) + ' h=' + Math.round(rect.height));
      }
      resolve(checks);
    } catch (error) {
      resolve([{name: 'narrow pass runs', pass: false,
        detail: String((error && error.stack) || error)}]);
    }
  })();
})
"""

REDUCED_SCRIPT = r"""
new Promise((resolve) => {
  const frame = document.getElementById('frame');
  const checks = [];
  const check = (name, pass, detail) => checks.push({name, pass: Boolean(pass), detail});
  const wait = (ms) => new Promise((done) => setTimeout(done, ms));
  (async () => {
    try {
      if (!(frame.contentDocument && frame.contentDocument.readyState === 'complete')) {
        await new Promise((done) => frame.addEventListener('load', done, {once: true}));
      }
      await wait(600);
      const win = frame.contentWindow;
      const doc = win.document;
      check('old pause control is absent', !doc.getElementById('motion-toggle'),
        doc.getElementById('motion-toggle') ? 'present' : 'absent');
      check('reduced motion hides custom cursor',
        win.getComputedStyle(doc.getElementById('cursor')).display === 'none',
        win.getComputedStyle(doc.getElementById('cursor')).display);
      check('reduced motion hides ghost layer',
        win.getComputedStyle(doc.getElementById('ghost-layer')).display === 'none',
        win.getComputedStyle(doc.getElementById('ghost-layer')).display);

      const loopSelectors = [
        '.ticker-track', '.footer-marquee div', '.hero-rings', '.orb-copy', '.orb-line--dash',
      ];
      const loopNames = loopSelectors.map((selector) => [
        selector, win.getComputedStyle(doc.querySelector(selector)).animationName,
      ]);
      check('reduced motion disables looping animations',
        loopNames.every((item) => item[1] === 'none'),
        loopNames.map((item) => item[0] + '=' + item[1]).join(','));
      const longAnimations = Array.from(doc.querySelectorAll('body *')).filter((el) => {
        const style = win.getComputedStyle(el);
        return style.animationName !== 'none' && Number.parseFloat(style.animationDuration) > 0.001;
      });
      check('reduced motion collapses remaining animations', longAnimations.length === 0,
        longAnimations.slice(0, 5).map((el) => el.className || el.tagName).join(',') || 'none');

      const hidden = [
        '.title-inner', '.hero-copy', '.hero-stats', '.hero-foot', '.reveal',
        '.manifesto-copy .word', '.t-line',
      ].filter((selector) => {
        const el = doc.querySelector(selector);
        return el && Number(win.getComputedStyle(el).opacity) < 1;
      });
      check('reduced motion keeps content visible', hidden.length === 0, hidden.join(',') || 'none');
      const boot = doc.getElementById('boot');
      check('boot skipped under reduced motion', !boot || boot.classList.contains('is-done'),
        boot ? boot.className : 'removed');
      resolve(checks);
    } catch (error) {
      resolve([{name: 'reduced motion pass runs', pass: false,
        detail: String((error && error.stack) || error)}]);
    }
  })();
})
"""

WIDE_SCRIPT = r"""
new Promise((resolve) => {
  const frame = document.getElementById('frame');
  (async () => {
    try {
      if (!(frame.contentDocument && frame.contentDocument.readyState === 'complete')) {
        await new Promise((done) => frame.addEventListener('load', done, {once: true}));
      }
      await new Promise((done) => setTimeout(done, 240));
      const win = frame.contentWindow;
      const doc = win.document;
      const checks = [];
      const check = (name, pass, detail) => checks.push({name, pass: Boolean(pass), detail: String(detail)});
      check('1366px iframe viewport', win.innerWidth === 1366, String(win.innerWidth));
      const cv = doc.querySelector('section#cv.section.cv');
      const style = cv ? win.getComputedStyle(cv) : null;
      check('CV section has no vertical padding',
        Boolean(style) && style.paddingTop === '0px' && style.paddingBottom === '0px',
        style ? 'top=' + style.paddingTop + ' bottom=' + style.paddingBottom : 'missing section');
      check('1366px no horizontal overflow', doc.documentElement.scrollWidth <= win.innerWidth,
        'scrollWidth=' + doc.documentElement.scrollWidth);
      const content = ['#cv .section-head', '#cv .cv-grid', '#cv .cv-demo-list'];
      check('CV content stays visible', content.every((selector) => {
        const el = doc.querySelector(selector);
        if (!el) return false;
        const rect = el.getBoundingClientRect();
        return rect.width > 0 && rect.height > 0;
      }), content.join(','));
      const wideWork = doc.querySelector('section#work.section.work');
      const wideServices = doc.querySelector('.services-block');
      const wideWorkStyle = wideWork ? win.getComputedStyle(wideWork) : null;
      const afterCapabilities1366 = wideWork && wideServices
        ? Math.round(wideWork.getBoundingClientRect().bottom - wideServices.getBoundingClientRect().bottom) : -1;
      check('1366px work bottom padding stays compact',
        Boolean(wideWorkStyle) && wideWorkStyle.paddingBottom === '48px' &&
          afterCapabilities1366 >= 47 && afterCapabilities1366 <= 49,
        'padding=' + (wideWorkStyle ? wideWorkStyle.paddingBottom : 'missing') +
          ' gap=' + afterCapabilities1366);
      const contact = doc.querySelector('section#contact.section.contact');
      const panel = doc.querySelector('.contact-panel');
      const footer = doc.querySelector('.site-footer');
      const lastStep = doc.querySelector('#process .process-step:last-of-type');
      const contactStyle = contact ? win.getComputedStyle(contact) : null;
      const footerStyle = footer ? win.getComputedStyle(footer) : null;
      check('1366px contact section drops vertical padding',
        Boolean(contactStyle) && contactStyle.paddingTop === '0px' && contactStyle.paddingBottom === '0px',
        contactStyle ? 'top=' + contactStyle.paddingTop + ' bottom=' + contactStyle.paddingBottom : 'missing section');
      const above = panel && lastStep
        ? Math.round(panel.getBoundingClientRect().top - lastStep.getBoundingClientRect().bottom) : -1;
      check('1366px contact panel follows last process step without extra gap', above >= 0 && above <= 1,
        'above=' + above);
      const below = panel && footer
        ? Math.round(footer.getBoundingClientRect().top - panel.getBoundingClientRect().bottom) : -1;
      check('1366px contact panel sits flush with footer',
        Boolean(footerStyle) && footerStyle.marginTop === '0px' && below >= 0 && below <= 1,
        'marginTop=' + (footerStyle ? footerStyle.marginTop : 'missing') + ' below=' + below);
      const actionButtons = Array.from(doc.querySelectorAll('.contact-actions .btn'));
      const actionTops = actionButtons.map((el) => el.getBoundingClientRect().top);
      check('1366px contact actions share one row',
        actionButtons.length === 3 &&
          Math.max(...actionTops) - Math.min(...actionTops) <= 1,
        'count=' + actionButtons.length + ' tops=' + actionTops.map((top) => Math.round(top)).join(','));
      resolve(checks);
    } catch (error) {
      resolve([{name: '1366px pass runs', pass: false,
        detail: String((error && error.stack) || error)}]);
    }
  })();
})
"""

CONNECTOR_SCRIPT = r"""
new Promise((resolve) => {
  const frame = document.getElementById('frame');
  const checks = [];
  const check = (name, pass, detail) => checks.push({name, pass: Boolean(pass), detail});
  const wait = (ms) => new Promise((done) => setTimeout(done, ms));
  let label = '';
  (async () => {
    try {
      if (!(frame.contentDocument && frame.contentDocument.readyState === 'complete')) {
        await new Promise((done) => frame.addEventListener('load', done, {once: true}));
      }
      await wait(2400);
      const win = frame.contentWindow;
      const doc = win.document;
      const list = doc.getElementById('process-list');
      const fill = doc.getElementById('process-fill');
      const panel = doc.querySelector('.contact-panel');
      const initialBorder = win.getComputedStyle(panel).borderTopColor;
      win.scrollTo({top: 0, behavior: 'instant'});
      win.dispatchEvent(new win.Event('scroll'));
      await wait(80);
      const initialComplete = fill.classList.contains('is-complete');
      const initialClass = fill.className;
      fill.style.transition = 'none';
      const scrollTarget = list.getBoundingClientRect().bottom + win.scrollY -
        win.innerHeight * 0.58 + 2;
      win.scrollTo({top: scrollTarget, behavior: 'instant'});
      win.dispatchEvent(new win.Event('scroll'));
      for (let i = 0; i < 50; i += 1) {
        if (Number.parseFloat(fill.style.height) > 99.9) break;
        await wait(20);
      }

      label = win.innerWidth + 'px ';
      const progress = Number.parseFloat(fill.style.height);
      const fillRect = fill.getBoundingClientRect();
      const panelRect = panel.getBoundingClientRect();
      const after = win.getComputedStyle(fill, '::after');
      const afterHeight = Number.parseFloat(after.height);
      const afterBottom = Number.parseFloat(after.bottom);
      const exists = after.content !== 'none' && Number.isFinite(afterHeight) && Number.isFinite(afterBottom);
      const connectorBottom = fillRect.bottom - afterBottom;
      const fillStyle = win.getComputedStyle(fill);

      check(label + 'process connector class absent before rail completes', !initialComplete,
        'class=' + initialClass);
      check(label + 'process fill reaches full progress', progress > 99.9, 'height=' + fill.style.height);
      check(label + 'process connector waits for rail completion',
        fill.classList.contains('is-complete') && exists, 'class=' + fill.className);
      check(label + 'process connector exists', exists, 'content=' + after.content);
      check(label + 'process connector spans seam', exists && afterHeight === 2 && afterBottom === -1,
        'height=' + afterHeight + ' bottom=' + afterBottom);
      check(label + 'process connector lands on panel top',
        exists && Math.abs(connectorBottom - panelRect.top) <= 1.01,
        'connector=' + connectorBottom.toFixed(3) + ' panel=' + panelRect.top.toFixed(3));
      check(label + 'process connector stays inside panel width',
        fillRect.left > panelRect.left && fillRect.left < panelRect.right,
        'x=' + Math.round(fillRect.left) + ' panel=' + Math.round(panelRect.left) + '..' + Math.round(panelRect.right));
      check(label + 'process fill paints above contact panel', fillStyle.zIndex === '1', fillStyle.zIndex);
      const gradientColors = fillStyle.backgroundImage.match(/rgba?\([^)]+\)/g) || [];
      const endColor = gradientColors[gradientColors.length - 1] || '';
      check(label + 'process connector keeps terminal color',
        exists && after.backgroundImage === 'none' && after.backgroundColor === endColor,
        'seam=' + after.backgroundColor + ' gradientEnd=' + endColor + ' image=' + after.backgroundImage);
      const panelStyle = win.getComputedStyle(panel);
      const frameColors = ['Top', 'Right', 'Bottom', 'Left']
        .map((side) => panelStyle['border' + side + 'Color']);
      const cornerColors = ['::before', '::after']
        .map((pseudo) => win.getComputedStyle(panel, pseudo).borderColor);
      check(label + 'contact frame unlit before rail completes',
        initialBorder !== 'rgb(255, 61, 141)', initialBorder);
      check(label + 'contact frame turns magenta with rail',
        frameColors.every((color) => color === 'rgb(255, 61, 141)'), frameColors.join(' '));
      check(label + 'contact frame corners turn magenta with rail',
        cornerColors.every((color) => color === 'rgb(255, 61, 141)'), cornerColors.join(' '));

      resolve(checks);
    } catch (error) {
      resolve([{name: label + 'connector pass runs', pass: false,
        detail: String((error && error.stack) || error)}]);
    }
  })();
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


def page_context(client, marker):
    tree = client.send("browsingContext.getTree", {"children": True})

    def walk(contexts):
        for context in contexts:
            yield context
            yield from walk(context.get("children") or [])

    for context in walk(tree.get("contexts") or []):
        if marker in (context.get("url") or ""):
            return context["context"]
    raise RuntimeError(f"no browsing context for {marker}")


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


def run_check(firefox, url, expression, reduced, followup=None):
    """Run one or two expressions in a fresh Firefox profile and return checks."""
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
            if followup is not None:
                target = page_context(client, "index.html")
                client.send("input.performActions", {
                    "context": target,
                    "actions": [{
                        "type": "key",
                        "id": "native-escape",
                        "actions": [
                            {"type": "keyDown", "value": "\ue00c"},
                            {"type": "keyUp", "value": "\ue00c"},
                        ],
                    }],
                })
                second = evaluate(client, target, followup)
                if isinstance(result, list) and isinstance(second, list):
                    result = result + second
                elif not isinstance(result, list):
                    result = second
            errors = [
                event for event in client.events
                if event.get("method") == "log.entryAdded"
                and event.get("params", {}).get("level") == "error"
                and not (
                    "downloadable font: download failed" in str(
                        event.get("params", {}).get("text", ""))
                    and "fonts.gstatic.com" in str(event.get("params", {}).get("text", ""))
                )
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
    wide_url = f"http://127.0.0.1:{http_port}{WIDE_PATH}"

    failed = 0
    try:
        checks = []
        for check_url, expression, reduced, followup in (
            (url, NORMAL_SCRIPT_A, False, NORMAL_SCRIPT_B),
            (narrow_url, NARROW_SCRIPT, False, None),
            (url, REDUCED_SCRIPT, True, None),
            (wide_url, WIDE_SCRIPT, False, None),
            (url, CONNECTOR_SCRIPT, False, None),
            (narrow_url, CONNECTOR_SCRIPT, False, None),
            (wide_url, CONNECTOR_SCRIPT, False, None),
        ):
            result = run_check(firefox, check_url, expression, reduced, followup)
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
