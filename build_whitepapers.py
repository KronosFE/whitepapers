#!/usr/bin/env python3
"""
build_whitepapers.py — Kronos Fusion Energy website whitepaper set (40 papers).

60% science / 40% marketing. Every quantitative claim comes from the certified canon of the
MetroVolt design paper (a single combined manuscript in four parts) and its deposited 81-simulation programme (S01-S81; Zenodo DOI
10.5281/zenodo.21248916). Messaging standards honored: "low-neutron" (never "aneutronic"),
locked LCOE ladder, MetroVolt = commercial / AEGIS = defense, honest gap statement per paper.

Run:  python3 build_whitepapers.py   -> writes 40 HTML files + index.html next to this script.
"""
import os, html, re

HERE = os.path.dirname(os.path.abspath(__file__))
DOI = "10.5281/zenodo.21248916"

CSS = """
:root{--ink:#101724;--mut:#5a6472;--acc:#b8882e;--line:#d9dce2;--wash:#f7f6f2;--navy:#12233f}
*{margin:0;padding:0;box-sizing:border-box}
body{font-family:Georgia,'Times New Roman',serif;color:var(--ink);background:#fff;line-height:1.62}
.page{max-width:820px;margin:0 auto;padding:56px 28px 40px}
.brand{font-family:Verdana,Arial,sans-serif;font-size:11px;letter-spacing:3px;color:var(--navy);
  border-bottom:2px solid var(--navy);padding-bottom:10px;display:flex;justify-content:space-between}
.brand b{color:var(--acc)}
.eyebrow{font-family:Verdana,Arial,sans-serif;font-size:10px;letter-spacing:2.5px;color:var(--acc);
  text-transform:uppercase;margin:34px 0 10px}
h1{font-size:33px;line-height:1.18;font-weight:700;text-wrap:balance}
.sub{font-size:16.5px;color:var(--mut);font-style:italic;margin:12px 0 4px;text-wrap:balance}
.lead{font-size:17px;margin:26px 0 6px;border-left:3px solid var(--acc);padding-left:16px}
h2{font-family:Verdana,Arial,sans-serif;font-size:13.5px;letter-spacing:.6px;text-transform:uppercase;
  color:var(--navy);margin:30px 0 8px}
p{margin:10px 0;font-size:15.5px}
.nums{background:var(--wash);border:1px solid var(--line);border-top:3px solid var(--acc);
  padding:16px 18px;margin:28px 0}
.nums h3{font-family:Verdana,Arial,sans-serif;font-size:10.5px;letter-spacing:2px;color:var(--acc);
  text-transform:uppercase;margin-bottom:8px}
.nums table{width:100%;border-collapse:collapse;font-size:14px}
.nums td{padding:5px 6px;border-bottom:1px solid var(--line);vertical-align:top}
.nums td:last-child{text-align:right;font-family:Verdana,Arial,sans-serif;font-size:13px;white-space:nowrap}
.gap{border:1px dashed var(--mut);padding:14px 16px;margin:26px 0;font-size:14.5px}
.gap b{font-family:Verdana,Arial,sans-serif;font-size:11px;letter-spacing:2px;color:var(--navy);
  text-transform:uppercase;display:block;margin-bottom:6px}
.cta{background:var(--navy);color:#f2ede2;padding:18px 20px;margin:30px 0 0;font-size:14.5px}
.cta a{color:#e8c476;text-decoration:none}
.foot{font-size:11.5px;color:var(--mut);margin-top:22px;border-top:1px solid var(--line);padding-top:12px}
@media print{.page{padding:20px}.cta{-webkit-print-color-adjust:exact;print-color-adjust:exact}}
"""

PAGE = """<!DOCTYPE html><html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{title} — Kronos Fusion Energy</title><style>{css}</style></head><body><div class="page">
<div class="brand"><span>KRONOS <b>FUSION</b> ENERGY</span><span>WHITEPAPER {n:02d} / 40</span></div>
<div class="eyebrow">{series}</div>
<h1>{title}</h1>
<div class="sub">{sub}</div>
<p class="lead">{lead}</p>
{body}
<div class="nums"><h3>The numbers</h3><table>{numrows}</table></div>
<div class="gap"><b>Straight answers</b>{gap}</div>
{live}
<div class="cta">Every figure in this paper traces to the openly deposited 81-simulation programme
(S01&ndash;S81) behind the Kronos MetroVolt design paper &mdash; data and code at
<a href="https://doi.org/{doi}">DOI {doi}</a> (CC BY 4.0). Read the series, run the code, check us.</div>
<div class="foot">Kronos MetroVolt is a conceptual design study. Quantitative values are
simulation-derived and carry the feasibility gates stated in the series; Tier-2 flagship-code
confirmations are deposited as runnable decks pending HPC execution. This document is
informational and is not an offer of securities. &copy; 2026 Kronos Fusion Energy, Los Angeles.</div>
</div></body></html>"""

def render(p):
    body = "".join(f"<h2>{html.escape(h)}</h2>" + "".join(f"<p>{t}</p>" for t in ps)
                   for h, ps in p["secs"])
    numrows = "".join(f"<td>{html.escape(k)}</td><td>{html.escape(v)}</td></tr><tr>"
                      for k, v in p["nums"])
    numrows = "<tr>" + numrows.rsplit("<tr>", 1)[0]
    lv = p.get("live")
    live = ("<div class=\"cta\"><b>Run it live.</b> " + lv[1] +
            " &mdash; in your browser, nothing installed, the same deposited coefficients: "
            f"<a href=\"https://www.kronosfusionenergy.com/live/{lv[0]}\">kronosfusionenergy.com/live/{lv[0]}</a>. "
            "The engine re-derives the paper's frozen numbers before any control unlocks.</div>") if lv else ""
    return PAGE.format(css=CSS, n=p["n"], series=p["series"], title=html.escape(p["title"]),
                       sub=html.escape(p["sub"]), lead=p["lead"], body=body,
                       numrows=numrows, gap=p["gap"], doi=DOI, live=live)

A, B, C, D = "Series A — The Machine", "Series B — Energy & Product", \
             "Series C — Economics & Market", "Series D — Programme & Trust"

PAPERS = [
dict(n=1, series=A, slug="negative-triangularity",
 title="Shaped to Behave: Why MetroVolt Runs the Triangle Upside-Down",
 sub="Negative triangularity trades a little textbook elegance for a plasma edge that doesn't bite.",
 lead="Most tokamaks point their plasma cross-section toward the center column. MetroVolt points it "
      "the other way — δ = −0.30 — and that one sign flip is the quietest big decision in the design.",
 secs=[("The science", [
   "Conventional 'positive-triangularity' plasmas earn their confinement in H-mode, a regime whose edge "
   "periodically erupts in edge-localized modes (ELMs) — millisecond heat pulses that erode any wall built "
   "by humans. Negative-triangularity (NT) plasmas, demonstrated on the DIII-D and TCV tokamaks, hold "
   "near-H-mode confinement <i>without</i> that eruptive edge: the magnetic geometry suppresses the "
   "instability drive at the boundary while turbulence in the core actually improves.",
   "MetroVolt freezes δ = −0.30 and verifies it the hard way: a free-boundary Grad–Shafranov equilibrium "
   "(FreeGS) computes the real shaped plasma at full current, returning a safety factor q95 of 4.94 at the "
   "43 MA benchmark — which is exactly why the operating point is set at 42.5 MA: backing off the current keeps the machine at or above its own q95 ≥ 5.0 floor."]),
  ("Why it matters", [
   "An ELM-free edge is not a luxury; it is what lets a first wall survive contact with a commercial duty "
   "cycle. Combined with the deliberately low heat load of the D-³He fuel cycle (0.10–0.12 MW/m²), the NT "
   "choice converts 'plasma-facing components' from a consumable into plant infrastructure.",
   "Our own deposited δ-scan (S77) even reports the adverse trend honestly: pushing the triangle deeper "
   "costs safety-factor margin. The frozen −0.30 sits at the favourable end of the trade — chosen, tested, "
   "and published, not asserted."]) ],
 nums=[("Triangularity δ", "−0.30 (frozen)"), ("Edge regime", "ELM-suppressed (NT)"),
       ("q95 at 43 MA benchmark", "4.94 (FreeGS)"), ("Operating floor", "q95 ≥ 5.0 at 42.5 MA"),
       ("Shape verification", "free-boundary equilibrium, deposited")],
 gap="NT confinement at MetroVolt scale extrapolates from DIII-D/TCV experiments; the required H98 is "
     "stated openly as 1.8–2.2 (mode-dependent) rather than assumed. The δ-scan that argues against going "
     "deeper (S77) is deposited alongside the results that favour us."),

dict(n=2, series=A, slug="spherical-tokamak-a2",
 title="Small Giant: The Aspect-Ratio-2 Spherical Tokamak",
 sub="A fatter torus squeezes more plasma pressure out of every tesla — and every dollar.",
 lead="MetroVolt's torus is nearly a sphere with a hole through it: major radius 5.75 m, minor radius "
      "2.875 m, aspect ratio exactly 2.0. Compactness here is not styling — it is physics leverage.",
 secs=[("The science", [
   "Plasma pressure scales with the square of the field, but what a magnet buys you depends on geometry: "
   "low-aspect-ratio machines reach higher normalized pressure (β) per unit field. MetroVolt runs a "
   "toroidal β of 10.66% and a normalized βN of 4.33 at the frozen point — numbers a conventional "
   "aspect-ratio-3 machine cannot hold at the same safety margins.",
   "Elongation κ = 2.56 stretches the plasma vertically, adding cross-section (2,402 m³ of plasma volume) "
   "and bootstrap current. The equilibrium, vertical stability, and the 0.42 m of spare radial build are "
   "all computed and deposited — the compactness closes as a system (S76), not as a slogan."]),
  ("Why it matters", [
   "Machine volume drives capital cost. At R₀ = 5.75 m, MetroVolt's vacuum vessel, magnets, and shield fit "
   "a build envelope that existing heavy industry can fabricate and existing sites can host, while still "
   "delivering gigawatt-class fusion power. The spherical-tokamak bet is that the shortest path to "
   "commercial fusion economics runs through a smaller, higher-β machine — and MetroVolt writes that bet "
   "down in checkable numbers."]) ],
 nums=[("Aspect ratio A", "2.0 (R₀ 5.75 m / a 2.875 m)"), ("Elongation κ", "2.56"),
       ("Toroidal β", "10.66%"), ("Normalized βN", "4.33 (limit 4.5 no-wall)"),
       ("Plasma volume", "2,402 m³"), ("Spare radial build", "0.42 m")],
 gap="High-β spherical-tokamak operation at this scale and field is beyond any existing device; the "
     "integrated feasibility claim rests on the deposited eight-constraint systems evaluation (S76) and "
     "carries the confinement gate stated in the series."),

dict(n=3, series=A, slug="d-he3-low-neutron",
 live=("reactivity.html","Plot the four Bosch&ndash;Hale reactivity curves yourself and see where D&ndash;&sup3;He wins"),
 title="The Fuel That Barely Bites: D-³He and the 5.25% Neutron Budget",
 sub="Choose the reaction, and you choose the plant you must build around it.",
 lead="Deuterium–helium-3 fusion releases its energy overwhelmingly in charged particles. In MetroVolt's "
      "staged, catalysed cycle, only 5.25% of fusion power leaves as neutrons — a design constant that "
      "quietly rewrites the entire plant.",
 secs=[("The science", [
   "D-T fusion — the mainstream choice — emits 80% of its energy as 14.1 MeV neutrons, which demand a "
   "meter-scale breeding blanket, activate the structure, and set the replacement clock for every "
   "component behind the wall. D-³He's primary reaction is neutron-free; the residual neutron budget comes "
   "from unavoidable D-D side reactions, and MetroVolt's staged fuel management holds it to a computed "
   "5.25% neutronicity at the 80:20 operating mix.",
   "That single number cascades: first-wall load 0.10–0.12 MW/m² (roughly an order of magnitude below a "
   "D-T plant), vessel dose ~1.0 dpa per full-power year, and — because there is no tritium fuel to breed "
   "— no breeding blanket at all."]),
  ("Why it matters", [
   "Low-neutron is a maintenance strategy, a licensing posture, and a cost line, all at once. The deposited "
   "low-neutron dividend study (S81) prices it: a comparable D-T plant faces ~20–25 blanket changeouts "
   "over 30 full-power years, capping its availability near 0.71–0.75 — a +33–42% levelized-cost penalty "
   "MetroVolt structurally never pays."]) ],
 nums=[("Neutronicity f_n", "5.25% (80:20 mix)"), ("First-wall load", "0.10–0.12 MW/m²"),
       ("Vessel dose rate", "≈1.0 dpa / full-power year"), ("Breeding blanket", "none required"),
       ("Avoided D-T penalty", "+33–42% LCOE (S81, derived)")],
 gap="D-³He requires hotter plasmas and better confinement than D-T, and helium-3 must be supplied — both "
     "are treated as first-class design constraints (see the fuel-supply and confinement papers), not "
     "footnotes. We say 'low-neutron', never 'aneutronic': 5.25% is small and it is not zero."),

dict(n=4, series=A, slug="frozen-operating-point",
 live=("burn.html","Drive the frozen machine&rsquo;s temperature, density and fuel-mix sliders"),
 title="The Frozen Point: One Operating Point, Zero Moving Goalposts",
 sub="Every number in the series describes the same machine — because we froze it and threw away the eraser.",
 lead="Early in the programme, MetroVolt's operating point was frozen: R₀ 5.75 m, Ip 42.5 MA, B₀ 6 T, "
      "κ 2.56, δ −0.30, the Mode-C fuel staging. Everything since — 81 deposited analyses — interrogates "
      "that one point instead of quietly optimizing it.",
 secs=[("The science", [
   "Design studies die by drift: each subsystem tunes the plasma to flatter itself, and the sum is a "
   "machine no single analysis ever checked. MetroVolt's freeze discipline forbids that. The deposited "
   "systems code (S76) closes all eight coupled constraints — density limit, β limit, safety factor, peak "
   "field, magnet stress, confinement requirement, radial build, and engineering gain — simultaneously at "
   "the frozen point.",
   "Design-space studies exist (S77–S81), but they are explicitly quarantined: they explore around the "
   "point and are barred from altering it. When one of them found an adverse trend, it was published as "
   "one (S77, S79)."]),
  ("Why it matters", [
   "A frozen point is what makes 'check us' a real offer. Any reader can rerun the deposit and land on the "
   "same 2.41 GW, the same q95, the same wall load — no hidden re-tuning between chapters. For partners "
   "and reviewers, that consistency is the product: a design you can audit is a design you can finance."]) ],
 nums=[("Frozen geometry", "R₀ 5.75 m · A 2.0 · κ 2.56 · δ −0.30"),
       ("Frozen operating current", "42.5 MA"), ("Frozen field", "B₀ 6 T (24.6 T peak)"),
       ("Fusion power (hot-ion ceiling)", "2.41 GW"), ("Constraints closed simultaneously", "8 of 8 (S76)")],
 gap="Freezing does not make the point right — it makes it checkable. The two governing gaps (required "
     "confinement, hot-ion two-fluid balance) are carried openly against this same frozen point."),

dict(n=5, series=A, slug="systems-code-closure",
 title="Does It All Close? Eight Constraints, One Answer",
 sub="The most dangerous failure mode in fusion design is a machine that works chapter by chapter and fails as a whole.",
 lead="S76 is MetroVolt's integrated systems evaluation: one code, one frozen point, eight coupled "
      "constraints that must all pass at once. They do — and the margins are published, including the "
      "uncomfortable ones.",
 secs=[("The science", [
   "The eight gates: Greenwald density fraction (1.16 of limit 1.30), normalized β (4.41 vs 4.50 Troyon), "
   "safety factor (q95 4.43 > 2 kink floor in the 0-D convention), peak conductor field (24.6 < 26 T), "
   "magnet hoop stress (604 < 800 MPa), confinement requirement (H98 1.89 < 2.0 by the 0-D convention), "
   "radial build (1.31 of 1.73 m), and engineering gain (Q_eng 2.78 > 1).",
   "The binding constraint — the one the design leans on hardest — is β/confinement physics, exactly "
   "matching the series' own risk statement: MetroVolt is 'a magnet-and-materials programme betting on a "
   "confinement result.' The systems code confirms the bet is the right one to interrogate."]),
  ("Why it matters", [
   "Plenty of concepts pass their own chapters; far fewer pass a simultaneous closure test and then "
   "publish which wall they stand closest to. Knowing the binding constraint tells investors and "
   "researchers precisely which experiment de-risks the most value — that is what makes an honest systems "
   "code a capital-allocation tool, not just a physics exercise."]) ],
 nums=[("Constraints evaluated", "8, coupled, simultaneous"), ("Result at frozen point", "all pass"),
       ("Binding constraint", "βN / confinement"), ("Engineering gain Q_eng", "2.78"),
       ("Magnet stress margin", "604 MPa vs 900 yield (1.5×)")],
 gap="S76 is a Tier-1 reduced-order closure — a consistency check, not a substitute for the flagship-code "
     "confirmations (PROCESS/SYCOMORE-class, magnet FEA) that are deposited as the Tier-2 programme."),

dict(n=6, series=A, slug="operating-window",
 live=("burn.html","Push the sliders until the honesty badges trip at the stated envelope"),
 title="Not a Knife-Edge: MetroVolt's Operating Window",
 sub="A physics demonstration needs one good shot. A power plant needs room to breathe.",
 lead="We mapped every combination of density and temperature around the frozen point — 667 coupled "
      "evaluations per posture through the full eight-constraint systems code (S80). The answer: 36% of "
      "the scanned plane runs the plant at positive net power.",
 secs=[("The science", [
   "Below the design point, the window is wide: density can fall 37% and ion temperature 38% before the "
   "plant stops closing — it degrades gracefully, shedding output rather than tripping a cliff. Above the "
   "point, the story is one-sided: MetroVolt rides the no-wall β limit, so there is no headroom at "
   "βN = 4.5. The wall-stabilised limit (βN = 5.0, adjudicated by the deposited MHD decks S22/S25) opens "
   "+10% density room above the point.",
   "The near-thermal posture fails this particular 0-D gate everywhere on the plane — a convention gap the "
   "study reports rather than hides: its feasibility rests on the profile-resolved accounting, and its "
   "break-even H98 (2.24 at the deposited 42 keV reference) is computed and emitted, not asserted."]),
  ("Why it matters", [
   "Operators buy windows, not points. A −37%/−38% graceful envelope means startup, ramp, and off-normal "
   "operation have somewhere to live; a mapped edge means control systems know exactly which boundary "
   "they defend. Publishing the one-sided upside is the marketing: it tells sophisticated readers we "
   "measured our room instead of imagining it."]) ],
 nums=[("Feasible fraction of scanned plane", "36% (with P_net > 0)"),
       ("Graceful room below point", "−37% density / −38% temperature"),
       ("Upside at no-wall limit", "none (βN binding)"),
       ("Upside with wall stabilization", "+10% density (βN 5.0)"),
       ("Grid", "29 × 23 = 667 evaluations / posture")],
 gap="S80 is a design-space study: it explores around the frozen point and does not alter it. The "
     "wall-stabilised upside inherits the rotation/kinetic-RWM requirements of S22/S25."),

dict(n=7, series=A, slug="confinement-requirement",
 title="Confinement, Stated Plainly: The H98 = 1.8–2.2 Requirement",
 sub="Most fusion concepts hide their hardest number. Ours is printed in the abstract.",
 lead="For MetroVolt to close, its plasma must hold energy 1.8 to 2.2 times better than the standard "
      "H-mode scaling law (IPB98(y,2)) predicts for its size and field — depending on operating mode. "
      "That multiplier, H98, is the design's single most important open question, and we treat it that way.",
 secs=[("The science", [
   "The requirement is mode-dependent and every value is published: 1.84 at the frozen hot-ion point on "
   "the profile basis, 1.91 at the 80:20 mix, up to ≈2.2 for the near-thermal operating baseline (the 0-D "
   "systems gate returns 2.24 at the deposited Ti = Te = 42 keV reference; the documented convention "
   "offset reconciles it to ≈2.2 on the profile basis).",
   "Why is it plausible? Negative-triangularity experiments already report confinement at or above "
   "H-mode-like levels without ELMs, and MetroVolt's high-β, high-density spherical geometry is the "
   "regime where NT core turbulence behaves best. The claim is extrapolated, gated, and assigned to a "
   "decision gate (S18) with deposited gyrokinetic decks waiting on HPC time."]),
  ("Why it matters", [
   "Every fusion venture is betting on something. We name our bet, price it, and publish the experiment "
   "that settles it. If NT confinement lands where the evidence points, MetroVolt closes with margin; the "
   "requirement band, the fallback posture, and the adverse cases are all in the open record."]) ],
 nums=[("Required H98 band", "≈1.8–2.2 (mode-dependent, profile basis)"),
       ("Frozen hot-ion point", "1.84"), ("Near-thermal baseline", "≈2.2 (0-D gate 2.24 @ 42 keV)"),
       ("Adjudicating gate", "S18 (nonlinear gyrokinetics)"), ("Evidence base", "DIII-D / TCV NT experiments")],
 gap="No machine has yet demonstrated H98 ≈ 2 at MetroVolt's scale. This is the design's governing gap, "
     "carried openly since the first page of the series — the deposited CGYRO decks (S13) are the test."),

dict(n=8, series=A, slug="plasma-current-q95",
 title="42.5 Million Amps, Safely: The q95 ≥ 5 Discipline",
 sub="Plasma current buys confinement — and sells stability. MetroVolt sets the exchange rate in public.",
 lead="MetroVolt drives 42.5 MA of plasma current, among the largest ever specified. What keeps that "
      "ambition honest is a self-imposed floor: the edge safety factor q95 stays at or above 5, verified "
      "by free-boundary equilibrium, not estimated from formulas.",
 secs=[("The science", [
   "The safety factor counts how many times a field line winds the long way around for each short-way "
   "turn; low q95 invites the kink instabilities and disruptions that end discharges violently. Formula "
   "estimates flatter shaped plasmas, so MetroVolt computes q95 from the actual FreeGS equilibrium at "
   "δ = −0.30: 4.94 at the 43 MA benchmark, with the operating point set at 42.5 MA to respect the ≥5.0 "
   "floor.",
   "The robustness study (S79) then asks the impolite question: what if current falls short? Answer, "
   "published: a 10% Ip shortfall is not recoverable by density trim — plasma current is the least "
   "forgiving parameter in the design. That finding shapes the control philosophy and the disruption "
   "engineering budget."]),
  ("Why it matters", [
   "A disruption at 42.5 MA stores real energy (10.3 GJ; ~590 MN vertical load — quantified in the "
   "deposit), so the q95 discipline is the difference between a power plant and a research risk. Buyers "
   "of firm power are really buying operating margin; ours is computed, floored, and stress-tested against "
   "its own worst parameter."]) ],
 nums=[("Plasma current Ip", "42.5 MA"), ("Safety-factor floor", "q95(eq) ≥ 5.0"),
       ("Benchmark", "q95 4.94 at 43 MA (FreeGS)"), ("Least forgiving parameter", "Ip (S79, adverse, published)"),
       ("Disruption ledger", "10.3 GJ · ~590 MN (mitigated by SPI)")],
 gap="Non-inductive sustainment of 42.5 MA relies on bootstrap plus current drive whose integrated "
     "demonstration is a Tier-2 item; the current-drive budget and its acceptance criteria are deposited."),
]

PAPERS += [
dict(n=9, series=A, slug="rebco-magnets",
 title="Holding 24.6 Tesla: REBCO Magnets Without Exotics",
 sub="The field that makes a compact machine possible is bought with tape you can already order.",
 lead="MetroVolt's toroidal field is 6 T at the plasma axis but 24.6 T at the innermost conductor — and "
      "that peak is carried by REBCO high-temperature superconducting tape, engineered with the margins "
      "published line by line.",
 secs=[("The science", [
   "The magnet system winds 172.6 MA-turns using roughly 31,300 km of REBCO tape. Peak on-conductor field "
   "is 24.6 T at the critical radius R_c = 1.40 m — just above the 24.4 T single-coil field already "
   "demonstrated publicly, and below the 26 T design allowable. Hoop stress lands at 604 MPa against a "
   "900 MPa yield basis (a 1.5× margin) using distributed-structure design, and the preload architecture "
   "is bladder-and-key, adapted from LHC-generation accelerator magnet practice.",
   "The deposited field lever (S78) adds a purchased insurance policy: moving the winding-pack centre "
   "to R_c = 1.44 m while re-rating to B₀ = 6.11 T holds the peak at exactly the demonstrated 24.4 T — "
   "inside the 0.42 m of spare radial build, with fusion power unchanged and Troyon/kink margins improved."]),
  ("Why it matters", [
   "Magnets are the pacing technology of compact fusion, and the difference between a claim and a plan is "
   "whether the peak field, stress, quench, and fatigue lines are written down against demonstrated "
   "anchors. MetroVolt's are — including the honest note that 24.6 T is demonstrated at single-coil, not "
   "yet full-system, scale."]) ],
 nums=[("Peak on-conductor field", "24.6 T at R_c = 1.40 m"),
       ("Demonstrated anchor", "24.4 T (single coil); S78 lever reaches it"),
       ("Total conductor", "≈31,300 km REBCO tape · 172.6 MA-turns"),
       ("Hoop stress", "604 MPa vs 900 yield (1.5×)"),
       ("Fatigue basis", ">10⁴ full-field ramp cycles (30-yr life)")],
 gap="24.6 T on-conductor has not been demonstrated at full-system scale; the design carries that "
     "distinction explicitly and deposits the S78 lever as the path onto the demonstrated anchor."),

dict(n=10, series=A, slug="field-lever-s78",
 live=("lever.html","Move the winding-pack radius and watch the 24.40 T demonstrated line hold"),
 title="One Turn Outboard: The Field Lever That Buys Demonstrated Margin",
 sub="Sometimes the highest-value engineering move in a reactor is four centimeters long.",
 lead="S78 asks a simple question: what does MetroVolt give up to bring its peak magnet field down onto "
      "the field the world has already demonstrated? The answer — almost nothing — is one of the "
      "design's best trades.",
 secs=[("The science", [
   "Peak conductor field scales as B₀·R₀/R_c. Moving the winding-pack centre from R_c = 1.40 m to "
   "1.44 m — four centimeters, absorbed by the build's 0.42 m spare — while re-rating to B₀ = 6.11 T "
   "holds the peak at 24.40 T: precisely the publicly demonstrated single-coil field, with fusion power "
   "unchanged and better Troyon (βN 4.41 → 4.33) and kink (q95 4.43 → 4.51) margins. Or spend the freed "
   "margin instead: density into the βN headroom buys +6% fusion power (2,409 → 2,557 MW), still at 24.40 T.",
   "Both branches run through the full eight-constraint systems evaluation — every number survives the "
   "simultaneous check — and the robustness envelope (S79) confirms the lever stacks with the "
   "wall-stabilised upside rather than competing with it."]),
  ("Why it matters", [
   "Financing risk prices the distance between a design point and a demonstrated anchor. S78 collapses "
   "that distance for the magnet — the single most scrutinized subsystem in compact fusion — for the cost "
   "of spare space the build already carried. It is the difference between 'trust our extrapolation' and "
   "'here is the knob that lands us on the record book.'"]) ],
 nums=[("The move", "R_c 1.40 → 1.44 m + B₀ → 6.11 T (in 0.42 m spare)"),
       ("Peak field after", "24.40 T = demonstrated single-coil field"),
       ("Spend branch", "density into freed βN → +6% Pfus (2,557 MW)"),
       ("Cost to plasma performance", "none — margins improve"),
       ("Status", "design-space study S78, deposited, standalone")],
 gap="S78 explores around the frozen point and does not alter it; adopting either branch would be a "
     "post-review engineering decision, and the paper says so."),

dict(n=11, series=A, slug="disruption-engineering",
 title="When Plasmas Quit: Engineering for the 10.3 GJ Disruption",
 sub="We sized the worst day in the plant's life before sizing the best one.",
 lead="At 43 MA, an unmitigated MetroVolt disruption would release 10.3 GJ of stored energy — 4.8 GJ "
      "magnetic plus 5.5 GJ thermal — and pull ~590 MN of vertical load. Those numbers are in the "
      "deposit because pretending otherwise is how fusion loses trust.",
 secs=[("The science", [
   "The disruption ledger (KX-24) quantifies the full event: stored-energy partition, a ~23 ms current "
   "quench, vertical displacement forces, and a runaway-electron avalanche gain that is flagged 'high' — "
   "which is why shattered-pellet injection (SPI) mitigation is a requirement, not an option, with the "
   "reduced DREAM deck deposited for flagship confirmation.",
   "Negative triangularity helps twice: the ELM-free edge removes the most frequent disruption trigger "
   "class, and the mode-trade study shows the lower-current operating branch eases the ledger to ≈9 GJ. "
   "Structural verdicts are computed at ≥2× yield criteria against the ~590 MN envelope."]),
  ("Why it matters", [
   "Utilities do not fear plasma physics; they fear unbudgeted downtime. A disruption case with numbers, "
   "mitigation hardware, and structural margins is an insurable event rather than an existential one. "
   "Publishing the 'high avalanche' flag is deliberate: it converts our hardest transient into a "
   "specified, testable engineering requirement."]) ],
 nums=[("Unmitigated stored energy", "10.3 GJ (4.8 magnetic + 5.5 thermal)"),
       ("Vertical load", "≈590 MN (≥2× yield structural criterion)"),
       ("Current quench", "≈23 ms"), ("Mitigation", "SPI — required, deck deposited (S30)"),
       ("Eased case", "≈9 GJ at 37.1 MA branch")],
 gap="Runaway-electron avalanche gain is high at this current; the full DREAM confirmation is a Tier-2 "
     "deposited deck pending HPC execution. The requirement is stated before the confirmation exists."),

dict(n=12, series=A, slug="gentle-first-wall",
 title="The Gentle Wall: 0.10–0.12 MW/m² and a Vessel That Lasts the Plant's Life",
 sub="The cheapest component is the one you never replace.",
 lead="MetroVolt's first wall sees 0.10–0.12 MW/m² of neutron load — roughly an order of magnitude below "
      "a D-T power plant. Over 30 full-power years that integrates to ~30 dpa, inside the vessel alloy's "
      "36-dpa qualification target: the wall is designed to die of old age with the plant.",
 secs=[("The science", [
   "Wall dose is fuel chemistry made visible: at 5.25% neutronicity, the deposited fluence ledger (KX10) "
   "gives 1.0 dpa per full-power year at the MetroVolt wall. The vessel class is a CrMoNbV high-entropy "
   "alloy carried against an explicit ≈36-dpa capability qualification — stated as a target for the alloy "
   "programme, not a solved problem.",
   "The same ledger, applied with the same conversion to a 2.0–2.5 MW/m² D-T comparator, yields 20–25 "
   "dpa/FPY — blanket and wall replacement every 1.2–1.5 full-power years, ~20–25 changeouts over a "
   "plant life. MetroVolt schedules zero."]),
  ("Why it matters", [
   "Availability is the quiet variable that decides fusion economics. A blanket-changeout cycle caps a "
   "D-T plant near 0.71–0.75 availability; MetroVolt's wall imposes no such cycle, preserving the "
   "N+1-redundant plant availability >0.9 computed in the series. That difference alone is worth +33–42% "
   "on levelized cost — derived, deposited, and ours to keep."]) ],
 nums=[("First-wall load", "0.10–0.12 MW/m²"), ("Dose rate", "1.0 dpa / full-power year (deposited)"),
       ("Lifetime dose", "≈30 dpa over 30 FPY ≤ 36-dpa qualification"),
       ("Scheduled wall/blanket changeouts", "0 (vs ~20–25 for D-T comparator)"),
       ("Availability protected", ">0.9 (N+1 basis)")],
 gap="The 36-dpa figure is a qualification target for the CrMoNbV alloy class at the design dose, "
     "carried openly as a materials-programme requirement rather than an achieved certification."),

dict(n=13, series=A, slug="turbulence-basis",
 title="Turbulence, Priced: The Gyrokinetic Case and the Runs That Will Test It",
 sub="We modeled the hardest physics with the honest tools — and deposited the decks for the harder ones.",
 lead="Whether MetroVolt's core holds heat comes down to microturbulence. The series builds its case in "
      "tiers: reduced-order gyrofluid physics computed everywhere, and full nonlinear gyrokinetic decks "
      "(CGYRO) frozen, documented, and waiting on supercomputer time.",
 secs=[("The science", [
   "Tier-1 analyses use TGLF-class quasi-linear transport with the frozen profiles: they identify the "
   "ion-temperature-gradient branch as the governing mode, show the near-thermal baseline (Ti/Te → 1) "
   "raising the ITG threshold ≈1.3× over the hot-ion case, and find density peaking at Greenwald "
   "fraction ≈1.15 stabilizing the trapped-electron branch. The series is explicit that TGLF is not a "
   "nonlinear simulation — that distinction is written into the register.",
   "Tier-2 is the test: deposited CGYRO input decks (S13) with acceptance criteria pre-registered, so "
   "when HPC allocations run them, pass/fail was defined before the answer existed."]),
  ("Why it matters", [
   "Confinement is our named bet, and this is its audit trail. Pre-registered acceptance criteria mean "
   "the community — not our marketing — grades the result. That structure converts a physics risk into a "
   "scheduled, third-party-checkable milestone."]) ],
 nums=[("Governing instability", "ITG branch (TGLF-class, Tier-1)"),
       ("Near-thermal advantage", "ITG threshold ≈1.3× higher at Ti/Te → 1"),
       ("TEM stabilizer", "density peaking at f_GW ≈ 1.15"),
       ("Tier-2 test", "nonlinear CGYRO decks (S13), pre-registered"),
       ("Status", "decks deposited, pending HPC execution")],
 gap="No nonlinear gyrokinetic simulation of the MetroVolt core exists yet — the series says so in plain "
     "words. The deposited S13 decks are the outstanding confirmation, and the H98 gate depends on them."),

dict(n=14, series=A, slug="mhd-stability",
 title="Stability With Headroom: βN 4.33 Today, +24% With the Wall",
 sub="The design point rides the free-plasma limit — and the upgrade path is already adjudicated.",
 lead="MetroVolt operates at normalized pressure βN = 4.33 against the no-wall Troyon limit of 4.5. "
      "The deposited MHD programme shows what disciplined ambition looks like: run at the free limit, "
      "and hold the wall-stabilised regime in reserve.",
 secs=[("The science", [
   "Ideal-MHD analyses (MISHKA/MARS-K-class decks, S22/S25) adjudicate the with-wall limit at βN ≈ 5.0, "
   "conditioned on plasma rotation and kinetic resistive-wall-mode stabilization — requirements stated, "
   "not waved away. The robustness envelope (S79) prices the prize: at βN = 5.0 the same frozen geometry "
   "delivers +24% fusion power (2,409 → 2,999 MW) at unchanged confinement quality, with the density "
   "limit becoming the next boundary.",
   "High-current beta analysis (KX-9) favours the 42.5 MA mode (βN 4.33 vs 4.96 for the alternative), "
   "while the disruption ledger favours lower current — a real trade, resolved by gate adjudication and "
   "published as such."]),
  ("Why it matters", [
   "A design that needs its best case to close is fragile; MetroVolt closes at the no-wall limit and "
   "treats wall stabilization as upside. For offtakers, that is a +24% power option on the same capital; "
   "for physicists, it is a falsifiable claim with the decks already public."]) ],
 nums=[("Operating βN", "4.33 (no-wall limit 4.5)"), ("Wall-stabilised limit", "βN ≈ 5.0 (S22/S25)"),
       ("Upside at βN 5.0", "+24% Pfus (2,409 → 2,999 MW)"),
       ("Conditions", "rotation + kinetic RWM stabilization"),
       ("Next boundary after β", "Greenwald fraction 1.30")],
 gap="Wall stabilization at reactor scale requires rotation and feedback performance that remain to be "
     "demonstrated; MetroVolt's baseline economics do not depend on it."),

dict(n=15, series=B, slug="direct-energy-conversion",
 title="Electricity Without the Steam Detour: Multi-Modal Direct Energy Conversion",
 sub="When fusion energy arrives as charged particles, you can harvest it like electricity — because it already is.",
 lead="Most fusion concepts end in a boiler. MetroVolt's D-³He cycle delivers the majority of its power "
      "in charged particles and radiation, so the plant harvests through a multi-modal train: direct "
      "electrostatic conversion, radiation-to-electric surfaces, and a compact bottoming cycle.",
 secs=[("The science", [
   "The deposited Table-22 power ledger runs the plant end-to-end on two postures. Conservative "
   "(unchanneled): 2,409 MW fusion yields 1.18 GW gross electric and 0.61 GW net, engineering gain "
   "Q_eng = 2.1. With the bounded proton-channeling credit: 1.34 GW gross, 0.84 GW net, Q_eng = 2.7. "
   "Every intermediate line — 312 → 183 MWe direct-converter chain, 894/410 MW bottoming split — is "
   "printed and reproducible.",
   "Direct conversion of charged-particle streams at high efficiency has experimental heritage in "
   "plasma direct converters; MetroVolt's contribution is an integrated, gated design that never books "
   "credit beyond what its own exhaust-physics analysis (S51/S65) supports."]),
  ("Why it matters", [
   "Skipping the full steam detour raises plant efficiency and deletes cost: less turbine hall, less "
   "cooling infrastructure, faster load response. The two-posture ledger gives buyers a floor and an "
   "upside on the same machine — and the floor already clears commercial thresholds."]) ],
 nums=[("Net electric (conservative)", "0.61 GWe · Q_eng 2.1"),
       ("Net electric (channeled)", "0.84 GWe · Q_eng 2.7"),
       ("Gross electric", "1.18 / 1.34 GW"), ("Fusion power basis", "2,409 MW (frozen point)"),
       ("Ledger", "Table 22, line-by-line, deposited")],
 gap="The DEC train's component efficiencies are engineering targets with cited heritage, and the "
     "channeling credit is bounded by the S72 analysis (≤30% tax redress) — the conservative posture is "
     "the baseline, not the brochure number."),

dict(n=16, series=B, slug="dec-gate-honesty",
 title="The Hard Question We Kept: Proton Channeling and the DEC Gate",
 sub="The single biggest efficiency lever in the plant is also the one we refuse to assume.",
 lead="If the 14.7 MeV fusion protons could be steered into the direct converter at full value, "
      "MetroVolt's output would jump. They cannot — not fully, not for free — and the series prices "
      "exactly how much of that dream survives contact with kinetics.",
 secs=[("The science", [
   "Fast protons born in D-³He fusion slow down on the plasma's electrons and ions before any extraction "
   "scheme can claim them. The deposited Fokker–Planck and exhaust analyses (S26, S51/S65, S72) bound "
   "the recoverable fraction: channeling 15–25% of the proton line redresses only 5–8% of the hot-ion "
   "sustainment tax — a ≤30% redress even at 100% channel efficiency.",
   "That bound has teeth: it demoted hot-ion operation from baseline to adjudicated upside and set the "
   "near-thermal posture as the plant's operating baseline. The decision is enshrined as a gate (P6) "
   "with pre-registered criteria."]),
  ("Why it matters", [
   "Every technology has a number its enthusiasts want to assume. Publishing the bound — and re-basing "
   "the whole plant on the posture that survives it — is why the rest of MetroVolt's ledger deserves "
   "belief. The upside remains real and gated: if channeling experiments beat the bound, the 0.84 GWe "
   "posture is already engineered."]) ],
 nums=[("Channeling bound", "≤30% tax redress at 100% efficiency (S72)"),
       ("Realistic credit", "15–25% of proton line ⇒ 5–8% of tax"),
       ("Design consequence", "near-thermal = baseline; hot-ion = P6-gated upside"),
       ("Gate", "P6, pre-registered criteria"), ("Analyses", "S26 · S51 · S65 · S72, deposited")],
 gap="DEC exhaust physics at reactor parameters is a named decision gate (S51/S65 avalanche item open); "
     "the plant's baseline economics are computed without the channeling credit."),
]

PAPERS += [
dict(n=17, series=B, slug="two-throttles",
 live=("reactivity.html","See the Mode-C hot-ion marker at 65 keV on the live reactivity curves"),
 title="Two Throttles: Near-Thermal Baseline, Hot-Ion Upside",
 sub="One machine, two honest operating postures — and the conservative one signs the contracts.",
 lead="MetroVolt is specified twice on purpose. The near-thermal posture (ion and electron temperatures "
      "equal) is the operating baseline the economics stand on; the hot-ion posture (Ti/Te = 1.9) is a "
      "physics upside held behind a pre-registered gate.",
 secs=[("The science", [
   "Hot-ion operation boosts fusion output — the deposited ceiling is 2.41 GW — but D-³He plasmas "
   "deposit fast-particle energy preferentially on electrons, taxing the very temperature split that "
   "makes hot-ion attractive. The completed Fokker–Planck gate (S26) and the channeling bound (S72: "
   "≤30% tax redress) size that tax honestly, which is why the baseline is near-thermal: ≈1.5 GW-class "
   "fusion, 0.4–0.5 GWe net on the fallback pricing, with its ≈2.2 profile-basis confinement requirement "
   "stated in the abstract.",
   "The hot-ion case is retained as the P6-adjudicated upside — 0.61 GWe conservative, 0.84 GWe with "
   "bounded channeling — engineered now, credited only when the gate says so. A bonus, published with "
   "the rest: the near-thermal core is also the more turbulence-stable one (ITG threshold ≈1.3× higher)."]),
  ("Why it matters", [
   "Two postures give customers a floor they can bank and an upside they don't pay for until it is "
   "proven. It also tells reviewers something rarer: this team downgraded its own headline number when "
   "its own physics said to."]) ],
 nums=[("Baseline (near-thermal)", "≈1.5 GW-class fusion · 0.4–0.5 GWe"),
       ("Upside (hot-ion, gated)", "2.41 GW fusion · 0.61–0.84 GWe"),
       ("Hot-ion tax redress bound", "≤30% (S72)"),
       ("Baseline confinement need", "H98 ≈ 2.2 (profile basis, stated)"),
       ("Adjudication", "gate P6, pre-registered")],
 gap="The near-thermal baseline carries the design's highest confinement requirement (≈2.2) — printed at "
     "the top of the band, not hidden under the hot-ion number. The two-fluid balance is one of the two "
     "named governing gaps of the series."),

dict(n=18, series=B, slug="one-metrovolt-output",
 title="0.61 to 0.84 Gigawatts: What One MetroVolt Delivers",
 sub="City-scale firm power from a machine that fits behind existing fences.",
 lead="On its conservative ledger a MetroVolt unit exports 0.61 GW of electricity — round-the-clock, "
      "fuel-secure, carbon-free. With the gated channeling credit the same machine books 0.84 GW. That "
      "is roughly a half-million-plus American homes from one compact plant.",
 secs=[("The science", [
   "The plant ledger is computed line by line at the frozen point (Table 22, deposited): 2,409 MW "
   "fusion; charged-particle and radiation streams harvested by the multi-modal direct-energy-conversion "
   "train; bottoming cycle on the balance; 1.18 GW gross; 0.61 GW net after all plant loads, at "
   "engineering gain Q_eng 2.1. The channeled posture lifts gross to 1.34 GW and net to 0.84 GW "
   "(Q_eng 2.7).",
   "Both postures obey the same discipline as the physics: no efficiency is booked beyond its cited "
   "heritage, and the sustainment power that runs the plasma is charged fully against output."]),
  ("Why it matters", [
   "0.61 GWe firm is a fleet-planning number: it replaces a retiring coal or gas unit on a similar grid "
   "interconnect, without the fuel logistics and without the emissions. The upside case is the same "
   "interconnect earning 38% more — a growth option embedded in every unit sold."]) ],
 nums=[("Net electric, conservative", "0.61 GWe (Q_eng 2.1)"),
       ("Net electric, channeled", "0.84 GWe (Q_eng 2.7)"),
       ("Gross electric", "1.18 / 1.34 GW"),
       ("Machine footprint", "R₀ = 5.75 m tokamak core"),
       ("Basis", "Table-22 ledger, deposited, reproducible")],
 gap="These are simulation-derived values at the frozen point, contingent on the confinement gate; the "
     "near-thermal fallback (0.4–0.5 GWe) is published with equal prominence in the series."),

dict(n=19, series=B, slug="low-neutron-dividend",
 title="The Low-Neutron Dividend: Zero Blanket Changeouts",
 sub="We derived our biggest economic advantage from our own materials ledger — both sides of it.",
 lead="S81 asks what MetroVolt's 5.25% neutron budget is worth over a plant lifetime, using only the "
      "deposited fluence ledger and applying the same conversion to both contenders. The answer is the "
      "strongest single exhibit in the economics case.",
 secs=[("The science", [
   "MetroVolt: 1.0 dpa per full-power year at the wall → 30 dpa over 30 FPY, inside the 36-dpa "
   "qualification — the first wall and vessel last the plant's life, and no breeding blanket exists to "
   "replace. D-T comparator at 2.0–2.5 MW/m² by the identical deposited conversion: 20–25 dpa/FPY, "
   "replacement every 1.2–1.5 FPY, ~20–25 changeouts over the same life, each a months-long outage.",
   "The blanket cycle alone caps the comparator's availability at 0.71–0.75. On capital-dominated "
   "economics that is a +33–42% levelized-cost penalty MetroVolt structurally avoids — derived, not "
   "asserted, with the honest flag that the magnet-conductor fluence line sits ~8% above a degradation "
   "onset (onset, not failure; margin posture carried in the series)."]),
  ("Why it matters", [
   "Fuel choice is usually argued with physics adjectives. S81 converts it to money using our own "
   "deposited numbers and mainstream external anchors — the kind of comparison a due-diligence team can "
   "re-run in an afternoon. It is the low-neutron thesis, priced."]) ],
 nums=[("MetroVolt lifetime wall dose", "30 dpa ≤ 36-dpa qualification"),
       ("MetroVolt scheduled changeouts", "0 (no breeding blanket)"),
       ("D-T comparator", "~20–25 changeouts · availability 0.71–0.75"),
       ("Avoided penalty", "+33–42% LCOE"),
       ("Method", "same deposited dpa conversion, both sides (S81)")],
 gap="The comparator uses stated, conservative-mainstream D-T assumptions (2.0–2.5 MW/m² wall load, "
     "~30 dpa windows, ~6-month changeouts); vary them and the dividend flexes — the script is deposited "
     "so anyone can."),

dict(n=20, series=B, slug="helium3-supply",
 title="Fuel for Decades: The Helium-3 Supply Strategy",
 sub="The rarest input in the plant is managed like what it is — a strategic commodity with a staged plan.",
 lead="A MetroVolt fleet runs on helium-3, and the series treats supply as an engineering system, not a "
      "hand-wave: measured consumption, staged sources, and an in-plant contribution computed against "
      "its own fuel cycle.",
 secs=[("The science", [
   "A unit consumes helium-3 at reactor scale (fleet planning uses ≈90 kg/yr class figures at full "
   "buildout in the series' economics). Sources are staged: terrestrial tritium-decay stockpiles "
   "(³He accrues at 0.42 liters per gram of tritium per year — the series' corrected, deposited figure), "
   "D-D-derived breeding inside the staged fuel cycle itself, and market/strategic reserves. The "
   "self-supply fraction is computed honestly: f_self ≈ 0.34 rising toward 0.48 across the staging, "
   "with the in-situ supply trajectory plotted from the deposited fuel-cycle integrator.",
   "The series is blunt where it must be: prompt in-plant breeding at ratio ≥1 does not close (§3.5 "
   "computes it negative) — self-sufficiency is partial by physics, which is exactly why the supply "
   "strategy is staged and external sourcing is a permanent line item."]),
  ("Why it matters", [
   "Fuel security is a solvable procurement problem when consumption is honest and sources are plural. "
   "The plan's shape — stockpile decay + partial self-breeding + reserves — is resilient to any single "
   "source disappointing, and every input to that plan is deposited where a fuel buyer can audit it."]) ],
 nums=[("Decay sourcing", "0.42 L ³He / g tritium / yr (deposited)"),
       ("Self-supply fraction", "f_self ≈ 0.34 → 0.48 (staged)"),
       ("Prompt breeding ≥ 1?", "no — computed negative, stated (§3.5)"),
       ("Fleet-scale demand class", "≈90 kg/yr at buildout"),
       ("Strategy", "stockpiles + partial self-breeding + reserves")],
 gap="Helium-3 markets at fleet scale do not exist yet; the series prices supply as a constraint and "
     "publishes the fuel-cycle integrator so the sensitivity is anyone's to compute."),

dict(n=21, series=B, slug="tritium-lean",
 title="Under One Kilogram: Tritium-Lean by Design",
 sub="The isotope that dominates fusion licensing is a trace species in this plant.",
 lead="MetroVolt caps per-site tritium inventory below one kilogram and consumes bred tritium "
      "internally as fuel-cycle feedstock. That single design rule reshapes safety analysis, licensing "
      "posture, and neighborhood conversations alike.",
 secs=[("The science", [
   "D-T plants must breed, extract, purify, and store tritium at multi-kilogram site inventories — the "
   "defining radiological source term of mainstream fusion. MetroVolt's D-³He cycle produces tritium "
   "only as a D-D side product; the staged fuel management burns it (catalysed operation) or holds it "
   "briefly as it decays into the very helium-3 the plant wants. The sub-kilogram cap is a designed "
   "operating rule of the fuel cycle, enforced by its own mass-balance ledger, deposited and plotted.",
   "Less inventory means smaller source terms in accident analyses, lighter confinement engineering, "
   "and a licensing conversation about a bounded trace species rather than a bulk process stream."]),
  ("Why it matters", [
   "Communities and regulators price the worst case. A plant whose entire site inventory of the "
   "mobile radioisotope is bounded below a kilogram — and falls with time by decay into fuel — starts "
   "that conversation from a categorically different place than a breeding-blanket plant. Tritium-lean "
   "is not just physics elegance; it is time-to-permit."]) ],
 nums=[("Per-site tritium cap", "< 1 kg (design rule)"),
       ("Breeding blanket", "none — no bulk tritium process stream"),
       ("Bred tritium fate", "burned / decays to ³He fuel"),
       ("Basis", "fuel-cycle mass balance, deposited"),
       ("Licensing posture", "trace-species source term")],
 gap="The cap is a design rule verified in simulation ledgers; operational tritium accountancy at plant "
     "scale remains an engineering-execution item and is scoped as such in the series."),

dict(n=22, series=B, slug="quiet-neighbor-activation",
 title="Quiet Neighbor: ~25× Lower Activation and the Low-Level-Waste Path",
 sub="What a fusion plant leaves behind is a choice made at the fuel line, decades in advance.",
 lead="Run the same activation physics on MetroVolt and on a D-T comparator and the structures answer "
      "differently: roughly twenty-five-fold lower activation, and a decommissioning stream that fits "
      "the existing low-level-waste disposal pathway.",
 secs=[("The science", [
   "Neutrons transmute structure; MetroVolt simply makes twenty times fewer of them per unit energy, and "
   "at softer relevance to the worst activation chains. The deposited analyses (S68 with the S39 "
   "neutronics basis) compute the ~25× activation advantage and map end-of-life inventories onto "
   "disposal classes: the vessel and internals track the low-level-waste pathway — no geological "
   "repository line item.",
   "This is the same fluence ledger that gives the 30-FPY wall life and the 36-dpa qualification "
   "target — one consistent neutron story from operations through decommissioning."]),
  ("Why it matters", [
   "Decommissioning liability is a real number on utility balance sheets. A LLW-pathway plant retires "
   "like industrial equipment, not like a nuclear legacy site — smaller bonds, shorter closeout, cleaner "
   "community story. 'Low-neutron' keeps paying after the last kilowatt-hour."]) ],
 nums=[("Activation vs D-T comparator", "~25× lower (S68/S39)"),
       ("Disposal pathway", "low-level waste (computed inventories)"),
       ("Geological repository need", "none identified"),
       ("Consistency", "same ledger as wall-life & shielding"),
       ("Wall life context", "30 dpa / 30 FPY ≤ 36-dpa qual")],
 gap="Activation results are computed with the deposited neutronics basis; isotope-level confirmatory "
     "runs with flagship transport codes are part of the Tier-2 deck programme."),

dict(n=23, series=B, slug="shielding-neutronics",
 title="Shield Craft: Multigroup Neutronics in a Compact Build",
 sub="Every centimeter between plasma and magnet is contested real estate. We surveyed it properly.",
 lead="A compact machine lives or dies by its shield: too thin and the magnets cook; too thick and the "
      "geometry that makes it cheap is gone. MetroVolt's shield is optimized with real multigroup "
      "transport physics — and the early wrong answer is left in the record.",
 secs=[("The science", [
   "First-pass analytic shielding suggested a tungsten-boride/B₄C recipe at ~0.9 m; the deposited "
   "multigroup analyses (S36/S37) corrected it: B₄C-led recipes fail (6× over target at 1.00 m), and the "
   "optimized WC/W₂B₅ stack closes the requirement at ≈1.20 m — a minimum that the radial build then "
   "absorbs while preserving 0.42 m of spare. The correction is documented, superseding note and all.",
   "Downstream, the shielded conductor fluence ledger totals 3.23×10²² n/m² over life against a "
   "3.0×10²² degradation-onset reference — ~8% above onset, carried openly with the margin posture "
   "(onset is not failure) in the magnet chapter."]),
  ("Why it matters", [
   "Shield honesty is magnet honesty: the most expensive components in the plant sit behind that stack. "
   "Publishing the failed recipe alongside the working one shows the optimization was real — and the "
   "8%-above-onset flag shows the ledger wasn't tuned to flatter itself."]) ],
 nums=[("Optimized shield", "WC/W₂B₅ stack, min ≈1.20 m"),
       ("Rejected recipe", "B₄C-led: 6× over at 1.00 m (documented)"),
       ("Spare build after shield", "0.42 m"),
       ("Lifetime conductor fluence", "3.23e22 vs 3.0e22 onset (~8% above; flagged)"),
       ("Method", "multigroup transport (S36/S37), deposited")],
 gap="The conductor-fluence line exceeds the cited degradation onset by ~8%; the series carries this as "
     "an open margin item rather than adjusting the ledger, and flagship Monte-Carlo confirmation (OpenMC "
     "decks) is deposited for Tier-2 execution."),

dict(n=24, series=B, slug="materials-receipts",
 title="Materials With Receipts: 4,744 Measured Points from the ITER Handbook",
 sub="Our structures are designed against curated measurements, not textbook constants.",
 lead="Every thermal and structural analysis in the MetroVolt series draws on a curated extraction of "
      "the ITER Material Properties Handbook: 4,744 unflagged measured data points across 35 materials, "
      "shipped inside the open deposit.",
 secs=[("The science", [
   "Reactor design fails quietly when material properties are single-number assumptions. The deposited "
   "basis carries per-point scatter for the properties that matter — thermal conductivity, yield "
   "strength, mean thermal expansion — with data-quality flags honored and an n > 2 rule per property "
   "curve. The plasma-facing and structural analyses (KX-3/KX-4 class) run on those measured curves "
   "directly.",
   "The vessel material itself — a CrMoNbV high-entropy-alloy class — is carried against an explicit "
   "≈36-dpa capability qualification target at the design dose: a stated materials-programme requirement, "
   "cleanly separated from the demonstrated database that everything else runs on."]),
  ("Why it matters", [
   "Due diligence teams ask one question of every engineering claim: against what data? MetroVolt's "
   "answer is a folder in the deposit. Measured scatter in, honest margins out — and the one place the "
   "design leans on future qualification is labeled as exactly that."]) ],
 nums=[("Curated dataset", "4,744 unflagged points · 35 materials"),
       ("Source", "ITER Material Properties Handbook (curated extraction)"),
       ("Properties driving design", "k(T) · yield(T) · expansion(T)"),
       ("Vessel class", "CrMoNbV HEA — 36-dpa qualification target"),
       ("Where it lives", "inside the open deposit (common/)")],
 gap="The HEA vessel qualification at 36 dpa is a target, not an achieved certification — stated in the "
     "series and in this paper's own table."),
]

PAPERS += [
dict(n=25, series=C, slug="honest-cost-ladder",
 live=("lcoe.html","Rebuild Table 26&rsquo;s cost ladder and stress every assumption"),
 title="The Honest Cost Ladder: FOAK $84–92 to Fleet $48–56",
 sub="One levelized-cost story, told the same way to physicists, financiers, and skeptics.",
 lead="MetroVolt's economics are published as a ladder, not a point: first-of-a-kind at $84–92/MWh, "
      "an NOAK trajectory of $48–84 across capex scenarios, and fleet maturity at $48–56 — every rung "
      "generated by a deposited, runnable calculation.",
 secs=[("The science", [
   "The ladder's engine is simple and stated: 7% WACC, 25-year amortization, 0.90 capacity factor, "
   "O&M-plus-fuel of $19–21/MWh tiered with capex class, and Wright's-law learning at 14.5% applied to "
   "first-of-a-kind capital of $6,500 / $9,000 / $11,500 per kWe (low / central / high). The nine "
   "NOAK-table cells that result — 55/52/48, 69/65/60, 84/79/72 across units 20/30/50 — reproduce from "
   "the deposited S63 script, deltas printed where rounding differs by a dollar.",
   "A speculative long-run floor of $18–30/MWh is discussed in the series with its assumptions exposed; "
   "the ladder's committed rungs stop at fleet $48–56."]),
  ("Why it matters", [
   "Fusion economics has a credibility problem built from single-point promises. A ladder with a "
   "runnable generator inverts that: the assumptions are the pitch. At the central trajectory MetroVolt "
   "meets firm-power markets on price without subsidies in the model — and every skeptic is one script "
   "away from checking."]) ],
 nums=[("FOAK", "$84–92 / MWh"), ("NOAK trajectory (units 20–50)", "$48–84 / MWh"),
       ("Fleet maturity", "$48–56 / MWh"),
       ("Basis", "7% WACC · 25-yr · CF 0.90 · LR 14.5%"),
       ("Generator", "S63 script + CSV, deposited")],
 gap="All rungs are conditional on the physics gates and on capex realization; the FOAK capex range "
     "itself ($6,500–11,500/kWe) is the dominant uncertainty and is carried as three explicit scenarios."),

dict(n=26, series=C, slug="required-ppa-band",
 title="What Buyers Sign: The $56–92 Required-PPA Band",
 sub="The number that matters to an offtaker is the price that makes the plant financeable.",
 lead="Across the NOAK window at unlevered returns of 8–12%, MetroVolt's required power-purchase price "
      "spans $56–92/MWh — squarely inside what firm, clean power already clears in real markets.",
 secs=[("The science", [
   "The band evaluates the same deposited cost ladder at investor hurdle rates: the levelized price at "
   "which units 20 through 50 clear an 8–12% unlevered IRR under the stated scenario conditioning. It "
   "is quoted as a Monte-Carlo scenario envelope in the series, with the deterministic ladder deposited "
   "as the traceable core (the S63 script prints both and says which is which).",
   "Context anchors from 2024–26 markets are cited in the series: recent firm-power and "
   "clean-baseload contracts — including nuclear-restart and advanced-energy PPAs — have printed at and "
   "above this band's midpoint."]),
  ("Why it matters", [
   "A required-PPA band inside observed market prints means MetroVolt does not need a policy miracle to "
   "pencil — it needs its physics gates. That is the correct dependency order for a technology company: "
   "the market risk is bounded and visible, so capital can price the science."]) ],
 nums=[("Required PPA", "$56–92 / MWh (8–12% unlevered IRR)"),
       ("Window", "NOAK units 20–50, scenario-conditioned"),
       ("Deterministic core", "deposited S63 ladder"),
       ("Market context", "2024–26 firm-power prints at/above midpoint"),
       ("Dependency", "physics gates, not subsidies (in-model)")],
 gap="The $56–92 envelope is scenario-conditioned; the deposited deterministic corners span wider "
     "(51–115), and the S63 script states both plainly rather than blending them."),

dict(n=27, series=C, slug="wrights-law",
 live=("lcoe.html","Bend the Wright&rsquo;s-law learning curve yourself, unit 1 to unit 50"),
 title="Learning Curves That Pay: Wright's Law from Unit 1 to Unit 50",
 sub="Fusion's cost future is a manufacturing question, and manufacturing questions have known math.",
 lead="Every doubling of cumulative production cuts unit cost by a roughly constant fraction — Wright's "
      "law, the most durable empirical rule in industrial economics. MetroVolt's fleet economics apply "
      "it at a published 14.5% learning rate, bucket by bucket.",
 secs=[("The science", [
   "The series decomposes plant capital into buckets with cited, published learning behavior — "
   "superconducting magnets, power electronics, structures, balance of plant — rather than applying one "
   "optimistic rate to everything. The composite 14.5% rate yields per-unit capex factors of ≈0.50 by "
   "unit 20, ≈0.46 by unit 30, and ≈0.41 by unit 50 against first-of-a-kind capital.",
   "Compact geometry is what makes the law bite: an R₀ = 5.75 m machine is a factory product with a "
   "supply chain, not a decade-long civil project. The learning that took photovoltaics and batteries "
   "down their cost curves needs production cadence — and cadence needs a machine you can actually "
   "iterate."]),
  ("Why it matters", [
   "The difference between $84 and $48 per MWh in the ladder is not a physics breakthrough — it is "
   "manufacturing repetition at a documented rate. Investors can diligence a learning assumption "
   "bucket-by-bucket against published industry data; that is a materially easier bet than diligencing "
   "a miracle."]) ],
 nums=[("Learning rate", "14.5% (bucket-decomposed, cited)"),
       ("Capex factor @ unit 20", "≈0.50 × FOAK"),
       ("@ unit 30 / 50", "≈0.46 / ≈0.41 × FOAK"),
       ("What it drives", "the $84 → $48 ladder descent"),
       ("Precedents", "PV, batteries, aerospace composites")],
 gap="Learning rates are empirical, not guaranteed; the ladder therefore publishes all three capex "
     "scenarios and the ladder math survives at the conservative rung."),

dict(n=28, series=C, slug="firm-power-markets",
 title="Firm Power, Priced: MetroVolt in Real Electricity Markets",
 sub="The grid's scarcest product is no longer energy — it is around-the-clock certainty.",
 lead="Wholesale markets increasingly pay two prices: one for energy, a larger one for firmness. "
      "MetroVolt is engineered for the second market — 0.61–0.84 GWe of dispatchable, fuel-secure, "
      "carbon-free output at >0.9 design availability.",
 secs=[("The science", [
   "Availability is engineered, not hoped: N+1 redundancy in the balance-of-plant analysis carries "
   "plant availability above 0.9, and the absence of a blanket-changeout cycle removes the outage "
   "class that caps D-T competitors near 0.71–0.75. The direct-energy-conversion train's electrical "
   "front end also responds faster than a steam plant, giving the unit real ancillary-services "
   "capability.",
   "Siting economics compound it: a compact core with modest exclusion needs can occupy retiring "
   "thermal-plant interconnects — the scarcest, most valuable real estate on the modern grid."]),
  ("Why it matters", [
   "Data centers, electrified industry, and reliability-constrained utilities are signing "
   "multi-decade firm contracts at historically strong prices. MetroVolt's required-PPA band ($56–92) "
   "sits inside those prints, and its availability story is structural rather than promised. Firm, "
   "clean, compact, sited on existing interconnects: that is the product."]) ],
 nums=[("Design availability", "> 0.9 (N+1 basis)"),
       ("Output per unit", "0.61–0.84 GWe firm"),
       ("Outage class avoided", "blanket changeouts (D-T: ~20–25/life)"),
       ("Required PPA", "$56–92 / MWh band"),
       ("Siting leverage", "retiring thermal interconnects")],
 gap="Availability >0.9 is a design-basis computation; demonstrated fleet availability is, by "
     "definition, a post-FOAK statistic. The economics rungs that depend on it say so."),

dict(n=29, series=C, slug="foak-bill-of-materials",
 title="What a First Plant Costs: Inside the $3.15B FOAK Bill of Materials",
 sub="Credible capital costs are built from the bottom, one subsystem at a time.",
 lead="MetroVolt's first-of-a-kind direct-cost basis is $3,150M, assembled as a line-item bill of "
      "materials — magnets to shield to conversion train to buildings — rather than scaled from "
      "someone else's reactor study.",
 secs=[("The science", [
   "The BOM prices the frozen design point: the ~31,300 km REBCO conductor order and winding, the "
   "WC/W₂B₅ shield stack at its computed ≈1.20 m minimum, the vessel in its qualification-target "
   "alloy class, the multi-modal DEC train, cryoplant, heating and current-drive systems, and "
   "balance of plant — each line carrying its own basis and contingency posture in the finance model.",
   "Dividing through the conservative 0.61 GWe net yields the capex-per-kilowatt figures that seed "
   "the published ladder scenarios; the model and the physics deposit quote each other, so the "
   "engineering and the economics cannot silently diverge."]),
  ("Why it matters", [
   "A bottom-up BOM is auditable: a supplier can quote against a line, a diligence engineer can "
   "challenge one, and cost learning can be tracked line-by-line as the fleet builds. The $3.15B "
   "figure is not small — it is simply real, and every rung of the cost ladder stands on it."]) ],
 nums=[("FOAK direct-cost basis", "$3,150M (line-item BOM)"),
       ("Largest lines", "magnets · shield · DEC train"),
       ("Conductor order", "≈31,300 km REBCO"),
       ("Feeds", "capex/kWe scenarios → LCOE ladder"),
       ("Consistency", "finance model reconciled to the physics deposit")],
 gap="FOAK costs carry first-unit risk by definition; the ladder's $6,500–11,500/kWe scenario spread "
     "exists precisely to hold that uncertainty in view rather than average it away."),

dict(n=30, series=C, slug="g1-gate-testbed",
 title="Half a Billion to Certainty: The G1 Gate Testbed",
 sub="Before anyone builds a $3B plant, physics gets one decisive, affordable trial.",
 lead="MetroVolt's roadmap runs through G1: an integrated gate testbed costed at ~$0.5B (deposited "
      "breakdown: $582M ±30%) whose sole mission is to adjudicate the pre-registered predictions the "
      "design's value hangs on.",
 secs=[("The science", [
   "G1 exists to retire the named gaps in order of leverage: the confinement requirement (the H98 "
   "band), the hot-ion two-fluid balance (P6), and the exhaust/DEC physics chain. Seven predictions "
   "(P1–P7) are pre-registered in the series with acceptance criteria fixed before any experiment "
   "runs — the same discipline as the deposited Tier-2 decks, applied to hardware.",
   "The cost breakdown is itself deposited (KX24 schedule): machine core, magnets at demonstrated "
   "field anchors, diagnostics, and facility, at gate scale rather than power-plant scale — which is "
   "what makes decisive physics affordable."]),
  ("Why it matters", [
   "Staged capital against pre-registered milestones is how disciplined investors buy deep-tech risk. "
   "G1 converts 'is the physics right?' from an open-ended fear into a scoped, ~$0.5B, "
   "criteria-in-advance project — and every downstream billion waits on its verdict."]) ],
 nums=[("G1 cost", "~$0.5B ($582M ±30%, deposited breakdown)"),
       ("Mission", "adjudicate P1–P7 pre-registered predictions"),
       ("Highest-leverage gates", "H98 band · P6 two-fluid · DEC chain"),
       ("Criteria", "fixed before first plasma"),
       ("Capital discipline", "FOAK waits on the verdict")],
 gap="G1's own engineering design is programme scope, not part of the deposited plant physics; its "
     "budget is a bottom-up estimate carried at ±30%."),

dict(n=31, series=C, slug="beyond-the-grid",
 title="Beyond the Grid: Hydrogen, Heat, and Off-Take Flexibility",
 sub="A firm gigawatt is a platform. Electricity is only its first product.",
 lead="MetroVolt's output profile — large, steady, and sited where industry already is — matches the "
      "emerging demand stack beyond the meter: electrolytic hydrogen, industrial heat integration, "
      "and 24/7 clean supply for compute campuses.",
 secs=[("The science", [
   "The series' market analysis prices the adjacencies with published anchors: firm-power prints from "
   "2024–26 markets and hydrogen economics where a 0.61–0.84 GWe unit runs an electrolyzer fleet at "
   "the capacity factors that dominate hydrogen cost. Because the plant's front end is electrical "
   "(DEC train) rather than purely thermal, load-following between grid export and behind-the-fence "
   "off-take is a control decision, not a retrofit.",
   "The same compactness that lowers capex shortens the distance to co-located demand — the plant "
   "fits inside industrial parks that a large thermal station never could."]),
  ("Why it matters", [
   "Multiple off-takes de-risk revenue: when grid prices soften, hydrogen or compute contracts firm "
   "the book. For a first fleet, that optionality is worth real basis points on financing — and it is "
   "native to the architecture rather than bolted on."]) ],
 nums=[("Unit output", "0.61–0.84 GWe, firm"),
       ("Off-take modes", "grid · hydrogen · industrial/compute"),
       ("Switching", "electrical front end — control, not retrofit"),
       ("Market anchors", "2024–26 firm-power & H₂ prints (cited)"),
       ("Siting", "industrial-park compatible footprint")],
 gap="Adjacent-market economics inherit the same physics gates as the core plant, and hydrogen "
     "competitiveness depends on regional power and policy prices the series cites but cannot fix."),

dict(n=32, series=C, slug="compact-siting",
 title="Compact Footprint, Big Siting Freedom",
 sub="The best site for new firm power is the one that already has wires — and now it can be.",
 lead="A tokamak core of major radius 5.75 m — the whole confinement device measured in meters, not "
      "hectares — changes what counts as a candidate site: brownfields, retiring plant footprints, "
      "industrial campuses.",
 secs=[("The science", [
   "Compactness is engineered, not asserted: the radial build closes at 1.31 m consumed of 1.73 m "
   "available (0.42 m spare, verified in the systems closure), the shield reaches its attenuation "
   "target at ≈1.20 m, and the low-neutron source term shrinks both the activation footprint and the "
   "emergency-planning conversation. Sub-kilogram tritium inventory (a design rule) keeps the "
   "radiological site envelope modest.",
   "The balance of plant is correspondingly lean — the DEC train displaces much of the steam-cycle "
   "acreage — so the binding siting constraints become interconnect capacity and cooling, both of "
   "which retiring thermal sites already own."]),
  ("Why it matters", [
   "Interconnection queues, not turbines, pace new firm power in most markets. A plant that re-uses "
   "existing grid injection points and industrial land skips years — and community acceptance starts "
   "from 'the site your town already hosts,' the easiest version of that conversation."]) ],
 nums=[("Machine scale", "R₀ 5.75 m · a 2.875 m"),
       ("Radial build", "1.31 of 1.73 m (0.42 m spare)"),
       ("Tritium site inventory", "< 1 kg (design rule)"),
       ("Steam-cycle acreage", "reduced (DEC-led front end)"),
       ("Target sites", "retiring thermal · brownfield · industrial")],
 gap="Site-specific licensing and cooling studies are, by nature, per-project work; the series "
     "establishes the envelope (source terms, footprint, inventory) those studies will start from."),
]

PAPERS += [
dict(n=33, series=D, slug="open-validation-manifest",
 live=("deposit.html","Browse the live deposit page &mdash; every S-number one click from its script"),
 title="81 Simulations, Zero Secrets: The Open Validation Manifest",
 sub="Our design's evidence isn't summarized on our website. It is downloadable from it.",
 lead="Every design-defining number in MetroVolt traces to a keyed entry in an 81-analysis manifest "
      "(S01–S81), deposited in the open under a permanent DOI — inputs, code, outputs, and the "
      "acceptance criteria we set before running.",
 secs=[("The science", [
   "The structure is deliberately two-tier and honest: 48 Tier-1 analyses computed by the deposited "
   "reduced-order engines with measured values and pass/fail verdicts; 24 Tier-2 runnable input decks "
   "for the community's flagship codes (CGYRO, OpenMC, ASCOT5, DREAM, TGLF) carrying frozen parameters "
   "and pre-registered acceptance criteria; 4 named decision gates; and 5 clearly quarantined "
   "design-space studies. 76 validation analyses plus 5 explorations: 81 in all, one manifest mapping "
   "every S-number to its files.",
   "The bound validation-package PDF is the human-readable companion; MANIFEST.md is the machine-"
   "readable spine; CC BY 4.0 is the license. Nothing about the design lives only in prose."]),
  ("Why it matters", [
   "Fusion claims usually ask for trust; this one asks for a code review. Referees, rivals, and "
   "customers all download the same evidence — which converts scrutiny from a threat into free "
   "verification. In a field of press releases, an auditable manifest is the differentiation."]) ],
 nums=[("Total register", "81 analyses (S01–S81)"),
       ("Composition", "48 Tier-1 · 24 Tier-2 decks · 4 gates · 5 design-space"),
       ("Flagship codes decked", "CGYRO · OpenMC · ASCOT5 · DREAM · TGLF"),
       ("License", "CC BY 4.0, permanent DOI"),
       ("Human companion", "bound 81-simulation validation package")],
 gap="Tier-2 decks are confirmations pending HPC execution — deposited so the community can run them "
     "before we do. The manifest's honesty is structural: adverse findings hold register rows too."),

dict(n=34, series=D, slug="run-it-yourself",
 live=("index.html","Watch the boot check re-derive the frozen numbers before the controls unlock"),
 title="Run It Yourself: 43 Scripts, One Command, Same Numbers",
 sub="Reproducibility isn't a promise in our methods section. It's a shell command.",
 lead="Download the deposit, run one command, and 43 Tier-1 scripts re-derive the design's numbers on "
      "your laptop — 43 OK, 0 failures, outputs matching the deposited CSVs.",
 secs=[("The science", [
   "The deposit ships its own verification harness: run_all.py executes every Tier-1 analysis — "
   "equilibrium, burn physics, kinetics, neutronics ledgers, power balance, even the LCOE table "
   "generator — and reports pass/fail against the deposited outputs. The certified line is 43 OK / "
   "0 FAIL (with 4 external-code items skipped by design), and the suite has been re-certified after "
   "every revision of the series.",
   "Reproduction is byte-serious: outputs are compared file-by-file, and when a reviewer-grade check "
   "found a single script whose rerun appended rather than rewrote its CSV, the bug and its fix went "
   "into the public record like everything else."]),
  ("Why it matters", [
   "The cheapest due diligence in energy is rerunning our math — we made sure of it. Every "
   "journalist's 'how do we know?' has a literal answer: python3 run_all.py. Institutions that "
   "cannot audit a plasma can still audit a pipeline, and that is the trust bridge fusion has been "
   "missing.",
   "And if you don't want to install anything: the same engine now runs live in your browser at "
   "kronosfusionenergy.com/live — WebAssembly Python, the deposited coefficients verbatim, and it "
   "re-derives the frozen numbers in front of you before a single slider unlocks."]) ],
 nums=[("Verification harness", "run_all.py, in the deposit"),
       ("In-browser edition", "kronosfusionenergy.com/live"),
       ("Certified result", "43 OK / 0 FAIL (4 external skips)"),
       ("Comparison", "file-by-file against deposited outputs"),
       ("Dependencies", "Python + open libraries (FreeGS et al.)"),
       ("Re-certified", "after every series revision")],
 gap="Tier-1 reproduction validates our reduced-order chain, not nature; the flagship-code decks and "
     "the G1 hardware gates are where nature votes."),

dict(n=35, series=D, slug="gates-not-vibes",
 title="Gates, Not Vibes: How MetroVolt Adjudicates Its Own Risks",
 sub="Every fusion design has open questions. Ours have names, numbers, and referees.",
 lead="MetroVolt's method is gate adjudication: each governing uncertainty is assigned to a named "
      "gate with pre-registered acceptance criteria, and design credit is only booked on the side of "
      "the gate that has already closed.",
 secs=[("The science", [
   "Four decision gates anchor the register — confinement (S18), the hot-ion two-fluid balance (S26), "
   "and the DEC exhaust chain (S51/S65) — plus seven pre-registered predictions (P1–P7) that the G1 "
   "testbed will adjudicate. Where a gate has closed against ambition, the design moved: S26/S72 "
   "demoted hot-ion operation to gated upside and made near-thermal the baseline.",
   "The mechanism's teeth are pre-registration: criteria are frozen and deposited before results "
   "exist, so neither we nor our reviewers can move goalposts afterward. The register's DS-tier rows "
   "(design-space) are barred by rule from altering the frozen point they explore."]),
  ("Why it matters", [
   "Investors call this staged risk retirement; scientists call it falsifiability; both fund it more "
   "readily than confidence. The gate ledger also makes progress legible — each closure is a discrete, "
   "verifiable value step, not another optimistic press cycle."]) ],
 nums=[("Named gates", "S18 · S26 · S51/S65 (+ P1–P7 at G1)"),
       ("Criteria", "pre-registered, deposited before results"),
       ("Design consequence example", "hot-ion → gated upside (S26/S72)"),
       ("Design-space rule", "explore only; frozen point immutable"),
       ("Where value moves", "one gate closure at a time")],
 gap="Two governing gaps remain open by the series' own statement — required confinement and the "
     "two-fluid balance. The gates exist because the answers do not, yet."),

dict(n=36, series=D, slug="adverse-findings-kept",
 title="The Findings We Kept That Hurt: Adverse Results in the Register",
 sub="You can tell a validation programme is real by what it publishes against itself.",
 lead="MetroVolt's register keeps its wounds: the δ-scan that refused to flatter deeper shaping, the "
      "robustness scan that named plasma current unforgiving, the breeding analysis that came back "
      "negative. They are deposited beside the favourable results, same format, same prominence.",
 secs=[("The science", [
   "S77 tested the reviewer-suggested deeper-triangularity lever and reported the adverse trend: "
   "safety factor falls with |δ|, so the frozen point already sits at the favourable end. S79's "
   "excursion matrix found B-field shortfalls recoverable but a 10% plasma-current shortfall not "
   "recoverable by density trim — 'least forgiving parameter' is our phrase, in our deposit. §3.5 "
   "computed prompt ³He breeding at ratio ≥1 as not achievable, forcing the staged supply strategy. "
   "The shield ledger carries its conductor-fluence line ~8% above a degradation onset, flagged rather "
   "than smoothed.",
   "Even the near-thermal baseline's confinement requirement — the design's hardest single number — "
   "was moved to the top of the published band (≈2.2) when the systems code said so."]),
  ("Why it matters", [
   "Selection bias is the quiet killer of technical credibility. A register that demonstrably retains "
   "its negative results converts every positive result into stronger evidence — reviewers know "
   "nothing was curated out. In diligence, our adverse findings are load-bearing assets."]) ],
 nums=[("Adverse δ-scan", "S77 — deeper shaping costs q95"),
       ("Unforgiving parameter", "Ip −10% unrecoverable (S79)"),
       ("Breeding ≥ 1", "computed negative (§3.5)"),
       ("Flagged margin", "conductor fluence ~8% above onset"),
       ("Baseline H98 posture", "≈2.2 — top of band, stated")],
 gap="This paper is the gap statement. The other 39 are honest because keeping results like these is "
     "the programme's operating rule, not its exception."),

dict(n=37, series=D, slug="regulated-like-fusion",
 title="Regulated Like Fusion, Not Fission: The 2026 Framework",
 sub="For the first time in the industry's history, the licensing path matches the physics.",
 lead="The U.S. fusion-specific regulatory framework (Federal Register 91(38), February 26, 2026) "
      "regulates fusion machines under the byproduct-materials regime — a risk-informed path built "
      "for what fusion actually is, and one that fits MetroVolt unusually well.",
 secs=[("The science", [
   "Fission licensing exists because of criticality, meltdown decay heat, and bulk actinide "
   "inventories; fusion has none of the three, and now the rulebook says so. Under the framework, "
   "the licensing conversation centers on the actual source terms: tritium inventory, activation "
   "products, and effluents.",
   "That is where MetroVolt's fuel choice compounds: sub-kilogram site tritium (a design rule), "
   "~25× lower structural activation than a D-T comparator, a low-level-waste decommissioning "
   "pathway, and a 5.25% neutron budget shrinking the shielding and dose analysis the application "
   "must carry. The series maps each source term to its deposited analysis."]),
  ("Why it matters", [
   "Regulatory schedule is a first-order cost driver for any first-of-a-kind plant. A "
   "byproduct-materials path, entered with the smallest source terms in the fusion field and an "
   "auditable analysis behind each one, is a licensing story measured in years — not the decade-class "
   "sagas that priced fission out of new builds."]) ],
 nums=[("Framework", "Federal Register 91(38), 26 Feb 2026"),
       ("Regime", "byproduct materials (risk-informed)"),
       ("MetroVolt source terms", "<1 kg T · ~25× lower activation · LLW path"),
       ("Neutron budget entering analysis", "5.25%"),
       ("Basis", "each source term → deposited analysis")],
 gap="Framework implementation and state-agreement details continue to evolve; the series cites the "
     "rule as published and keeps MetroVolt's source-term analyses independent of any particular "
     "implementation outcome."),

dict(n=38, series=D, slug="aegis-defense-energy",
 title="AEGIS: Energy Assurance for Defense Missions",
 sub="The same physics that makes clean baseload makes something rarer — energy sovereignty at the installation scale.",
 lead="AEGIS is Kronos Fusion Energy's defense product line: the company's openly published physics basis, packaged "
      "for national-security missions where fuel convoys, grid fragility, and multi-decade siting "
      "certainty are the operative constraints.",
 secs=[("The science", [
   "The attributes defense planners price are native to the low-neutron architecture: fuel-secure "
   "operation measured in years (helium-3 mass, not fuel convoys), sub-kilogram tritium inventory "
   "and a low-level-waste pathway compatible with installation environmental postures, compact "
   "footprint suited to secured perimeters, and an electrical (DEC-led) front end with the response "
   "characteristics microgrids and directed-load missions demand.",
   "AEGIS inherits the entire open validation discipline — the same 81-analysis register, gates, and "
   "reproducibility harness behind the commercial line — because a defense customer's diligence is the "
   "most demanding kind."]),
  ("Why it matters", [
   "Installation energy resilience is a stated national-security requirement, and firm, fuel-secure, "
   "grid-independent generation at the 0.5–1 GW scale has no incumbent solution. AEGIS positions the "
   "MetroVolt physics where the value of assurance is highest and procurement rewards documented "
   "rigor — the register is the compliance package."]) ],
 nums=[("Product line", "AEGIS (defense) — shared open physics basis"),
       ("Fuel logistics", "years of ³He by mass; no convoy dependence"),
       ("Site posture", "<1 kg tritium · LLW pathway · compact core"),
       ("Grid mode", "islandable, electrical front end"),
       ("Diligence package", "the same open 81-analysis register")],
 gap="AEGIS mission engineering (hardening, integration, security accreditation) is programme scope "
     "beyond the deposited plant physics; the physics gates are identical to the commercial line and "
     "close on the same schedule."),

dict(n=39, series=D, slug="gate-roadmap",
 title="From Paper to Power: The MetroVolt Gate Roadmap",
 sub="The plan is public: close the gates, in order, in the open.",
 lead="MetroVolt's roadmap is the same document as its risk register. Each stage exists to close "
      "named gates, and each closure is verifiable by anyone holding the deposit.",
 secs=[("The science", [
   "Now: the combined design paper and its 81-analysis deposit are public; the reproduction suite "
   "certifies 43/43; flagship-code decks await HPC allocations — community groups can run them "
   "before we do. Next: Tier-2 execution retires the simulation-side gates (nonlinear confinement "
   "S13/S18, exhaust S51, disruption S30). Then G1 — the ~$0.5B gate testbed — adjudicates the "
   "pre-registered P1–P7 on hardware, led by the confinement band and the two-fluid balance.",
   "Only then does FOAK capital deploy against the $3.15B bill of materials, with the Wright's-law "
   "fleet ladder ($84–92 FOAK → $48–56 fleet) taking over as the operative curve."]),
  ("Why it matters", [
   "Every stage has a falsifiable exit criterion set in advance, so progress is measured in gates "
   "closed rather than announcements made. Partners can enter at the risk tier that suits them — "
   "HPC collaboration today, G1 participation next, fleet offtake after — all against one continuous, "
   "public evidence chain."]) ],
 nums=[("Today", "series + deposit public · 43/43 reproduction"),
       ("Next", "Tier-2 HPC decks (S13/S18 · S51 · S30)"),
       ("Then", "G1 testbed ~$0.5B — P1–P7 adjudication"),
       ("After gates", "FOAK ($3.15B BOM) → fleet ladder"),
       ("Progress metric", "gates closed, publicly checkable")],
 gap="Dates are deliberately absent: a gated roadmap sequences on evidence, not calendars. The two "
     "governing physics gaps are the schedule's honest drivers."),

dict(n=40, series=D, slug="readers-guide",
 title="Start Here: A Reader's Guide to the Four-Paper Series",
 sub="Forty whitepapers summarize it. Four papers prove it. One deposit lets you check it.",
 lead="The Kronos MetroVolt series is a single machine described end-to-end in four self-contained, "
      "cross-referenced papers — every claim traceable to the open 81-analysis deposit. Here is the "
      "map.",
 secs=[("The series", [
   "Part 1 — Integrated Design Basis: the frozen point, the consistency chain, the risk register, and "
   "the honesty rules everything else obeys. Part 2 — Confinement, Stability, and Current Drive: the "
   "H98 band, negative-triangularity physics, MHD limits, the 42.5 MA discipline. Part 3 — Fuel "
   "Cycle, Neutronics, and Magnets/Shield: helium-3 strategy, the 5.25% neutron budget and its "
   "dividends, REBCO magnets at 24.6 T, the multigroup shield. Part 4 — Direct Energy Conversion, "
   "Balance of Plant, and Economics: the two-posture power ledger, availability, the cost ladder and "
   "required-PPA band.",
   "Around them: the combined preprint, the bound 81-simulation validation package, and the Zenodo "
   "deposit with MANIFEST.md mapping every S-number to runnable files."]),
  ("How to check us", [
   "Skeptics start with the deposit's run_all.py (43 scripts, one command). Physicists start with the "
   "Tier-2 decks for their own code. Economists start with the S63 ladder script. Everyone else can "
   "start with whitepaper 33 — the manifest tour — and follow curiosity from there."]) ],
 nums=[("Part 1", "design basis · frozen point · risk register"),
       ("Part 2", "confinement · stability · current drive"),
       ("Part 3", "fuel cycle · neutronics · magnets & shield"),
       ("Part 4", "conversion · plant · economics"),
       ("The check", "DOI 10.5281/zenodo.21248916 — run it")],
 gap="Whitepapers are summaries with a marketing mandate; where any nuance here and the series "
     "disagree, the series and its deposit are the record."),
]

INDEX = """<!DOCTYPE html><html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Whitepaper Library — Kronos Fusion Energy</title><style>{css}
.idx a{{color:var(--ink);text-decoration:none}} .idx a:hover{{color:var(--acc)}}
.idx .it{{margin:7px 0;font-size:15.5px}} .idx .no{{font-family:Verdana,Arial,sans-serif;font-size:11px;color:var(--acc);margin-right:8px}}
.idx .st{{color:var(--mut);font-style:italic;font-size:13.5px;display:block;margin-left:34px}}</style></head>
<body><div class="page idx">
<div class="brand"><span>KRONOS <b>FUSION</b> ENERGY</span><span>WHITEPAPER LIBRARY</span></div>
<div class="eyebrow">Website publications</div>
<h1>The MetroVolt Whitepaper Library</h1>
<div class="sub">Forty short papers — 60% science, 40% why-it-matters — each traceable to the open
81-simulation deposit (DOI {doi}).</div>
{groups}
<div class="cta">Prefer the full record? The combined design paper, the bound validation package, and all
code and data live at <a href="https://doi.org/{doi}">DOI {doi}</a> (CC BY 4.0).</div>
<div class="foot">&copy; 2026 Kronos Fusion Energy, Los Angeles. Conceptual design study; see any
paper's footer for the standing disclosures.</div>
</div></body></html>"""

if __name__ == "__main__":
    assert len(PAPERS) == 40, f"expected 40 papers, have {len(PAPERS)}"
    ns = [p["n"] for p in PAPERS]
    assert ns == list(range(1, 41)), "numbering must be 1..40"
    assert len(set(p["slug"] for p in PAPERS)) == 40, "slugs must be unique"
    for p in PAPERS:
        fn = f"KFE-WP{p['n']:02d}_{p['slug']}.html"
        with open(os.path.join(HERE, fn), "w", encoding="utf-8") as f:
            f.write(render(p))
    groups = ""
    for s in (A, B, C, D):
        groups += f'<h2>{s}</h2>'
        for p in PAPERS:
            if p["series"] == s:
                fn = f"KFE-WP{p['n']:02d}_{p['slug']}.html"
                groups += (f'<div class="it"><span class="no">{p["n"]:02d}</span>'
                           f'<a href="{fn}">{html.escape(p["title"])}</a>'
                           f'<span class="st">{html.escape(p["sub"])}</span></div>')
    with open(os.path.join(HERE, "index.html"), "w", encoding="utf-8") as f:
        f.write(INDEX.format(css=CSS, doi=DOI, groups=groups))
    print(f"wrote 40 whitepapers + index.html in {HERE}")
