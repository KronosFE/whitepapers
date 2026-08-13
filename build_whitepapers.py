#!/usr/bin/env python3
"""
build_whitepapers.py — Kronos Fusion Energy website whitepaper set (100 papers).

Design-and-physics only. NO economics, ROI, capital, LCOE, margins, valuation, funding, or fuel
prices appear anywhere in this set (founder rule: those live in the confidential data room, never on
the public site). Every quantitative claim is grounded in the frozen canon of 2026-07-31:

  * Hyperion (breeder, spherical tokamak, D-T · internal Mode D2): design point P_fus 88.7 MW,
    Q 3.424, Ip 9.86 MA, R_0 1.2 m, A 2.5, TBR 1.8, ash basis f_He4 = 0.05 (Z_eff 1.158), heating power
    density 2.37 MW/m3 (2.22x SPARC), Q_plasma ~1.9 at demonstrated H98 = 1.0; first-wall neutron
    loading 1.966 MW/m2. STEADY-STATE, CF damage-life-limited 0.58-0.83 (central 0.69). Mode D2 adds an
    ENVIRONMENTAL DESIGN LAYER (physics unchanged from D1): low-activation RAFM steel -> waste <= Class C
    for the listed 10 CFR 61.55 isotopes AT a certified low-activation heat (Nb<10ppm; D2-44), public
    dose CLOSES at detritiation factor 1-34 vs ITER-class 1,000-10,000 (D2-45), remote federal siting,
    emergency plan required (D2-41). Ag-108m residual + curie inventory NOT frozen (open).
  * Aegis / MetroVolt (one D-3He magnetic mirror, two housings · internal Mode M): LOCKED Mode M closing
    point (M-45, reproducible on the deposit's own solver) -- Q_E 1.31 and f_n 5.44% (both LENGTH-
    INDEPENDENT, H69) at n_p/n_c=16, x(He3)=0.30, Ti=90 keV, ne=2.6e20 m^-3, B_m 17 T, beta_c 0.55,
    a_c 0.86 m. Net electric SCALES with central-cell length: +104 / +850 / +2832 MWe at l_c
    55 / 440 (Aegis) / 1400 (MetroVolt) m; P_fus 0.54 / 4.3 / 13.7 GW. MANDATORY caveat that travels
    with the number (M-47): closure is REQUIREMENT-class, NOT demonstrated -- it needs end-plug density
    n_p/n_c ~16 (plug density 4.16e21 m^-3 = 347x GDT-measured / 26x the best published mirror design,
    H53's largest open item); at n_p/n_c=10 the machine does NOT close (Q_E 0.63, net -160 MWe). Fuel-
    cleanliness TRAJECTORY (M-46): closes across x(He3) in [0.20, ~0.43]; f_n falls 9.53% -> 2.77% (~3.4x);
    free clean-shift x=0.30 -> 0.35 (f_n 5.44% -> 4.18%); near-aneutronic x>=0.45 does NOT close (redesign,
    not a fuel change). LOW-NEUTRON, never aneutronic. CF plug-limited (first-wall life 104-428 fpy ->
    ~0.035-0.144 changes in 30 yr, M-42). throat field 17 T (WHAM HTS), beta 0.55 (GDT 0.5-0.6). Specific
    length/power/He-3 product cards deliberately omitted. WITHDRAWN (do NOT quote): burner Q_E 1.002 /
    1.191 / 1.825 and net +2.78 / +128.5 / +363 MWe (M22/M-40/M-44 withdrawn 2026-08-02, non-reproducible).

Mode D2/M evolution (2026-08-02): the next step from D1/L, driven by BETTER ENVIRONMENTAL performance and
BETTER ECONOMICS, NOT new physics -- same closed physics, a cleaner and more durable machine. The hard,
novel work (a solved power balance at demonstrated confinement) is DONE and frozen; the rest (economics,
public dose, waste class) is standard engineering with known solutions. Messaging invariants honored:
"low-neutron" never "aneutronic"; named gates not hidden assumptions; labeled history kept. Palette +
type per KRONOS_DESIGN_SYSTEM.md section 2/3 (web paper family).

Run:  python3 build_whitepapers.py   -> writes 100 HTML files + index.html next to this script.
"""
import os, html, re

# Escape <, >, and bare & (not part of a valid HTML entity), while PRESERVING
# author-written entities like &mdash; &sup2; &ge; in short fields (titles, subs,
# nums cells). Plain html.escape() double-escapes those entities into visible
# "&sup2;" text; this keeps literal < > safe AND lets entities render as symbols.
def esc(s):
    s = str(s).replace('<', '&lt;').replace('>', '&gt;')
    return re.sub(r'&(?!(?:[a-zA-Z][a-zA-Z0-9]*|#[0-9]+|#x[0-9a-fA-F]+);)', '&amp;', s)

HERE = os.path.dirname(os.path.abspath(__file__))
DEPOSIT = "the openly deposited Kronos simulation programme and design-point records (CC BY 4.0)"

CSS = """
:root{--ink:#101724;--mut:#5a6472;--acc:#b8882e;--line:#d9dce2;--wash:#f7f6f2;--navy:#12233f}
*{margin:0;padding:0;box-sizing:border-box}
body{font-family:Georgia,'Times New Roman',serif;color:var(--ink);background:#fff;line-height:1.62}
.page{max-width:820px;margin:0 auto;padding:56px 28px 40px}
.brand{font-family:Verdana,Arial,sans-serif;font-size:11px;letter-spacing:3px;color:var(--navy);
  border-bottom:2px solid var(--navy);padding-bottom:10px;display:flex;justify-content:space-between}
.brand b{color:var(--acc)}
a.back{font-family:Verdana,Arial,sans-serif;font-size:10.5px;letter-spacing:1.5px;color:var(--mut);
  text-decoration:none;text-transform:uppercase;display:inline-block;margin-top:18px}
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
<div class="brand"><span>KRONOS <b>FUSION</b> ENERGY</span><span>WHITEPAPER {n:03d} / {total}</span></div>
<div class="eyebrow">{series}</div>
<h1>{title}</h1>
<div class="sub">{sub}</div>
<p class="lead">{lead}</p>
{body}
<div class="nums"><h3>The numbers</h3><table>{numrows}</table></div>
<div class="gap"><b>Straight answers</b>{gap}</div>
<div class="cta">Kronos is the fusion company that shows its work. Every figure here traces to {deposit}.
Read the series, run the code, check us. &mdash; <a href="index.html">All whitepapers</a></div>
<div class="foot">Conceptual design and simulation study; no machine has been built. Quantitative values
are simulation-derived and carry the feasibility gates named in the text; superseded values are kept
in the record with era labels. This document is informational and is not an offer of securities.
&copy; 2026 Kronos Fusion Energy, Inc. &middot; Los Angeles, California.</div>
<a class="back" href="index.html">&larr; Back to the whitepaper library</a>
</div></body></html>"""

def render(p, total):
    body = "".join("<h2>%s</h2>" % esc(h) + "".join("<p>%s</p>" % t for t in ps)
                   for h, ps in p["secs"])
    rows = "".join("<tr><td>%s</td><td>%s</td></tr>" % (esc(k), esc(v))
                   for k, v in p["nums"])
    return PAGE.format(css=CSS, n=p["n"], total=total, series=esc(p["series"]),
                       title=esc(p["title"]), sub=esc(p["sub"]),
                       lead=p["lead"], body=body, numrows=rows, gap=p["gap"], deposit=DEPOSIT)

A = "Hyperion — The Breeder"
B = "The Burner — Aegis & MetroVolt"
C = "Low-Neutron by Design"
D = "Direct Energy Conversion & Power Handling"
E = "The Fuel Cycle — Tritium & Helium-3"
F = "Method, Safety & Trust"
G = "The Mode D2/M Evolution — Cleaner and More Durable"

def wp(series, slug, title, sub, lead, secs, nums, gap):
    return dict(series=series, slug=slug, title=title, sub=sub, lead=lead, secs=secs, nums=nums, gap=gap)

PAPERS = []

# ---------------------------------------------------------------------------
# SERIES A — Hyperion (breeder, spherical tokamak, D-T) — 20 papers
# ---------------------------------------------------------------------------
PAPERS += [
wp(A, "breeder-first",
 "The Machine That Fathers the Sun-Fuel: Why Kronos Builds the Breeder First",
 "Every fusion economy needs a fuel supply before it needs a power plant. Hyperion is the fuel supply.",
 "Hyperion is a compact deuterium-tritium spherical tokamak whose product is not electricity but "
 "materials: tritium, helium-3, and 14 MeV neutrons. It is named for the Titan who fathered Helios "
 "the sun &mdash; the machine that fathers the fuel everything after it burns.",
 [("The idea",
   ["The hardest bottleneck in a helium-3 fusion economy is not the reactor; it is the helium-3. "
    "Kronos resolves the sequence by building a breeder first: a machine whose job is to make the "
    "scarce inputs, sized to a real requirement rather than a physics optimum. Hyperion requires "
    "fusion gain only &mdash; no net-electricity milestone &mdash; at confinement consistent with "
    "what the field has already demonstrated."]),
  ("Why it matters",
   ["Ordering the programme this way turns the burner's fuel dependency from a hope into a schedule: "
    "a decade of breeder production supplies the demonstrator that follows. The design bar is "
    "deliberately modest &mdash; gain, not closure &mdash; which is what makes Hyperion the "
    "near-term, buildable member of the family."])],
 [("Machine", "spherical tokamak, D-T fuel"), ("Physics bar", "fusion gain only (no Q_E>1)"),
  ("Product streams", "tritium, helium-3, 14 MeV neutrons"), ("Design gain Q", "3.424 (computed)"),
  ("Role", "near-term fuel foundry")],
 "Hyperion does not generate electricity, and it is not meant to. Its economics are stated honestly "
 "elsewhere as conditional on one thing no simulation can settle &mdash; the government contracting "
 "instrument &mdash; which is a conversation, not an experiment."),

wp(A, "spherical-tokamak-a25",
 "Small by Geometry: The Aspect-Ratio-2.5 Spherical Tokamak",
 "A fatter torus wins more plasma pressure from every tesla &mdash; that is the whole compactness case.",
 "Hyperion's plasma is a squat torus: major radius 1.2 m, aspect ratio 2.5. Low aspect ratio is not "
 "styling; it is the geometric lever that lets a small machine hold reactor-relevant pressure.",
 [("The science",
   ["Normalized plasma pressure per unit field rises as the torus grows fatter. A low-aspect-ratio "
    "spherical tokamak therefore reaches useful fusion conditions in a build envelope existing "
    "industry can fabricate, at a plasma current a fraction of the giant tokamaks'. Hyperion exploits "
    "that lever deliberately, because the breeder's value is buildability, not record-setting."]),
  ("Why it matters",
   ["Machine volume drives everything downstream &mdash; fabrication, siting, schedule. Keeping R_0 at "
    "1.2 m puts Hyperion inside precedent set by compact HTS devices already built, which is why the "
    "programme can talk about a four-year build with a straight face."])],
 [("Major radius R_0", "1.2 m"), ("Aspect ratio A", "2.5"),
  ("Machine class", "compact spherical tokamak"), ("Fabrication", "existing heavy industry"),
  ("Design intent", "buildability over optimum")],
 "Compactness closes as a system only when every constraint is checked together; Hyperion's design "
 "point is published so the geometry can be audited, not admired."),

wp(A, "gain-solved-not-scaled",
 "Solved, Not Scaled: Where Q = 3.424 Actually Comes From",
 "The most important thing about Hyperion's gain is how it was obtained, not how large it is.",
 "Hyperion's fusion gain, Q = 3.424, is computed from a power balance at the machine's own operating "
 "point &mdash; not extrapolated from a scaling law anchored to somebody else's reactor. That "
 "distinction is the single most protective statement in the whole design record.",
 [("The science",
   ["Fusion concepts routinely quote a gain by taking a demonstrated machine's Q and rescaling it by a "
    "power law in size. That procedure hides the anchor: change the reference machine and the number "
    "moves. Hyperion instead solves its own coupled power balance, so the gain is a property of this "
    "plasma at this operating point."]),
  ("Why it matters",
   ["A gain that is solved can be reproduced from the deposited inputs; a gain that is scaled can only "
    "be trusted. The Kronos record even preserves the earlier scaled figure it withdrew, so anyone can "
    "see exactly which class of error the freeze on 'solved, not scaled' was written to prevent."])],
 [("Design gain Q", "3.424 (power-balance solve)"), ("Method", "coupled balance at the operating point"),
  ("Not", "a size-scaled extrapolation"), ("Basis", "declared ash f_He4 = 0.05 (Z_eff 1.158)"),
  ("Record", "withdrawn scaled value kept, labeled")],
 "The frozen 3.424 is conditional on a declared ash fraction (f_He4 = 0.05). If the true ash is lower, "
 "gain rises &mdash; the frozen value is a floor, not a ceiling &mdash; and any change moves by "
 "recorded restatement, never silently."),

wp(A, "design-point",
 "The Breeder's Design Point, on One Card",
 "One operating point, every subsystem checked against the same numbers.",
 "Hyperion's design point is a single card: 88.7 MW of fusion power at Q = 3.424, R_0 1.2 m, aspect "
 "ratio 2.5, tritium breeding ratio 1.8. The whole programme interrogates this one point rather than "
 "quietly re-tuning it chapter to chapter.",
 [("The science",
   ["A design that lets each subsystem flatter itself becomes a machine no single analysis ever "
    "checked. Hyperion's card fixes the geometry, the gain, and the breeding ratio at once, and every "
    "derived quantity &mdash; power density, tritium yield, neutron rate &mdash; is computed against "
    "that fixed point."]),
  ("Why it matters",
   ["A fixed card is what makes 'check us' a real offer: rerun the deposit and you land on the same "
    "88.7 MW, the same Q, the same breeding ratio. For partners and reviewers, an auditable design is "
    "the product."])],
 [("Fusion power P_fus", "88.7 MW"), ("Fusion gain Q", "3.424"), ("Plasma current Ip", "9.86 MA"),
  ("Major radius R_0", "1.2 m"), ("Aspect ratio A", "2.5"), ("Tritium breeding ratio", "1.8")],
 "The card is a computed design point, not a built machine. Its confinement requirement is modest by "
 "design (H98 = 1.0), which is precisely why Hyperion is the buildable, near-term member of the family."),

wp(A, "one-third-iter-current",
 "9.86 Million Amps: Current as a Buildability Choice",
 "Plasma current is the hardest engineering bill in a tokamak, and Hyperion's is set by its compact geometry.",
 "Hyperion runs 9.86 MA of plasma current (8.36 MA driven) &mdash; the frozen design-point value. That "
 "is well below the mega-amp plasmas of the flagship tokamaks, and it is a consequence of compact "
 "spherical-tokamak geometry rather than a stretch: lower current means lower stored energy and gentler "
 "disruptions.",
 [("The science",
   ["A spherical tokamak reaches useful plasma pressure at lower current than a conventional aspect "
    "ratio, so Hyperion buys its fusion conditions at 9.86 MA rather than the tens of mega-amps a "
    "larger, higher-aspect machine would need. The lower the current, the smaller the disruption energy "
    "the structure must survive."]),
  ("Why it matters",
   ["Current sets the disruption budget and the magnet ambition together. Holding it to 9.86 MA on a "
    "compact machine is how the breeder stays inside demonstrated engineering rather than betting on a "
    "first-of-its-kind coil set."])],
 [("Plasma current Ip", "9.86 MA (8.36 driven)"),
  ("Consequence", "lower disruption energy"), ("Magnet ambition", "inside precedent"),
  ("Design goal", "buildability"), ("Machine", "compact spherical tokamak")],
 "9.86 MA is the frozen design-point value (H01). An older founder-boilerplate framing of "
 "'one-third of ITER's current' (~4.9 MA) does not match this frozen figure and is being corrected "
 "across the product-facing material to the frozen value."),

wp(A, "power-density",
 "Denser Than SPARC: Heating Power Density as the Real Metric",
 "How hard a fusion core works is measured per cubic metre, and Hyperion works hard.",
 "Hyperion's heating power density is 2.37 MW/m&sup3; &mdash; 2.22 times SPARC's &mdash; computed "
 "against built devices, not against a spreadsheet ideal. Power density, not raw megawatts, is the "
 "honest measure of how demanding a compact core is.",
 [("The science",
   ["A small machine that makes real fusion power necessarily runs a high power density. Benchmarking "
    "Hyperion against SPARC &mdash; a device under construction with published parameters &mdash; keeps "
    "the comparison anchored to hardware people can point at, rather than to an unbuilt reference."]),
  ("Why it matters",
   ["Power density sets the thermal and materials duty of the core. Stating it against a real machine "
    "tells reviewers exactly how far beyond demonstrated practice Hyperion reaches, and in which "
    "direction the engineering has to work."])],
 [("Heating power density", "2.37 MW/m&sup3;"), ("Versus SPARC", "2.22x"),
  ("Benchmark", "built / under-construction devices"), ("Fusion power", "88.7 MW"),
  ("Metric role", "true measure of core duty")],
 "A high power density is a demand on cooling and materials, stated plainly. It is computed against "
 "SPARC's published figures so the multiple can be re-derived by anyone."),

wp(A, "confinement-h98-one",
 "No Heroics Required: Confinement at H98 = 1.0",
 "Hyperion's gain does not depend on beating the confinement scaling law &mdash; only on meeting it.",
 "Hyperion reaches Q_plasma ~1.9 at a confinement quality of H98 = 1.0: exactly the standard H-mode "
 "scaling, no enhancement assumed. That is the quietest and most important line in the breeder's case.",
 [("The science",
   ["Most compact-fusion gain claims lean on a confinement multiplier above 1.0 &mdash; a bet that the "
    "plasma holds heat better than the reference law predicts. Hyperion does not need that bet. Its "
    "design point closes at the demonstrated H98 = 1.0, so the gain rests on physics the field has "
    "already shown at scale."]),
  ("Why it matters",
   ["A design that only needs the scaling law it inherits is a categorically lower-risk design than one "
    "that needs to beat it. This is the structural reason the breeder is buildable now while the burner "
    "carries named physics gates."])],
 [("Confinement quality", "H98 = 1.0 (demonstrated)"), ("Q_plasma", "~1.9 at the paper point"),
  ("Enhancement assumed", "none"), ("Risk posture", "meets scaling, does not beat it"),
  ("Contrast", "burner requires named gates")],
 "H98 = 1.0 is what a large body of experiment already supports; Hyperion asks for nothing beyond it, "
 "which is why 'buildable now' is a claim the design record can back."),

wp(A, "tbr-lever",
 "Breeding Ratio Is a Lever, Not a Constant",
 "How much tritium Hyperion makes per tritium burned is a design choice, and the design chose 1.8.",
 "Hyperion's tritium breeding ratio is 1.8 &mdash; but the important claim is that breeding ratio is a "
 "lever the design sets, computed from the blanket scan's own values, not a fixed constant of nature.",
 [("The science",
   ["Tritium breeding ratio depends on blanket geometry, material, and neutron spectrum &mdash; all "
    "design variables. Hyperion's 1.8 comes out of a scan over those variables, so it can be traded "
    "against other requirements rather than quoted as an immovable given."]),
  ("Why it matters",
   ["Treating breeding ratio as a lever is what lets Hyperion be sized to a customer's tritium "
    "requirement instead of to a physics optimum. The surplus above 1.0 is the margin that lets the "
    "machine supply the national requirement and seed the helium-3 stream at once."])],
 [("Tritium breeding ratio", "1.8 (design lever)"), ("Source", "blanket scan values"),
  ("Not", "a fixed constant"), ("Surplus over self-supply", "0.8"),
  ("Enables", "sizing to the requirement")],
 "1.8 is a computed lever setting, not a guarantee of the as-built blanket; the breeding programme is "
 "where that value is demonstrated, and the scan that produced it is deposited."),

wp(A, "three-streams",
 "Three Products From One Plasma: Tritium, Helium-3, Neutrons",
 "Hyperion is a foundry, not a generator &mdash; and it makes three materials the United States cannot source at scale.",
 "A single D-T plasma in Hyperion yields three distinct product streams: tritium for the national "
 "requirement, helium-3 as its decay co-product, and 14 MeV neutrons for materials qualification. The "
 "breeder's value is that all three come off the same machine.",
 [("The science",
   ["D-T fusion is neutron-rich by nature. Hyperion turns that into an asset: the blanket breeds "
    "tritium (breeding ratio 1.8), the tritium decays into helium-3, and the fast-neutron flux is "
    "itself a product for irradiation testing. One core, three streams."]),
  ("Why it matters",
   ["Each stream addresses a genuine supply gap. The programme carries them honestly &mdash; tritium as "
    "the primary product stream, helium-3 as upside, and beam-hours for neutron irradiation carried at "
    "zero because that market is unpriced anywhere in the world &mdash; so no stream is double-counted."])],
 [("Stream 1", "tritium (national requirement)"), ("Stream 2", "helium-3 (decay co-product)"),
  ("Stream 3", "14 MeV neutrons (materials qual)"), ("Breeding ratio", "1.8"),
  ("Neutron beam-hours", "carried unpriced, never banked")],
 "The neutron stream is real physics but has no established market price, so the programme books it at "
 "zero and sweeps it rather than banking speculative value &mdash; the honest treatment of an "
 "unpriced product."),

wp(A, "14mev-neutrons",
 "The 14 MeV Neutron a Mirror Cannot Make",
 "Materials qualification needs fusion-spectrum neutrons, and only the D-T breeder produces them at rate.",
 "Hyperion's D-T fill produces 14 MeV neutrons at full rate &mdash; the fusion-spectrum neutron that "
 "materials qualification actually requires, and the one a low-neutron D-3He mirror deliberately does "
 "not make. This is why the breeder, not the burner, serves the irradiation market.",
 [("The science",
   ["Structural materials for any fusion plant must be qualified against 14 MeV neutrons, whose damage "
    "spectrum differs from fission neutrons. Producing them requires a D-T reaction; the burner's "
    "D-3He cycle is chosen precisely to suppress neutrons, so it cannot serve this need. Hyperion's "
    "D-T fill fills exactly that gap."]),
  ("Why it matters",
   ["The retired standalone neutron-source concept could only reach a fraction of a reference "
    "irradiation facility. Subsuming that role into Hyperion &mdash; where the D-T fill makes 14 MeV "
    "neutrons the 2.45 MeV mirror never could &mdash; turns a weak standalone product into a strong "
    "co-product of the breeder."])],
 [("Neutron energy", "14 MeV (fusion spectrum)"), ("Source", "D-T fill in Hyperion"),
  ("Burner equivalent", "none (low-neutron by design)"), ("Use", "materials qualification"),
  ("History", "standalone neutron-source concept retired into Hyperion")],
 "Old neutron-source figures (0.186 MW fusion, '0.31x a reference facility', 9 m straight-bore mirror "
 "geometry) do NOT transfer to Hyperion and are retired &mdash; the spherical tokamak is a different "
 "machine with a full-rate D-T spectrum."),

wp(A, "tritium-to-requirement",
 "Sized to the Requirement: Tritium at 1.87-4.0 kg/yr",
 "Hyperion is built to a stated national tritium need, not to whatever a physics optimum happens to yield.",
 "Hyperion's tritium output is specified as a range, 1.87 to 4.0 kg per year, sized to the customer's "
 "requirement rather than to a physics maximum. Designing to a requirement is a different discipline "
 "from designing to a peak.",
 [("The science",
   ["Because breeding ratio is a lever, tritium yield can be dialed to a target. Hyperion spans "
    "1.87-4.0 kg/yr by choice, matching the machine to the national requirement instead of chasing the "
    "largest number the plasma could produce."]),
  ("Why it matters",
   ["A requirement-sized machine is a smaller, cheaper, more licensable machine than a maximised one. "
    "It also means the tritium inventory on site stays inside existing civil licensing practice, which "
    "is a schedule advantage, not just a safety one."])],
 [("Tritium output", "1.87-4.0 kg/yr"), ("Sizing basis", "national requirement, not optimum"),
  ("Adjustable via", "breeding-ratio lever"), ("Inventory posture", "inside civil licensing practice"),
  ("Primary stream", "tritium")],
 "The output band is a design choice against a stated requirement; the specific contracted figure is a "
 "commercial matter kept out of the public record. The physics that makes the band achievable is "
 "deposited."),

wp(A, "helium3-coproduct",
 "How a Tritium Machine Makes Helium-3",
 "The burner's scarce fuel is a free decay product of the breeder's primary output.",
 "Helium-3 is Hyperion's co-product: tritium decays into helium-3 with a 12.3-year half-life, so every "
 "kilogram of tritium the breeder makes becomes a helium-3 stockpile over time. The breeder quietly "
 "manufactures the burner's fuel.",
 [("The science",
   ["Tritium is radioactive and decays to helium-3. A tritium inventory is therefore a helium-3 source "
    "that accrues at roughly 0.42 litres of helium-3 per gram of tritium per year. Hyperion's tritium "
    "production thus doubles as a slow, reliable helium-3 accrual."]),
  ("Why it matters",
   ["This closes the family's fuel logic: the breeder's decade of tritium production seeds the helium-3 "
    "the burner needs. The co-product is carried as upside only, subject to a price-endogeneity rule so "
    "it is never over-credited."])],
 [("Co-product", "helium-3 from tritium decay"), ("Accrual", "~0.42 L He-3 / g tritium / yr"),
  ("Half-life basis", "tritium 12.3 yr"), ("Credited as", "upside only"),
  ("Role", "seeds burner fuel supply")],
 "Helium-3 accrual is real physics but is carried as upside, not banked into the base case &mdash; the "
 "programme applies a price-endogeneity rule so a scarce co-product cannot inflate the story."),

wp(A, "declared-ash",
 "Declaring the Ash: Why f_He4 = 0.05 Is Printed, Not Buried",
 "The number under the gain is the helium ash fraction &mdash; and Kronos writes it down.",
 "Hyperion's gain of 3.424 rests on a declared helium ash fraction, f_He4 = 0.05, giving Z_eff = 1.158. "
 "The value matters less than the discipline: the basis is stated in the entry, not left silent.",
 [("The science",
   ["Helium ash from fusion dilutes the fuel and raises the effective charge Z_eff, taxing the gain. "
    "Hyperion declares its ash fraction explicitly at 5%, so the 3.424 is conditional on a stated "
    "assumption anyone can test, rather than on a hidden one."]),
  ("Why it matters",
   ["An internal audit once flagged an ash fraction carried silently &mdash; the exact defect class that "
    "moved several earlier frozen values. The remedy was not new arithmetic but a declared basis. That "
    "is how a research programme earns the right to freeze a number."])],
 [("Ash fraction", "f_He4 = 0.05 (declared)"), ("Effective charge", "Z_eff = 1.158"),
  ("Effect on gain", "dilution tax, stated"), ("Direction", "lower ash -> higher gain (floor, not ceiling)"),
  ("Discipline", "declared basis, recorded restatement")],
 "If a later determination finds a different ash fraction, the gain moves by recorded restatement, not "
 "silent change &mdash; and because dilution scales with density, a lower true ash only raises gain "
 "above the frozen floor."),

wp(A, "duty-cycle",
 "Capacity Factor: Damage-Life-Limited, Not Duty-Limited",
 "Hyperion runs steady-state, so its uptime is set by how long the first wall survives, not by a pulse cycle.",
 "A breeder's product is fuel per year, and that depends on capacity factor &mdash; the fraction of time "
 "the machine actually runs. Hyperion runs steady-state (bootstrap plus driven current together carry the "
 "full plasma current), so its capacity factor is damage-life-limited, not duty-limited: a defensible band "
 "of 0.58 to 0.83, central 0.69.",
 [("The science",
   ["Because the machine is steady-state, there is no pulse duty cycle to cap uptime; what limits it is "
    "first-wall damage. At about 19.66 displacements-per-atom per full-power year the wall reaches a "
    "life of roughly 2.5 full-power years, which sets the capacity-factor band at 0.58 to 0.83 (central "
    "0.69). This supersedes the older pulsed 0.1442 figure, which assumed the wrong operating mode."]),
  ("Why it matters",
   ["Because tritium delivered per year scales directly with capacity factor, and availability is the "
    "dominant lever on the breeder's whole case, the basis matters: a steady-state, damage-life-limited "
    "band is a physically grounded number, where a pulsed duty figure was simply the wrong model. The "
    "band is wide because it is contingent on three research inputs, and the record says so."])],
 [("Operating mode", "steady-state (bootstrap + driven = Ip)"), ("Capacity factor", "0.58-0.83 (central 0.69)"),
  ("Limit", "damage-life, not duty cycle"), ("First-wall damage", "~19.66 dpa/fpy -> life ~2.5 fpy"),
  ("Supersedes", "the pulsed 0.1442 basis")],
 "The 0.58-0.83 band is damage-life-limited and contingent on three research inputs (H29); it is a "
 "steady-state basis that replaces the earlier pulsed 0.1442. No economic figure is attached here."),

wp(A, "four-year-build",
 "A Four-Year Build, by Precedent",
 "Hyperion's schedule is anchored to a real compact-HTS device, not to an aspiration.",
 "Hyperion's build is scoped at roughly four years, using the award-to-plasma schedule of a compact "
 "HTS mirror device as the precedent. It is a schedule analog, stated as one &mdash; the design itself "
 "already exists in the Kronos record.",
 [("The science",
   ["Schedule risk is real and usually understated. Rather than invent a timeline, Hyperion borrows the "
    "demonstrated award-to-plasma duration of a built compact HTS device as its analog, then flags that "
    "it is exactly that: a schedule comparison, not a construction guarantee."]),
  ("Why it matters",
   ["A four-year figure anchored to a real project is checkable; a four-year figure pulled from ambition "
    "is not. The distinction is the same discipline the whole programme applies to its physics numbers."])],
 [("Build duration", "~4 years"), ("Basis", "compact-HTS award-to-plasma precedent"),
  ("Status", "schedule analog, stated as such"), ("Design maturity", "exists in the record (Modes A-F)"),
  ("Machine", "compact spherical tokamak")],
 "The four-year figure is a schedule analog, not a committed construction timeline; the current planning "
 "target is to begin breeder construction in Q2 2027, but dated commitments live only on revisable "
 "surfaces, never in the frozen physics record."),

wp(A, "fuel-follows-purpose",
 "Fuel Follows Purpose: Why the Breeder Burns D-T",
 "Hyperion and the burners run different fuels on purpose &mdash; each fuel chosen for what the machine must do.",
 "Hyperion burns deuterium-tritium while Aegis and MetroVolt burn deuterium-helium-3. That is not "
 "inconsistency; it is the programme's governing rule &mdash; fuel follows purpose, not platform.",
 [("The science",
   ["A pressure-limited spherical tokamak wants reactivity, and D-T is the most reactive fuel; its high "
    "reactivity lets Hyperion reach its fusion conditions at a much lower plasma current than a less "
    "reactive fuel would need. Buildability wins, so the breeder burns D-T. The burners, whose product "
    "is clean electricity, choose D-3He to suppress neutrons."]),
  ("Why it matters",
   ["Matching fuel to mission is why one company can field both a neutron-rich foundry and a "
    "low-neutron generator without contradiction. The rule keeps each machine honest about why it "
    "burns what it burns."])],
 [("Breeder fuel", "D-T (reactivity, buildability)"), ("Burner fuel", "D-3He (low-neutron electricity)"),
  ("Rule", "fuel follows purpose, not platform"), ("Why D-T for the breeder", "highest reactivity -> lower current"),
  ("Why D-3He for the burner", "suppresses neutrons")],
 "The two fuel choices are deliberate and documented; neither machine is a compromise of the other. "
 "The rule is stated so the family reads as a strategy, not a hedge."),

wp(A, "tritium-inventory-licensing",
 "Inside Existing Practice: Hyperion's Tritium Inventory",
 "The breeder's radiological posture is bounded by design to stay inside civil licensing practice.",
 "Hyperion is sized so its on-site tritium inventory stays inside the envelope of existing civil "
 "licensing practice. That is a design constraint applied from the start, not a hope pinned on after "
 "the physics.",
 [("The science",
   ["Tritium inventory is the defining radiological source term of a D-T machine. By sizing Hyperion to "
    "a requirement rather than a maximum, and by moving bred tritium into product rather than "
    "accumulating it, the design keeps the standing inventory bounded within practiced limits."]),
  ("Why it matters",
   ["Licensing timeline is often the real critical path for a fusion first-of-a-kind. A machine whose "
    "inventory sits inside existing practice starts that conversation from precedent, which is a "
    "schedule asset as much as a safety one."])],
 [("Source term", "on-site tritium inventory"), ("Posture", "inside civil licensing practice"),
  ("Mechanism", "requirement-sized, product-flushed"), ("Benefit", "licensing by precedent"),
  ("Design stage", "constraint applied from the start")],
 "The inventory claim is a design rule verified in the mass-balance ledger; operational tritium "
 "accountancy at plant scale remains an execution item and is scoped as one."),

wp(A, "gain-only-bar",
 "Gain Only: The Milestone Hyperion Does Not Need to Clear",
 "The breeder is buildable because it is excused from the hardest bar in fusion &mdash; net electricity.",
 "Hyperion requires fusion gain and nothing more. It does not have to reach net electricity (Q_E > 1), "
 "the closure milestone that gates the burners. Removing that requirement is what makes the breeder the "
 "near-term member of the family.",
 [("The science",
   ["Net electricity demands not just fusion gain but a whole plant that produces more electricity than "
    "it consumes &mdash; a far harder, systems-level bar. Hyperion's product is materials, so it is "
    "measured on plasma gain alone, which it reaches at demonstrated confinement."]),
  ("Why it matters",
   ["Every hard gate a machine must clear before it delivers product adds years and risk. By defining the "
    "breeder's success as gain, not closure, Kronos gives itself a buildable first product whose "
    "output funds the harder machines behind it."])],
 [("Required bar", "fusion gain (Q_plasma ~1.9)"), ("Not required", "net electricity (Q_E>1)"),
  ("Confinement need", "H98 = 1.0 (demonstrated)"), ("Consequence", "near-term buildability"),
  ("Contrast", "burners are gated on closure")],
 "Gain-only is a genuine simplification, not a rebranding of closure &mdash; Hyperion's ledger never "
 "claims net electricity, and the burner papers state the closure gates plainly."),

wp(A, "hts-magnets-breeder",
 "HTS Magnets for a Compact Core",
 "High-temperature superconducting tape is what lets a 1.2-metre machine reach reactor conditions.",
 "Hyperion's compactness is bought with high-temperature superconducting (REBCO-class) magnets &mdash; "
 "the same tape technology already demonstrated at high field in built devices. The magnet is the "
 "pacing technology, and Hyperion uses a demonstrated one.",
 [("The science",
   ["Reaching reactor-relevant field in a small bore requires the high current density only HTS tape "
    "provides. Hyperion's field system is built on that demonstrated capability rather than on a "
    "speculative conductor, keeping the highest-risk subsystem anchored to hardware."]),
  ("Why it matters",
   ["Because the magnet is the subsystem most scrutinised in compact fusion, building it from "
    "demonstrated tape rather than an extrapolation is what lets the four-year, buildable-now framing "
    "hold together."])],
 [("Conductor", "HTS (REBCO-class) tape"), ("Anchor", "demonstrated high-field devices"),
  ("Role", "enables compact bore"), ("Machine", "R_0 1.2 m spherical tokamak"),
  ("Risk posture", "demonstrated, not extrapolated")],
 "The magnet technology is demonstrated at the component level; full-system integration at Hyperion's "
 "geometry is the engineering task, carried openly as such."),

wp(A, "sized-to-requirement",
 "Designing to a Requirement, Not an Optimum",
 "The most consequential choice in Hyperion is a philosophy: build what is needed, not what is maximal.",
 "Hyperion is sized to the government's stated materials requirement rather than to the physics "
 "optimum the plasma could reach. That single philosophical choice cascades through the whole design "
 "&mdash; smaller, safer, more licensable, buildable sooner.",
 [("The science",
   ["A physics-optimum machine maximises output; a requirement-sized machine hits a target and stops. "
    "Hyperion chooses the latter, using the breeding-ratio lever to match a stated need. The result is "
    "a machine defined by what it must deliver, not by what it could."]),
  ("Why it matters",
   ["Every subsystem inherits the discipline: modest current, bounded inventory, demonstrated "
    "confinement, precedent-based schedule. Requirement-sizing is the quiet decision that makes 'the "
    "buildable one' true across the whole card."])],
 [("Sizing basis", "stated requirement"), ("Not", "physics optimum"), ("Lever", "tritium breeding ratio"),
  ("Cascade", "modest current, bounded inventory"), ("Result", "buildable, licensable, near-term")],
 "Requirement-sizing is a design philosophy, applied consistently; the specific contracted requirement "
 "is a commercial matter kept off the public site. The physics that meets it is deposited."),
]

# ---------------------------------------------------------------------------
# SERIES B — The Burner (Aegis & MetroVolt, D-3He magnetic mirror) — 22 papers
# ---------------------------------------------------------------------------
PAPERS += [
wp(B, "two-housings-one-machine",
 "One Generator, Two Housings: Aegis and MetroVolt",
 "Aegis and MetroVolt are the same D-3He mirror in two markets &mdash; not two machines.",
 "Aegis (fixed defense installations) and MetroVolt (data-center campuses) are a single generator in "
 "two configurations. The physics, the fuel, the gates are identical; only the length, the siting, and "
 "the customer differ.",
 [("The science",
   ["Both are deuterium-helium-3 magnetic mirrors with direct energy conversion. Because the mirror's "
    "central-cell length sets machine size at essentially no cost to closure, the same physics point "
    "serves a shorter defense housing and a longer data-center housing by lengthening the cell, not by "
    "changing the concept."]),
  ("Why it matters",
   ["Treating the burner as one machine in two housings means every physics result &mdash; confinement, "
    "neutron budget, converter performance &mdash; is shared. A gate cleared for Aegis is cleared for "
    "MetroVolt, which is why the programme develops them together."])],
 [("Aegis", "fixed-site defense housing (shorter cell)"), ("MetroVolt", "data-center housing (longer cell)"),
  ("Shared", "D-3He mirror, DEC, all physics gates"), ("Difference", "length, siting, market"),
  ("Scaling rule", "length sets size, not closure")],
 "Aegis is sold as fixed-installation power, never shipboard, and MetroVolt as behind-the-meter "
 "campus power, never city grid &mdash; the housings differ, the generator does not."),

wp(B, "why-a-mirror",
 "Open Field Lines: Why the Burner Is a Mirror",
 "The burner's signature move is to let the plasma leak &mdash; on purpose, into a converter.",
 "The burner is a magnetic mirror, not a tokamak: its field lines are open, so charged particles stream "
 "out the ends by design. That leak is not a loss to be plugged; it is the power stream the direct "
 "converter harvests.",
 [("The science",
   ["A mirror confines plasma along a straight central cell between two high-field throats. Particles "
    "energetic enough to escape the throat flow out along open field lines into an expander and a "
    "direct-conversion end tank. For a fuel like D-3He that releases its energy in charged particles, "
    "open ends are a feature: the exhaust is electricity waiting to be collected."]),
  ("Why it matters",
   ["Open geometry is simpler to build and maintain than a closed torus, and it hands the D-3He cycle a "
    "natural path to direct conversion without a steam loop. The burner's architecture follows from its "
    "fuel."])],
 [("Geometry", "open-ended magnetic mirror"), ("Central cell", "straight, between two throats"),
  ("Exhaust", "charged particles on open field lines"), ("Harvest", "expander + direct converter"),
  ("Fuel fit", "D-3He releases energy as charged particles")],
 "Open field lines mean end losses are intrinsic; the burner's whole case is that those losses are "
 "recovered as directed power, and the fraction recovered is a named, published quantity."),

wp(B, "reference-point",
 "The Locked Mode M Closing Point: Q_E 1.31, On One Hard Requirement",
 "The burner has a reproducible closing point &mdash; contingent on an end-plug density that is specified, not yet demonstrated.",
 "The burner's closing point is locked and reproduces on the deposit's own solver: engineering gain "
 "Q_E 1.31 at a helium-3 fraction of 0.30. But it is honest about the price. At the reference end-plug "
 "density ratio of 10 the machine does not close (Q_E 0.63, net -160 MWe); closure needs a plug density "
 "ratio near 16 &mdash; a requirement, not a demonstrated result.",
 [("The science",
   ["The solve computes every channel: fusion power by cross section, radiation by synchrotron and "
    "bremsstrahlung, axial loss by ambipolar theory, confinement from Pastukhov theory. At the design "
    "point (n_p/n_c=16, x=0.30, Ti=90 keV, ne=2.6×10²⁰ m⁻³) it reproduces Q_E 1.31 and "
    "f_n 5.44%, both length-independent. Net electric then scales with central-cell length: +104 MWe at "
    "55 m, +850 at Aegis (440 m), +2832 at MetroVolt (1400 m)."]),
  ("Why it matters",
   ["A closing point is only as good as its reproducibility and its honesty about what it assumes. This "
    "one reproduces from the shipped code, and it names the single hard condition it rests on &mdash; the "
    "end-plug density &mdash; rather than burying it. Alpha channelling is assumed nowhere."])],
 [("Design-point gain Q_E", "1.31 (length-independent)"), ("Neutron fraction", "5.44% (length-independent)"),
  ("Reference n_p/n_c=10", "does NOT close (Q_E 0.63, -160 MWe)"), ("Net at l_c 55/440/1400 m", "+104 / +850 / +2832 MWe"),
  ("Closure status", "requirement-class (plug ~16), not demonstrated")],
 "The closing point reproduces on the deposit's own solver (M-45); closure is REQUIREMENT-class, "
 "contingent on the end-plug density (M-47), never presented as demonstrated. Alpha channelling is "
 "assumed nowhere. Earlier Q_E 1.002 / 1.191 / 1.825 are WITHDRAWN as non-reproducible."),

wp(B, "binding-requirement",
 "The One Number That Decides Closure: Plug Density Ratio",
 "Not field, not size, not fuel mix &mdash; the burner's fate rests on the end-plug density ratio.",
 "The burner's closing point rests on one condition above all others: the end-plug density must reach "
 "n_p/n_c &asymp; 16. That is a plug density of 4.16&times;10&sup2;&sup1; per cubic metre &mdash; about "
 "347 times what the GDT mirror experiment has measured, and 26 times the best published mirror design. "
 "It is the single binding requirement, and it is specified, not demonstrated.",
 [("The science",
   ["Mirror confinement is set by the confining electrostatic potential, which scales with the logarithm "
    "of the plug-to-central density ratio through Pastukhov theory. At the reference ratio of 10 the "
    "machine does not close (Q_E 0.63, net -160 MWe); at n_p/n_c=16 it reaches the locked Q_E 1.31. "
    "Getting there needs a plug density 347&times; above GDT-measured &mdash; the largest open item in "
    "the whole design (H53)."]),
  ("Why it matters",
   ["Naming one number, in one component, that one experiment must eventually demonstrate is the most "
    "useful thing a design study can do. The burner does not spread its risk across a dozen soft "
    "assumptions; it concentrates it in a single requirement and states plainly that the requirement is "
    "not yet met."])],
 [("Binding parameter", "end-plug density ratio n_p/n_c"), ("Closing value", "~16 (Q_E 1.31)"),
  ("Reference n_p/n_c=10", "does NOT close (Q_E 0.63, -160 MWe)"), ("Plug density needed", "4.16&times;10&sup2;&sup1; m&#8315;&sup3; = 347&times; GDT / 26&times; best mirror"),
  ("Status", "requirement-class, not demonstrated (M-47)")],
 "The plug density ratio is specified as a requirement, not a demonstrated capability: ~16 implies a "
 "plug density 347&times; above GDT-measured. This is the design's single largest open item (H53), named "
 "and handed to the next track &mdash; not booked as solved."),

wp(B, "length-sets-size",
 "Length Sets Size, Not Closure",
 "The mirror's central-cell length is a free knob &mdash; it changes power and footprint, not whether the machine works.",
 "The burner's central-cell length is a degree of freedom, not a physics constraint. Fusion power, "
 "radiation, and axial loss all scale together with volume, so length sets the size of the machine "
 "&mdash; from a short reference cell to the longer production housings &mdash; while the engineering "
 "gain barely moves.",
 [("The science",
   ["At fixed cell radius, every power channel scales with length, so their ratio &mdash; the "
    "engineering gain &mdash; is nearly independent of it. The reference solve confirms it: 15 m and "
    "100 m give Q_E 0.615 and 0.632. Length can therefore be chosen for power output, wall loading, or "
    "siting without paying in closure."]),
  ("Why it matters",
   ["This is what lets one physics point serve two products: the defense housing runs a shorter cell "
    "and the data-center housing a longer one, both on the same closure physics. The scaling is a "
    "design convenience, deposited and checkable; the specific production lengths and powers are held "
    "off the public record until the design cards are reconciled."])],
 [("Free knob", "central-cell length"), ("Scales with length", "fusion power, radiation, axial loss"),
  ("Nearly independent of length", "engineering gain Q_E"), ("Defense housing", "shorter cell"),
  ("Data-center housing", "longer cell")],
 "Length is genuinely free in closure but not in cost or fuel demand &mdash; a longer machine burns "
 "more helium-3. The scaling is a physics result; the product cards apply it to two market sizes."),

wp(B, "aegis-card",
 "Aegis: The Defense Housing of the Burner",
 "Aegis is the defense configuration &mdash; resilient, fuel-logistics-free power for fixed installations.",
 "Aegis is the defense housing of the D-3He burner: the shorter central-cell configuration, sized to "
 "the fuel that will exist when it is built, and configured as a fixed-site generator for defense "
 "installations rather than a shipboard plant.",
 [("The science",
   ["Aegis applies the burner's reference physics in a shorter central cell: same D-3He mirror, same "
    "closure gates, same direct-conversion train. Because length sets machine size at little cost to "
    "closure, the defense housing is simply a shorter cell than the data-center housing, carrying the "
    "same physics and the same helium-3 fuel dependency."]),
  ("Why it matters",
   ["A fixed installation values resilient power that arrives without a fuel convoy. Aegis is pitched "
    "as installation energy against delivered-fuel logistics &mdash; a comparison that favors it &mdash; "
    "and never as a propulsion-cost argument, which it would lose."])],
 [("Configuration", "fixed-site (defense)"), ("Housing", "shorter central cell"),
  ("Physics", "burner reference point, gated"), ("Closure gates", "plug density ratio, electron DEC"),
  ("Not", "shipboard (naval case closed negative)")],
 "Specific length, power, and helium-3 figures for Aegis are unresolved across the design sources and "
 "are deliberately omitted here pending reconciliation. What is firm: it is fixed-site, it carries the "
 "same closure gates as the data-center housing, and its demonstrator is sized to available fuel."),

wp(B, "metrovolt-card",
 "MetroVolt: The Data-Center Housing of the Burner",
 "MetroVolt is the commercial configuration &mdash; firm, carbon-free campus power with no steam cycle and no long-lived waste.",
 "MetroVolt is the data-center housing of the same D-3He burner: the longer central-cell configuration, "
 "for behind-the-meter campus power. It is deliberately the last product in the sequence because it "
 "must clear the highest bars, including a helium-3 supply at scale.",
 [("The science",
   ["MetroVolt is the burner's reference physics in a longer central cell: the same D-3He mirror, the "
    "same direct-conversion architecture, the same closure gates. A longer cell means more fusion power "
    "and a larger helium-3 appetite &mdash; the enabling fuel condition that puts this housing last in "
    "line."]),
  ("Why it matters",
   ["A data-center campus buys firm, clean power with no fuel logistics and no long-lived waste. "
    "MetroVolt delivers that from a machine whose direct conversion needs no steam cycle &mdash; but "
    "only once closure physics and a helium-3 supply at scale both arrive."])],
 [("Configuration", "behind-the-meter data center"), ("Housing", "longer central cell"),
  ("Physics", "burner reference point, gated"), ("Closure gates", "plug density ratio, electron DEC"),
  ("Sequence", "last product; highest bars")],
 "MetroVolt's fuel need at commercial scale (28-54 kg/yr) is many times current world helium-3 supply &mdash; a dependency "
 "on lunar helium-3 that Kronos states plainly as external to the company. It waits for the fuel "
 "landscape to change."),

wp(B, "fixed-site-not-shipboard",
 "Fixed Site, Not Shipboard: A Computed Negative Kept in the Open",
 "The naval-propulsion version of Aegis does not fit in a hull &mdash; and Kronos published the reason.",
 "Aegis is a fixed-site generator, not a shipboard one, because the naval case closes negative. A "
 "shipboard mirror would need 263-362 m of central cell against the 273 m longest straight run inside "
 "the largest carrier hull &mdash; and only one hull in the world could even be fueled.",
 [("The science",
   ["The burner's central cell is long because length sets power, and a militarily useful shipboard "
    "output requires 263-362 m. That exceeds the 273 m longest straight run available inside a "
    "Ford-class hull for most of the range, and the fuel logistics fit only a single vessel class. The "
    "geometry simply does not close at sea."]),
  ("Why it matters",
   ["Publishing the negative keeps someone from rediscovering it in a board meeting. Freezing 'Aegis is "
    "fixed-site' converts a computed dead end into a settled framing, so the product is pitched where "
    "it wins &mdash; installations &mdash; not where it loses."])],
 [("Configuration", "fixed-site installation"), ("Shipboard cell need", "263-362 m"),
  ("Longest hull straight run", "273 m (Ford-class)"), ("Fuelable hulls", "one class, worldwide"),
  ("Status", "naval case closed negative, published")],
 "The naval negative is a computed result kept in the record with its numbers, not quietly dropped "
 "&mdash; labeled history so no one re-litigates it from scratch."),

wp(B, "footprint",
 "A Generator on 1.66 Acres",
 "The burner's folded footprint is small enough to site where power is actually needed.",
 "Folded into its installation, an Aegis generator occupies about 1.66 acres. A long mirror does not "
 "have to be a long building &mdash; the central cell can be folded into a compact site plan, which is "
 "what makes fixed-site defense power practical.",
 [("The science",
   ["The central cell's length is a magnetic geometry, not a straight-line building requirement; the "
    "machine can be folded and stacked into a site footprint far smaller than its unrolled length would "
    "suggest. The result is a generator footprint measured in acres, not miles."]),
  ("Why it matters",
   ["Siting is a real constraint for installation power. A 1.66-acre footprint fits inside existing "
    "fence lines, which is the difference between a generator you can place at the point of use and one "
    "you cannot."])],
 [("Folded footprint", "~1.66 acres"), ("Central cell", "long, foldable (Aegis housing)"),
  ("Geometry", "foldable, not straight-line building"), ("Siting", "inside existing fence lines"),
  ("Configuration", "fixed installation")],
 "The footprint is a folded-geometry estimate for the fixed-site configuration; detailed site "
 "engineering is a downstream task. The figure is a design-layout result, not a permitted plan."),

wp(B, "throat-field-17t",
 "17 Tesla, Already Built: The Mirror Throat Field",
 "The burner's high-field magnets sit on a demonstrated number, not an extrapolated one.",
 "The burner's mirror throats run at 17 tesla &mdash; exactly the field WHAM's built HTS magnets have "
 "demonstrated. The highest-field magnet in the machine is anchored to hardware that already exists.",
 [("The science",
   ["A mirror confines by the ratio of throat field to central field, so throat field is a pacing "
    "parameter. The burner specifies 17 T, the demonstrated capability of built HTS mirror magnets, "
    "rather than a speculative higher field. The design leans on a measured anchor for its most "
    "demanding coil."]),
  ("Why it matters",
   ["Because the throat field is demonstrated, the confinement question reduces to the plug density "
    "ratio, not to whether the magnets can be built. The window study confirms the machine is "
    "insensitive to throat field over 8-35 T &mdash; the coil is not the risk."])],
 [("Throat field B_m", "17 T"), ("Anchor", "WHAM built HTS magnets (measured)"),
  ("Window insensitivity", "8-35 T (Q_E flat)"), ("Central field B_0c", "4.30 T (derived)"),
  ("Risk", "not the magnet")],
 "17 T is measured at the component level; integrating the full mirror coil set is engineering, not "
 "physics risk. The confinement risk lives in the plug ratio, stated separately."),

wp(B, "beta-055",
 "Beta 0.55, Inside What GDT Measured",
 "The burner runs at a plasma pressure fraction experiments have already reached.",
 "The burner operates at a plasma beta of 0.55 &mdash; the ratio of plasma pressure to magnetic "
 "pressure &mdash; a value that sits inside the 0.5-0.6 band the GDT mirror experiment has measured. "
 "High beta is assumed here only where hardware supports it.",
 [("The science",
   ["Beta sets how much plasma pressure the field holds, and mirrors achieve high beta naturally. The "
    "burner assumes 0.55, explicitly inside GDT's measured 0.5-0.6 range, so the pressure assumption is "
    "grounded in a device that has run rather than in an aspiration. High beta also dilates the "
    "effective mirror ratio, aiding confinement."]),
  ("Why it matters",
   ["Anchoring beta to a measured range keeps one more parameter out of the speculative column. It is "
    "part of a consistent posture: assume demonstrated values, name the one requirement (plug ratio) "
    "that is not yet demonstrated."])],
 [("Plasma beta", "0.55"), ("Measured anchor", "GDT 0.5-0.6"), ("Effect", "dilates effective mirror ratio"),
  ("Window", "0.45-0.60 within 10% of reference"), ("Posture", "demonstrated value assumed")],
 "Beta 0.55 is inside a measured band, not at an unproven extreme; it is one of the anchored "
 "assumptions that lets the design concentrate its stated risk in a single parameter."),

wp(B, "mirror-ratio-settled",
 "The Mirror-Ratio Penalty, Settled: 1.21x, Not 3.3x",
 "A worry that the burner's confinement carried a hidden penalty turned out to be overstated by design.",
 "A reviewer raised that the burner's central field and 17 T throat implied a modest mirror ratio and "
 "a large confinement penalty. Checked directly, the penalty is 1.21x, not the 3.3x the simple "
 "heuristic suggested &mdash; and the two concerns do not compound.",
 [("The science",
   ["The relevant mirror ratio is not throat field over central field; at beta 0.55 the pressure "
    "dilation raises the effective ratio to 5.89, nearly 50% above the vacuum value. And Pastukhov "
    "confinement enters through a logarithmic function of that ratio, so sweeping the throat field from "
    "12 to 30 T moves confinement time only from 1.99 s to 2.42 s. The penalty is 1.21x."]),
  ("Why it matters",
   ["Working the concern all the way through &mdash; rather than waving it off or conceding it &mdash; "
    "is the method. Confinement in this device is set by the plug density ratio through an exponential, "
    "which is exactly why the mirror ratio does not dominate and the penalties do not stack."])],
 [("Feared penalty", "3.3x (heuristic)"), ("Actual penalty", "1.21x (computed)"),
  ("Effective mirror ratio R_mc", "5.89 (beta-dilated)"), ("Confinement sweep", "1.99-2.42 s over 12-30 T"),
  ("Dominant parameter", "plug density ratio (exponential)")],
 "The mirror-ratio question is resolved with numbers, not assertion; the confinement risk it was "
 "feared to hide lives entirely in the plug density ratio, which the design names as its binding "
 "requirement."),

wp(B, "pastukhov-confinement",
 "How a Mirror Holds Plasma: Pastukhov and the Confining Potential",
 "The burner's confinement is electrostatic &mdash; a potential hill the plasma must climb to escape.",
 "A mirror confines ions not just magnetically but electrostatically: the plug builds a potential hill, "
 "and confinement time rises exponentially with the ratio of that potential to the ion temperature. "
 "Pastukhov ambipolar theory is the physics behind the burner's whole confinement case.",
 [("The science",
   ["In the burner, the confining potential phi_i equals the electron temperature times the logarithm "
    "of the plug-to-central density ratio &mdash; 211 keV at the reference point. Confinement time then "
    "scales as exp(phi_i/T_i), which is why the density ratio, not the field, dominates. The reference "
    "point reaches a 3.06 s particle confinement time from this mechanism."]),
  ("Why it matters",
   ["Understanding that confinement is exponential in the plug ratio is what makes the design's risk "
    "legible: a single, deep, testable requirement rather than a diffuse set of field and geometry "
    "assumptions. The mechanism tells you exactly which experiment matters."])],
 [("Mechanism", "Pastukhov ambipolar confinement"), ("Confining potential phi_i", "211 keV (reference)"),
  ("Scaling", "confinement ~ exp(phi_i/T_i)"), ("Particle confinement time", "3.06 s (reference)"),
  ("Set by", "plug density ratio")],
 "The confinement prefactor absorbs an ion-collision mixing rule calibrated to a published D-T tandem "
 "point; it is a shape assumption, stated, not an independently validated magnitude."),

wp(B, "electron-temperature-solved",
 "Solved, Not Assumed: The Electron Temperature",
 "The burner's electron temperature is an output of the power balance, and it is not equal to the ion temperature.",
 "In the burner's reference solve, the electron temperature is 91.8 keV &mdash; computed from the "
 "electron power balance, not assumed, and deliberately not set equal to the 100 keV ion temperature. "
 "Solving for it rather than pinning it is a small discipline with large consequences.",
 [("The science",
   ["D-3He plasmas deposit fast-particle energy preferentially on electrons, so assuming T_e = T_i "
    "would misstate both radiation and confinement. The burner solves the electron power balance "
    "explicitly, returning T_e = 91.8 keV against T_i = 100 keV. Radiation, confinement, and the "
    "converter spec all follow from the solved value."]),
  ("Why it matters",
   ["Because synchrotron radiation and the confining potential both depend on electron temperature, "
    "getting it from physics rather than assumption is what keeps the ledger honest. It is one of the "
    "corrections the burner's independent solve made to the prior evaluator."])],
 [("Electron temperature T_e", "91.8 keV (solved)"), ("Ion temperature T_i", "100 keV (free)"),
  ("Relationship", "T_e < T_i (not assumed equal)"), ("Source", "electron power balance"),
  ("Feeds", "radiation, confinement, converter spec")],
 "Solving T_e removes a hidden assumption but places the result partly in the fitted range of the "
 "synchrotron model; the temperature sits at 91.8 keV, inside the fit, while some window points reach "
 "its edge &mdash; stated in the limitations."),

wp(B, "charged-power-budget",
 "The Charged-Power Budget: Why Open Systems Are Different",
 "A mirror must pay its end losses out of charged power &mdash; and that single fact governs the burner.",
 "The deepest result in the burner's physics is not about confinement at all: an open system must fund "
 "its axial end losses out of the charged power it produces. That charged-power budget, not confinement "
 "quality, is the mechanism that decides whether a mirror closes.",
 [("The science",
   ["In a mirror, particles leave along open field lines, carrying energy out the ends. That loss must "
    "be balanced by the fraction of fusion power that arrives as charged particles &mdash; the rest, in "
    "neutrons and radiation, cannot pay it. The frozen record makes it concrete at the deposited point "
    "(ion temperature 90 keV): pure D-D radiates 41.4% of its power as neutrons, leaving only 173.7 MW "
    "of charged power against an 8,779 MW axial loss &mdash; a 51-fold shortfall, so the machine cannot "
    "close. At the helium-3-rich design mix (x_He3 0.30) the neutron fraction is 5.44% and the "
    "charged-particle power covers the axial loss, so the budget closes at engineering gain Q_E 1.31 "
    "&mdash; provided the end-plug density requirement (n_p/n_c ~16) is met."]),
  ("Why it matters",
   ["This is why the distinction between the burner and the breeder is load-bearing, not cosmetic: the "
    "same result that sinks pure D-D in a mirror does not transfer to Hyperion's closed tokamak, which "
    "has no open-end loss to fund. Naming the mechanism is what makes the fuel choice defensible."])],
 [("Governing mechanism", "charged-power budget (not confinement)"),
  ("Pure D-D (deposited pt, Ti 90 keV)", "173.7 MW charged vs 8,779 MW axial (51x), f_n 41.4%"),
  ("Design D-3He mix (x 0.30)", "f_n 5.44%, closes Q_E 1.31 (plug ~16 required)"), ("Applies to", "open (mirror) systems"),
  ("Does not transfer to", "Hyperion (closed tokamak)")],
 "The charged-power budget is specific to open systems; it is the reason the burner insists on a "
 "helium-3-rich mix and the reason its physics does not carry over to the breeder. The distinction is "
 "computed, not asserted."),

wp(B, "why-dd-fails",
 "Why Pure Deuterium Does Not Close in a Mirror",
 "Deuterium-only fuel has better mirror confinement than D-3He &mdash; and still cannot close. Here is why.",
 "Pure deuterium-deuterium fuel actually confines better in the burner's mirror than D-3He does &mdash; "
 "yet it cannot reach net electricity. The failure is not confinement; it is that at a high neutron "
 "fraction, too little charged power is left to fund the axial loss.",
 [("The science",
   ["In the deposited arbiter, pure D-D reaches an engineering gain of only 0.4314, a net deficit "
    "(-8,255 MWe), despite a longer confinement time than D-3He. The reason is the charged-power budget: "
    "at the deposited point (ion temperature 90 keV), a 41.4% neutron fraction leaves just 173.7 MW of "
    "charged power against an 8,779 MW axial loss &mdash; a 51-fold shortfall. (A higher-temperature "
    "250 keV scan reports 47.3% / 420 MW / 7,815 MW; those are scan values at a different temperature, "
    "not the deposited point.) The machine starves regardless of how well it confines."]),
  ("Why it matters",
   ["This is the counterintuitive result that proves the mechanism. Better confinement does not rescue "
    "a fuel whose energy leaves as neutrons, because neutrons cannot pay end losses. It is the cleanest "
    "demonstration of why the burner must run helium-3-rich."])],
 [("D-D engineering gain Q_E", "0.4314 (net -8,255 MWe)"), ("D-D confinement", "longer than D-3He, still fails"),
  ("Deposited point (Ti 90 keV)", "f_n 41.4%, 173.7 MW charged vs 8,779 MW axial (51x)"),
  ("Ti 250 keV scan (labeled)", "47.3% / 420 MW / 7,815 MW")],
 "The D-D result is computed in the deposited arbiter, not asserted; it is the negative control that "
 "makes the charged-power-budget mechanism &mdash; and the helium-3 requirement &mdash; rigorous "
 "rather than rhetorical."),

wp(B, "closure-boundary",
 "The Closure Window: Helium-3 Fraction 0.20 to 0.43",
 "There is a fuel-mix window in which the burner closes &mdash; bounded on both sides, and published.",
 "On the locked closing config the burner closes across a helium-3 fraction window of about 0.20 to "
 "0.43. Below 0.20 the charged-power budget cannot fund the end losses; above ~0.43 the fuel no longer "
 "reacts hard enough. The design point sits inside it at x = 0.30. The window is a computed result, "
 "stated as one.",
 [("The science",
   ["Sweeping the helium-3 fraction at the closing plug ratio (n_p/n_c=16), the machine is net-positive "
    "from about x=0.20 to x=0.43, with the design point at x=0.30 giving Q_E 1.31. Across the window the "
    "neutron fraction falls from 9.53% to 2.77%. Above ~0.43 the reaction rate drops too far and closure "
    "is lost &mdash; a redesigned machine, not a fuel change, would be needed for near-aneutronic "
    "operation."]),
  ("Why it matters",
   ["A published closure window tells a fuel planner exactly how helium-3-rich the mix must be, and "
    "tells a physicist exactly which mixes to test. It is the fuel-side companion to the plug-density "
    "requirement on the confinement side."])],
 [("Closure window", "x_He3 in [0.20, ~0.43]"), ("Design point", "x_He3 0.30 (Q_E 1.31)"),
  ("Neutron fraction across window", "9.53% -> 2.77%"), ("Above ~0.43", "closure lost (redesign needed)"),
  ("Also required", "plug density ratio ~16 (not demonstrated)")],
 "The closure window is a computed fuel-mix result on the locked config (M-46); reaching net electricity "
 "also requires the end-plug density (M-47), which is specified, not demonstrated. Both conditions must "
 "hold. Earlier x&ge;0.15 / Q_E 1.191 numbers are WITHDRAWN."),

wp(B, "fuel-mix-lever",
 "The Fuel Mix Is a Neutron Knob &mdash; and the Machine Gets Cleaner With Time",
 "Raising the helium-3 fraction cuts neutron output ~4x across the closure window &mdash; and one step is free in gain.",
 "The burner's helium-3 fraction is a lever on neutron production, computed on the locked closing "
 "config. Across the closure window x_He3 &isin; [0.20, ~0.43] the neutron fraction falls about "
 "3.4-fold, from 9.53% at the x=0.20 floor to 2.77% at the clean edge. So as lunar helium-3 matures, "
 "the same machine can be run measurably cleaner over its life.",
 [("The science",
   ["A higher helium-3 fraction means fewer D-D reactions, the neutron source, so the neutron fraction "
    "falls steeply while gain stays strong. On the locked config (n_p/n_c=16): the x=0.30 design point "
    "runs f_n 5.44% at Q_E 1.31; shifting to x=0.35 cleans it to f_n 4.18% while staying net-positive "
    "&mdash; the FREE clean-shift. Below x=0.20 and above ~0.43 the machine no longer closes; true "
    "near-aneutronic operation (x &ge; 0.45) needs a redesigned machine, not just more fuel."]),
  ("Why it matters",
   ["The mix is a tuned operating choice, not luck, and it improves with the fuel supply: a leaner "
    "helium-3 fraction burns less scarce fuel but makes more neutrons, a richer one does the reverse "
    "&mdash; up to the closure edge. Publishing the whole trajectory, and naming the free clean-shift on "
    "it, makes the burner's low-neutron character a design decision the reader can second-guess."])],
 [("Lever", "helium-3 fraction x_He3 (locked config)"), ("Closure window", "x in [0.20, ~0.43]"),
  ("x=0.30 design point", "f_n 5.44%, Q_E 1.31"), ("x=0.35 free clean-shift", "f_n 4.18% (still net-positive)"),
  ("x >= 0.45", "closure lost; needs a REDESIGN")],
 "The trajectory is computed on the locked closing config (M-46, burner_closure_table); the free "
 "clean-shift to x=0.35 and the loss of closure below 0.20 / above ~0.43 are frozen. Reaching net "
 "electricity anywhere in the window still requires the plug-density condition (M-47), not demonstrated."),

wp(B, "ion-temperature-optimum",
 "An Interior Optimum: Ion Temperature at 80-100 keV",
 "The burner's ion temperature has a real peak, not a monotone trend &mdash; and the design sits on it.",
 "The burner runs at an ion temperature of 100 keV, near a genuine interior optimum in the 80-100 keV "
 "band. Higher is not simply better: reactivity rises with temperature while the confining potential "
 "relative to it falls, so confinement degrades. The design sits on the balance.",
 [("The science",
   ["Two effects compete. Fusion reactivity climbs with ion temperature, favoring hotter plasma. But "
    "the confining potential ratio phi_i/T_i falls as T_i rises, degrading confinement. The product has "
    "a maximum in the 80-100 keV range &mdash; a real optimum, computed, not a monotone push toward "
    "higher temperature."]),
  ("Why it matters",
   ["Finding and sitting on an interior optimum, rather than assuming hotter is always better, is the "
    "kind of result that only falls out of a self-consistent solve. It also means the operating window "
    "is two-sided in temperature, which is friendlier to control."])],
 [("Ion temperature T_i", "100 keV"), ("Optimum band", "80-100 keV (interior)"),
  ("Rises with T_i", "reactivity"), ("Falls with T_i", "confining ratio phi_i/T_i"),
  ("Window", "70-120 keV within 10% of reference")],
 "The optimum is a computed interior maximum, not an assumed ceiling; the design sits on it, and the "
 "two-sided window is published in the sensitivity ranking."),

wp(B, "operating-window",
 "Wide in Nine of Ten Parameters &mdash; and That Is the Problem",
 "The burner is not a knife-edge. Its trouble is the opposite: most knobs barely matter.",
 "Across ten swept parameters, the burner's engineering gain is flat to within 10% over enormous "
 "ranges &mdash; a factor of 6.7 in length, 3.8 in density, 4.4 in throat field. It is a wide window, "
 "not a fragile point. The catch is that the width comes from those parameters barely mattering.",
 [("The science",
   ["Nine of the ten parameters &mdash; length, density, field, radius, fuel mix, beta, temperature, "
    "converter efficiency, channelling &mdash; move the gain only modestly, so the design degrades "
    "gracefully rather than tripping a cliff. But none of them reaches closure either. Only the tenth, "
    "the plug density ratio, moves the gain by a factor of 11 and is the one that reaches net "
    "electricity."]),
  ("Why it matters",
   ["A wide window is genuinely good for operability, and the burner has one. But publishing that the "
    "width means most knobs are inert &mdash; and that a single knob carries the closure &mdash; is the "
    "honest reading, and it points every experiment at the right parameter."])],
 [("Flat within 10%", "9 of 10 parameters"), ("Length range flat", "factor 6.7"),
  ("Density range flat", "factor 3.8"), ("Field range flat", "factor 4.4"),
  ("Reaches closure", "plug density ratio only (x11)")],
 "The wide window is real operability and, read honestly, also a statement that most parameters are "
 "inert. The design does not hide behind the width &mdash; it names the one parameter that is not flat."),

wp(B, "unchannelled-baseline",
 "Unchannelled on Purpose: No Speculative Physics in the Baseline",
 "The burner's baseline assumes zero alpha channelling &mdash; because no one has ever measured it.",
 "The burner's reference point assumes no alpha channelling at all. That is deliberate: alpha "
 "channelling has never been measured at any scale, so building the baseline on it would make the whole "
 "design conditional on an unmeasured parameter. Kronos declines to do that.",
 [("The science",
   ["Alpha channelling would redirect fast-ion energy to useful channels, and the literature calls the "
    "effect speculative in its own words. The channelling track established that radiative benefit needs "
    "an efficiency of at least 0.577 and the converter benefit at least 0.875 &mdash; with no "
    "measurement of the efficiency existing at any scale. The required-versus-demonstrated gap has no "
    "denominator."]),
  ("Why it matters",
   ["And in this ledger, channelling barely helps: sweeping its efficiency from 0 to 1 moves the gain "
    "from 0.632 to 0.597 &mdash; it goes down, because it cools the electrons and shortens confinement. "
    "Channelling is a radiation lever, not a gain lever, so the baseline loses nothing by excluding it."])],
 [("Baseline channelling", "none (eta_alpha = 0)"), ("Measured efficiency", "none, at any scale"),
  ("Radiative benefit needs", "eta_alpha &ge; 0.577"), ("Converter benefit needs", "eta_alpha &ge; 0.875"),
  ("Gain effect 0->1", "0.632 -> 0.597 (down)")],
 "Unchannelled is the baseline because it needs no speculative physics; channelling is carried as a "
 "radiation lever, not credited to the gain. The gap cannot even be stated as a ratio because the "
 "denominator &mdash; a measured efficiency &mdash; does not exist."),

wp(B, "experiment-not-power-plant",
 "A Reproducible Closing Point, and the One Requirement It Rests On",
 "The burner has a locked, reproducible closing point (Q_E 1.31) &mdash; honest that its closure is a requirement, not yet demonstrated.",
 "The burner's closing point is locked and reproduces from the deposit's own solver: engineering gain "
 "Q_E 1.31 at helium-3 fraction 0.30. It is also honest about its price. At the reference end-plug "
 "density ratio of 10 the machine does not close (Q_E 0.63, net -160 MWe); reaching Q_E 1.31 needs a "
 "plug density ratio near 16, a condition specified but not demonstrated.",
 [("The science",
   ["On the locked config the engineering gain is Q_E 1.31 and the neutron fraction 5.44%, both "
    "length-independent; net electric then scales with central-cell length (+104 / +850 / +2832 MWe at "
    "55 / 440 / 1400 m). Closure is contingent on an end-plug density of 4.16&times;10&sup2;&sup1; per "
    "cubic metre &mdash; 347&times; above what the GDT mirror has measured. Earlier Q_E figures of 1.002, "
    "1.191 and 1.825 did not reproduce from the code and are withdrawn."]),
  ("Why it matters",
   ["A closing point you can rerun, that names the one hard thing it assumes, is worth more than a "
    "flattering number that does not reproduce. The physics gives a reproducible net-positive point; "
    "whether it can be built hinges on the plug density, which the record flags as the single largest "
    "open item rather than booking it as solved."])],
 [("Design-point gain Q_E", "1.31 (reproducible, length-independent)"), ("Neutron fraction", "5.44%"),
  ("Reference n_p/n_c=10", "does NOT close (Q_E 0.63, -160 MWe)"), ("Closure condition", "plug ratio ~16 (347x GDT), not demonstrated"),
  ("Withdrawn", "Q_E 1.002 / 1.191 / 1.825 (non-reproducible)")],
 "The closing point reproduces on the deposit's own solver (M-45); closure is REQUIREMENT-class (M-47), "
 "contingent on the end-plug density and never presented as demonstrated. The non-reproducible "
 "Q_E 1.002 / 1.191 / 1.825 are withdrawn."),
]

# ---------------------------------------------------------------------------
# SERIES C — Low-Neutron by Design — 16 papers
# ---------------------------------------------------------------------------
PAPERS += [
wp(C, "low-neutron-never-aneutronic",
 "Low-Neutron, Never Aneutronic: A Few Percent Is Small and It Is Not Zero",
 "The burner's fuel is quiet, not silent &mdash; and the language stays honest about the difference.",
 "The burner's D-3He cycle sends 5.44% of its power out as neutrons at the locked design point. That "
 "is roughly an order of magnitude below a D-T plant &mdash; genuinely low-neutron &mdash; but it is not "
 "zero, and Kronos never calls it aneutronic. The mandatory descriptor is low-neutron; the word matters "
 "as much as the number.",
 [("The science",
   ["D-3He's primary reaction is neutron-free, but unavoidable deuterium-deuterium side reactions and a "
    "secondary D-T burn leave a residual neutron budget: a frozen 5.44% of fusion power at the design "
    "point (helium-3 fraction 0.30). Running richer cleans it further &mdash; 4.18% at x=0.35 &mdash; but "
    "true near-aneutronic operation (x &ge; 0.45) breaks closure and needs a different machine. "
    "'Aneutronic' would imply zero; the real figure is small, finite, and engineered for."]),
  ("Why it matters",
   ["Overclaiming 'aneutronic' is a credibility trap the field has fallen into before. By fixing the "
    "mandatory term at 'low-neutron' and printing the percentage, the burner's shielding, activation, and "
    "maintenance stories all rest on the true number rather than on a marketing word."])],
 [("Neutron fraction (design point)", "5.44% of fusion power (M-43 restated)"), ("At x=0.35 clean-shift", "4.18%"),
  ("Versus D-T", "~order of magnitude lower"), ("Mandatory descriptor", "low-neutron (never aneutronic)"),
  ("Near-aneutronic (x >= 0.45)", "needs a redesigned machine")],
 "'Aneutronic' appears in the record only as a quoted historical term, immediately corrected. The frozen "
 "descriptor is low-neutron: 5.44% is small, and it is not zero."),

wp(C, "fn-not-a-constant",
 "The Neutron Fraction Is Not a Fuel Constant",
 "How neutronic the burner is depends on how well it confines &mdash; a coupling most models miss entirely.",
 "The burner's neutron fraction is not a fixed property of its fuel. Computed from cross sections with "
 "every reaction channel, it is 5.44% at the locked design point and varies with the fuel mix and "
 "confinement &mdash; from 9.53% at the x=0.20 floor to 2.77% at the clean edge &mdash; because tritium "
 "burnup, and therefore neutron output, scales with both.",
 [("The science",
   ["The prior evaluator carried the neutron fraction as a constant, 4.8%. Recomputed from the stored "
    "cross sections with all D-D channels and the secondary D-T burn, it is not constant at all: better "
    "confinement means longer particle residence, more tritium burnup, and more neutrons. The fraction "
    "moves from 1% to 17.3% across the 51,840-point scan."]),
  ("Why it matters",
   ["This is a real, counterintuitive coupling: a design that improves confinement makes itself more "
    "neutronic. A model with a constant neutron fraction cannot see it. Publishing the coupling is what "
    "lets the shielding and materials cases be sized to the operating point rather than to an average."])],
 [("Design-point neutron fraction", "5.44% (locked config)"), ("Fuel-mix range", "9.53% (x=0.20) -> 2.77% (clean edge)"),
  ("Driver", "tritium burnup ~ confinement + fuel mix"), ("Prior model", "constant 4.8% (superseded)"),
  ("Free clean-shift", "4.18% at x=0.35")],
 "The neutron fraction is a computed, confinement- and mix-coupled quantity, not a fuel constant; the "
 "design-point value is 5.44% and the trajectory is published so the coupling is visible rather than "
 "averaged away."),

wp(C, "confinement-neutron-coupling",
 "The Coupling Nobody Models: Better Confinement, More Neutrons",
 "Improving the plasma's confinement raises its neutron output &mdash; a trade the design has to hold in view.",
 "There is a coupling in the burner that constant-fraction models cannot represent: the same longer "
 "confinement that pushes the machine toward closure also raises tritium burnup and neutron production. "
 "The design has to hold both ends of that trade at once.",
 [("The science",
   ["Longer particle confinement time means deuterium ions linger, more D-D reactions occur, more "
    "tritium is bred and then burned in secondary D-T reactions &mdash; each of which is neutronic. So "
    "the plug density ratio that buys closure also, indirectly, raises the neutron fraction. Both "
    "effects come from the same confinement improvement."]),
  ("Why it matters",
   ["Naming the coupling keeps the low-neutron claim honest at the operating point rather than at the "
    "reference alone. It also tells the materials programme to qualify against the neutron budget of the "
    "closing machine, not the more comfortable baseline."])],
 [("Coupling", "confinement up -> neutrons up"), ("Mechanism", "tritium burnup rises with residence time"),
  ("Shared driver", "plug density ratio / confinement"), ("Consequence", "closure raises f_n"),
  ("Invisible to", "constant-fraction models")],
 "The coupling is a computed consequence of the reaction network, not a modeling artifact; it means the "
 "low-neutron budget must be quoted at the operating point, which the design does."),

wp(C, "gentle-wall",
 "The Gentle Wall: Far Below the Breeder's Neutron Load",
 "A low-neutron fuel gives the burner a first wall that is comfortable, not consumable.",
 "The burner's first wall sees a neutron load far below the breeder's frozen 1.966 MW/m&sup2; &mdash; a "
 "small fraction of it, because the burner runs at a neutron fraction of 5.44% against the breeder's "
 "neutron-dominated D-T budget. The low-neutron fuel turns the first wall from a scheduled consumable "
 "into plant infrastructure.",
 [("The science",
   ["Wall load is fuel chemistry made visible: at the burner's 5.44% neutron fraction, the flux of "
    "damaging neutrons reaching the wall is a small fraction of the breeder's 1.966 MW/m&sup2; and of a "
    "D-T machine's. The exact per-housing fleet ratio recomputes on this corrected design-point neutron "
    "fraction and is carried as provisional, not a frozen number."]),
  ("Why it matters",
   ["A gentle wall is a maintenance strategy. A D-T plant replaces its wall and blanket on a cycle "
    "measured in months; a low-neutron burner is designed for a wall that lasts. That difference "
    "compounds into availability, which is what firm-power customers actually buy."])],
 [("Burner neutron fraction", "5.44% (design point)"), ("Breeder first-wall load", "1.966 MW/m&sup2; (frozen)"),
  ("Burner first-wall load", "far below the breeder (order of magnitude+)"), ("Wall status", "infrastructure, not consumable"),
  ("Fleet ratio", "recomputes on f_n 5.44% (provisional, not frozen)")],
 "The breeder first-wall neutron loading is frozen at 1.966 MW/m&sup2;; the burner's is far below it at "
 "f_n 5.44%. The exact per-housing cleanliness ratio recomputes on this f_n (M-43 restated) and is "
 "carried as provisional, not quoted as a frozen figure."),

wp(C, "dhe3-vs-dt-budget",
 "D-3He Versus D-T: The Neutron Budget Compared",
 "Choosing the fuel is choosing the plant you must build around it &mdash; and the neutron budget is the fork.",
 "A D-T plant sends about 80% of its energy out as 14 MeV neutrons; the burner's D-3He cycle sends "
 "5.44% at its design point. That roughly order-of-magnitude difference in neutron budget is the single "
 "fork from which the two plants' entire designs diverge.",
 [("The science",
   ["D-T's 14.1 MeV neutrons demand a meter-scale breeding blanket, activate the structure, and set a "
    "replacement clock. D-3He's charged-particle output needs none of that: no breeding blanket, a "
    "gentle wall, and a path to direct conversion. The burner pays a confinement price for the quiet "
    "fuel and buys a categorically different plant with it."]),
  ("Why it matters",
   ["The neutron budget is not one design parameter among many; it decides the blanket, the wall life, "
    "the activation inventory, the maintenance cadence, and the licensing posture all at once. Kronos "
    "fields both fuels &mdash; D-T in the breeder, D-3He in the burner &mdash; because each budget suits "
    "a different job."])],
 [("D-T neutron budget", "~80% of energy"), ("D-3He neutron budget", "5.44% (design point)"),
  ("D-T requires", "breeding blanket, frequent wall changes"), ("D-3He requires", "no blanket, gentle wall"),
  ("Trade", "quiet fuel for harder confinement")],
 "The comparison uses conservative mainstream D-T assumptions; the burner's advantage is in maintenance "
 "and materials, and the confinement cost of D-3He is stated openly as the price of the quiet budget."),

wp(C, "fuel-mix-neutron-knob",
 "Tuning the Neutron Output From the Fuel Line",
 "The burner's neutron production is set decades in advance, at the fuel mix &mdash; and it is adjustable.",
 "How many neutrons the burner makes is chosen at the fuel line. On the locked closing config the design "
 "mix is x=0.30 (f_n 5.44%); shifting to x=0.35 cleans it to 4.18% while staying net-positive. Neutron "
 "output is a knob, and the design turned it down.",
 [("The science",
   ["Neutrons in the burner come from D-D side reactions and the secondary D-T burn. Fewer deuterium-"
    "deuterium encounters means fewer neutrons, so a helium-3-richer mix is a quieter mix. Across the "
    "closure window x_He3 &isin; [0.20, ~0.43] the neutron fraction falls from 9.53% to 2.77%; the design "
    "point sits at x=0.30 (5.44%), with a free clean-shift to x=0.35 (4.18%). Beyond ~0.43 the machine "
    "no longer closes."]),
  ("Why it matters",
   ["A designer who can trade neutron output against fuel demand can place the machine wherever "
    "the mission needs it. The published trade curve makes that a transparent engineering choice, not a "
    "hidden assumption."])],
 [("Neutron knob", "helium-3 fraction x_He3 (locked config)"), ("Design point x=0.30", "f_n 5.44%"),
  ("Free clean-shift x=0.35", "f_n 4.18% (net-positive)"), ("Closure window", "x in [0.20, ~0.43], f_n 9.53% -> 2.77%"),
  ("Above ~0.43", "does not close")],
 "The fuel-mix knob trades neutrons against fuel demand across the frozen closure window (M-46); the "
 "design point 0.30 is a chosen balance with the full curve deposited. Reaching net electricity still "
 "requires the end-plug density (M-47), not demonstrated."),

wp(C, "tritium-burnup",
 "The Secondary Burn: Where the Burner's Neutrons Come From",
 "The burner breeds a little tritium and burns 17% of it &mdash; and that secondary D-T is a real neutron source.",
 "The burner's neutrons are not all from D-D directly. Deuterium-deuterium reactions breed tritium in "
 "the plasma, and about 17.3% of it burns in secondary D-T reactions before it leaves &mdash; a "
 "neutronic channel the design computes explicitly rather than ignoring.",
 [("The science",
   ["One branch of the D-D reaction produces tritium, which can then fuse with deuterium in a 14 MeV "
    "neutron reaction. The burner computes this secondary burnup from the deuterium density, reactivity, "
    "and particle confinement time, finding 17.3% burnup at the reference point &mdash; a real "
    "contribution to the neutron budget, and one that grows with confinement."]),
  ("Why it matters",
   ["Accounting for the secondary burn is why the burner's neutron fraction is computed from the full "
    "reaction network, not from the D-3He channel alone. It is also the mechanism behind the "
    "confinement-neutron coupling: better confinement burns more of the bred tritium."])],
 [("Bred-tritium burnup", "17.3% (reference)"), ("Channel", "secondary D-T (14 MeV)"),
  ("Source", "D-D breeding branch"), ("Computed from", "n_D, reactivity, confinement time"),
  ("Grows with", "confinement")],
 "The secondary burn is computed from the reaction network, not assumed away; it is part of why the "
 "burner's neutron fraction rises with confinement and why the budget is quoted at the operating point."),

wp(C, "no-breeding-blanket",
 "No Breeding Blanket: The Component the Burner Deletes",
 "Because the burner does not run on tritium, it needs no blanket to breed it &mdash; and that removes a whole plant.",
 "The burner has no breeding blanket, because it burns no tritium as fuel. Deleting the blanket removes "
 "the single most maintenance-intensive, most-activated, most-replaced component of a D-T plant &mdash; "
 "a simplification the low-neutron fuel makes possible.",
 [("The science",
   ["A D-T plant must surround its plasma with a meter-scale lithium blanket to breed the tritium it "
    "consumes, then extract, purify, and recycle that tritium. The burner's D-3He fuel needs none of it: "
    "its fuel arrives as helium-3, so there is no breeding requirement and no blanket to build, cool, or "
    "replace."]),
  ("Why it matters",
   ["The blanket is where much of a D-T plant's cost, activation, and downtime live. A burner without "
    "one is structurally simpler and structurally quieter. The absence is a direct dividend of choosing "
    "a low-neutron fuel."])],
 [("Breeding blanket", "none (burner)"), ("Reason", "no tritium fuel to breed"),
  ("Removed", "blanket cost, activation, replacement"), ("Fuel form", "helium-3, supplied"),
  ("Contrast", "D-T plant requires a blanket")],
 "The burner needs no breeding blanket; Hyperion, the D-T breeder, deliberately does breed &mdash; the "
 "two machines differ because their fuels differ, and neither is a compromise of the other."),

wp(C, "activation-llw",
 "Quiet Structures: Activation and the Low-Level-Waste Path",
 "Fewer neutrons means less activated steel &mdash; and a decommissioning stream that fits existing disposal.",
 "Run the same activation physics on the burner and on a D-T comparator and the structures answer "
 "differently: the burner makes far fewer neutrons, so it activates far less, and its end-of-life "
 "inventory maps onto the existing low-level-waste disposal pathway rather than a deep repository.",
 [("The science",
   ["Neutrons transmute structural materials into activated isotopes; the burner simply makes far fewer "
    "of them per unit energy, and at a spectrum less punishing to the worst activation chains. The "
    "result is an end-of-life inventory that tracks the low-level-waste class &mdash; no geological-"
    "repository line item for the vessel and internals."]),
  ("Why it matters",
   ["Decommissioning liability is a real obligation on any plant's books. A machine that retires like "
    "industrial equipment rather than a nuclear legacy site has a shorter, cleaner closeout. Low-neutron "
    "keeps paying after the last kilowatt-hour."])],
 [("Activation", "far lower than a D-T comparator"), ("Driver", "5.44% neutron fraction (design point)"),
  ("Waste class", "low-level-waste pathway"), ("Repository line", "none for vessel/internals"),
  ("Benefit", "shorter, cleaner decommissioning")],
 "The activation advantage follows from the same neutron budget as the wall life; the disposal-class "
 "mapping is a computed result, and the operating-point neutron fraction (not the baseline) sets the "
 "conservative case."),

wp(C, "materials-dose-life",
 "Designed to Die of Old Age: Materials Dose Over Plant Life",
 "The burner's wall is engineered to reach the end of the plant's life, not to be swapped on a cycle.",
 "Integrated over a plant lifetime, the burner's low neutron load (5.44% at the design point) keeps the "
 "accumulated materials dose inside what the structural alloy can tolerate &mdash; a frozen first-wall "
 "life of 104 to 428 full-power years, against about 2.5 for the breeder. That translates to roughly "
 "0.035 to 0.144 first-wall changes across 30 years: scheduled-replacement waste is essentially zero.",
 [("The science",
   ["Materials damage accumulates as displacement-per-atom (dpa) from neutron flux. Because the burner's "
    "neutron fraction is only 5.44%, its wall load is roughly an order of magnitude below a D-T "
    "plant's, giving a frozen first-wall life of 104-428 fpy. The consequence is that the burner's "
    "capacity factor is plug-limited, not damage-limited &mdash; the opposite of the breeder, and a "
    "genuine mirror advantage (B31)."]),
  ("Why it matters",
   ["A wall that lasts the plant's life removes the biggest scheduled outage in fusion operations. That "
    "is the difference between a plant that spends months per year changing components and one that "
    "mostly runs &mdash; the availability advantage the low-neutron thesis rests on."])],
 [("Damage metric", "displacement per atom (dpa)"), ("First-wall life", "104-428 fpy (vs breeder ~2.5)"),
  ("Neutron fraction", "5.44% (M-43 restated)"), ("Capacity factor", "plug-limited, not damage-limited"),
  ("Scheduled changeouts", "none by design")],
 "The first-wall life (104-428 fpy) and the plug-limited CF are frozen (B31); the plug-reliability CF "
 "number itself is a standing research ask, not yet pinned. The dose is set by the operating-point "
 "neutron budget."),

wp(C, "neutron-mirror-cannot-make",
 "Two Neutrons, Two Purposes: 2.45 MeV Versus 14 MeV",
 "The burner's neutrons are the wrong energy for materials testing &mdash; on purpose. That job belongs to the breeder.",
 "The burner makes mostly 2.45 MeV neutrons from D-D reactions; materials qualification needs 14 MeV "
 "fusion-spectrum neutrons. That mismatch is deliberate: the burner is built to suppress neutrons, so "
 "the irradiation job belongs to Hyperion's D-T fill, not to the mirror.",
 [("The science",
   ["The dominant neutron from a low-neutron D-3He mirror is the 2.45 MeV D-D neutron, useful for little "
    "and made in small quantity. The 14 MeV neutron that qualifies fusion materials requires a D-T "
    "reaction at rate &mdash; which is exactly what the breeder provides and the burner avoids."]),
  ("Why it matters",
   ["This is the clean division of labor in the family: the breeder is deliberately neutron-rich to "
    "serve materials qualification, and the burner is deliberately neutron-poor to serve clean power. "
    "Each machine's neutron character is a design choice matched to its mission."])],
 [("Burner neutron", "mostly 2.45 MeV (D-D)"), ("Qualification neutron", "14 MeV (D-T)"),
  ("Burner role", "suppress neutrons (clean power)"), ("Breeder role", "make neutrons (materials qual)"),
  ("Division", "fuel matched to mission")],
 "The burner cannot serve the 14 MeV irradiation market and is not meant to; that role sits with "
 "Hyperion. Old mirror-neutron-source figures do not transfer to either machine and are retired."),

wp(C, "breeder-deliberately-neutronic",
 "The Breeder Is Neutron-Rich on Purpose",
 "One machine in the family wants neutrons &mdash; and designs to make them at full rate.",
 "While the burner suppresses neutrons, Hyperion does the opposite: its D-T fill is chosen precisely "
 "because it makes 14 MeV neutrons at full rate. In a family defined by low-neutron power, the breeder "
 "is the deliberate exception, and for good reason.",
 [("The science",
   ["Hyperion's three product streams &mdash; tritium, helium-3, and neutrons &mdash; all depend on a "
    "neutron-rich D-T reaction. The blanket breeds tritium from the neutron flux, and the flux itself is "
    "a product for materials irradiation. Neutron richness is the breeder's whole point, so it uses the "
    "fuel that maximizes it."]),
  ("Why it matters",
   ["Understanding that the two machines want opposite neutron budgets is what makes the family coherent. "
    "The breeder's neutrons qualify the materials and breed the fuel; the burner's quiet cycle then "
    "turns that fuel into clean power. The contrast is the strategy."])],
 [("Breeder fuel", "D-T (neutron-rich)"), ("Neutron energy", "14 MeV, full rate"),
  ("Uses neutrons for", "tritium breeding + materials qual"), ("Burner", "neutron-poor by design"),
  ("Family logic", "opposite budgets, matched to mission")],
 "The breeder's neutron richness is a deliberate design choice serving materials qualification and fuel "
 "breeding; it is the counterpart to the burner's low-neutron cycle, and the two are documented as a "
 "matched pair."),

wp(C, "tritium-lean-burner",
 "Tritium-Lean by Design: A Trace Species in the Burner",
 "The isotope that dominates fusion licensing is only a fleeting trace in the burner.",
 "The burner holds tritium only as a fleeting D-D side product, bred and burned inside the plasma "
 "rather than stored. Its site inventory of the mobile radioisotope stays a trace quantity &mdash; a "
 "categorically different licensing conversation from a breeding-blanket plant.",
 [("The science",
   ["A D-T plant maintains multi-kilogram tritium inventories &mdash; its defining radiological source "
    "term. The burner's D-3He cycle produces tritium only as a transient D-D by-product, roughly 17% of "
    "which burns immediately, the rest decaying toward the helium-3 the plant wants. There is no bulk "
    "tritium process stream to store."]),
  ("Why it matters",
   ["Communities and regulators price the worst case, and the worst case scales with inventory. A plant "
    "whose mobile-isotope inventory is a bounded trace &mdash; and falls with time by decay into fuel "
    "&mdash; starts the safety conversation from a different place. Tritium-lean is time-to-permit."])],
 [("Burner tritium", "trace, transient D-D by-product"), ("Storage", "none (no bulk stream)"),
  ("Fate", "~17% burned; rest decays to He-3"), ("Source term", "trace species"),
  ("Contrast", "D-T plant holds kilograms")],
 "The tritium-lean claim is a design property of the burner's fuel cycle verified in the mass-balance "
 "ledger; operational tritium accountancy at plant scale remains an execution item, scoped as one."),

wp(C, "shielding-low-neutron",
 "Shielding a Quiet Machine",
 "Fewer neutrons means thinner shields, lighter structures, and more of the machine doing useful work.",
 "The burner's shielding requirement follows directly from its 5.44% neutron fraction: with roughly an "
 "order of magnitude fewer neutrons than a D-T plant, the shield is thinner and lighter, and more of "
 "the machine's mass and volume goes to producing and converting power.",
 [("The science",
   ["Shield thickness scales with the neutron flux it must attenuate. A low-neutron burner needs far "
    "less shielding mass than a D-T plant, which frees volume and reduces the activated inventory the "
    "shield itself would otherwise become. The gentle wall and the light shield are two faces of the "
    "same neutron budget."]),
  ("Why it matters",
   ["Shielding is dead weight and dead cost &mdash; necessary, but not productive. Every meter of shield "
    "the low-neutron fuel deletes is volume returned to the converter and the plant. It compounds the "
    "compactness the mirror geometry already provides."])],
 [("Shield driver", "neutron flux (5.44% fraction)"), ("Versus D-T", "far thinner / lighter"),
  ("Freed", "volume and mass for power systems"), ("Activated shield mass", "reduced"),
  ("Compounds", "mirror compactness")],
 "Shielding scales with the operating-point neutron budget, which rises with confinement; the shield is "
 "sized to the closing machine, not the baseline, consistent with how the wall load is treated."),

wp(C, "maintenance-dividend",
 "The Maintenance Dividend of Low Neutrons",
 "The quiet fuel's biggest payoff is not physics &mdash; it is the outages that never have to happen.",
 "The burner's low-neutron budget converts into a maintenance dividend: no breeding blanket to replace, "
 "a first wall that lasts the plant's life, and no months-long changeout cycle. The machine is designed "
 "to run rather than to be serviced.",
 [("The science",
   ["A D-T plant's neutron flux forces a replacement cadence on its blanket and wall measured in "
    "months, each swap a major outage. The burner's 5.44% neutron fraction removes that cadence: with no "
    "blanket and a lifetime wall, the scheduled-outage burden that dominates D-T operations largely "
    "disappears."]),
  ("Why it matters",
   ["Uptime is what firm-power and installation customers actually buy. A machine whose low-neutron fuel "
    "removes the biggest scheduled outages is a machine that can promise availability &mdash; the "
    "quiet-fuel dividend expressed as the thing customers care about."])],
 [("Blanket changeouts", "none (no blanket)"), ("Wall changeouts", "~0.035-0.144 in 30 yr (M-42)"),
  ("Driver", "5.44% neutron fraction"), ("Removed", "months-long D-T changeout cycle"),
  ("Delivered", "availability / uptime")],
 "The maintenance dividend is a qualitative, physics-driven consequence of the low-neutron budget; no "
 "cost or economic figure is attached here &mdash; those live in the confidential data room, off the "
 "public site."),

wp(C, "neutron-provenance",
 "Neutron Provenance: Every Channel Computed From Cross Sections",
 "The burner's neutron budget is not a literal in a file &mdash; it is derived, channel by channel.",
 "The burner's neutron output is computed from stored cross sections across every reaction channel "
 "&mdash; the D-3He primary, both D-D branches, and the secondary D-T burn &mdash; not carried as a "
 "hardcoded constant. The provenance of every neutron is traceable.",
 [("The science",
   ["The solve partitions fusion power by reaction: the neutron-free D-3He channel dominates, with the "
    "D-D neutron branch, the D-D proton branch, and a computed secondary D-T burn each contributing. The "
    "neutron fraction &mdash; 5.44% of fusion power at the deposited design point &mdash; is the sum of "
    "these, each derived from cross sections and plasma parameters, not a hardcoded literal."]),
  ("Why it matters",
   ["A neutron fraction computed from first principles can be re-derived and challenged; a constant "
    "cannot. This is the same discipline the whole programme applies &mdash; solve it, don't assume it "
    "&mdash; applied to the number the plant's shielding, activation, and licensing all depend on."])],
 [("Neutron fraction (design point)", "5.44% of fusion power"), ("D-3He primary", "neutron-free (dominant)"),
  ("Channels summed", "D-3He, both D-D, secondary D-T"), ("Method", "stored cross sections"),
  ("Not", "a hardcoded constant")],
 "The neutron budget is derived channel-by-channel and reproduces independently; the prior model's "
 "constant fraction was superseded by this computation, with the older value kept as labeled history."),
]

# ---------------------------------------------------------------------------
# SERIES D — Direct Energy Conversion & Power Handling — 14 papers
# ---------------------------------------------------------------------------
PAPERS += [
wp(D, "electricity-without-steam",
 "Electricity Without the Steam Detour",
 "When fusion energy arrives as charged particles, you can collect it like electricity &mdash; because it already is.",
 "Most fusion concepts end in a boiler. The burner's D-3He cycle delivers the bulk of its power in "
 "charged particles streaming out the mirror ends, so the plant harvests them directly &mdash; on the "
 "loss cone, with an electrostatic converter, no steam loop required.",
 [("The science",
   ["Charged particles leaving the mirror throat carry directed kinetic energy along open field lines. "
    "A direct-energy converter decelerates them against an electrostatic field and collects the current "
    "&mdash; converting particle energy to electricity without an intermediate thermal cycle. For a fuel "
    "whose output is already charged, the steam detour is an unnecessary loss."]),
  ("Why it matters",
   ["Skipping the full steam cycle raises plant efficiency and deletes cost: less turbine hall, less "
    "cooling, faster load response. Direct conversion is the architectural payoff of choosing a "
    "charged-particle fuel, and the mirror's open ends are what make it reachable."])],
 [("Harvest", "direct electrostatic conversion"), ("Input", "charged particles on the loss cone"),
  ("Steam cycle", "not required for the direct stream"), ("Fuel fit", "D-3He output is charged"),
  ("Benefit", "higher efficiency, faster load response")],
 "Direct conversion of charged-particle streams has experimental heritage; the burner's contribution is "
 "an integrated, gated design that never books converter credit beyond what its own exhaust-physics "
 "analysis supports."),

wp(D, "expander-end-tank",
 "The Expander: Turning a Beam Into a Collectible Sheet",
 "Before the burner can convert its exhaust, it has to spread it out &mdash; that is what the expander does.",
 "Between the ion-end throat and the converter sits the expander: a region where the field fans out from "
 "the 26.49 T ion-end throat down to about 0.5 tesla, spreading the dense exhaust beam so it can be "
 "collected without melting anything. That is a 53-fold expansion.",
 [("The science",
   ["Exhaust leaving the 26.49 T ion-end throat is far too concentrated to collect directly &mdash; about "
    "195 MW/m&sup2; at the aperture. Letting the field drop from 26.49 T to 0.5 T is a 53x expansion, "
    "which cuts the end-wall load to about 3.7 MW/m&sup2;. Only after this spreading can the direct "
    "converter handle the stream."]),
  ("Why it matters",
   ["The expander is what makes direct conversion physically survivable: it converts an unmanageable "
    "beam into a collectible sheet. It is also an honestly-flagged stretch &mdash; no such end-expander "
    "spec exists yet, so the 53x ratio is stated as a requirement, not a solved value."])],
 [("Ion-end throat field", "26.49 T (frozen A11)"), ("Expansion", "53x (26.49 T -> 0.5 T)"),
  ("Aperture load", "~195 MW/m&sup2;"), ("End-wall load after expansion", "~3.7 MW/m&sup2;"),
  ("Status", "requirement; no spec exists (B30)")],
 "The 53x expander is stated, not engineered &mdash; no end-expander spec exists (frozen B30), so it is "
 "one of the burner's honest engineering stretches, carried as such in the limitations."),

wp(D, "directed-fraction",
 "The Number That Feeds the Converter: Directed Fraction 0.648",
 "How much of the burner's power arrives as collectible directed energy is a computed value &mdash; with synchrotron charged.",
 "At the reference point, 0.648 of the burner's power reaches the converter as directed particle energy "
 "&mdash; computed with synchrotron radiation charged against it, not with an idealized ceiling. The "
 "directed fraction is what the whole direct-conversion case is built on, so it is computed honestly.",
 [("The science",
   ["The directed fraction is the share of power leaving as collectible charged-particle energy after "
    "radiation and other losses are subtracted. The reference solve returns 0.648 with synchrotron "
    "charged &mdash; a real, loss-inclusive value. An earlier evaluator quoted 0.871, but that figure "
    "had no synchrotron term at all."]),
  ("Why it matters",
   ["The converter must be specified against the power that actually reaches it, not against an "
    "optimistic ceiling. Using 0.648 rather than 0.871 sizes the converter to reality and keeps the "
    "plant ledger from booking energy that radiation already took."])],
 [("Directed fraction", "0.648 (synchrotron charged)"), ("Prior ceiling", "0.871 (no synchrotron)"),
  ("Feeds", "converter specification"), ("Loss subtracted", "synchrotron radiation"),
  ("Basis", "reference-point solve")],
 "The directed fraction is computed with radiation charged; the higher 0.871 figure is a "
 "zero-synchrotron ceiling, not a design value, and the converter is specified against the loss-"
 "inclusive number."),

wp(D, "ceiling-not-design",
 "0.871 Is a Ceiling, Not a Design Value",
 "A flattering directed-fraction number exists in the record &mdash; and the design refuses to use it.",
 "The figure 0.871 appears in the burner's lineage as a directed-particle fraction. It is a ceiling "
 "computed with no synchrotron radiation, reproducing to six significant figures from its own "
 "definition &mdash; but it is not the design's directed fraction, and the converter is not specified "
 "against it.",
 [("The science",
   ["The prior mirror evaluator had no synchrotron term in either the electron balance or the ledger, so "
    "its 0.871 directed fraction was a zero-radiation ceiling. Charging synchrotron at the reference "
    "point brings the real directed fraction to 0.648. The ceiling is mathematically exact but "
    "physically unreachable."]),
  ("Why it matters",
   ["Specifying a converter against a ceiling would oversize the harvest and overstate the plant output. "
    "Keeping 0.871 labeled as a ceiling &mdash; and designing against 0.648 &mdash; is the difference "
    "between a brochure and a buildable specification."])],
 [("Ceiling value", "0.871 (zero-synchrotron)"), ("Design value", "0.648 (synchrotron charged)"),
  ("Ceiling reproducibility", "6 significant figures"), ("Converter spec basis", "0.648"),
  ("Status of 0.871", "ceiling, labeled")],
 "0.871 is retained in the record as a labeled ceiling, not quoted as the directed fraction; this is "
 "the labeled-history discipline applied to a number that would otherwise flatter the converter spec."),

wp(D, "end-wall-heat",
 "Handling the Heat: 3.7 MW/m2 on the End Wall",
 "The burner's exhaust has to land somewhere &mdash; and where it lands is engineered to survive it.",
 "The burner's axial power loss &mdash; about 906 MW over two apertures, some 195 MW/m&sup2; at the "
 "throat &mdash; is far too concentrated to collect directly. The end-expander spreads it 53-fold to "
 "roughly 3.7 MW/m&sup2; on the end wall. Sizing that surface to survive the heat flux is as much a part "
 "of the design as the plasma itself.",
 [("The science",
   ["The 906 MW axial loss arrives across two apertures at about 195 MW/m&sup2; &mdash; unhandleable as "
    "is. A 53x field expansion (26.49 T to 0.5 T) drops it to about 3.7 MW/m&sup2;, a flux the collecting "
    "surfaces can take continuously. The end-wall load follows from the axial power and the expansion "
    "ratio together, both carried in the frozen record (B30)."]),
  ("Why it matters",
   ["Power handling is where many fusion concepts quietly fail; a converter that cannot survive its own "
    "input is not a converter. Publishing the axial power, the aperture flux, and the post-expansion "
    "end-wall load makes the heat-handling problem explicit and sizable, not hidden."])],
 [("Axial power loss", "~906 MW (two apertures)"), ("Aperture flux", "~195 MW/m&sup2;"),
  ("Expansion", "53x (26.49 T -> 0.5 T)"), ("End-wall load", "~3.7 MW/m&sup2;"),
  ("Status", "requirement; no spec exists (B30)")],
 "The end-wall load follows from the frozen axial power and 53x expansion (B30); no end-expander spec "
 "exists yet, so the heat-handling design is scoped against these figures and carried openly as a stretch."),

wp(D, "electron-dec-gate",
 "Electron Direct Conversion: A Named Gate, Not an Assumption",
 "One of the two things standing between the burner and net electricity is a converter that must be demonstrated.",
 "Electron direct conversion &mdash; efficiently collecting the electron component of the exhaust "
 "&mdash; is one of the burner's two named closure gates, alongside the plug density ratio. The "
 "programme states it as a gate that must be demonstrated, not as a capability it assumes.",
 [("The science",
   ["Collecting the directed ion energy is comparatively well understood; doing the same for the "
    "electron stream at high efficiency is not yet demonstrated at the burner's parameters. Because the "
    "converter's overall efficiency feeds directly into the engineering gain, electron direct conversion "
    "is a genuine gate on closure, and the design record names it as one."]),
  ("Why it matters",
   ["Naming the converter as a gate &mdash; rather than folding an assumed efficiency into the ledger "
    "&mdash; is what keeps the burner's closure claim honest. It tells experimentalists exactly which "
    "converter demonstration unlocks the plant, and it keeps the baseline conservative until then."])],
 [("Gate", "electron direct conversion"), ("Paired with", "plug density ratio"),
  ("Status", "to be demonstrated"), ("Feeds", "converter efficiency -> engineering gain"),
  ("Posture", "gate, not assumption")],
 "Electron direct conversion is carried as a named, unproven gate; the burner's baseline does not "
 "assume it is solved, and closure requires it alongside the plug density ratio."),

wp(D, "synchrotron-dominant-loss",
 "The Dominant Loss: Synchrotron Radiation at Half the Fusion Power",
 "The single largest energy loss in the burner is not the end leak &mdash; it is the light the electrons emit.",
 "The burner's biggest loss channel is synchrotron radiation: at the reference point it carries 100 MW, "
 "50.8% of the fusion power, as electrons spiraling in the strong field radiate. It is the loss that "
 "dominates the ledger and, therefore, the design's largest single uncertainty.",
 [("The science",
   ["Electrons at ~92 keV gyrating in a multi-tesla field emit synchrotron radiation strongly. At the "
    "reference point this is 100.1 MW &mdash; more than the directed end loss, more than bremsstrahlung, "
    "more than the neutron power combined. It is the term the engineering gain is most sensitive to, and "
    "it grows with electron temperature and field."]),
  ("Why it matters",
   ["Because synchrotron dominates the loss ledger, the accuracy of the synchrotron model largely "
    "decides whether the design closes. That is why the burner brackets it across published treatments "
    "rather than trusting a single formula &mdash; the honesty is in the uncertainty band."])],
 [("Synchrotron loss", "100.1 MW (reference)"), ("Share of fusion power", "50.8%"),
  ("Larger than", "directed loss, brems, neutrons"), ("Grows with", "electron temperature, field"),
  ("Role", "dominant loss, largest uncertainty")],
 "Synchrotron is the dominant loss and the decisive uncertainty; the burner's survival depends on "
 "reabsorption of that radiation, which is treated separately and flagged as the design's most "
 "consequential open question."),

wp(D, "synchrotron-bracket",
 "Bracketing the Uncertainty: Trubnikov, AFJ, and the Optically-Thin Bound",
 "The burner does not trust one synchrotron formula &mdash; it publishes the whole bracket, including the one that fails.",
 "The synchrotron loss that decides the burner's ledger is not known to one number. The design brackets "
 "it across published treatments: 57.9 MW (Trubnikov), 100.1 MW (the AFJ fit used at the reference "
 "point), and a 3,038 MW strict optically-thin bound &mdash; under which the design never closes.",
 [("The science",
   ["Synchrotron loss depends on how much emitted radiation is reabsorbed by the plasma. The three "
    "treatments span an enormous range: the optically-thin bound assumes no reabsorption and gives "
    "3,038 MW &mdash; 15.6x the fusion power &mdash; at which point the machine cannot close at any "
    "parameter combination. The reference uses the AFJ fit at 100 MW; Trubnikov is lower still."]),
  ("Why it matters",
   ["Publishing the full bracket, including the bound under which the design fails, is the opposite of "
    "cherry-picking. It tells the reader exactly how much of the burner's viability rides on "
    "reabsorption &mdash; which is precisely the quantity no one has measured at these conditions."])],
 [("Trubnikov", "57.9 MW"), ("AFJ (used)", "100.1 MW"), ("Optically-thin bound", "3,038 MW (never closes)"),
  ("Optically-thin vs fusion", "15.6x fusion power"), ("Decides", "whether the design closes")],
 "The synchrotron bracket is published in full, including the failing bound; the AFJ fit is used 8% "
 "outside its fitted temperature range at some window points, and it decides the answer &mdash; stated "
 "plainly as the dominant uncertainty."),

wp(D, "reabsorption",
 "Survival by Reabsorption: The Burner's Most Consequential Assumption",
 "The design closes only because the plasma reabsorbs most of its own synchrotron light &mdash; and that fraction is unmeasured.",
 "Under the strict no-reabsorption bound, the burner radiates 15.6 times its fusion power and never "
 "closes. The design survives only because the plasma reabsorbs most of that synchrotron radiation "
 "&mdash; a reabsorption fraction that has not been measured at these temperatures. This is stated as "
 "the most consequential open item in the harvest chain.",
 [("The science",
   ["Synchrotron radiation emitted by the electrons can be reabsorbed before it escapes, and the burner "
    "operates in a regime where that reabsorption is essential: the fitted model that gives a closeable "
    "100 MW loss extrapolates the reabsorption, while the optically-thin bound &mdash; zero reabsorption "
    "&mdash; gives 3,038 MW and no closure. No measurement of the reabsorption fraction at these "
    "conditions was available."]),
  ("Why it matters",
   ["This is where the burner is most exposed, and the record says so directly. Rather than hide the "
    "dependence inside a chosen formula, the design isolates it: closure rides on cyclotron "
    "reabsorption, which is exactly the experiment that would settle the burner's biggest question."])],
 [("No-reabsorption case", "3,038 MW radiated (never closes)"), ("Radiated vs fusion", "15.6x"),
  ("Survival requires", "cyclotron reabsorption"), ("Reabsorption fraction", "unmeasured at these conditions"),
  ("Status", "most consequential open item")],
 "The burner survives only through synchrotron reabsorption, and the reabsorption fraction is unmeasured "
 "at these temperatures &mdash; the single decisive uncertainty, isolated and named rather than buried "
 "in a formula choice."),

wp(D, "bremsstrahlung-crosscheck",
 "Bremsstrahlung, Cross-Checked",
 "The burner's second radiation channel is computed two ways, and the design uses the more cautious one.",
 "Bremsstrahlung &mdash; braking radiation from electron-ion collisions &mdash; carries 29.9 MW, about "
 "15% of fusion power, at the reference point. The design computes it two ways and reports the lower, "
 "so the ledger is mildly optimistic in a stated, bounded direction.",
 [("The science",
   ["The burner's bremsstrahlung form truncates its temperature series and omits the electron-electron "
    "term, so it under-estimates above ~100 keV. A published 2024 fit (Xie) is carried as a cross-check "
    "and runs 8% higher, at 32.3 MW. The reference uses the lower 29.9 MW value, and says so."]),
  ("Why it matters",
   ["Carrying a cross-check and naming which value is used &mdash; and in which direction it errs &mdash; "
    "is the difference between a number and an audited number. The 8% optimism is small, bounded, and "
    "disclosed, which is exactly how a design earns trust on the numbers that are not disclosed as "
    "uncertain."])],
 [("Bremsstrahlung (used)", "29.9 MW (15.2% of fusion)"), ("Cross-check (Xie 2024)", "32.3 MW (+8%)"),
  ("Value used", "the lower one"), ("Bias direction", "mildly optimistic, stated"),
  ("Under-estimates above", "~100 keV")],
 "The bremsstrahlung form under-estimates above ~100 keV; the Xie cross-check is carried at +8%, and "
 "the reference uses the lower value &mdash; a disclosed, bounded optimism, not a hidden one."),

wp(D, "recirculating-power",
 "Recirculating Power: What the Plug Costs the Plant",
 "The burner spends a large fraction of its own output keeping the plug alive &mdash; and that spend is the ledger's crux.",
 "The burner's engineering gain is what survives after the plant pays to sustain its own plug and drive "
 "its own plasma. At the reference point that recirculating fraction is 158% &mdash; the plant "
 "circulates more power internally than it nets &mdash; which is exactly why Q_E sits at 0.63.",
 [("The science",
   ["Auxiliary heating power of 195 MW sustains the reference plasma, split between ions and electrons, "
    "against a directed output that only partly funds it. The recirculating fraction of 158% is the gap "
    "the plug ratio must close: raising the plug density ratio deepens the confining potential, cuts the "
    "auxiliary power required, and drives the recirculating fraction down toward closure."]),
  ("Why it matters",
   ["The recirculating power is where closure is won or lost. Publishing it &mdash; rather than a bare "
    "gain number &mdash; shows precisely how much the plant spends on itself and how much the binding "
    "plug requirement has to recover. It makes the closure gate quantitative."])],
 [("Auxiliary heating power", "195.4 MW (reference)"), ("Recirculating fraction", "158%"),
  ("Engineering gain Q_E", "0.632"), ("Closed by", "raising plug density ratio"),
  ("Split", "68.3 MW ions / 127.1 MW electrons")],
 "The recirculating fraction is above 100% at the reference point &mdash; an honest statement that the "
 "baseline is an experiment, not a power plant. The plug density ratio is the parameter that drives it "
 "toward closure."),

wp(D, "converter-efficiency-window",
 "Converter Efficiency in the Window",
 "The direct converter's efficiency matters &mdash; but not as much as the one parameter that actually decides closure.",
 "The direct converter's efficiency is the fourth-ranked parameter in the burner's sensitivity study: "
 "it moves the engineering gain by about 1.4x across its range, with a comfortable window of 0.586 to "
 "0.80. It matters, but it is not the knob that reaches net electricity.",
 [("The science",
   ["Sweeping the converter efficiency moves the gain by a factor of 1.4 &mdash; meaningful, but far "
    "below the factor-of-11 swing the plug density ratio produces. The window within 10% of the "
    "reference spans 0.586 to 0.80, so the converter has real operating room without being the binding "
    "constraint."]),
  ("Why it matters",
   ["Knowing where the converter ranks tells the programme how hard to push it. The converter must be "
    "good, and electron direct conversion must be demonstrated, but the sensitivity study is clear that "
    "the plug ratio &mdash; not converter efficiency &mdash; is the parameter closure hinges on."])],
 [("Converter efficiency rank", "4th of 10"), ("Gain span", "~1.4x across range"),
  ("Window", "0.586-0.80"), ("Versus plug ratio", "x11 swing (dominant)"),
  ("Gate status", "electron DEC still required")],
 "Converter efficiency has a real but secondary effect on closure; the demonstration gate is electron "
 "direct conversion, and the dominant closure parameter remains the plug density ratio."),

wp(D, "multi-modal-harvest",
 "Diversified Power Handling: Directed, Radiated, and Residual",
 "The burner does not rely on a single conversion path &mdash; it collects power in several complementary ways.",
 "The burner harvests power in more than one mode: directed charged particles through the electrostatic "
 "converter, radiated power through radiation-handling surfaces, and the thermal balance through a "
 "compact bottoming cycle. No single path has to carry the whole plant.",
 [("The science",
   ["The reference ledger routes the fusion power through several channels &mdash; directed particle "
    "energy to the direct converter, synchrotron and bremsstrahlung radiation to radiation surfaces, and "
    "residual thermal power to a bottoming cycle. Each channel is computed and specified against its own "
    "physics, so the harvest is diversified rather than staked on one converter."]),
  ("Why it matters",
   ["A diversified harvest is more robust than a single-path one: if any single conversion mode "
    "underperforms, the others still contribute. It also lets the plant capture power that a "
    "direct-converter-only design would simply lose as heat."])],
 [("Mode 1", "directed charged particles (DEC)"), ("Mode 2", "radiated power (radiation surfaces)"),
  ("Mode 3", "residual thermal (bottoming cycle)"), ("Design", "diversified harvest"),
  ("Robustness", "no single path carries the plant")],
 "Each harvest channel is computed against its own physics and cited heritage; the direct-conversion "
 "path carries a named electron-DEC gate, and no channel books credit beyond what its analysis "
 "supports."),

wp(D, "lower-bound-convention",
 "Honest Lower Bounds: The Energy Convention the Ledger Uses",
 "Where the physics was ambiguous, the burner chose the convention that understates its own output.",
 "Where the burner's axial-loss energy accounting could be read two ways, the design chose the "
 "convention that excludes the plug potential from both sides &mdash; making the directed power a lower "
 "bound on converter input and the plug power a lower bound on recirculation. It rounds against itself.",
 [("The science",
   ["The calibration source's own equations proved internally inconsistent when evaluated at its stated "
    "point, so rather than tune an unsourced factor to make them fit, the burner adopts the unambiguous "
    "internal-energy form for axial loss. The consequence, stated in the code: directed power is a lower "
    "bound on converter input, plug power a lower bound on recirculation."]),
  ("Why it matters",
   ["Choosing the self-penalizing convention where the physics is ambiguous is the clearest signal of "
    "intent in the whole ledger. A design that rounds against itself when uncertain is a design whose "
    "favorable numbers can be trusted, because it did not manufacture them."])],
 [("Ambiguity", "axial-loss energy convention"), ("Choice", "exclude plug potential from both sides"),
  ("Directed power", "lower bound on converter input"), ("Plug power", "lower bound on recirculation"),
  ("Rejected", "tuning an unsourced factor")],
 "The convention is conservative by construction; where the calibration source was self-inconsistent, "
 "the burner reports the bounded form rather than fitting an unsourced factor &mdash; the numbers err "
 "toward understating output."),
]

# ---------------------------------------------------------------------------
# SERIES E — The Fuel Cycle: Tritium & Helium-3 — 12 papers
# ---------------------------------------------------------------------------
PAPERS += [
wp(E, "fuel-follows-purpose-cycle",
 "Fuel Follows Purpose, Not Platform",
 "The whole family's fuel logic reduces to one rule &mdash; and the fuel cycle is where it plays out.",
 "The breeder burns D-T and the burners burn D-3He, and the reason is a single rule: fuel follows "
 "purpose, not platform. The fuel cycle is where that rule becomes concrete &mdash; one machine makes "
 "the scarce isotope, the others consume it.",
 [("The science",
   ["Hyperion's purpose is to make materials, so it burns the most reactive, most neutronic fuel: D-T. "
    "The burners' purpose is clean electricity, so they burn the low-neutron, charged-particle fuel: "
    "D-3He. The cycle links them &mdash; the breeder's tritium decays to helium-3, which the burners "
    "need &mdash; so the rule is not just a slogan but a supply chain."]),
  ("Why it matters",
   ["A family whose fuel choices are each justified by mission, and whose fuel cycle physically connects "
    "them, reads as a strategy rather than a set of unrelated machines. The rule is what makes the "
    "sequencing &mdash; breeder first, burners after &mdash; inevitable rather than arbitrary."])],
 [("Rule", "fuel follows purpose, not platform"), ("Breeder", "D-T (materials, buildability)"),
  ("Burners", "D-3He (clean electricity)"), ("Link", "breeder tritium decays to burner He-3"),
  ("Consequence", "breeder-first sequencing")],
 "The rule is documented and applied consistently; the fuel cycle physically connects the machines, "
 "which is why the programme's sequencing follows from physics rather than preference."),

wp(E, "helium3-both-sides",
 "Helium-3: The Burner's Fuel, the Breeder's Co-Product",
 "The scarcest input in the family is made by one member and consumed by the others.",
 "Helium-3 sits on both sides of the family ledger: it is the fuel the burners must consume and the "
 "co-product the breeder quietly makes. Understanding the fuel cycle means understanding that one "
 "machine's output is another's input.",
 [("The science",
   ["The burners run on a D-3He mix and consume helium-3 at commercial scale (28-54 kg/yr per unit). Hyperion produces helium-3 two "
    "ways: as the decay product of the tritium it breeds, and as a direct D-D breeding channel in the "
    "plasma. The breeder's decade of production is what seeds the helium-3 the burners will need."]),
  ("Why it matters",
   ["This coupling is the strategic core of the programme. It means the burners' fuel dependency is not "
    "purely external &mdash; part of it is manufactured in-house by the breeder &mdash; while the "
    "remainder is stated honestly as a supply bet. The cycle turns a weakness into a sequence."])],
 [("Helium-3 role (burners)", "fuel (consumed)"), ("Helium-3 role (breeder)", "co-product (made)"),
  ("Breeder sources", "tritium decay + D-D breeding"), ("Link", "breeder output seeds burner input"),
  ("Remainder", "external supply, stated as a bet")],
 "The in-house helium-3 stream is carried as upside under a price-endogeneity rule, not banked into the "
 "base case; the burners' full fuel need still depends on external supply, which the programme states "
 "plainly."),

wp(E, "he3-demand-card-scale",
 "The Burner's Helium-3 Appetite",
 "The burners' demand for helium-3 is large enough to be the enabling condition of the whole product line.",
 "At production scale the burners need helium-3 at a level many times current world supply. That demand "
 "is not a hidden footnote &mdash; it is the enabling condition of the burner line, and the reason the "
 "burners are sequenced after the breeder that makes their fuel.",
 [("The science",
   ["Helium-3 demand scales with fusion power and therefore with machine length: a longer housing burns "
    "more fuel. At production scale the requirement is many times today's world supply for either "
    "housing, which is why the fuel condition, not the plasma physics, sets the delivery order of the "
    "product line."]),
  ("Why it matters",
   ["Publishing that the demand exceeds current supply &mdash; rather than assuming the fuel &mdash; is "
    "what makes the programme's sequencing honest. The burners cannot run at production scale on today's "
    "helium-3, and the record says so, which is exactly why they are the later products in the family."])],
 [("Helium-3 demand", "many times current world supply"), ("Scales with", "fusion power / machine length"),
  ("Status", "stated fuel constraint (enabling condition)"), ("Consequence", "burners sequenced after the breeder"),
  ("Specific card figures", "unresolved; omitted pending reconciliation")],
 "Specific per-housing helium-3 figures are unresolved across the design sources and are omitted here; "
 "what is firm and load-bearing is that production-scale demand exceeds current world supply, which is "
 "why the burners depend on a changed fuel landscape. No economics or price appears."),

wp(E, "lunar-helium3",
 "The External Gate: Lunar Helium-3",
 "The commercial burner fleet's largest dependency is not physics at all &mdash; it is where the fuel comes from.",
 "A commercial burner needs helium-3 at 28 to 54 kilograms per year &mdash; a level only lunar supply "
 "can plausibly provide, and a dependency entirely outside Kronos's control. The programme states it "
 "plainly and treats it as an external bet, with a leading authority on lunar helium-3 among the "
 "company's co-founders.",
 [("The science",
   ["A single commercial-scale burner needs 28-54 kg/yr of helium-3, far beyond terrestrial sources: "
    "tritium-decay stockpiles (~2 kg/yr) and in-plant breeding cover only a demonstrator. The balance "
    "points to lunar regolith helium-3 &mdash; an entire supply industry that does not yet exist and is "
    "not expected before roughly 2036. Kronos names this as the enabling condition, external to the "
    "company."]),
  ("Why it matters",
   ["Stating a dependency you cannot solve in-house is the hardest kind of honesty, and the programme "
    "does it: the commercial burner fleet is deliberately gated on lunar helium-3 precisely because its "
    "fuel landscape must change first. The bet is named, the expertise is on the founding team, and the "
    "number is not hidden."])],
 [("Commercial unit need", "28-54 kg/yr He-3"), ("Terrestrial cover", "~2 kg/yr decay (demonstrator only)"),
  ("Dependency", "lunar helium-3 supply (~2036)"), ("Kronos control", "external (stated bet)"),
  ("Expertise", "lunar He-3 authority among co-founders")],
 "The lunar helium-3 dependency is an external, unresolved bet stated plainly; it is why the commercial "
 "burner fleet waits for the fuel landscape to change (~2036), and no economic claim is attached to it here."),

wp(E, "tritium-decay-he3",
 "Stockpile That Ripens: Tritium Decay to Helium-3",
 "Every gram of tritium is a slow helium-3 factory &mdash; and the rate is a known physical constant.",
 "Tritium decays into helium-3 at a fixed rate &mdash; about 0.42 litres of helium-3 per gram of "
 "tritium per year. A tritium stockpile is therefore a helium-3 source that ripens on its own, which is "
 "one of the ways the breeder seeds the burners' fuel.",
 [("The science",
   ["Tritium's 12.3-year half-life means a stockpile continuously converts to helium-3. The Kronos "
    "record carries the corrected, deposited accrual figure of 0.42 L of helium-3 per gram of tritium "
    "per year. Terrestrial tritium-decay stockpiles are thus a real, if slow, helium-3 source that "
    "requires no new physics to exploit."]),
  ("Why it matters",
   ["Decay accrual is the most reliable helium-3 source there is, because it is just physics running on "
    "its own clock. It is one leg of a staged supply strategy &mdash; stockpile decay, in-plant "
    "breeding, and external reserves &mdash; that is resilient to any single source disappointing."])],
 [("Accrual rate", "~0.42 L He-3 / g tritium / yr"), ("Mechanism", "tritium decay (12.3-yr half-life)"),
  ("Source type", "terrestrial stockpiles"), ("New physics required", "none"),
  ("Role", "one leg of staged supply")],
 "The decay accrual is a known physical rate carried in the deposited fuel-cycle record; it is a "
 "partial, reliable supply leg, not a complete solution &mdash; the burners' full need still depends on "
 "additional sources."),

wp(E, "in-situ-breeding",
 "Breeding Fuel in the Burner: The D-D Helium-3 Channel",
 "The burner makes a little of its own helium-3 as it runs &mdash; a partial, honestly-bounded credit.",
 "The burner's own D-D reactions breed helium-3 directly in the plasma &mdash; about 1.1 x 10^19 nuclei "
 "per second at the reference point. It is a real makeup credit, but a partial one, and the design "
 "carries it as such rather than claiming self-sufficiency.",
 [("The science",
   ["One branch of the D-D reaction produces helium-3. In the burner this breeds helium-3 at roughly "
    "1.1 x 10^19 per second at the reference point &mdash; a genuine in-plant source. But it is a "
    "makeup credit, not an inventory solution: the reference solve does not even credit it back into the "
    "fuel mix, keeping the ledger conservative."]),
  ("Why it matters",
   ["In-situ breeding reduces, but does not eliminate, the burner's external helium-3 dependence. "
    "Carrying it as an uncredited partial makeup &mdash; rather than as a path to fuel independence "
    "&mdash; keeps the supply story honest and the external bet clearly stated."])],
 [("In-plant He-3 breeding", "~1.1 x 10^19 /s (reference)"), ("Channel", "D-D reaction branch"),
  ("Status", "partial makeup credit"), ("Credited to fuel mix?", "no (conservative)"),
  ("Effect", "reduces, not removes, external need")],
 "In-situ breeding is a partial makeup credit, not an inventory calculation, and is deliberately not "
 "credited back into the reference fuel mix; the burner's external helium-3 dependence remains real and "
 "stated."),

wp(E, "tbr-in-hyperion",
 "Breeding at 1.8: How Hyperion Makes More Than It Burns",
 "The breeder's surplus tritium is the whole point &mdash; and the breeding ratio is a design lever set to 1.8.",
 "Hyperion breeds 1.8 units of tritium for every unit it burns. That surplus above self-supply is what "
 "lets the breeder deliver tritium to the national requirement and seed the helium-3 stream at once "
 "&mdash; and the ratio is a lever the design sets, not a constant it inherits.",
 [("The science",
   ["A tritium breeding ratio above 1.0 means net production. Hyperion's blanket scan sets the ratio at "
    "1.8, leaving a 0.8 surplus above what the plasma consumes. That surplus, sized by the "
    "breeding-ratio lever, is delivered as product tritium &mdash; some to the national requirement, "
    "some ripening into helium-3."]),
  ("Why it matters",
   ["The breeding ratio is the knob that makes Hyperion a foundry rather than a self-consuming reactor. "
    "Setting it at 1.8 sizes the surplus to a real requirement, and treating it as a lever means the "
    "output can be tuned to demand rather than fixed by physics."])],
 [("Tritium breeding ratio", "1.8"), ("Surplus over self-supply", "0.8"),
  ("Surplus delivered as", "product tritium + He-3 accrual"), ("Ratio type", "design lever"),
  ("Source", "blanket scan")],
 "The 1.8 breeding ratio is a computed lever setting demonstrated in the blanket scan; the as-built "
 "blanket is where it is proven, and the surplus sizing follows a stated requirement, not a maximum."),

wp(E, "tritium-national-requirement",
 "Tritium to the National Requirement",
 "The breeder's primary product answers a supply gap the United States cannot currently fill at scale.",
 "Hyperion's primary product is tritium, delivered to a national requirement the country cannot "
 "currently source at scale. The breeder is sized to that requirement &mdash; 1.87 to 4.0 kg per year "
 "&mdash; rather than to a physics maximum, because the requirement, not the optimum, is the point.",
 [("The science",
   ["Tritium is scarce and decays continuously, so any national stockpile needs replenishment. "
    "Hyperion's D-T machine, breeding at a ratio of 1.8, produces a tunable surplus in the 1.87-4.0 "
    "kg/yr band &mdash; sized by the breeding-ratio lever to meet a stated requirement rather than to "
    "maximize output."]),
  ("Why it matters",
   ["Answering a genuine national supply gap is what gives the breeder a near-term purpose independent "
    "of the burners. It is the foundry's first product, and the machine is designed around delivering it "
    "reliably rather than spectacularly."])],
 [("Primary product", "tritium"), ("Output band", "1.87-4.0 kg/yr"), ("Sized to", "national requirement"),
  ("Breeding ratio", "1.8"), ("Purpose", "near-term supply gap")],
 "The tritium output band is a design choice against a stated requirement; the specific contracted "
 "figure and any economics are commercial matters kept off the public site. The physics that delivers "
 "the band is deposited."),

wp(E, "tritium-lean-cycle",
 "Tritium-Lean: The Burner's Fuel-Cycle Discipline",
 "The burner holds almost no tritium &mdash; a fuel-cycle property, not a safety add-on.",
 "The burner's fuel cycle is tritium-lean by construction: it produces tritium only as a transient D-D "
 "by-product, burns much of it immediately, and lets the rest decay toward helium-3. Its standing "
 "tritium inventory is a trace, enforced by the cycle's own mass balance.",
 [("The science",
   ["Unlike a D-T plant, the burner never stores tritium as fuel. The D-D breeding branch makes a small "
    "amount, about 17% of which burns in secondary reactions; the remainder decays to helium-3 &mdash; "
    "the fuel the plant actually wants. The mass-balance ledger holds the standing inventory to a trace "
    "quantity."]),
  ("Why it matters",
   ["A fuel cycle that keeps tritium a trace species is a fuel cycle with a small radiological source "
    "term. Tritium-lean is therefore both a licensing posture and a fuel-cycle fact, and it falls "
    "directly out of choosing D-3He over D-T."])],
 [("Burner tritium", "transient D-D by-product"), ("Burned immediately", "~17%"),
  ("Remainder", "decays to helium-3"), ("Standing inventory", "trace (mass-balance enforced)"),
  ("Consequence", "small radiological source term")],
 "Tritium-lean is a fuel-cycle property verified in the mass-balance ledger; operational tritium "
 "accountancy at plant scale is an execution item, scoped openly, and the burner never stores tritium "
 "as fuel."),

wp(E, "he3-unpriced-stream",
 "Carried at Zero: The Unpriced Neutron Stream",
 "One of the breeder's products has no market price anywhere in the world &mdash; so the programme books it at zero.",
 "Hyperion's 14 MeV neutron beam-hours are a real product with a real use &mdash; materials "
 "qualification &mdash; but no established market price exists for them anywhere in the world. The "
 "programme carries this stream at zero and sweeps it, never banking speculative value.",
 [("The science",
   ["Fusion-spectrum neutron irradiation is a genuine capability Hyperion provides, but beam-hours for "
    "14 MeV neutron testing are unpriced &mdash; there is no market benchmark to value them against. "
    "Rather than invent a price, the programme books the stream at zero and treats any future value as "
    "upside outside the base case."]),
  ("Why it matters",
   ["Booking an unpriced product at zero is the conservative, honest treatment: it keeps the breeder's "
    "case from resting on a number no market has ever set. If a neutron-irradiation market emerges, it "
    "is pure upside; the base case does not depend on it."])],
 [("Stream", "14 MeV neutron beam-hours"), ("Market price", "none, worldwide"),
  ("Carried at", "zero (swept)"), ("Future value", "upside, outside base case"),
  ("Treatment", "conservative, never banked")],
 "The neutron beam-hour stream is real physics carried at zero value because it is unpriced anywhere; "
 "this is a design/strategy statement of conservatism, not an economic projection, and no revenue "
 "figure is claimed."),

wp(E, "sequencing-breeder-fuels-demo",
 "Sequencing the Fuel: A Breeder Decade Feeds the Demonstrator",
 "The programme's order is a fuel-supply argument &mdash; make the fuel first, burn it later.",
 "The family is sequenced by fuel: Hyperion runs first and produces helium-3 for a decade, and that "
 "accumulated supply fuels the burner demonstrator that follows. The order of the products is the fuel "
 "cycle expressed as a schedule.",
 [("The science",
   ["Hyperion produces about 4 kg/yr of net tritium &mdash; roughly twice the entire world commercial "
    "tritium flow, making it the largest producer worldwide &mdash; and that surplus ripens into helium-3 "
    "by decay at about 2 kg/yr. That decay stream fuels a ~10 MWe self-fuelled Aegis demonstrator; a "
    "commercial unit's 28-54 kg/yr need waits on external supply. The sequence is dictated by the time "
    "it takes to accumulate the scarce fuel."]),
  ("Why it matters",
   ["Sequencing this way turns the burners' fuel dependency from an open-ended hope into a "
    "supply-limited schedule. The demonstrator's size is set by available fuel, and the breeder's decade "
    "of production is what makes any burner build possible at all."])],
 [("First", "Hyperion (breeder), ~4 kg/yr net T = 2x world flow"), ("Duration", "~decade of production"),
  ("Then", "~10 MWe self-fuelled Aegis demonstrator"), ("Fuel", "~2 kg/yr breeder decay He-3"),
  ("Commercial", "28-54 kg/yr, external supply gated")],
 "The sequencing is a fuel-supply strategy, not a dated commitment; the current plan is to begin breeder "
 "construction in Q2 2027, the demonstrator is sized to available fuel, and the specific timeline lives "
 "on revisable surfaces, never in the frozen physics record."),

wp(E, "burner-waits-for-2036-fuel",
 "A Self-Fuelled Demonstrator: ~10 MWe on the Breeder's Decay Helium-3",
 "The first burner is a ~10 MWe Aegis demonstrator, sized to the helium-3 the breeder's own tritium decays into.",
 "The first burner is a demonstrator, not a plant: about 10 MWe, self-fuelled by the helium-3 that "
 "Hyperion's surplus tritium decays into &mdash; roughly 2 kilograms per year. It is fuel, not physics, "
 "that sets its size, and a commercial unit's fuel need is many times larger.",
 [("The science",
   ["Surplus tritium decays to helium-3 at about 2 kg/yr per standing inventory &mdash; enough to fuel a "
    "roughly 10 MWe self-fuelled Aegis demonstrator (Phase 2), but far short of a commercial unit's "
    "28-54 kg/yr. So the demonstrator is sized to the self-supplied fuel, and the commercial burner "
    "fleet is honestly gated on an external helium-3 supply (lunar, ~2036)."]),
  ("Why it matters",
   ["Scoping the first burner to fuel the breeder itself produces keeps the whole programme honest about "
    "the helium-3 constraint. It proves the physics and the closure gates at a size the fuel supply can "
    "actually support, deferring commercial-scale power to a changed fuel landscape."])],
 [("Demonstrator output", "~10 MWe (self-fuelled Aegis, Phase 2)"), ("Fuel source", "~2 kg/yr breeder decay He-3"),
  ("Commercial unit need", "28-54 kg/yr He-3"), ("Commercial fleet gate", "external He-3 (lunar, ~2036)"),
  ("Sets the size", "available fuel, not physics")],
 "The ~10 MWe self-fuelled demonstrator and the 28-54 kg/yr commercial fuel need are frozen (B32); the "
 "commercial fleet's build timing waits explicitly on an external helium-3 supply that does not yet "
 "exist. No economics appear here."),
]

# ---------------------------------------------------------------------------
# SERIES F — Method, Safety & Trust — 16 papers
# ---------------------------------------------------------------------------
PAPERS += [
wp(F, "shows-its-work",
 "The Fusion Company That Shows Its Work",
 "Kronos's differentiator is not a claim about performance &mdash; it is a commitment to candor.",
 "Kronos states its identity plainly: the fusion company that shows its work. Every headline number "
 "traces to a deposited computation, every gate is named, and every superseded value stays in the "
 "record with a label. Candor is the product as much as the physics.",
 [("The science",
   ["The commitment is concrete, not rhetorical: stated gates, published sensitivities, and labeled "
    "history. The burner's below-unity baseline is on the first page; the breeder's confinement "
    "requirement is in the abstract; the synchrotron uncertainty that could sink the design is bracketed "
    "in the open. Nothing load-bearing is hidden."]),
  ("Why it matters",
   ["In a field crowded with overclaims, an auditable design is a rare and valuable thing. Reviewers and "
    "partners can rerun the deposit and check every number, which means the numbers can be believed. "
    "Showing the work is how Kronos earns trust it does not ask for on faith."])],
 [("Identity", "the fusion company that shows its work"), ("Expressed as", "stated gates, published sensitivities, labeled history"),
  ("Baseline", "below-unity, on the first page"), ("Uncertainties", "bracketed in the open"),
  ("Result", "auditable design")],
 "The candor is structural, not decorative: the one standing disclaimer is that this is conceptual "
 "design and simulation study, no machine has been built &mdash; and every number carries the gates "
 "stated in the text."),

wp(F, "frozen-points-recorded-withdrawals",
 "Frozen Points and Recorded Withdrawals",
 "A frozen number at Kronos is a commitment against silent change &mdash; not a claim of final truth.",
 "When Kronos freezes a quantity, it commits only to one thing: that the value will not change "
 "silently. A frozen number can still be withdrawn when better analysis requires it &mdash; but the "
 "withdrawal is dated, reasoned, and every document carrying the old value is swept.",
 [("The science",
   ["The freeze mechanism has teeth and has been exercised: of fourteen quantities frozen in one round, "
    "three were withdrawn and two restated within hours, each because it rested on a basis the freeze "
    "itself superseded. The remaining values stand, each re-verified from its source before freezing."]),
  ("Why it matters",
   ["A freeze that permits recorded withdrawal is stronger, not weaker, than one that pretends "
    "permanence. It lets the programme commit to consistency while staying correctable &mdash; the "
    "opposite of the silent design drift that produces a machine no single analysis ever checked."])],
 [("Freeze means", "no silent change"), ("Withdrawal", "dated, reasoned, documents swept"),
  ("Exercised", "3 withdrawn, 2 restated of 14 in one round"), ("Standing values", "re-verified from source"),
  ("Prevents", "silent design drift")],
 "A frozen value is a commitment against silent change, not a claim of truth; the withdrawal rule keeps "
 "the record correctable, and every superseded value stays labeled rather than erased."),

wp(F, "reproduce-from-source",
 "Reproduced From Source: Eleven of Eleven Checks",
 "Before a number is frozen, it is re-derived from its origin &mdash; and the re-derivation is logged.",
 "Every quantity Kronos froze in the product round was re-verified from its source immediately before "
 "freezing: eleven of eleven numerical checks reproduced. A number is eligible to be frozen only if it "
 "is sourced, derived from a sourced value, or recomputed from raw data.",
 [("The science",
   ["The freeze criterion is explicit: a quantity qualifies only if its provenance is traceable and "
    "nothing in flight can move it. Each candidate is recomputed from its origin, and the check is "
    "logged. In the product freeze, all eleven numerical re-derivations reproduced their frozen values "
    "exactly."]),
  ("Why it matters",
   ["Reproduction-from-source is the practical meaning of 'check us.' It is not enough that a number "
    "appears in a report; it must regenerate from its inputs. That discipline is what lets an outside "
    "reviewer trust the frozen card without taking any single document on faith."])],
 [("Checks", "11 of 11 reproduced"), ("Eligibility", "sourced, derived, or recomputed"),
  ("Timing", "re-verified immediately before freezing"), ("Logged", "each re-derivation"),
  ("Standard", "provenance traceable")],
 "The reproduction checks are logged and reproduced completely for the frozen set; eligibility requires "
 "traceable provenance, which is how the programme distinguishes a frozen number from a merely quoted "
 "one."),

wp(F, "bit-exact-verification",
 "Bit-Exact: Verifying Against the Prior Evaluator",
 "When the burner's new solver replaced the old one, it first reproduced the old one exactly &mdash; then corrected it.",
 "The burner's independent physics evaluator was validated by reproducing the prior evaluator "
 "bit-for-bit before it was trusted to correct it: a maximum relative error of 2.3 x 10^-15 across 72 "
 "values. Only then did the new solver's corrections carry weight.",
 [("The science",
   ["The new evaluator transcribed the prior model verbatim as one code path and ran it against every "
    "stored case, matching to machine precision &mdash; 2.3 x 10^-15 across 72 values including "
    "temperature, fusion power, radiation, and gain. Having proven it reproduces the old physics "
    "exactly, its independent physics (neutron budget from cross sections, synchrotron charged, "
    "Pastukhov confinement) could then be trusted where it disagreed."]),
  ("Why it matters",
   ["A new model that cannot reproduce the old one is not a correction; it is a different guess. "
    "Establishing bit-exact reproduction first is what lets the burner's corrections &mdash; the neutron "
    "fraction, the directed fraction, the D-T Q_E literal &mdash; stand as genuine improvements rather "
    "than disagreements."])],
 [("Reproduction error", "2.3 x 10^-15 (72 values)"), ("Method", "prior model transcribed verbatim"),
  ("Then added", "independent physics (cross sections, synchrotron, Pastukhov)"),
  ("Corrections", "neutron fraction, directed fraction, D-T literal"),
  ("Standard", "reproduce, then correct")],
 "The bit-exact reproduction establishes the new evaluator's fidelity before its corrections are "
 "trusted; the discrepancies it then found were diagnosed one by one, not asserted."),

wp(F, "declared-over-silent",
 "Declared Basis Over Silent Basis",
 "The recurring lesson in the Kronos record is not about arithmetic &mdash; it is about stating your assumptions.",
 "The most-repeated correction in the Kronos record is never that the math was wrong; it is that a "
 "basis was silent. The remedy, applied consistently, is to declare the assumption &mdash; the helium "
 "ash fraction, the confinement factor, the cost-recovery factor &mdash; so any change moves by "
 "recorded restatement.",
 [("The science",
   ["An audit of the breeder's gain found it rested on an undeclared ash fraction &mdash; the same "
    "silent-basis defect that had moved earlier frozen values. The arithmetic was correct; the problem "
    "was that the basis was not stated. The fix was to write f_He4 = 0.05 (Z_eff 1.158) into the entry, "
    "not to change the number."]),
  ("Why it matters",
   ["A declared basis converts a hidden assumption into a testable one. If a later determination "
    "disagrees, the value moves by recorded restatement rather than silent change &mdash; and reviewers "
    "always know exactly what each number is conditional on. Declaration is the whole discipline."])],
 [("Recurring defect", "silent basis (not bad math)"), ("Remedy", "declare the assumption"),
  ("Examples", "ash fraction, confinement factor, CRF"), ("On change", "recorded restatement"),
  ("Result", "assumptions testable")],
 "The declared-basis discipline is applied across the frozen set; each conditional value names its "
 "assumption in the entry, so nothing is conditional on a basis the reader cannot see."),

wp(F, "named-gates",
 "Named Gates, Not Hidden Assumptions",
 "Every Kronos machine states the specific things that must be demonstrated before it works.",
 "Rather than fold optimistic assumptions into its ledgers, Kronos names its gates: the burner's plug "
 "density ratio and electron direct conversion, the breeder's contracting instrument. A gate is a "
 "specific, testable thing that must be demonstrated &mdash; and each machine's gates are printed, not "
 "buried.",
 [("The science",
   ["A gate is different from a risk: it is a named requirement with a pass/fail condition. The burner's "
    "net electricity is gated on an end-plug density ratio of about 16 (347&times; GDT-measured) and on "
    "demonstrated electron direct conversion. The breeder's economics are gated on a government "
    "contracting instrument &mdash; a conversation, not an experiment. Each gate is stated where the "
    "reader can see it."]),
  ("Why it matters",
   ["Naming gates tells investors and researchers precisely which demonstration de-risks the most value, "
    "and it keeps the baseline honest by refusing to assume the gate is already passed. A gated design "
    "is a design you can plan experiments around."])],
 [("Burner gates", "plug density ratio, electron DEC"), ("Breeder gate", "government contracting instrument"),
  ("Gate definition", "named, testable, pass/fail"), ("Baseline", "does not assume gates passed"),
  ("Benefit", "de-risking is targetable")],
 "Gates are named and testable, and the baselines do not assume them passed; this is what separates a "
 "gated design from one that hides its assumptions inside a favorable ledger."),

wp(F, "labeled-history",
 "Labeled History: Superseded Values Are Kept, Not Deleted",
 "When a Kronos number changes, the old one stays in the record with an era label &mdash; on purpose.",
 "Kronos does not delete superseded values; it labels them. The old scaled gain, the earlier tokamak "
 "design point, the zero-synchrotron directed-fraction ceiling &mdash; each stays in the record as "
 "labeled history, so the reasoning that moved the number is visible.",
 [("The science",
   ["The labeled-history rule keeps the trail intact: a withdrawn value is annotated, not erased, so "
    "anyone can see what changed and why. The retired tokamak-era numbers, the withdrawn scaled gain, "
    "and the ceiling directed fraction all remain in the record with era labels rather than vanishing "
    "into a clean but unaccountable final version."]),
  ("Why it matters",
   ["A record that erases its own history cannot be audited; a record that labels it can. Keeping "
    "superseded values visible is what lets a reviewer reconstruct the design's evolution and trust that "
    "the current numbers are the result of correction, not concealment."])],
 [("Rule", "superseded values kept, labeled"), ("Examples", "scaled gain, tokamak point, 0.871 ceiling"),
  ("Annotation", "era label, not deletion"), ("Enables", "auditing the evolution"),
  ("Prevents", "unaccountable clean version")],
 "Labeled history is a deliberate discipline: the current numbers are traceable to the corrections that "
 "produced them, and no superseded value is quietly dropped from the record."),

wp(F, "deterministic-solves",
 "Deterministic by Construction: No Randomness in the Answer",
 "The burner's design point is a solve on a fixed grid &mdash; run it again and you get the same number.",
 "Every number in the burner's reference phase is a deterministic solve on a fixed grid. A random seed "
 "is set purely for hygiene; no randomness enters the physics anywhere. Rerun the scan &mdash; 51,840 "
 "points, zero failures &mdash; and the answer is identical.",
 [("The science",
   ["The reference phase evaluates a fixed design-space grid with no Monte Carlo, no stochastic solver, "
    "no random sampling in the physics. A seed is set only for reproducibility hygiene. The scan covers "
    "51,840 design points and 84 window points with zero failures, and every point is a deterministic "
    "function of its inputs."]),
  ("Why it matters",
   ["Determinism is what makes 'reproduce from source' literally true: there is no run-to-run variation "
    "to explain away. An outside reviewer who reruns the deposit lands on the exact same design point, "
    "which is the strongest possible form of an auditable result."])],
 [("Solve type", "deterministic, fixed grid"), ("Randomness in physics", "none"),
  ("Seed", "hygiene only"), ("Scan", "51,840 points, 0 failures"),
  ("Reproducibility", "identical on rerun")],
 "The design point is deterministic; the only randomness is a seed set for hygiene and used nowhere in "
 "the physics, so reproduction from source yields the identical result."),

wp(F, "largest-open-item",
 "Naming the Largest Open Item",
 "The burner's design record points directly at its own biggest weakness &mdash; and calls it the next track's job.",
 "The burner's design record does not hide its hardest problem; it names it. The end-plug &mdash; the "
 "component that must reach a density ratio of about 16 for closure &mdash; is specified as a "
 "requirement, not designed, and the record calls it 'the single largest open item' and hands it to the "
 "next track.",
 [("The science",
   ["A plug density ratio of ~16 implies a plug density of 4.16&times;10&sup2;&sup1; per cubic metre "
    "&mdash; 347&times; what the GDT mirror has measured and 26&times; the best published mirror design. "
    "The record names that requirement, states that it does not design the plug, does not cost it, and "
    "does not demonstrate it is achievable &mdash; and identifies it explicitly as the next track's "
    "subject (H53). At the reference ratio of 10 the machine does not close."]),
  ("Why it matters",
   ["Pointing at your own largest weakness is the opposite of salesmanship, and it is exactly what makes "
    "the rest of the design credible. A programme that names its hardest gate rather than burying it is "
    "a programme whose favorable numbers can be trusted."])],
 [("Largest open item", "the end-plug density (H53)"), ("Requirement", "n_p/n_c ~16 (Q_E 1.31)"),
  ("Plug density", "4.16&times;10&sup2;&sup1; m&#8315;&sup3; = 347&times; GDT / 26&times; best mirror"),
  ("At reference ratio 10", "does NOT close (Q_E 0.63)"), ("Status", "specified, not demonstrated")],
 "The plug is named as the single largest open item and explicitly not solved in this phase; the design "
 "concentrates its risk in one component and says so, rather than spreading it across soft assumptions."),

wp(F, "independent-crosschecks",
 "Cross-Checks From Independent Physics",
 "The burner's headline gain is trusted because a different method reached nearly the same number.",
 "The burner's engineering gain, Q_E 0.63, is not a single calculation but a convergence: an "
 "independent evaluator computing the neutron budget from cross sections, partitioning fusion products "
 "by slowing-down theory, charging synchrotron, and deriving confinement from Pastukhov theory lands "
 "within 3.8% of the prior figure.",
 [("The science",
   ["The prior model reached Q_E 0.657 without computing any of those four physics pieces. The new "
    "evaluator computes all four independently and reaches 0.632 &mdash; a genuine cross-check, not a "
    "re-run of the same assumptions. Supporting quantities agree too: central field within 1.0%, plasma "
    "volume within 0.6%."]),
  ("Why it matters",
   ["A number reached two independent ways is far stronger than a number reached once. The 3.8% "
    "agreement on gain, from methods that share no assumptions, is what lets the burner treat Q_E 0.63 "
    "as robust while still correcting the supporting numbers the two methods disagreed on."])],
 [("Gain (independent)", "Q_E 0.632"), ("Gain (prior)", "Q_E 0.657"), ("Agreement", "3.8%"),
  ("Independent pieces", "neutron budget, product partition, synchrotron, confinement"),
  ("Supporting agreement", "field 1.0%, volume 0.6%")],
 "The gain is corroborated by independent physics, not a single method; the two approaches agree to "
 "3.8% on the headline while disagreeing on supporting numbers, which the record diagnoses individually."),

wp(F, "read-limitations-first",
 "Read the Limitations First",
 "The burner's design record asks you to read its caveats before quoting anything above them.",
 "The burner's reference document carries an explicit instruction: read the limitations before quoting "
 "any number. Ten of them are listed &mdash; from the undesigned plug to the synchrotron model's fitted "
 "range to the flat-profile approximation &mdash; because a number without its caveat is a number "
 "waiting to be misused.",
 [("The science",
   ["The limitations are specific and consequential: the plug is a requirement not a design; the "
    "confinement prefactor is a calibrated shape assumption; the synchrotron fit is used slightly "
    "outside its range and it decides the answer; the profiles are flat; the bremsstrahlung form is "
    "mildly optimistic. Each is stated with its direction and magnitude."]),
  ("Why it matters",
   ["Putting the caveats first &mdash; and telling the reader to read them first &mdash; inverts the "
    "usual practice of burying limitations in a back section. It is the clearest expression of the "
    "'shows its work' identity: the design would rather be understood than admired."])],
 [("Instruction", "read limitations before quoting"), ("Listed", "10 limitations"),
  ("Examples", "undesigned plug, synchrotron fit range, flat profiles"), ("Each stated with", "direction and magnitude"),
  ("Placement", "before the results, not after")],
 "The limitations are foregrounded, not buried, and every headline number is meant to be read with "
 "them; this is the operational meaning of showing the work."),

wp(F, "safety-posture",
 "Safety Posture: A Trace Source Term and No Repository",
 "The burner's low-neutron fuel makes its safety case categorically different from a D-T plant's.",
 "The burner's safety posture follows from its physics: a trace tritium inventory rather than "
 "kilograms, an end-of-life inventory on the low-level-waste pathway rather than a geological "
 "repository, and a gentle wall rather than an activated one. The low-neutron fuel writes the safety "
 "case.",
 [("The science",
   ["Because the burner burns D-3He, its mobile radioisotope inventory is a trace D-D by-product, its "
    "structures activate far less than a D-T plant's, and its decommissioning stream fits existing "
    "low-level-waste disposal. There is no bulk tritium process stream and no breeding blanket to "
    "become high-activation waste."]),
  ("Why it matters",
   ["Safety analyses price the worst case, and the worst case scales with inventory and activation. A "
    "plant whose source term is a bounded trace and whose waste is low-level starts every safety and "
    "licensing conversation from a categorically better place than a breeding-blanket machine."])],
 [("Tritium inventory", "trace (D-D by-product)"), ("Waste class", "low-level-waste pathway"),
  ("Repository line", "none for vessel/internals"), ("Activation", "far below D-T"),
  ("Written by", "the low-neutron fuel")],
 "The safety posture is a physics consequence of the low-neutron fuel, verified in the mass-balance and "
 "activation ledgers; operational accountancy at plant scale remains an execution item, scoped openly."),

wp(F, "licensing-posture",
 "Licensing Posture of a Low-Neutron Plant",
 "The burner's biggest schedule advantage may be regulatory, and it comes straight from the fuel choice.",
 "A low-neutron plant with a trace tritium inventory presents regulators with a bounded, trace-species "
 "source term rather than a bulk radiological process. That is a licensing conversation that can start "
 "from precedent &mdash; which is a schedule advantage as much as a safety one.",
 [("The science",
   ["Licensing scales with the source term. The burner's sub-trace mobile-isotope inventory, absence of "
    "a breeding blanket, and low-level-waste decommissioning stream mean the plant is characterized by "
    "bounded, well-understood quantities rather than by the multi-kilogram tritium process a D-T plant "
    "must license."]),
  ("Why it matters",
   ["Licensing timeline is often the real critical path for a first-of-a-kind. A plant whose source "
    "term sits inside practiced limits starts that path from precedent rather than from a novel bulk "
    "process &mdash; time-to-permit is part of the low-neutron dividend."])],
 [("Source term", "bounded trace species"), ("Blanket", "none"), ("Waste", "low-level-waste pathway"),
  ("Conversation", "starts from precedent"), ("Advantage", "time-to-permit")],
 "The licensing posture is a design consequence of the fuel choice; the specific regulatory pathway is "
 "an execution matter, and no schedule or economic commitment is claimed here."),

wp(F, "experiment-not-power-plant-method",
 "An Experiment, Not a Power Plant: The Founder's Baseline",
 "The phrase that governs every Kronos claim is a refusal to call an experiment a power plant.",
 "The founder's stated baseline for the burner is a discipline: it is an experiment, not a power plant. "
 "The claim is staged &mdash; an unchannelled experiment resting on no speculative physics, with "
 "confinement and conversion as measurable gates, not assumptions. The language is chosen to keep the "
 "claim honest.",
 [("The science",
   ["The baseline makes no bet on unmeasured physics: no alpha channelling, no assumed converter "
    "efficiency, a below-unity gain stated plainly. Closure is staged behind measurable gates &mdash; "
    "the plug density ratio and electron direct conversion &mdash; so the path from experiment to plant "
    "is a sequence of demonstrations, each of which can be checked."]),
  ("Why it matters",
   ["Calling the baseline an experiment is what earns the right to state the closing numbers when they "
    "come. A concept that calls its experiment a power plant forfeits credibility on everything after; "
    "one that stages the claim keeps it. The phrase is the method in miniature."])],
 [("Baseline", "an experiment, not a power plant"), ("Rests on", "no speculative physics"),
  ("Channelling", "none assumed"), ("Closure", "staged behind measurable gates"),
  ("Gates", "plug ratio, electron DEC")],
 "The 'experiment, not a power plant' framing is the founder-ratified baseline; closure is staged "
 "behind measurable gates, and the burner never claims net electricity it has not demonstrated."),

wp(F, "sensitivity-published",
 "Sensitivity Published, Not Buried",
 "Kronos ranks its parameters by how much they matter &mdash; and publishes the ranking, inconvenient entries included.",
 "The burner's sensitivity study ranks all ten design parameters by how much they move the engineering "
 "gain, and the ranking is published in full. It reveals an uncomfortable truth &mdash; nine parameters "
 "barely matter and one carries the whole closure &mdash; and Kronos prints it anyway.",
 [("The science",
   ["The ranking spans a factor of 11 (plug density ratio) down to essentially flat (central-cell "
    "length, channelling efficiency). Publishing it tells the reader exactly where the design is robust "
    "and where it is exposed. The single dominant parameter is the binding requirement; the wide, flat "
    "window in the other nine is real operability."]),
  ("Why it matters",
   ["A published sensitivity ranking is a map of a design's real risks. It points every experiment at "
    "the parameter that matters and prevents effort from being spent on knobs that do not move the "
    "answer. Burying it would hide both the operability and the single point of exposure."])],
 [("Parameters ranked", "10, by gain sensitivity"), ("Top", "plug density ratio (x11)"),
  ("Bottom", "length, channelling (flat)"), ("Reveals", "9 inert, 1 binding"),
  ("Status", "published in full")],
 "The sensitivity ranking is published complete, including the finding that most parameters are inert; "
 "it is a map of the design's real exposure, not a curated selection."),

wp(F, "open-deposit",
 "Open Deposit: Data and Code, Not Just Claims",
 "Every headline number in the Kronos record traces to deposited data and runnable code.",
 "Kronos does not ask to be believed; it asks to be checked. The design points, the scans, the "
 "evaluators, and the verification logs are deposited so any reader can rerun the physics and land on "
 "the same numbers. The deposit is the difference between a claim and a result.",
 [("The science",
   ["The reference phase deposits the design-point tables with every parameter basis-tagged, the "
    "operating-window and sensitivity scans, the verification checks, and the evaluator code itself. "
    "The breeder's frozen quantities each carry an evidence class &mdash; computed, derived, or "
    "retrieved. Nothing load-bearing exists only as an assertion."]),
  ("Why it matters",
   ["Openly deposited data and code are what make 'check us' more than a slogan. A reviewer with the "
    "deposit can reproduce the design point, test the sensitivities, and audit the corrections &mdash; "
    "which is the strongest guarantee a design study can offer, and the one Kronos builds its identity "
    "on."])],
 [("Deposited", "design points, scans, evaluators, checks"), ("Parameters", "basis-tagged"),
  ("Frozen values", "carry an evidence class"), ("Reproducible", "rerun -> same numbers"),
  ("Identity", "check us, don't trust us")],
 "The deposit is openly available under a permissive license and contains no economics, cap table, or "
 "confidential material &mdash; only the design and physics needed to reproduce the numbers. Check the "
 "work; the code is there."),
]

# ---------------------------------------------------------------------------
# SERIES G — The Mode D2/M Evolution: cleaner and more durable — 4 papers
# Environmental + economic evolution of D1/L; the plasma physics is inherited UNCHANGED.
# The detailed breeder environmental design layer (waste-class ceilings, dpa/steel lever, emergency-plan
# multiples, RAFM/siting design detail) is INTERNAL-ONLY and lives off the public site; only the
# high-level "physics closes, the rest is engineering" message + public-dose-closes are public.
# ---------------------------------------------------------------------------
PAPERS += [
wp(G, "physics-closes-rest-is-engineering",
 "Breeder Physics Closed; Burner Closing Point Locked on One Requirement",
 "The breeder's power balance is closed and reproduces; the burner has a reproducible closing point contingent on a single named requirement.",
 "The two machines are at different, honestly stated places. The breeder's physics is closed: it reaches "
 "Q 3.424 at 88.7 MW and breeds 4 kg of tritium a year, closing without a wall, and it reproduces from "
 "the deposited config. The burner has a reproducible closing point too &mdash; Q_E 1.31 at helium-3 "
 "fraction 0.30 &mdash; but that closure is REQUIREMENT-class: it rests on an end-plug density near "
 "347 times what has been measured, specified rather than demonstrated.",
 [("The science",
   ["Breeder H01-H05 (Q 3.424, closes_nowall) reproduces at config 22021. The burner's Q_E 1.31 / "
    "f_n 5.44% closing point (M-45) reproduces on the deposit's own solver, but only at plug density "
    "ratio n_p/n_c ~16; at the reference ratio 10 it does not close (Q_E 0.63, net -160 MWe). The plug "
    "density is the single largest open item (M-47, H53). The environmental items &mdash; economics, "
    "public dose, waste class &mdash; are engineering and procurement with known solutions."]),
  ("Why it matters",
   ["Honesty about where each machine stands is the load-bearing claim. The breeder's physics is done; "
    "the burner has a reproducible net-positive point whose realization hinges on one hard, named "
    "confinement requirement. Neither is oversold, and the earlier non-reproducible burner gains "
    "(Q_E 1.002 / 1.191 / 1.825) are withdrawn rather than defended."])],
 [("Breeder physics", "Q 3.424, 88.7 MW, closes no-wall (frozen, reproduces)"), ("Burner closing point", "Q_E 1.31, f_n 5.44% (reproducible)"),
  ("Burner caveat", "requirement-class: plug ~16 (347x GDT), not demonstrated"), ("Reference n_p/n_c=10", "does NOT close (Q_E 0.63)"),
  ("Withdrawn", "burner Q_E 1.002 / 1.191 / 1.825 (non-reproducible)")],
 "Breeder closure is frozen and reproduces; the burner closing point (M-45) reproduces but is "
 "requirement-class (M-47), never presented as demonstrated. The capital number, margins, lunar He-3, "
 "and the plug-density requirement stay explicitly open."),

wp(G, "public-dose-closes",
 "Public Dose Closes, With Room to Spare",
 "The offsite dose requirement is met by an ordinary detritiation system, far inside demonstrated practice.",
 "The breeder's public-dose case closes as an achievable requirement. Meeting the offsite dose target "
 "needs a detritiation factor between 1 and 34 &mdash; against an ITER-class demonstrated capability of "
 "1,000 to 10,000. The margin is two to four orders of magnitude; this is a design task with a known "
 "solution, not a physics gap.",
 [("The science",
   ["The required detritiation factor to meet the public-dose target is 1 to 34. Demonstrated ITER-class "
    "detritiation runs 1,000 to 10,000 &mdash; so the requirement sits far inside proven capability, with "
    "remote siting reducing it further. Detritiation is off-the-shelf technology, not a first-of-a-kind "
    "development."]),
  ("Why it matters",
   ["Public dose is often assumed to be a hard barrier for a tritium facility. Showing it needs only a "
    "single-to-double-digit detritiation factor, against demonstrated four-digit capability, converts a "
    "feared unknown into a routine engineering specification &mdash; part of why the non-physics items "
    "are the easy part."])],
 [("Required detritiation factor", "1-34"), ("Demonstrated ITER-class", "1,000-10,000"),
  ("Margin", "~2-4 orders of magnitude"), ("Detritiation", "off-the-shelf technology"),
  ("Status", "closes as an achievable requirement (D2-45)")],
 "The dose closure is frozen as an achievable requirement (D2-45); the detritiation design itself remains "
 "an open engineering item, and the underlying facility-specific derivation is held internal."),

wp(G, "burner-replacement-waste-near-zero",
 "The Burner's Scheduled-Replacement Waste Is Essentially Zero",
 "A first wall that lasts a century of full-power operation is a first wall you almost never replace.",
 "The burner's low-neutron budget gives its first wall a life of 104 to 428 full-power years. Over a "
 "30-year plant life that works out to between 0.035 and 0.144 first-wall changes &mdash; effectively "
 "none. Scheduled-replacement waste, the dominant activated-waste stream in a D-T plant, is essentially "
 "zero for the burner.",
 [("The science",
   ["First-wall life scales inversely with neutron flux. At the burner's design-point neutron fraction "
    "of 5.44%, the frozen first-wall life is 104-428 full-power years (B31); dividing a 30-year "
    "operating window by that life gives 0.035-0.144 wall changes. The burner's capacity factor is "
    "therefore plug-limited, not damage-limited &mdash; the opposite of the breeder."]),
  ("Why it matters",
   ["The scheduled replacement of activated first walls and blankets is the waste stream and the outage "
    "that dominate D-T fusion operations. Removing it almost entirely is both an environmental result "
    "and an availability result &mdash; the low-neutron fuel paying off twice."])],
 [("First-wall life", "104-428 fpy (frozen B31)"), ("Changes in 30 yr", "~0.035-0.144 (~none)"),
  ("Scheduled-replacement waste", "essentially zero"), ("CF limit", "plug-limited, not damage-limited"),
  ("Contrast", "D-T replaces wall/blanket on a monthly-scale cycle")],
 "The near-zero replacement-waste result is frozen (M-42, derived from B31 life 104-428 fpy); the "
 "plug-reliability capacity factor that ultimately sets uptime is a standing research ask, not yet pinned."),

wp(G, "why-not-fully-aneutronic",
 "Why Not Fully Aneutronic: The x >= 0.45 Redesign",
 "The burner could be made far cleaner &mdash; but true near-aneutronic operation is a different machine, and the record says so.",
 "It is tempting to push the burner toward zero neutrons by loading it with helium-3, but on the locked "
 "config that breaks closure. Above a helium-3 fraction of about 0.43 the power balance no longer closes: "
 "the helium-3-heavy fuel does not react hard enough to fund the mirror's end losses. True near-aneutronic "
 "operation is a named future machine, not this design.",
 [("The science",
   ["On the locked closing config the window is x_He3 in [0.20, ~0.43]. Below 0.20 the charged-power "
    "budget starves; above ~0.43 the reaction rate falls too far and the machine no longer closes. "
    "Reaching near-aneutronic cleanliness (x &ge; 0.45) would require a redesigned machine &mdash; higher "
    "field, density, or size &mdash; not just more fuel."]),
  ("Why it matters",
   ["The honest version of the aneutronic dream names its cost. Helium-3-helium-3 fusion is a north star "
    "worth stating, but presenting it as a tweak to this machine would be false. The record keeps it as a "
    "labeled future option, which is what lets the low-neutron claim on the actual design stay credible."])],
 [("Closure window", "x_He3 in [0.20, ~0.43]"), ("Below 0.20", "charged-power budget starves"),
  ("Above ~0.43", "reaction rate too low; does not close"), ("Near-aneutronic (x >= 0.45)", "requires a REDESIGNED machine"),
  ("3He-3He", "a north star, not this design")],
 "The closure window [0.20, ~0.43] and the loss of closure above it are frozen on the locked config "
 "(M-46); the near-aneutronic redesign is a named option, not a current design point. The earlier "
 "x=0.5/0.95 collapse figures were on the withdrawn config and are dropped."),
]

# ---------------------------------------------------------------------------
# Assign sequential numbers and build
# ---------------------------------------------------------------------------
for i, p in enumerate(PAPERS, start=1):
    p["n"] = i

TOTAL = len(PAPERS)

INDEX_CSS = CSS + """
.lede{font-size:17px;margin:22px 0 10px;color:var(--ink)}
.seriesblock{margin:34px 0 8px}
.seriesblock h2{font-family:Verdana,Arial,sans-serif;font-size:13px;letter-spacing:1.2px;
  text-transform:uppercase;color:var(--navy);border-bottom:2px solid var(--acc);padding-bottom:6px;margin-bottom:4px}
ol.papers{list-style:none;counter-reset:none}
ol.papers li{border-bottom:1px solid var(--line);padding:11px 4px}
ol.papers a{color:var(--navy);text-decoration:none;font-size:16px}
ol.papers a:hover{color:var(--acc)}
.num{font-family:Verdana,Arial,sans-serif;font-size:12px;color:var(--acc);margin-right:10px}
.psub{display:block;font-size:13.5px;color:var(--mut);font-style:italic;margin-top:3px}
"""

def build_index():
    order = [A, B, C, D, E, F, G]
    blocks = []
    for s in order:
        items = [p for p in PAPERS if p["series"] == s]
        lis = "".join(
            '<li><span class="num">%03d</span><a href="%s">%s</a>'
            '<span class="psub">%s</span></li>' % (
                p["n"], "KFE-WP%03d_%s.html" % (p["n"], p["slug"]),
                esc(p["title"]), esc(p["sub"]))
            for p in items)
        blocks.append('<div class="seriesblock"><h2>%s</h2><ol class="papers">%s</ol></div>'
                      % (esc(s), lis))
    body = "".join(blocks)
    return """<!DOCTYPE html><html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Whitepaper Library — Kronos Fusion Energy</title><style>{css}</style></head><body><div class="page">
<div class="brand"><span>KRONOS <b>FUSION</b> ENERGY</span><span>WHITEPAPER LIBRARY</span></div>
<div class="eyebrow">Design &amp; Physics Series &middot; {total} papers</div>
<h1>The Kronos Whitepaper Library</h1>
<p class="lede">A library of short papers on the Kronos design and its low-neutron fuel cycle &mdash; the
Hyperion breeder, the Aegis and MetroVolt burner, and the method that ties them together. Every paper
leads with the physics, names its gates, and traces to deposited data and code. No economics, no
forecasts &mdash; design and low-neutron, on the record.</p>
{body}
<div class="foot">Conceptual design and simulation study; no machine has been built. Values are
simulation-derived and carry the feasibility gates named in each paper; superseded values are kept in
the record with era labels. Informational only; not an offer of securities.
&copy; 2026 Kronos Fusion Energy, Inc. &middot; Los Angeles, California.</div>
</div></body></html>""".format(css=INDEX_CSS, total=TOTAL, body=body)

if __name__ == "__main__":
    written = 0
    for p in PAPERS:
        fn = "KFE-WP%03d_%s.html" % (p["n"], p["slug"])
        with open(os.path.join(HERE, fn), "w", encoding="utf-8") as f:
            f.write(render(p, TOTAL))
        written += 1
    with open(os.path.join(HERE, "index.html"), "w", encoding="utf-8") as f:
        f.write(build_index())
    print("Wrote %d whitepapers + index.html (%d total papers) to:" % (written, TOTAL))
    print(HERE)
    # sanity: slug uniqueness
    slugs = [p["slug"] for p in PAPERS]
    dupes = set(s for s in slugs if slugs.count(s) > 1)
    print("Duplicate slugs:", dupes if dupes else "none")
    print("Series counts:", {s: sum(1 for p in PAPERS if p['series']==s)
                             for s in [A,B,C,D,E,F,G]})
