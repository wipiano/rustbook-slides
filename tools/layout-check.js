// In-page layout check: paste into a chapter page's console (or evaluate it with Playwright).
// Returns slides whose flow content runs into the footer band or past the canvas, and code lines wider than their box.
// Measured in canvas px (1920x1080), independent of the frame's scale.
() => {
  const issues = [];
  document.querySelectorAll(".frame").forEach(frame => {
    const sec = frame.querySelector("section");
    const s = parseFloat(getComputedStyle(frame).getPropertyValue("--s"));
    const top = sec.getBoundingClientRect().top, left = sec.getBoundingClientRect().left;
    const pinned = el => { for (let e = el; e && e !== sec; e = e.parentElement) if (getComputedStyle(e).position === "absolute") return true; return false; };
    let maxBottom = 0;
    sec.querySelectorAll("p, li, h1, h2, h3, table, img, svg").forEach(el => {
      if (pinned(el)) return;
      const r = el.getBoundingClientRect();
      maxBottom = Math.max(maxBottom, (r.bottom - top) / s);
      if ((r.right - left) / s > 1920 - 100) issues.push(`${frame.id}: ${el.tagName} reaches x=${Math.round((r.right - left) / s)}`);
    });
    // The footer band starts at y≈990 (pinned at bottom:48 with a 24px line); 944 is the end of the body padding.
    if (maxBottom > 990) issues.push(`${frame.id}: content bottom y=${Math.round(maxBottom)} overlaps footer`);
    sec.querySelectorAll('p[style*="nowrap"]').forEach(p => {
      if (p.scrollWidth > p.clientWidth + 1) issues.push(`${frame.id}: code line wider than box by ${Math.round(p.scrollWidth - p.clientWidth)}px: ${p.textContent.slice(0, 40)}`);
    });
  });
  return issues;
}
