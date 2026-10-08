---
target: план і його стани (plan.html, -empty, -error, -loading)
total_score: 28
max_score: 40
na_heuristics: 
p0_count: 0
p1_count: 1
target_identity: "file:/Users/valeriiadryha/prevently2/wireframes/plan.html"
target_fingerprint: "sha256:a29e5dc4a6053f7efa88fb6bbee13e82136d8f837f352e233d9f87a88d6bab62"
target_path: /Users/valeriiadryha/prevently2/wireframes/plan.html
timestamp: 2026-10-08T08-56-26Z
slug: wireframes-plan-html
---
⚠️ DEGRADED: single-context (sub-agents not spawned: harness policy allows them only on explicit user request)

Target: wireframes/plan.html + states plan-empty, plan-error, plan-loading — «Ніжна» over the wireframe via wireframes/_nizhna.css

## Design Health Score
| # | Heuristic | Score | Key issue |
|---|---|---|---|
| 1 | Visibility of system status | 3 | Skeletons + "рахуємо на цьому пристрої"; loading→loaded jump of the excluded section |
| 2 | Match real world | 3 | Plain Ukrainian, recognisable exam icons; "ризик-орієнтовані" leans on the subtitle |
| 3 | User control | 3 | Every card folds back, tab bar always there, three exits on error |
| 4 | Consistency | 2 | "Зараз · 2" counts "не позначено", but only "прострочено" looked actionable; key section h2 17px vs 20px elsewhere; chevron illegible |
| 5 | Error prevention | 3 | No destructive actions on this screen; marking happens on its own screen |
| 6 | Recognition | 3 | Layer source in the heading, words on statuses; key section below the fold |
| 7 | Flexibility | 2 | Filter strip is the only accelerator |
| 8 | Aesthetic & minimalist | 3 | Calm, one accent; excluded items read as a wall of text |
| 9 | Error recovery | 3 | Plain language, three ordered exits, privacy reassurance first |
| 10 | Help | 3 | "Про підхід" one tap away, source on every item, disclaimer |
| Total | | 28/40 | Good |

## Design specificity
Content structure and niche colour are product-specific (pink/peach, pastel exam badges, layer sources in headings). Card anatomy is health-app generic. The product's distinctive half — "Розглянули і не включили" — had the weakest visual voice: plain text rows without the fact-row language the plan cards use.

Detector: CLI 38 findings on 4 files, but the static scan resolved only the grey _wireframe.css (contrast on service annotations outside the phone, h2 15/h3 14 of the grey layer) — not representative. Browser (rendered): plan 13, empty 8, error 3, loading 1. Real: tight-leading ×6, cramped-padding ×1 (unverified tag). False positives: nested-cards (phone bezel; flattening bezel 3→0), em-dash (Ukrainian punctuation, text frozen), text-occlusion on hidden content of a closed card, dark-glow from the detector's own overlay.

## Priority issues
1. [P1] "Розглянули і не включили" left the first screen: 721px (wireframe 625, viewport 670). Ніжна scale: mini cards 90–107px vs 66–83. Inline-status variant measured 700 and looked cramped. Needs owner decision.
2. [P2] "не позначено" looked like "пройдено" while the counter calls it "Зараз". Fix: .due states in a pill (outline), colour only in overdue.
3. [P2] Key section heading smaller than layer headings (17 vs 20). Fix: one h2 size.
4. [P2] "З'явиться у твоєму плані" is a 12px caption without an anchor. Fix: fact row with calendar chip, as in plan cards.
5. [P2] Solar Bold Duotone alt-arrow-down at 18px reads as a tick/bird. Fix: round-alt-arrow-down 24px.

## Persona red flags
- П1 Перевіряльниця: first screen shows layers and four cards, no hint of the excluded section; inside, "Розглянули і не включили у твій чекап:" repeats ×3 (text frozen).
- Casey: expanded-card actions in the thumb zone; filter chips 31px tall (AA ≥24, below 44).
- Sam: focus ring follows card radius; state = word + icon shape; icons are CSS pseudo-elements, not announced; 31/31 contrast pairs pass.

## Minor
- Tight leading on multi-line 13px text; unverified tag cramped; loading→loaded jump; widows in header line.
- Error page: three equal cards, order shown only by button weight.
- Empty state: "Найближче" card weighs the same as an item — absence not yet shown as confidently as presence.

## Questions to consider
- What if "пройдено" items took one line — would the excluded section come back, and is that a fair priority?
- Should absence get its own visual signature — the only element on the screen that is not a white card?
