/* Full-resolution viewer. Actual-size mode always starts at the top-left. */
(() => {
  const dialog = document.getElementById('image-viewer');
  const viewport = dialog.querySelector('.viewer-viewport');
  const canvas = dialog.querySelector('.viewer-canvas');
  const img = document.getElementById('viewer-image');
  const output = document.getElementById('zoom-level');
  const close = document.getElementById('viewer-close');
  let scale = 1, fitMode = false, trigger, drag, pinch;

  function render(value, fit = false, reset = false) {
    if (!img.naturalWidth) return;
    const old = scale;
    const centerX = (viewport.scrollLeft + viewport.clientWidth / 2) / old;
    const centerY = (viewport.scrollTop + viewport.clientHeight / 2) / old;
    scale = Math.max(.05, Math.min(5, value));
    fitMode = fit;
    canvas.classList.toggle('fit', fit);
    img.style.width = `${img.naturalWidth * scale}px`;
    img.style.height = `${img.naturalHeight * scale}px`;
    output.value = `${Math.round(scale * 100)}%`;
    if (reset || fit) { viewport.scrollLeft = 0; viewport.scrollTop = 0; }
    else { viewport.scrollLeft = centerX * scale - viewport.clientWidth / 2; viewport.scrollTop = centerY * scale - viewport.clientHeight / 2; }
  }
  function fit() {
    render(Math.min(1, (viewport.clientWidth - 24) / img.naturalWidth, (viewport.clientHeight - 24) / img.naturalHeight), true, true);
  }
  function actual() { render(1, false, true); }
  function action(name) {
    if (name === 'in') render(scale * 1.25);
    if (name === 'out') render(scale / 1.25);
    if (name === 'actual') actual();
    if (name === 'fit') fit();
  }
  document.addEventListener('click', event => {
    const button = event.target.closest('[data-image]');
    if (!button) return;
    trigger = button;
    document.getElementById('viewer-title').textContent = button.dataset.title;
    img.alt = button.dataset.title;
    img.removeAttribute('style');
    img.onload = () => { actual(); viewport.focus({ preventScroll: true }); };
    img.src = button.dataset.image;
    dialog.showModal();
    document.body.classList.add('modal-open');
    close.focus();
    if (img.complete && img.naturalWidth) actual();
  });
  dialog.querySelectorAll('[data-action]').forEach(button => button.addEventListener('click', () => action(button.dataset.action)));
  close.addEventListener('click', () => dialog.close());
  dialog.addEventListener('close', () => {
    document.body.classList.remove('modal-open');
    drag = pinch = undefined;
    viewport.classList.remove('dragging');
    trigger?.focus({ preventScroll: true });
  });
  dialog.addEventListener('keydown', event => {
    if (event.ctrlKey || event.metaKey || event.altKey) return;
    const names = { '+': 'in', '=': 'in', '-': 'out', '0': 'actual', f: 'fit', F: 'fit' };
    if (names[event.key]) { event.preventDefault(); action(names[event.key]); }
    // Native modal dialog contains focus; wrap explicitly for consistent browsers.
    if (event.key === 'Tab') {
      const targets = [...dialog.querySelectorAll('button, [tabindex="0"]')];
      if (event.shiftKey && document.activeElement === targets[0]) { event.preventDefault(); targets.at(-1).focus(); }
      else if (!event.shiftKey && document.activeElement === targets.at(-1)) { event.preventDefault(); targets[0].focus(); }
    }
  });
  viewport.addEventListener('wheel', event => {
    if (event.ctrlKey || event.metaKey) {
      event.preventDefault(); render(scale * (event.deltaY < 0 ? 1.1 : 1 / 1.1));
    }
  }, { passive: false });
  viewport.addEventListener('pointerdown', event => {
    if (event.pointerType !== 'mouse' || event.button !== 0) return;
    drag = { x: event.clientX, y: event.clientY, left: viewport.scrollLeft, top: viewport.scrollTop };
    viewport.setPointerCapture(event.pointerId);
    viewport.classList.add('dragging');
  });
  viewport.addEventListener('pointermove', event => {
    if (!drag) return;
    viewport.scrollLeft = drag.left - (event.clientX - drag.x);
    viewport.scrollTop = drag.top - (event.clientY - drag.y);
  });
  const stopDrag = () => { drag = undefined; viewport.classList.remove('dragging'); };
  viewport.addEventListener('pointerup', stopDrag);
  viewport.addEventListener('pointercancel', stopDrag);
  const distance = touches => Math.hypot(touches[0].clientX - touches[1].clientX, touches[0].clientY - touches[1].clientY);
  viewport.addEventListener('touchstart', event => { if (event.touches.length === 2) pinch = { distance: distance(event.touches), scale }; }, { passive: true });
  viewport.addEventListener('touchmove', event => {
    if (pinch && event.touches.length === 2) { event.preventDefault(); render(pinch.scale * distance(event.touches) / pinch.distance); }
  }, { passive: false });
  viewport.addEventListener('touchend', () => { pinch = undefined; });
  window.addEventListener('resize', () => { if (dialog.open && fitMode) fit(); });
})();
