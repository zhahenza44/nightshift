const filterButtons = document.querySelectorAll("[data-filter]");
const projectCards = document.querySelectorAll(".project-card");
const menuToggle = document.querySelector("#menu-toggle");
const mobileMenu = document.querySelector("#mobile-menu");

function applyFilter(track) {
  projectCards.forEach((card) => {
    card.hidden = track !== "all" && card.dataset.track !== track;
  });

  filterButtons.forEach((button) => {
    button.setAttribute('aria-pressed', String(button.dataset.filter === track));
  });
}

filterButtons.forEach((button) => {
  button.addEventListener("click", () => applyFilter(button.dataset.filter));
});

function setMenuOpen(isOpen) {
  menuToggle.setAttribute("aria-expanded", String(isOpen));
  menuToggle.setAttribute("aria-label", isOpen ? "Close menu" : "Open menu");
  mobileMenu.toggleAttribute("inert", !isOpen);
}

menuToggle.addEventListener("click", () => {
  const isOpen = menuToggle.getAttribute("aria-expanded") === "true";
  setMenuOpen(!isOpen);
  if (!isOpen) {
    mobileMenu.querySelector("a")?.focus();
  }
});

mobileMenu.querySelectorAll("a").forEach((link) => {
  link.addEventListener("click", () => setMenuOpen(false));
});

document.addEventListener("keydown", (event) => {
  if (event.key === 'Escape' && menuToggle.getAttribute("aria-expanded") === "true") {
    setMenuOpen(false);
    menuToggle.focus();
  }
});

const motionToggle = document.querySelector('#motion-toggle');
const motionLabel = motionToggle.querySelector('.motion-toggle-label');

function setMotionPaused(isPaused) {
  document.documentElement.classList.toggle('motion-paused', isPaused);
  motionToggle.setAttribute('aria-pressed', String(isPaused));
  const label = isPaused ? 'Resume motion' : 'Pause motion';
  motionToggle.setAttribute('aria-label', label);
  motionLabel.textContent = label;
}

motionToggle.addEventListener('click', () => {
  setMotionPaused(motionToggle.getAttribute('aria-pressed') !== 'true');
});

const reduceMotion = window.matchMedia('(prefers-reduced-motion: reduce)');
const clamp = (value, min, max) => Math.min(max, Math.max(min, value));

function resetMagnet(button) {
  button.style.setProperty('--mag-x', '0px');
  button.style.setProperty('--mag-y', '0px');
}

document.querySelectorAll('.btn').forEach((button) => {
  button.addEventListener('pointermove', (event) => {
    if (reduceMotion.matches || event.pointerType !== 'mouse') return;
    const rect = button.getBoundingClientRect();
    const x = clamp(((event.clientX - rect.left) / rect.width - 0.5) * 4, -2, 2);
    const y = clamp(((event.clientY - rect.top) / rect.height - 0.5) * 4, -2, 2);
    button.style.setProperty('--mag-x', x.toFixed(2) + 'px');
    button.style.setProperty('--mag-y', y.toFixed(2) + 'px');
  });
  ['pointerleave', 'pointercancel', 'blur'].forEach((type) => {
    button.addEventListener(type, () => resetMagnet(button));
  });
});

reduceMotion.addEventListener('change', () => {
  if (reduceMotion.matches) document.querySelectorAll('.btn').forEach(resetMagnet);
});

const progressBar = document.querySelector('#scroll-progress-bar');

function updateProgress() {
  const max = document.documentElement.scrollHeight - window.innerHeight;
  const ratio = max > 0 ? Math.min(1, Math.max(0, window.scrollY / max)) : 0;
  progressBar.style.width = (ratio * 100).toFixed(2) + '%';
}

updateProgress();
window.addEventListener('scroll', updateProgress, {passive: true});
window.addEventListener('resize', updateProgress);

const projectGrid = document.querySelector('#project-grid');
if (projectGrid && 'IntersectionObserver' in window) {
  projectGrid.classList.add('reveal-pending');
  const revealObserver = new IntersectionObserver((entries, observer) => {
    entries.forEach((entry) => {
      if (!entry.isIntersecting) return;
      projectGrid.classList.add('is-revealed');
      observer.disconnect();
    });
  }, {threshold: 0.12});
  revealObserver.observe(projectGrid);
}
