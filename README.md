# Website Publications — MetroVolt Whitepaper Library

Forty short whitepapers for the Kronos Fusion Energy website — 60% science / 40% marketing —
each traceable to the certified canon of the MetroVolt four-paper series and its deposited
81-simulation programme (S01–S81; DOI 10.5281/zenodo.21248916).

## Contents
- `KFE-WP01…WP40_*.html` — the forty papers, self-contained (inline CSS, no external assets),
  web-ready and print-friendly (each prints to a clean 2-page PDF from any browser).
- `index.html` — the library page, grouped by series:
  - **Series A — The Machine** (WP01–14): shape, geometry, fuel, frozen point, systems closure,
    operating window, confinement, current, magnets, field lever, disruptions, wall, turbulence, MHD.
  - **Series B — Energy & Product** (WP15–24): DEC, the channeling gate, two postures, output,
    low-neutron dividend, ³He supply, tritium-lean, activation, shielding, materials.
  - **Series C — Economics & Market** (WP25–32): cost ladder, PPA band, Wright's law, firm power,
    FOAK BOM, G1 testbed, off-take flexibility, siting.
  - **Series D — Programme & Trust** (WP33–40): open manifest, reproducibility, gates, adverse
    findings, regulation, AEGIS (defense), roadmap, reader's guide.
- `build_whitepapers.py` — the generator. All content lives here as data; edit and rerun
  (`python3 build_whitepapers.py`) to regenerate every page consistently.

## Standards enforced
- Every number is the canonical value from the certified publication set (81 = 76 + 5; 2.41 GW;
  42.5 MA; 24.6/24.4 T; 5.25%; H98 1.8–2.2; 10.3 GJ ledger; locked LCOE ladder; 43/43 suite).
- "Low-neutron", never "aneutronic" (WP03 states the rule on purpose).
- MetroVolt = commercial; AEGIS = defense (WP38).
- Every paper carries a "Straight answers" honest-gap box, the DOI check-us CTA, and the
  conceptual-design disclaimer footer. No confidential material (cap table, raise plans) anywhere.

## Updating after a canon change
Change the value in `build_whitepapers.py`, rerun it, and spot-check with the publication set's
`check_package.py` philosophy: normalized scans, positive value grids.
