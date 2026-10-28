# Builds index.html in METR's visual language. Canvas 1600x900, rendered at 80% (1280x720).
import yaml, numpy as np

GREEN, GREEN_L, GREY_DOT = "#2e7d32", "#a5c8a7", "#9e9e9e"
SLATE, INK, BODY, MUTED, BAND, RULE = "#222a34", "#222a34", "#4d5561", "#8a929c", "#f6f7f8", "#e6e8eb"
WGREY = "#b42318"   # weakness red

# ---------------- data ----------------
d = yaml.safe_load(open("benchmark_results_1_1.yaml"))["results"]
def yr(D): return D.year + (D.timetuple().tm_yday - 1) / 365.25
pts = sorted((yr(v["release_date"]), v["metrics"]["p50_horizon_length"]["estimate"], k)
             for k, v in d.items() if v["metrics"]["is_sota"])
fit = [p for p in pts if p[1] < 960]                       # METR excludes > 16 h
fx = np.array([p[0] for p in fit]); fy = np.log2([p[1] for p in fit])
b, a = np.polyfit(fx, fy, 1)
assert abs(365.25 / b - 187.78) < 0.1                       # reproduces METR's 188 days
m = fx >= 2024
b2, a2 = np.polyfit(fx[m], fy[m], 1)
DAYS_ALL, DAYS_NEW = 365.25 / b, 365.25 / b2

# ---------------- overlay on metr_chart.png (3420 x 1585 px) ----------------
IW, IH = 3420, 1585
K = 1.71
def ix(t): return (429 + 219 * (t - 2020)) * K
def iy_min(mins): return (363 - 142 * np.log10(mins / 60)) * K
def ours(t): return iy_min(2 ** (a2 + b2 * t))
def metr(x): return 1440 - (x - 509) * 993 / 2597          # METR dashed line, measured

SW = 4.5                                                     # ~1.2 css px at this scale
t0, t1, ws = 2024.36, 2026.35, 2025.25
ov = []
# W2: highlight METR's own straight trend line (no refit drawn)
hx0, hx1 = ix(2022.9), ix(2026.3)
ov.append(f'<line x1="{hx0:.0f}" y1="{metr(hx0):.0f}" x2="{hx1:.0f}" y2="{metr(hx1):.0f}" stroke="{WGREY}" stroke-width="20" stroke-linecap="round" opacity="0.13"/>')
def S(x): ov.append(x.replace("STROKE_S", f'stroke="{GREEN}" stroke-width="{SW}"').replace("STROKE_W", f'stroke="{WGREY}" stroke-width="{SW}"'))
S('<rect x="150" y="290" width="196" height="1092" rx="14" fill="none" STROKE_S/>')               # S1 tick column
S('<line x1="393" y1="668" x2="706" y2="668" STROKE_S stroke-linecap="round"/>')                   # S2 underline
S('<rect x="362" y="182" width="2808" height="144" rx="4" fill="none" STROKE_S/>')                 # S3 hatch band
S('<rect x="3002" y="176" width="26" height="280" rx="13" fill="none" STROKE_W/>')                 # W1 whisker
S('<line x1="1958" y1="172" x2="2482" y2="172" STROKE_W stroke-linecap="round"/>')                 # W3 "50%"
S('<ellipse cx="2313" cy="913" rx="74" ry="50" fill="none" STROKE_W/>')                             # W4 light dots
wy = (ours(t1) + metr(ix(t1))) / 2
# tags: fixed size; every connector ends at the middle of the tag side it touches
KU = IW / 800                                   # image px per layout unit (chart drawn 800 units wide)
HW, HH = 28 * KU / 2, 19 * KU / 2               # tag half width / half height in image px
TAGS = [("S1", "s", 248, 290 - 34 - HH), ("S2", "s", 706 + HW, 668), ("S3", "s", 2330, 254),
        ("W1", "w", 3002 - 90 - HW, 248), ("W2", "w", 3165, 690), ("W3", "w", 2482 + HW, 172),
        ("W4", "w", 2313, 963 + 40 + HH)]
T = {t: (x, y) for t, _, x, y in TAGS}
CONN = [  # (tag, side, target x, target y)
    ("S1", "bottom", 248, 290),
    ("W1", "right", 3002, 248),
    ("W2", "top", hx1 + 2, metr(hx1) + 12),
    ("W4", "top", 2313, 963),
]
def side(tag, sd):
    x, y = T[tag]
    return {"top": (x, y - HH), "bottom": (x, y + HH), "left": (x - HW, y), "right": (x + HW, y)}[sd]
for tag, sd, tx, ty in CONN:
    sx, sy = side(tag, sd)
    c = GREEN if tag[0] == "S" else WGREY
    ov.append(f'<line x1="{sx:.0f}" y1="{sy:.0f}" x2="{tx:.0f}" y2="{ty:.0f}" stroke="{c}" stroke-width="{SW}"/>')
overlay = "\n".join(ov)

tags = "".join(f'<span class="tg {k} ch" style="left:{x / IW * 100:.3f}%;top:{y / IH * 100:.3f}%">{t}</span>' for t, k, x, y in TAGS)
oursnote = (f'<div class="anno" style="left:{2600 / IW * 100:.2f}%;top:{1010 / IH * 100:.2f}%">'
            f'<svg width="30" height="8"><line x1="2" y1="4" x2="28" y2="4" stroke="{SLATE}" stroke-width="2.2" stroke-dasharray="1 4" stroke-linecap="round"/></svg>'
            f'our refit, 2024 on</div>')

# ---------------- reanalysis: zoom on 2023.7-2026.5 with both fits ----------------
W, H = 636, 176
L, R, T, B = 64, 470, 14, 150
X0, X1 = 2023.7, 2026.5
X = lambda t: L + (t - X0) / (X1 - X0) * (R - L)
LO, HI = np.log10(2.2), np.log10(2600)
Y = lambda mins: B - (np.log10(mins) - LO) / (HI - LO) * (B - T)
fitY = lambda a_, b_, t: Y(2 ** (a_ + b_ * t))
ci = {k: v["metrics"]["p50_horizon_length"] for k, v in d.items()}
s = [f'<svg viewBox="0 0 {W} {H}" width="{W}" height="{H}" class="plot">',
     f'<defs><clipPath id="pc"><rect x="{L}" y="{T}" width="{R - L}" height="{B - T}"/></clipPath></defs>']
for mins, lab in [(6, "6 min"), (60, "1 hour"), (960, "16 hours")]:
    s.append(f'<line x1="{L}" x2="{R}" y1="{Y(mins):.1f}" y2="{Y(mins):.1f}" stroke="#f0f1f3"/>')
    s.append(f'<text x="{L - 8}" y="{Y(mins) + 3.5:.1f}" text-anchor="end" class="tk">{lab}</text>')
for t in (2024, 2025, 2026):
    s.append(f'<text x="{X(t):.1f}" y="{B + 16}" text-anchor="middle" class="tk">{t}</text>')
s.append(f'<line x1="{L}" x2="{R}" y1="{B}" y2="{B}" stroke="{BODY}" stroke-width="0.8"/>')
s.append(f'<g clip-path="url(#pc)">')
ws_ = 2025.25
s.append(f'<polygon points="{X(ws_):.1f},{fitY(a2, b2, ws_):.1f} {X(X1):.1f},{fitY(a2, b2, X1):.1f} {X(X1):.1f},{fitY(a, b, X1):.1f} {X(ws_):.1f},{fitY(a, b, ws_):.1f}" fill="{SLATE}" opacity="0.07"/>')
s.append(f'<line x1="{X(X0):.1f}" y1="{fitY(a, b, X0):.1f}" x2="{X(X1):.1f}" y2="{fitY(a, b, X1):.1f}" stroke="{GREEN}" stroke-width="1.8" stroke-dasharray="5,5"/>')
s.append(f'<line x1="{X(2024.36):.1f}" y1="{fitY(a2, b2, 2024.36):.1f}" x2="{X(X1):.1f}" y2="{fitY(a2, b2, X1):.1f}" stroke="{SLATE}" stroke-width="2.2" stroke-dasharray="1 4.5" stroke-linecap="round"/>')
zp = [p for p in pts if p[0] >= X0]
for t, h, k in zp:
    s.append(f'<line x1="{X(t):.1f}" x2="{X(t):.1f}" y1="{Y(ci[k]["ci_low"]):.1f}" y2="{Y(ci[k]["ci_high"]):.1f}" stroke="{GREEN_L}" stroke-width="1.2" opacity="0.7"/>')
for t, h, k in zp:
    s.append(f'<circle cx="{X(t):.1f}" cy="{Y(h):.1f}" r="5" fill="{GREY_DOT if h >= 960 else GREEN}" stroke="#fff" stroke-width="1.2"/>')
s.append('</g>')
for k, lab, dx, dy, an in [("gpt_4o_inspect", "GPT-4o", 0, 17, "middle"), ("o3_inspect", "o3", -9, 0, "end"),
                           ("claude_opus_4_6_inspect", "Opus 4.6", -9, 2, "end")]:
    t, h, _ = next(p for p in pts if p[2] == k)
    s.append(f'<text x="{X(t) + dx:.1f}" y="{Y(h) + dy:.1f}" text-anchor="{an}" class="lb">{lab}</text>')
yo, ym_ = fitY(a2, b2, X1), fitY(a, b, X1)
s.append(f'<text x="{R + 12}" y="{yo + 2:.1f}" class="el" fill="{SLATE}">Our fit, 2024 on</text>')
s.append(f'<text x="{R + 12}" y="{yo + 16:.1f}" class="es">doubles every {DAYS_NEW:.0f} days</text>')
ym_ = max(ym_ + 4, yo + 36)
s.append(f'<text x="{R + 12}" y="{ym_:.1f}" class="el" fill="{GREEN}">METR’s trend</text>')
s.append(f'<text x="{R + 12}" y="{ym_ + 14:.1f}" class="es">doubles every {DAYS_ALL:.0f} days</text>')
s.append("</svg>")
resid = "\n".join(s)

# ---------------- legend glyphs ----------------
def g(svg): return f'<svg class="gl" viewBox="0 0 30 18" width="28" height="17">{svg}</svg>'
HATCH = ('<defs><pattern id="h{n}" width="4" height="4" patternUnits="userSpaceOnUse" patternTransform="rotate(45)">'
         '<line x1="0" y1="0" x2="0" y2="4" stroke="#b9b9b9" stroke-width="1.4"/></pattern></defs>')
GL = {
 "point": g(f'<circle cx="15" cy="9" r="5" fill="{GREEN}"/>'),
 "whisker": g(f'<line x1="15" y1="2" x2="15" y2="16" stroke="{GREEN_L}" stroke-width="1.6"/><line x1="11" y1="2" x2="19" y2="2" stroke="{GREEN_L}" stroke-width="1.6"/><line x1="11" y1="16" x2="19" y2="16" stroke="{GREEN_L}" stroke-width="1.6"/>'),
 "dash": g(f'<line x1="2" y1="9" x2="28" y2="9" stroke="{GREEN}" stroke-width="2" stroke-dasharray="4 3"/>'),
 "hatch": g(HATCH.format(n=1) + '<rect x="2" y="2" width="26" height="14" fill="url(#h1)" stroke="#cfcfcf"/>'),
 "text": g(f'<text x="15" y="13.5" text-anchor="middle" font-size="12" font-weight="600" fill="{INK}">Aa</text>'),
 "x": g(f'<line x1="3" y1="13" x2="26" y2="13" stroke="{INK}" stroke-width="1.5"/><path d="M22 9.5 L27 13 L22 16.5" fill="none" stroke="{INK}" stroke-width="1.5"/>'),
 "y": g(f'<line x1="15" y1="16" x2="15" y2="2.5" stroke="{INK}" stroke-width="1.5"/><path d="M11.5 6 L15 1.5 L18.5 6" fill="none" stroke="{INK}" stroke-width="1.5"/>'),
 "len": g(f'<line x1="10" y1="12" x2="10" y2="16" stroke="{GREEN_L}" stroke-width="2"/><line x1="20" y1="2" x2="20" y2="16" stroke="{GREEN_L}" stroke-width="2"/>'),
 "lum": g(f'<circle cx="9" cy="9" r="5" fill="{GREEN}"/><circle cx="21" cy="9" r="5" fill="{GREEN_L}"/>'),
 "grey": g(HATCH.format(n=2) + f'<rect x="2" y="3" width="13" height="12" fill="url(#h2)" stroke="#cfcfcf"/><circle cx="22" cy="9" r="5" fill="{GREY_DOT}"/>'),
}
MARKS = [("point", "Point", "one AI model (26 in all)"), ("whisker", "Vertical line", "95% bootstrap CI"),
         ("dash", "Dashed line", "METR’s exponential fit"), ("hatch", "Hatched area", "above 16 h"),
         ("text", "Text", "model and task names")]
CHANS = [("x", "x position", "release date", "Q interval"), ("y", "y position, log", "50% horizon (human min)", "Q ratio"),
         ("len", "Whisker length", "width of the CI", "Q ratio"), ("lum", "Luminance", "frontier at release or not", "N"),
         ("grey", "Gray hue, texture", "beyond the 16 h ceiling", "N")]
marks_rows = "".join(f'<div class="lr m">{GL[k]}<span class="ln">{n}</span><span class="lm">{x}</span></div>' for k, n, x in MARKS)
chan_rows = "".join(f'<div class="lr c">{GL[k]}<span class="ln">{n}</span><span class="lm">{x}</span><span class="ty">{t}</span></div>' for k, n, x, t in CHANS)

# ---------------- critique copy ----------------
def item(code, kind, head, body):
    return f'<div class="it"><span class="tg in {kind}">{code}</span><div><h4>{head}</h4><p>{body}</p></div></div>'
STR = "".join([
 item("S1", "s", "Log scale makes doubling a straight line",
      "Steady growth reads as a steady slope, through position on a common scale, the most accurate channel (L4). Ratios also fit Weber’s law (L4)."),
 item("S2", "s", "Example tasks give the axis meaning",
      "“Train classifier” at about an hour turns minutes into kinds of work, a conceptual unit (data models, L2)."),
 item("S3", "s", "It marks where its data stops",
      "Hatching and the gray Mythos dot pop out preattentively (L4), so the chart claims nothing its tasks cannot measure (expressiveness, L2)."),
])
WEAK = "".join([
 item("W1", "w", "Uncertainty is drawn at 20% opacity",
      "Opus 4.6 reads as 12 h, yet its 95% CI spans 5 to 61 h. Faint whiskers sink into the ground (L5). <b>Fix:</b> solid CI bars."),
 item("W2", "w", "One straight line hides a bend",
      "Every frontier model since o3 sits above METR’s line. Continuity (L5) reads it as one pace. <b>Fix:</b> add the recent fit."),
 item("W3", "w", "“50%” carries the headline",
      "At 80% success Opus 4.6 drops from 12 h to 70 min, yet the threshold sits only in the title and a rotated label (L4). <b>Fix:</b> plot both."),
 item("W4", "w", "Light and split dots go unexplained",
      "No key for light green, 10 of 26 models named, two models share one split dot (expressiveness, L2). <b>Fix:</b> key and jitter."),
])

split_items = lambda h: ['<div class="it">' + x for x in h.split('<div class="it">') if x]
_S, _W = split_items(STR), split_items(WEAK)
ROWS = ''.join((_S[i] if i < len(_S) else '<div></div>') + _W[i] for i in range(len(_W)))
M, GAP, PAD = 48, 32, 16        # outer margin, gutter, chart padding
CX, CY, CWID = M + PAD, 158 + GAP + PAD, 800
TX = M + CWID + 2 * PAD + GAP  # left edge of the right-hand column
TW = 1600 - M - TX
CHT = CWID * IH / IW
BOT = CY - PAD + CHT + 46 + GAP            # top of the two small panels
MARKS_INLINE = "".join(f'<div class="cr m">{GL[k]}<span class="ln">{n}</span><span class="lm">{x}</span></div>' for k, n, x in MARKS)
CHAN_ROWS = "".join(f'<div class="cr">{GL[k]}<span class="ln">{n}</span><span class="lm">{x}</span><span class="ty">{t}</span></div>' for k, n, x, t in CHANS)

html = f"""<!doctype html>
<html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>METR Time Horizon Critique</title>
<link href="https://fonts.googleapis.com/css2?family=Instrument+Sans:wght@400;500;600;700&family=Montserrat:ital,wght@0,400;0,500;0,600;1,400&display=swap" rel="stylesheet">
<style>
@page {{ size:1280px 720px; margin:0; }}
* {{ box-sizing:border-box; }}
html,body {{ margin:0; background:#fff; }}
@media screen {{ body {{ margin:0 auto; }} }}
body {{ width:1280px; height:720px; overflow:hidden; color:{BODY};
        font-family:"Instrument Sans",-apple-system,"Helvetica Neue",Arial,sans-serif;
        -webkit-print-color-adjust:exact; print-color-adjust:exact; }}
.page {{ position:relative; width:1600px; height:900px; zoom:0.8; }}

.hero {{ position:absolute; left:0; top:0; width:1600px; background:{BAND}; text-align:center; padding:20px 0 20px; }}
h1 {{ margin:0; font-size:30px; font-weight:400; color:{INK}; letter-spacing:-0.3px; line-height:1.15; }}
.authors {{ margin-top:8px; font-size:15px; color:{INK}; }}
.authors span {{ margin:0 10px; }}
.affil {{ margin-top:3px; font-size:12.5px; color:{MUTED}; }}
.btns {{ margin-top:10px; display:flex; justify-content:center; gap:8px; }}
.btn {{ display:inline-flex; align-items:center; gap:6px; height:27px; padding:0 13px; border-radius:14px; background:{SLATE}; color:#fff;
        font-size:12.5px; font-weight:500; text-decoration:none; }}
.btn svg {{ width:13px; height:13px; }}

.fig {{ position:absolute; left:{CX}px; top:{CY}px; width:{CWID}px; height:{CHT:.0f}px; container-type:inline-size; }}
.fig img {{ width:100%; height:100%; display:block; mix-blend-mode:multiply; }}
.chbg {{ position:absolute; background:#f4f5f7; border-radius:10px; }}
.re svg {{ background:#f4f5f7; border-radius:10px; }}
.fig svg.ov {{ position:absolute; inset:0; width:100%; height:100%; }}
.anno {{ position:absolute; font:italic 400 12px Montserrat,sans-serif; color:{SLATE}; display:flex; align-items:center; gap:6px;
         background:rgba(255,255,255,0.92); padding:1px 4px; }}
.cap {{ position:absolute; left:{CX}px; top:{CY + CHT + 6:.0f}px; width:{CWID}px; text-align:center;
        font:italic 400 11.5px Montserrat,sans-serif; color:{MUTED}; }}
.cap .k {{ font-style:normal; display:inline-flex; align-items:center; gap:5px; margin-left:12px; }}
.cap .tg.in {{ display:inline-block; height:15px; line-height:15px; font-size:9px; padding:0 4px; }}

.tg {{ position:absolute; transform:translate(-50%,-50%); height:19px; padding:0 6px; border-radius:4px;
       font:600 10.5px/19px Montserrat,sans-serif; color:#fff; letter-spacing:0.2px; box-shadow:0 0 0 2.5px #f4f5f7; }}
.tg.ch {{ width:3.5cqw; height:2.375cqw; line-height:2.375cqw; font-size:1.3125cqw; padding:0; text-align:center; border-radius:0.5cqw; box-shadow:0 0 0 0.3cqw #f4f5f7; }}
.tg.s {{ background:{GREEN}; }} .tg.w {{ background:{WGREY}; }}
.tg.in {{ position:static; transform:none; box-shadow:none; justify-self:start; width:26px; padding:0; text-align:center; }}

.text {{ position:absolute; left:{TX}px; top:{CY - PAD}px; width:{TW}px; display:grid; grid-template-columns:1fr 1fr; column-gap:32px; row-gap:18px; align-items:start; }}
.text .sh2 {{ margin:0 0 -2px; }}
.text .it {{ margin-bottom:0; }}
.sh2 {{ font-size:18px; font-weight:500; margin:0 0 14px; line-height:1.2; text-align:center; }}
.sh2.s {{ color:{GREEN}; }} .sh2.w {{ color:{WGREY}; }}
.it {{ display:grid; grid-template-columns:34px 1fr; margin-bottom:14px; }}
.it h4 {{ margin:0 0 3px; font-size:14px; line-height:1.3; font-weight:600; color:{INK}; }}
.it p {{ margin:0; font-size:12.6px; line-height:1.45; }}
.it p b {{ color:{INK}; font-weight:600; }}

.panel {{ position:absolute; top:{BOT:.0f}px; width:460px; }}
.panel h3 {{ margin:0 0 8px; font-size:18px; font-weight:500; color:{INK}; line-height:1.2; text-align:center; }}
.panel .lead {{ font-size:12.6px; line-height:1.45; margin:0 0 4px; text-align:center; }}
.panel .lead b {{ color:{INK}; font-weight:600; }}
.mc {{ left:{M}px; width:{CWID + 2 * PAD}px; }} .re {{ left:{TX}px; width:{TW}px; }}
.re svg {{ display:block; margin:0 auto; }}
.plot .tk {{ font:400 10.5px Montserrat,sans-serif; fill:{BODY}; }}
.plot .lb {{ font:500 10.5px Montserrat,sans-serif; fill:{INK}; }}
.plot .el {{ font:500 11px Montserrat,sans-serif; }}
.plot .es {{ font:italic 400 10.5px Montserrat,sans-serif; fill:{MUTED}; }}
.mis {{ display:grid; grid-template-columns:repeat(3, auto); justify-content:start; gap:6px 34px; font-size:12.6px; margin:4px 0 14px; }}
.mi {{ display:inline-flex; align-items:center; gap:5px; }}
.mi b {{ color:{INK}; font-weight:600; }}
.mcg {{ margin-top:29px; display:grid; grid-template-columns:300px 420px; column-gap:44px; justify-content:center; }}
.cr {{ display:grid; grid-template-columns:32px 128px 1fr 74px; align-items:center; height:35px; font-size:12.6px; }}
.cr.m {{ grid-template-columns:32px 106px 1fr; }}
.cr .ty {{ justify-self:end; }}
.ln {{ font-weight:600; color:{INK}; }}
.ty {{ font:500 10.5px Montserrat,sans-serif; color:{BODY}; border:1px solid #d5d9de; border-radius:10px; padding:1px 8px; white-space:nowrap; }}
.gl {{ display:block; flex:none; }}
.lbl {{ font-size:10.5px; font-weight:600; letter-spacing:1.1px; text-transform:uppercase; color:{MUTED}; margin:0 0 4px; }}

/* ---------------- responsive: below 1100px the slide becomes a single flowing column ---------------- */
@media screen and (max-width: 1099px) {{
  html, body {{ background:#fff !important; }}
  body {{ width:auto; height:auto; overflow:visible; zoom:1 !important; box-shadow:none; }}
  .page {{ zoom:1; width:auto; height:auto; display:flex; flex-direction:column; padding:0 0 40px; }}
  .page > * {{ position:static !important; left:auto !important; top:auto !important; width:auto !important; height:auto !important; }}
  .chbg {{ display:none; }}
  .hero {{ order:0; padding:28px 20px 24px; }}
  h1 {{ font-size:clamp(22px, 5.4vw, 30px); line-height:1.2; }}
  .authors span {{ display:inline-block; margin:2px 8px; }}
  .affil {{ padding:0 8px; }}
  .btns {{ flex-wrap:wrap; }}
  .page > .fig {{ position:relative !important; }}
  .fig {{ order:1; margin:24px 16px 0; aspect-ratio:3420 / 1585; background:#f4f5f7; border-radius:10px; }}
  .fig img {{ mix-blend-mode:multiply; }}
  .cap {{ order:2; margin:10px 20px 0; line-height:1.9; }}
  .text {{ order:3; margin:32px 20px 0; display:flex !important; flex-direction:column; gap:16px; }}
  .text > div:not(.it):not(.sh2) {{ display:none; }}
  .text .sh2 {{ text-align:left; margin:0; font-size:21px; }}
  .text .sh2.s {{ order:0; }}
  .text .it:has(.tg.s) {{ order:1; }}
  .text .sh2.w {{ order:2; margin-top:18px; }}
  .text .it:has(.tg.w) {{ order:3; }}
  .it h4 {{ font-size:16px; }}
  .it p {{ font-size:15px; line-height:1.55; }}
  .panel.mc {{ order:4; margin:44px 20px 0; }}
  .panel.re {{ order:5; margin:44px 16px 0; }}
  .panel h3 {{ font-size:21px; text-align:left; padding:0 4px; }}
  .panel .lead {{ text-align:left; font-size:15px; padding:0 4px; margin-bottom:12px; }}
  .re svg {{ width:100%; height:auto; }}
  .mcg {{ margin-top:8px !important; grid-template-columns:1fr !important; row-gap:18px; }}
  .cr, .cr.m {{ grid-template-columns:32px minmax(110px, 34%) 1fr auto !important; height:auto !important; min-height:36px; font-size:14px; }}
}}
@media screen and (max-width: 560px) {{
  .cr, .cr.m {{ grid-template-columns:28px 1fr auto !important; row-gap:0; padding:6px 0; }}
  .cr .lm {{ grid-column:2 / 4; grid-row:2; color:{MUTED}; font-size:13px; }}
  .cr .ty {{ grid-column:3; grid-row:1; }}
  .cap .k {{ margin-left:8px; }}
}}
</style>
<script>
function fit() {{ if (matchMedia('print').matches) return;
  if (innerWidth < 1100) {{ document.body.style.zoom = ''; document.documentElement.style.background = '#fff'; return; }}
  const f = Math.min(innerWidth / 1280, innerHeight / 720);
  document.body.style.zoom = f;
  const h = document.querySelector('.hero').getBoundingClientRect().height * f;
  document.documentElement.style.background = `#fff linear-gradient(#f6f7f8, #f6f7f8) no-repeat top / 100% ${{h}}px`;
  document.documentElement.style.minHeight = '100vh'; }}
addEventListener('resize', fit); addEventListener('DOMContentLoaded', fit);
</script>
</head>
<body><div class="page">

<div class="hero">
  <h1>METR’s Time Horizon Chart Is Easy to Read, and Easy to Overread</h1>
  <div class="authors"><span>Valmik Nahata</span><span>Varun Sinha</span><span>Rishab Kolan</span><span>Rishil Chintalapati</span></div>
  <div class="affil">UC San Diego, DSC 106 Project 2.5 &nbsp;·&nbsp; {{vnahata, v1sinha, rkolan, rchintalapati}}@ucsd.edu</div>
  <div class="btns">
    <a class="btn" href="https://metr.org/time-horizons/"><svg viewBox="0 0 16 16"><path d="M2 13 L6 8 L9 10 L14 3" fill="none" stroke="#fff" stroke-width="1.8"/></svg>Original chart</a>
    <a class="btn" href="https://metr.org/assets/benchmark_results_1_1.yaml"><svg viewBox="0 0 16 16"><ellipse cx="8" cy="4" rx="5.5" ry="2" fill="none" stroke="#fff" stroke-width="1.5"/><path d="M2.5 4 V12 C2.5 13 5 14 8 14 C11 14 13.5 13 13.5 12 V4" fill="none" stroke="#fff" stroke-width="1.5"/></svg>Dataset</a>
    <a class="btn" href="https://github.com/METR/eval-analysis-public"><svg viewBox="0 0 16 16"><path d="M5.5 4 L1.8 8 L5.5 12 M10.5 4 L14.2 8 L10.5 12" fill="none" stroke="#fff" stroke-width="1.6"/></svg>METR analysis code</a>
  </div>
</div>

<div class="chbg" style="left:{M}px;top:{CY - PAD}px;width:{CWID + 2 * PAD}px;height:{CHT + 46:.0f}px"></div>
<div class="fig">
  <img src="metr_chart.png" alt="METR time horizon chart">
  <svg class="ov" viewBox="0 0 {IW} {IH}" preserveAspectRatio="none">{overlay}</svg>
  {tags}
</div>
<div class="cap">METR, Time Horizon 1.1, 50% success, log scale. Our additions:<span class="k"><span class="tg in s">S</span>strength</span><span class="k"><span class="tg in w">W</span>weakness</span></div>

<div class="panel re">
  <h3>Our reanalysis</h3>
  <div class="lead">Since o3, every frontier model sits <b>above</b> METR’s line. A fit from 2024 on doubles every <b>{DAYS_NEW:.0f} days</b> (METR: {DAYS_ALL:.0f}).</div>
  {resid}
</div>
<div class="panel mc">
  <h3>Marks and channels</h3>
  <div class="mcg">
    <div>{MARKS_INLINE}</div>
    <div>{CHAN_ROWS}</div>
  </div>
</div>

<div class="text">
  <div class="sh2 s">Strengths</div><div class="sh2 w">Weaknesses</div>
  {ROWS}
</div>

</div></body></html>
"""
open("index.html", "w", encoding="utf-8").write(html)
print(f"chart bottom {CY + CHT:.0f}, panels top {BOT:.0f}")
