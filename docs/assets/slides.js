// Scale each 1920x1080 slide to its frame, and draw <x-connector> (a Slides-runtime element browsers don't know) as SVG.
(() => {
  const frames = [...document.querySelectorAll(".frame")];
  const fit = () => frames.forEach(f => f.style.setProperty("--s", f.clientWidth / 1920));
  new ResizeObserver(fit).observe(document.querySelector(".deck"));
  fit();

  const NS = "http://www.w3.org/2000/svg";
  document.querySelectorAll("x-connector").forEach((c, i) => {
    const [x1, y1, x2, y2] = ["x1", "y1", "x2", "y2"].map(a => parseFloat(c.getAttribute(a)));
    const route = c.getAttribute("route") || "straight";
    const d = route === "hv" ? `M${x1} ${y1}H${x2}V${y2}` : route === "vh" ? `M${x1} ${y1}V${y2}H${x2}` : `M${x1} ${y1}L${x2} ${y2}`;
    const color = c.style.color || "#20252b";
    const width = parseFloat(c.style.borderWidth) || 2;
    const svg = document.createElementNS(NS, "svg");
    svg.setAttribute("class", "connector");
    svg.innerHTML = `<defs><marker id="ah${i}" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="8" markerHeight="8"
      markerUnits="userSpaceOnUse" orient="auto-start-reverse"><path d="M0 0L10 5L0 10z" fill="${color}"/></marker></defs>
      <path d="${d}" fill="none" stroke="${color}" stroke-width="${width}"/>`;
    const head = c.getAttribute("head") || "end";
    const p = svg.lastElementChild;
    if (head === "end" || head === "both") p.setAttribute("marker-end", `url(#ah${i})`);
    if (head === "both") p.setAttribute("marker-start", `url(#ah${i})`);
    c.replaceWith(svg);
  });
})();
