"""4 Oct 2026: bring the viewer side panel (plans + schedule of spaces) up to the current design, in both index.html copies."""
import os
HERE = os.path.dirname(os.path.abspath(__file__))
FILES = [os.path.join(HERE, 'index.html'), os.path.join(HERE, '..', '..', '..', 'will-os', 'equino', 'model', 'index.html')]
for p in FILES:
    h = open(p, encoding='utf-8', newline='').read(); nl = '\r\n' if '\r\n' in h else '\n'
    def rp(a, b):
        global h
        assert a in h, (p, a[:60]); h = h.replace(a, b, 1)
    # --- schedule table
    rp('<tr><td>Pasillo <span class="en">Corridor</span></td><td>12 × 64 ft</td></tr>',
       '<tr><td>Pasillo abierto de punta a punta <span class="en">Corridor, open end to end</span></td><td>12 × 88 ft</td></tr>')
    rp('<tr><td>Alfalfa bajo techo <span class="en">Alfalfa bay, under roof</span></td><td>16 × 36 ft</td></tr>',
       '<tr><td>Alfalfa, dos bodegas con reja al pasillo <span class="en">Alfalfa, two bays, pipe panel to the aisle</span></td><td>2 × (24 × 12 ft) · 576 ft²</td></tr>')
    rp('<tr><td>Bajo techo <span class="en">Under roof</span></td><td>3,024 ft²</td></tr>',
       '<tr><td>Bajo techo <span class="en">Under roof</span></td><td>3,312 ft²</td></tr>')
    rp('<tr><td>Techo mariposa, 1:12 <span class="en">Butterfly roof, 1:12</span></td><td>84 × 36 ft</td></tr>',
       '<tr><td>Techo mariposa, 1:12 <span class="en">Butterfly roof, 1:12</span></td><td>92 × 36 ft</td></tr>')
    rp('<tr><td>Captación del techo <span class="en">Roof catchment</span></td><td>≈1,900 gal/in</td></tr>',
       '<tr><td>Captación del techo <span class="en">Roof catchment</span></td><td>≈2,050 gal/in</td></tr>')
    rows = ['<tr><td>Puerta corrediza de madera del lavado <span class="en">Wash room sliding wooden door</span></td><td>7 × 9 ft · abertura 6 × 9</td></tr>',
            '<tr><td>Losa de concreto del lavado <span class="en">Wash pad, concrete</span></td><td>12 × 24 ft</td></tr>',
            '<tr><td>Bebedero de piedra en la losa <span class="en">Stone trough at the pad</span></td><td>14 × 3 ft</td></tr>',
            '<tr><td>Bebedero largo de piedra, 57 ft frente al hastial <span class="en">Long stone trough, 57 ft off the gable</span></td><td>44 × 3.5 ft</td></tr>',
            '<tr><td>Entrada bordeada de plantas nativas <span class="en">Entry drive lined with native planting</span></td><td>14 ft de ancho · 14 ft wide</td></tr>']
    anchor = '<span class="en">Wash · tack and feed, road end, solid straw-bale or cob infill</span></td><td>12 × 14 ft c/u</td></tr>'
    rp(anchor, anchor + nl + nl.join('      ' + r for r in rows))
    rp('<tr><td>Corte · relleno <span class="en">Cut · fill</span></td><td>3,185 · 2,714 yd³</td></tr>',
       '<tr><td>Corte · relleno <span class="en">Cut · fill</span></td><td>3,344 · 2,844 yd³</td></tr>')
    # --- stalls plan: corridor through, two 24 x 12 alfalfa bays, 88 ft, roof 92 x 36
    a0 = h.index("    stalls: () => {"); a1 = h.index("    stable: () => {")
    stalls = r"""    stalls: () => { const s = 2.85, ox = 40, oy = 26; let g = '';                       // 4 Oct: corridor through, two 24 x 12 alfalfa bays, 88 x 52
      const R = (x, y, w, h, f, extra = '') => `<rect x="${ox + x * s}" y="${oy + y * s}" width="${w * s}" height="${h * s}" fill="${f}" stroke="currentColor" stroke-width=".8" ${extra}/>`;
      for (let q = 0; q < 4; q++) { g += R(q * 16, 0, 16, 20, 'var(--chip)'); g += R(q * 16, 32, 16, 20, 'var(--chip)'); g += `<text x="${ox + (q * 16 + 8) * s}" y="${oy + 12 * s}" font-size="9" text-anchor="middle" fill="currentColor">${q + 5}</text><text x="${ox + (q * 16 + 8) * s}" y="${oy + 44 * s}" font-size="9" text-anchor="middle" fill="currentColor">${q + 1}</text>`; }
      g += R(64, 8, 24, 12, '#e3cf95') + R(64, 32, 24, 12, '#e3cf95');
      g += `<text x="${ox + 76 * s}" y="${oy + 14.5 * s}" font-size="8" text-anchor="middle" fill="#26241f">alfalfa 24×12</text><text x="${ox + 76 * s}" y="${oy + 38.5 * s}" font-size="8" text-anchor="middle" fill="#26241f">alfalfa 24×12</text>`;
      g += `<line x1="${ox + 64 * s}" y1="${oy + 20 * s}" x2="${ox + 88 * s}" y2="${oy + 20 * s}" stroke="var(--clay)" stroke-width="2.2"/><line x1="${ox + 64 * s}" y1="${oy + 32 * s}" x2="${ox + 88 * s}" y2="${oy + 32 * s}" stroke="var(--clay)" stroke-width="2.2"/>`;
      g += `<rect x="${ox - 2 * s}" y="${oy + 8 * s}" width="${92 * s}" height="${36 * s}" fill="none" stroke="var(--clay)" stroke-dasharray="4 3" stroke-width="1"/>`;
      g += `<text x="${ox + 32 * s}" y="${oy + 27.5 * s}" font-size="8.5" text-anchor="middle" fill="currentColor">pasillo abierto · corridor 12 ft</text>`;
      g += `<circle cx="${ox - 11 * s}" cy="${oy + 26 * s}" r="${4 * s}" fill="var(--water)" fill-opacity=".35" stroke="currentColor" stroke-width=".8"/><line x1="${ox - 9 * s}" y1="${oy + 26 * s}" x2="${ox - 2 * s}" y2="${oy + 26 * s}" stroke="var(--water)" stroke-width="2.5"/>`;
      g += `<line x1="${ox}" y1="${oy + 57 * s}" x2="${ox + 88 * s}" y2="${oy + 57 * s}" stroke="currentColor" stroke-width=".8"/><text x="${ox + 44 * s}" y="${oy + 57 * s + 11}" font-size="9" text-anchor="middle" fill="currentColor">88 ft · 4 × 16 + 24</text>`;
      g += `<text x="${ox + 89.5 * s}" y="${oy + 27.5 * s}" font-size="7.5" fill="var(--muted)">NE →</text>`;
      return `<svg viewBox="0 0 330 222" role="img" aria-label="Plano de las caballerizas techadas · Covered stalls plan" style="color:var(--ink)">${g}<text x="6" y="14" font-size="9" fill="var(--muted)">roof ▭ dashed · 92 × 36 ft · naranja = reja y puerta al pasillo</text></svg>`; },
"""
    h = h[:a0] + stalls.replace('\n', nl) + h[a1:]
    # --- stable plan: concrete pad, pad trough, wooden sliding door
    old = "      g += T(12, 94, 'patio abierto', 'var(--muted)', 6.5) + T(12, 101, 'open apron · road', 'var(--muted)', 6.5);"
    new = r"""      g += R(0, 82, 24, 12, '#d9d4cb');                                                         // 4 Oct: 12 x 24 concrete wash pad
      g += `<rect x="${ox - 3 * s}" y="${oy + 82 * s}" width="${3 * s}" height="${14 * s}" fill="var(--water)" fill-opacity=".5" stroke="currentColor" stroke-width=".8"/>`;   // 14 x 3 stone trough on the pad's west edge
      g += `<line x1="${ox + 9 * s}" y1="${oy + 82.6 * s}" x2="${ox + 16 * s}" y2="${oy + 82.6 * s}" stroke="#8a6a42" stroke-width="3"/>`;   // wooden sliding door, parked east of the wash opening
      g += T(12, 89, 'losa · pad 12×24', 'var(--muted)', 6) + T(12, 100, 'puerta corrediza · sliding door', 'var(--muted)', 5.6);"""
    rp(old, new.replace('\n', nl))
    open(p, 'w', encoding='utf-8', newline='').write(h); print(os.path.relpath(p, HERE), 'ok')
