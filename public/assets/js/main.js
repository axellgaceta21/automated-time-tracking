/* Accessible report tabs and section-aware navigation. No runtime dependencies. */
(() => {
  const tabs = [...document.querySelectorAll('[role="tab"]')];
  function activate(tab, focus = false) {
    tabs.forEach(item => {
      const selected = item === tab;
      item.setAttribute('aria-selected', String(selected));
      item.tabIndex = selected ? 0 : -1;
      document.getElementById(item.getAttribute('aria-controls')).hidden = !selected;
    });
    if (focus) tab.focus();
  }
  tabs.forEach((tab, index) => {
    tab.addEventListener('click', () => activate(tab));
    tab.addEventListener('keydown', event => {
      let next;
      if (event.key === 'ArrowRight') next = (index + 1) % tabs.length;
      if (event.key === 'ArrowLeft') next = (index - 1 + tabs.length) % tabs.length;
      if (event.key === 'Home') next = 0;
      if (event.key === 'End') next = tabs.length - 1;
      if (next !== undefined) { event.preventDefault(); activate(tabs[next], true); }
    });
  });
  document.querySelector('[data-open-dashboard]').addEventListener('click', event => {
    event.preventDefault();
    activate(document.getElementById('tab-dashboard'));
    document.getElementById('tab-dashboard').scrollIntoView({ block: 'center' });
    document.getElementById('tab-dashboard').focus({ preventScroll: true });
  });
  const links = [...document.querySelectorAll('.site-header nav a')];
  const sections = links.map(link => document.querySelector(link.getAttribute('href')));
  let scheduled = false;
  function update() {
    const offset = document.querySelector('.site-header').offsetHeight + 100;
    let active = sections[0];
    sections.forEach(section => { if (section.getBoundingClientRect().top <= offset) active = section; });
    if (window.innerHeight + window.scrollY >= document.documentElement.scrollHeight - 5) active = sections.at(-1);
    links.forEach(link => {
      if (link.hash === `#${active.id}`) link.setAttribute('aria-current', 'location');
      else link.removeAttribute('aria-current');
    });
    scheduled = false;
  }
  window.addEventListener('scroll', () => { if (!scheduled) { scheduled = true; requestAnimationFrame(update); } }, { passive: true });
  window.addEventListener('resize', update);
  update();
})();
