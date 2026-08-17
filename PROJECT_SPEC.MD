# Project Spec

Living external memory for the AI-assisted cloud kitchen inventory simulation. Update after every session. Assignment source of truth: [`docs/CONSOLIDATED_INSTRUCTIONS.MD`](docs/CONSOLIDATED_INSTRUCTIONS.MD). Prompt patterns: [`docs/prompt_templates.md`](docs/prompt_templates.md).

This file is the **single source of truth** (assignment Task 2 / §11). The Template 1 granular plan that lived in `IMPLEMENTATION_PLAN.MD` is merged here. Local agent prompt queues (formerly `PROMPT_PROGNOSTICATION.MD`) are parked under `waste-bin/` and are not submission deliverables.

**Last updated:** 2026-08-16 (Template 4 usage-log examples; approvals marked Approved)

---

## Session re-anchor

```text
Here is our project context. We are building a Python-based cloud kitchen inventory simulation using seed_data.py (Recipes, Inventory, Orders, Restock, Status). We have completed [DONE]. Current work: [CURRENT]. Do not modify any previously implemented functions.
```

**Today’s fill-in**

- **SP6 stamped 2026-08-14:** base assignment (Tasks 1–10), DR1–DR8, SP7, SP3/SP4, and **Assumption Closeout AC1–AC15** are complete. Living spec matches that reality.
- **Still open (not claimed done):** Student self-check **“I understand the code.”**
- **Ignored / not claimed:** **SP5** waste-bin delete (exclude `waste-bin/` from any submission zip). **Extra credit** not taken.
- Do not modify previously implemented functions unless the prompt names them. Do not implement Part II extras unless we explicitly take extra credit.

---

## Where we are

| | |
|--|--|
| **Together** | (none required — SP6 stamped) |
| **Solo** | Confirm “understand the code” |
| **Ignored** | SP5 / waste-bin (exclude from zip; not claimed deleted) |
| **Just finished** | **SP6** — living spec stamped for base + AC |
| **You are here** | Zip for submit |
| **Do not** | Claim SP5 deleted. Claim extra credit. |

```text
BASE ████████████████  Tasks 1–10 + DR + SP3/SP4/SP7 + AC1–AC15
SPEC ████████████████  SP6 stamped (honest caveats below)
OPEN ░░░░░░░░░░░░░░░░  “understand the code”
```

**SP6 stamp verdict (2026-08-14):** Living `PROJECT_SPEC.MD` is **submission-ready for the base assignment and Assumption Closeout**. It is **not** a claim that every human submit-polish item is closed: “understand the code” remains on you. Suite currently **79 OK** (re-run locally before zip if desired). Extra credit **not** taken. SP5 **not** claimed as deleted.

---

## Approvals

Code reviewed. All items below are **Approved** unless noted.

| Item | Decision |
|------|----------|
| Template 1 (granular plan; now this file) | Approved |
| Template 2 Data Connectivity (DC1–DC9) | Approved |
| Template 2 Order Processing (OP1–OP15) | Approved |
| Template 2 Restock (RS1–RS6) | Approved |
| Template 2 Business summary (SM1–SM4) | Approved |
| Template 2 Refactor (RF1–RF4) | Approved |
| Template 2 Writeup (WR1–WR3) | Approved |
| main() display (DC7) | Approved |
| Fulfillment expiry: past expiry blocks; expiring soon does not | Approved |
| Simulation date `2026-05-10`; tests pass `reference_date` | Approved |
| Failed-order restock: rebuild + OP15 | Approved |
| Code to date (through OP6) | Approved |
| RS1 named constants | Approved |
| Extra credit (K) | Not approved |
| Template 1 assumptions/gaps audit plan | Approved |
| Template 2 Remaining Gaps Closeout (SP7 optional; SP3–SP4; SP6) | Approved. SP5 waste-bin ignored / not joint |
| Template 2 Assumption Closeout (AC1–AC15) | Approved |
| RF2 / RF3 which two refactors | Approved. A `_inventory_by_name`; B `_days_until_expiry` |
| SM3 output form (console / dict / Markdown) | Approved. Console print + returned dict. No Markdown file |
| Three-source audit (base complete; submit polish only) | Approved |
| Template 2 Submit Polish (SP1–SP6; SP7 optional) | Approved |
| SP1 checklist gaps-only audit | Approved |
| SP6 living-spec stamp (base + AC; caveats) | Approved |
| Template 4 debugging examples (RS3, RS4, SP7, RX1) | Approved |

---

## Punch list

Legend: `[x]` done · `[~]` partial · `[ ]` not started · **← YOU ARE HERE**

Core loop: look up recipe(s) and total scaled ingredients → check stock **and** expiry → if ok, deduct and mark Delivered → if not, Not Delivered, reason, and restock missing/expiring/unavailable items.

### Project / process

- [x] **Setup (code)** — `main.py`, `seed_data.py`, `test_main.py`, `PROJECT_SPEC.MD`, `AI_USAGE_LOG.MD`. Import works.
- [x] **Setup (writeup)** — Drafted in `WRITTEN_RESPONSE.MD`. **SP3** recorded. **SP4** recorded (historical 49 OK; current suite **79 OK** as of SP6 stamp).
- [x] **Spec** — this file; **SP6 stamped 2026-08-14** (base + AC; see stamp verdict).
- [x] **Refactor** — RF2 `_inventory_by_name`; RF3 `_days_until_expiry`; DR1–DR8; **RF5/RF6 (2026-08-16)** split `process_orders` (127→32 lines) and `build_manager_summary` (162→54). Public signatures unchanged.
- [x] **Reflection (400–600 words)** — Answers all six questions (589 words); covers Template 4 use and the de-duplication / integration passes.
- [~] **Submit polish (SP1–SP6)**
  - [x] SP1 WR3 checklist gaps only
  - [x] SP3 Record `main.py` run
  - [x] SP4 Record unittest run
  - [x] SP5 Remove `waste-bin/` — **ignored / not joint** (exclude from zip; **not** claimed deleted)
  - [x] SP6 Stamp PROJECT_SPEC submission-ready — **Done 2026-08-14** (honest caveats in Where we are)
  - [x] SP7 Fail-reason wording if `expired`/`unusable` — **Done 2026-08-12**
- [x] **Assumption Closeout (AC1–AC15)** — **Complete 2026-08-14.**
### Simulation behavior

- [x] **Load and display** — Loaders + printers + tests. `main()` prints all five seed tables first, then processes, then prints updated inventory / restock / status, then the manager summary.
- [x] **Recipe lookup** — Exact name match; `None` if missing; qty 2 doubles grams.
- [x] **Inventory availability** — Quantity + past expiry (`days < 0`) block fulfillment. Expiring soon does not. None / empty / negative quantities do not crash.
- [x] **Fulfill and deduct** — All-or-nothing; deduct on success; no deduct on fail (including expiry fail). Restock on fail is rebuild + OP15 merge.
- [x] **Cumulative deduction** — `deepcopy` working inventory; later orders see remaining stock; final snapshot after all orders.
- [x] **Restock and expiry (full requirement)** — Rules, fields, constants, date, tests, and failed-order items without silent duplicates.
- [x] **Business-friendly summary** — Counts, reasons, inventory, restock, expiry concerns. `main()` prints the text and returns the dict.
- [x] **Summary tests** — Counts match processed orders; failed orders with reasons; live restock in the summary; dict plus manager-readable `text`.

### Reflection questions (Task 11)

1. How did AI help you move faster?
2. Where did AI make mistakes or questionable assumptions?
3. How did testing help you evaluate AI-generated code?
4. What did you change or reject from the AI’s suggestions?
5. How did `PROJECT_SPEC.md` help maintain context?
6. What would you do differently in a future AI-assisted coding project?

### Sequence (assignment Tasks 1–11)

Work **top to bottom**. Implement rows wait until you send that prompt. Internal IDs (DC/OP/RS/…) are for prompts only; the writeup uses assignment Tasks 1–11.

| # | ID | Assignment | What | Status |
|---|----|------------|------|--------|
| 1 | T1 | Task 2 | Whole-project plan | Approved |
| 2 | DC | Task 3 | Template 2 Data Connectivity | Approved |
| 3 | DC9 / DC1 | Tasks 1–3 | Inspect loaders; import `seed_data` | Approved |
| 4 | DC2–DC6, DC8 | Task 3 | Load/print/tests | Approved |
| 5 | DC7 | Task 3 | `main()` prints all five seed tables | Approved |
| 6 | OP | Tasks 4–7 | Template 2 Order Processing | Approved |
| 7 | OP1–OP5, OP8–OP13 | Tasks 4, 6, 7 | Lookup through cumulative | Approved |
| 8 | OP6 | Task 5 | Expiry in `check_inventory_availability` | Approved |
| 9 | OP7 | Task 5 | Bad inputs on availability | **Done** |
| 10 | OP14 | Task 6 | Re-check fulfill after expiry | **Done** |
| 11 | RS | Task 8 | Template 2 Restock and Expiry | Approved |
| 12 | RS1 | Task 8 / 10 | Named constants | **Done** |
| 13 | RS2 | Task 8 | Inspect current restock vs spec | **Done** |
| 14 | **RS3** | Task 8 | Multi-reason + full fields + all three rules | **Done** |
| 15 | RS4 | Task 8 | Explicit simulation date in restock | **Done** |
| 16 | RS5 | Task 8 | Refresh restock from final inventory | **Done** |
| 17 | RS6 | Task 8 | Restock unit tests | **Done** |
| 18 | OP15 | Task 6 | Failed-order items on restock | **Done** |
| 19 | SM | Task 9 | Template 2 Business Summary | Approved |
| 20 | SM1–SM4 | Task 9 | Manager summary + tests | **Done** |
| 21 | RF | Task 10 | Template 2 Refactor | Approved |
| 22 | RF1–RF3 | Task 10 | Suggest, then two accepted refactors | **Done (A + B)** |
| 23 | WR | Task 11 | Template 2 Writeup | Approved |
| 24 | WR1–WR2 | Tasks 1 writeup, 11 | Skeleton + reflection | **Done** |
| 25 | SP | Submit | Template 2 Submit Polish | **Approved; SP1 done** |
| 26 | SP1 | Submit | Checklist gaps only (WR3) | **Done 2026-08-12** |
| 28 | RGC | Submit | Template 2 Remaining Gaps Closeout | **SP7/SP3/SP4/SP6 done; SP5 ignored** |
| 29 | SP7 | Optional | Fail-reason wording if `expired`/`unusable` | **Done 2026-08-12** |
| 30 | SP3 | Submit | Record `python main.py` run | **Done 2026-08-12** |
| 31 | SP4 | Submit | Record `python -m unittest -v` | **Done 2026-08-12 (49 OK)** |
| 32 | SP5 | Submit | Remove `waste-bin/` from tree | **Ignored — not joint (2026-08-12)** |
| 33 | SP6 | Submit | Stamp PROJECT_SPEC submission-ready | **Done 2026-08-14** (caveat: understand-the-code) |
| 34 | AC | Quality | Template 2 Assumption Closeout | **Approved; AC1 done** |
| 35 | AC1 | Quality | Seed import + loaders comments | **Done 2026-08-12** |
| 36 | AC2 | Quality | Grams everywhere including buns | **Done 2026-08-12 (50 tests)** |
| 37 | AC3 | Quality | Exact recipe name match | **Done 2026-08-12 (51 tests)** |
| 38 | AC4 | Quality | Expired vs expiring-soon | **Done 2026-08-12** |
| 39 | AC5 | Quality | Availability defaults + bad inputs | **Done 2026-08-12 (52 tests)** |
| 40 | AC6 | Quality | Restock raise on bad date (RF3) | **Done 2026-08-12 (53 tests)** |
| 41 | AC7 | Quality | Lookup last-wins + snapshot qty-only | **Done 2026-08-13 (65 tests)** |
| 42 | AC8 | Quality | All-or-nothing / no partial deduct | **Done 2026-08-13 (66 tests)** |
| 43 | AC9 | Quality | Status seed vs append | **Done 2026-08-13 (69 tests)** |
| 44 | AC10 | Quality | SP7 reason labels | **Done 2026-08-13 (69 tests)** |
| 45 | AC11 | Quality | Restock rules + replace table | **Done 2026-08-13 (70 tests)** |
| 46 | AC12 | Quality | OP15 duplicate + par | **Done 2026-08-13 (73 tests)** |
| 47 | AC13 | Quality | Working inventory deepcopy | **Done 2026-08-13 (74 tests)** |
| 48 | AC14 | Quality | Missing-recipe reason path | **Done 2026-08-13 (75 tests)** |
| 49 | AC15 | Quality | Summary + main display | **Done 2026-08-14 (75 tests)** |
| — | K | Extra credit | One option | Only after base works; **not approved** |

---

## 1. What we are building and why

Python simulation of a **single operational day** in a delivery-only **cloud kitchen**: multiple virtual brands share one kitchen, staff, equipment, and a **single inventory**.

The program must: process orders; look up and scale recipes; check shared inventory (quantity **and** expiry); update delivery status; deduct grams on delivered orders only; track expiry risk; produce a restock plan; produce a business-friendly summary.

This is not only working code. The assignment also requires guiding AI, inspecting output, testing, debugging, and documenting decisions. Every technical choice should reduce **stockouts, waste, or rejected orders**.

**Why it matters:** after aggregator commissions (often 20–30%) and other costs, contribution margins are often 5–15%. Stockouts lose sales and ranking; expiry can waste 8–15% of food cost; rejected/partial orders hurt ratings.

---

## 2. Decisions already made

- **Fulfillment:** all-or-nothing. Failed orders do **not** deduct inventory. Partial fulfillment is extra credit only.
- **Recipe match:** exact `Orders.item` ↔ `Recipes.name`. Missing recipe → do not crash; record reason; skip that item’s demand.
- **Working inventory:** `deepcopy` during processing; mutate the live inventory table only after **all** orders (`apply_final_inventory_snapshot`).
- **Earlier order wins** when two orders compete for the same ingredient.
- **Restock timing (base):** apply restock rules to **final** inventory after all orders. Restock-every-N-orders is not a substitute.
- **Restock labels:** `"Expiring soon"`, `"Out of stock"`, `"Running low on stock"`.
- **Thresholds (must become named constants):** running low ≤ 1,000g; par 10,000g; expiring soon within 5 days of the simulation date.
- **Restock qty:** out of stock → 10,000g; expiring soon → 10,000g; running low → `10000 - current_qty` (e.g. 500g → 9,500g).
- **Simulation date:** `2026-05-10`. Tests always pass an explicit `reference_date`. Do not use `date.today()` as the silent production default. Approved
- **Fulfillment expiry:** past expiry (`days < 0`) blocks. Expiring soon does not; it only flags restock. Approved
- **Failed-order restock:** rebuild from final-inventory rules and ensure failed-order missing/unusable items appear without duplicates (OP15). Approved
- **main() display:** print all five seed tables first, then process, then print updated inventory / restock / status. Approved
- **One task per implementation prompt.** Do not rebuild the whole project in one shot.
- **Do not modify previously implemented functions** unless the prompt names them.
- **Template 1:** first AI plan (five coarse components, chat only) was **rejected**. The granular plan is this file (formerly `IMPLEMENTATION_PLAN.MD`). Approved (granular revision)

---

## 3. Constraints the AI must follow

- Use the **provided** seed schema. Do not invent a different data model.
- Implement **one small task** at a time. Validation hooks + tests before moving on.
- Failed tests: Template 4 (root cause), then re-run **all** tests.
- After every AI-generated function, run the 5-point review.
- Thresholds, par, and expiry window must be **named constants**, not scattered magic numbers.
- No credentials or API keys in the repo.
- Keep simulation logic in `main.py` unless there is a clear reason not to.
- Student remains Navigator / Reviewer / Decision-Maker. Plausible ≠ correct.

### How every implementation slice is done

1. **Template 3** — one named task only.
2. **S1 validation hook** — assumptions, uncertainty, incomplete parts (inline comments).
3. **S2 tests** — `unittest` in `test_main.py`; isolate mutable tables with `deepcopy`.
4. You run `python -m unittest -v`.
5. **Template 4** if anything fails — root cause, then re-run **all** tests.
6. **S4 five-point review** — correctness, hidden assumptions, hard-coded values, bad inputs, business-critical logic.
7. **S5** — update this file (punch list, where we are, gaps).
8. **S6** — log the major interaction in `AI_USAGE_LOG.MD`.

Stop the next slice until the current one is reviewed.

---

## 4. Data structures

Inspect `seed_data.py`. Do not assume a different schema.

| Structure | Role | Seed shape | Key fields |
|-----------|------|------------|------------|
| **Recipes** | Item → ingredients + grams | 5 items (Margherita Pizza, Chicken Burger, Caesar Salad, Pasta Alfredo, Chocolate Cake) | `recipe_id`, `name`, `ingredients[{name, qty_grams}]` |
| **Inventory** | Shared stock + expiry | 14 ingredients | `ingredient`, `qty_grams`, `expiry_date` (string `YYYY-MM-DD`) |
| **Orders** | Incoming demand | 5 orders, brands Taco Bell and Subway | `order_id`, `brand`, `items[{item, qty}]` |
| **Restock** | Flagged ingredients + reason | 5 seeded rows; live table rebuilt after processing | `item`, `qty_needed_grams`, `reason` — **required output also needs current quantity and expiry info** |
| **Status** | Delivery result per order | 5 rows | `order_id`, `delivered` (bool), `remark` |

Tests should treat `qty_grams` as a number and `expiry_date` as a string.

---

## 5. Business rules (must implement)

### Quantity scaling

Line qty 2 → double every ingredient gram. Scale linearly.

### Missing / unknown recipes

Handle gracefully. Clear failure reason. Do not crash.

### Availability (before fulfill)

Account for ingredient name, quantity required vs available, and **expiry / unusable** if dates exist. Return whether the order can be fulfilled and what is missing or unavailable.

### Fulfillment

If **all** required ingredients are available (enough quantity, not expired/unusable): mark **Delivered** and deduct used grams.

Otherwise: mark **Not Delivered**; record the reason; add missing/unavailable ingredients to restock (no silent duplicates); **no** partial inventory deduction.

### Cumulative inventory

1. Order 1 consumes inventory if delivered.
2. Order 2 checks stock remaining after Order 1.
3. Later orders check stock remaining after all prior **delivered** orders.
4. Final inventory reflects all delivered orders.
5. Do not reset inventory between orders except in isolated tests.
6. Print/update the final inventory table only after all orders are processed.

### Restock and expiry (after orders)

Flag if **any** condition holds. **Preserve all reasons** (do not overwrite with `elif`).

| Condition | Rule | Qty needed |
|-----------|------|------------|
| Out of stock | qty = 0 | 10,000g |
| Running low | qty ≤ 1,000g | to reach 10,000g |
| Expiring soon | within 5 days of simulation date | 10,000g |

Each restock row must include: ingredient name, **current quantity**, reason(s), quantity needed to reach par, **relevant expiry information**.

Healthy stock (above 1,000g, not expiring soon) is not flagged.

---

## 6. Implementation plan

Build **top to bottom**. Assignment prompt patterns: [`docs/prompt_templates.md`](docs/prompt_templates.md).

| # | Component | Why | Status |
|---|-----------|-----|--------|
| A | Project setup + spec | Files, import, living requirements | Code done; writeup open |
| B | Data connectivity | Load and show all five tables | Done (DC7) |
| C | Recipe → demand | Name → ingredients → scaled grams | Done |
| D | Availability | Quantity **and** expiry; bad inputs | Done (OP6, OP7) |
| E | Fulfillment | Deliver + deduct, or reject + reason | Done (OP15) |
| F | Cumulative processing | Order 2 sees stock left after Order 1 | Done |
| G | Restock and expiry | Final-inventory flags; **all** reasons; full fields | Done (RS1–RS6 + OP15) |
| H | Business summary | Manager-readable day report | Done (SM1–SM4) |
| I | Refactor | ≥2 documented improvements | Done (RF2 + RF3; later RF5 + RF6 size split) |
| J | Writeup | Written response, reflection, checklist | Drafted; personal edit + WR3 open |
| K | Extra credit | One option only, after base works | Not approved |
| L | Submit polish / Remaining Gaps / Assumption Closeout | Close gaps; verify assumptions before stamp | **AC1–AC15 + SP6 stamped** |

### Three-source audit (2026-08-12) — accepted

Sources compared separately:

| Source | What it is | Audit verdict |
|--------|------------|---------------|
| **Part I** | Graded assignment brief (`docs/INSTRUCTIONS.MD` Part I) | Base Tasks 1–10 / R1–R7 met. Reflection present. Checklist / run evidence still open. |
| **Part II** | Project Plan PDF (`docs/INSTRUCTIONS.MD` Part II) | Steps 1–5 + §10 practical path met. Design narrative extras (partial fulfillment; restock every N) **not** built — correct for base. Template 4 examples are in `AI_USAGE_LOG.MD` (RS3 if/elif, RS4 `date.today()`, SP7 fail-reason wording, RX1 expired restock). |
| **CONSOLIDATED** | Merge; Part I wins conflicts | Same as Part I for graded scope. Plan extras demoted. Submit polish remaining. |

**Not base gaps (do not add as required punch items):** partial fulfillment; restock-every-N checkpoints; Part II §9 enhancements; Markdown report (extra-credit option D).

### Code in `main.py` vs this plan

| Function | Status |
|----------|--------|
| `load_*` / `print_*` (five tables) | Done |
| Import `seed_data` | Done — file is `seed_data.py` |
| `find_recipe_by_name` | Done; exact match; `None` on miss |
| `calculate_ingredient_requirements` | Done; linear scale |
| `combine_requirements` | Done |
| `check_inventory_availability` | Quantity + past expiry + bad-input guards |
| `deduct_inventory` | Done; success path only |
| `update_status_entry` | Done; may append if `order_id` is new |
| `process_orders` | All-or-nothing; deepcopy working inventory; restock via rebuild + OP15 merge |
| `add_failed_order_items_to_restock` | **Done (OP15).** Missing/unavailable failed-order items; skip names already on the table. |
| `_inventory_by_name` | **RF2.** Shared ingredient-name lookup. |
| `_days_until_expiry` | **RF3.** Shared expiry-day parse. Restock does not catch; others do. |
| `_classify_inventory_stock_flags` | **DR1–DR3.** Shared qty/expiry flags; wired into restock + manager summary. **RX1:** also flags expired (Part I R6). |
| `_resolve_order_lines` / `_decide_order_outcome` / `_process_single_order` | **RF5.** `process_orders` split: pure lookup, pure decision, and the one place that deducts and writes status. |
| `_split_orders_by_delivery` / `_summarize_inventory_health` / `_render_manager_summary_text` | **RF6.** `build_manager_summary` split: order classification, inventory health, and presentation. |
| `apply_final_inventory_snapshot` | Done |
| `calculate_restock_needs` | Multi-reason + full fields. Default date `SIMULATION_DATE` (2026-05-10). |
| `refresh_restock_table` | Full rebuild; not a per-fail append |
| `build_manager_summary` | **SM1–SM2 done.** Counts, reasons, final inventory, restock, low/out/expired/expiring soon. |
| `main()` summary output | **SM3 done.** Prints `summary["text"]` after processing; returns the dict. No Markdown file. |
| Named constants | **Done (RS1)** |
| Documented refactors | **Done.** RF2 `_inventory_by_name`; RF3 `_days_until_expiry`. |
| Reflection | **Done** in `WRITTEN_RESPONSE.MD` (589 words) |

### Remaining slices (do not skip)

| ID | Must | Must not |
|----|------|----------|
| RS1 | **Done.** Named constants: 1,000g / 10,000g / 5 days. | Change restock *behavior* (that is RS3). |
| RS2 | Inspect restock vs this spec. List gaps only. | Write features. |
| RS3 | **Done.** Preserve all reasons. Full fields. All three rules. | Change fulfillment to partial. |
| RS4 | **Done.** `SIMULATION_DATE = date(2026, 5, 10)`. Tests pass `reference_date`. | Silent `date.today()`. |
| RS5 | **Done.** Inspect: rebuilds from final inventory after all orders; `clear` + `extend`. | Restock-every-N as the base rule. |
| RS6 | **Done.** Zero; 500g; ≤1,000g; above threshold; expiring soon; multiple reasons; healthy not flagged. | |
| OP15 | **Done.** Rebuild from final inventory, then add failed-order missing/unusable items once. | Change all-or-nothing. |
| SM1 | **Done.** Delivered / not-delivered counts, lists, and reasons. | Inventory, restock, expiry, or `main()` wiring. |
| SM2 | **Done.** Final inventory, restock, low/out/expired/expiring soon. | Extra credit reporting (option D) as a substitute. Wire into `main()`. |
| SM3 | **Done.** Console print of manager text; `main()` returns the dict. | Markdown file (extra-credit report). Change SM1–SM2 content. |
| SM4 | **Done.** Counts match processed orders; failed orders with reasons; restock included; dict/`text` a manager can read. | Other features. |
| RF1 | **Done (suggest only).** Inventory lookup dict; expiry-day parse; restock vs summary flags. | Change signatures. Apply a refactor in this pass. |
| RF4 | **Done (suggest only).** Constants leftover; `process_orders` size; restock error handling; quiet functions. | Apply a refactor in this pass. |
| RF2 | **Done.** `_inventory_by_name` used by availability, deduct, and OP15 restock. Public signatures unchanged. | Second refactor. Change public signatures. |
| RF3 | **Done.** `_days_until_expiry`. Restock still raises on a bad date; availability and summary still catch. | Change public signatures. Extra credit. |
| WR1 | **Done (draft).** Headings + bullets in `WRITTEN_RESPONSE.MD`. | Invent process. Change simulation code. |
| WR2 | **Done (589 words).** Six questions answered from log/spec. | Invent successes or failures. |
| WR3 | Merged into **SP1** (gaps-only checklist audit). | Implement features in the same prompt. |
| SP1 | **Done 2026-08-12.** Gaps-only audit vs Part I / CONSOLIDATED §19 / writeup before-submit. See **SP1 gap list** below. | Tick checklist boxes. Edit reflection. Delete files. Run code. |
| SP3 | **Done 2026-08-12.** `python main.py` exit 0; seed tables → process → updates → manager summary recorded in writeup. | Change simulation logic. Fix failures by rewriting closed tasks. |
| SP4 | **Done 2026-08-12** (49 OK); **re-run 2026-08-16 → 79 OK**. Recorded in writeup. | Change tests to force green. Skip failing tests. |
| SP5 | Remove `waste-bin/` from the project tree (or confirm it will not be in the submission zip). | Delete submission deliverables (`main.py`, tests, spec, log, writeup, seed). |
| SP6 | **Done 2026-08-14.** Living spec stamped for base + AC; checklist ticks only what is true; understand-the-code left open. | Re-open Tasks 1–9. Claim SP5 deleted. Claim extra credit. |
| SP7 | **Done 2026-08-12.** Fail-reason / status remark names `expired` and `unusable` via `_format_unavailable_ingredient_reason`. Deduction unchanged. | Change public signatures. Bundle other SP tasks. |

### SP1 gap list (2026-08-12) — gaps only; boxes not ticked

Compared: Part I final checklist, CONSOLIDATED §19, `WRITTEN_RESPONSE.MD` before-submit bullets. Repo inspected for file presence; no fresh `main.py` / unittest run in this task (reserved for SP3/SP4).

#### Still open (required closers)

| # | Open gap | One-line evidence | Closer |
|---|----------|-------------------|--------|
| 2 | `main.py` run not recorded for submit | **Closed SP3:** exit 0; print order confirmed in `WRITTEN_RESPONSE.MD` | **Done** |
| 3 | Unit test run not recorded for submit | **Closed SP4:** 49 OK recorded; **SP6 note:** suite now **79 OK** (2026-08-14) | **Done** |
| 4 | Spec / checklists not stamped submission-ready | **Closed SP6:** stamped 2026-08-14 (understand-the-code still open) | **Done** |
| 5 | Student self-check: “understand the code” | Part I / §19 item; only you can confirm — **left unticked at SP6** | **Still open (you)** |

#### Optional / parked (not required to submit)

| # | Item | Evidence | Closer |
|---|------|----------|--------|
| 7 | Fail-reason wording when detail status is `expired` | **Closed SP7:** remarks use “Expired ingredients” / “Unusable ingredients”; shortage label kept for missing/insufficient | **Done** |

#### Already true (do **not** tick in SP1; tick only when SP3–SP6 / you confirm)

| Checklist item | Evidence (read-only) |
|----------------|----------------------|
| Deliverables present | `main.py`, `seed_data.py`, `test_main.py`, `PROJECT_SPEC.MD`, `AI_USAGE_LOG.MD`, `WRITTEN_RESPONSE.MD` on disk |
| Program uses `seed_data.py` | File present; import documented in writeup/spec (instructor file was `seed_data-1.py`) |
| Cumulative inventory / restock rules / failed-order reasons / success+failure tests | Closed under Tasks 1–10; suite and behavior accepted in three-source audit |
| `AI_USAGE_LOG.md` documents process | File present; major interactions logged through SP Template 2 / SP1 |
| Reflection answers all six required questions | 589 words; all six answered |
| Extra credit not taken | Spec approvals: Extra credit (K) not approved |
| No credentials / API keys in tree | No credential files among submission deliverables (`.DS_Store` / `__pycache__` are local junk — exclude from zip; not SP-scoped) |

#### SP1 validation hooks

1. **Assumptions to verify:** Prior audit’s “47 tests OK” / `main.py` exit 0 are **historical** evidence only; SP3/SP4 must re-run and record. “Understand the code” is yours alone.
2. **Uncertain:** Whether you prefer deleting `waste-bin/` (SP5) vs excluding it from the zip only.
3. **Incomplete / follow-up (post-SP6):** “understand the code” still required for a full personal submit. SP5 ignored (exclude `waste-bin/` from zip). SP7 done.

### Submit polish plan (from three-source audit)

**Goal:** Make the submission match Part I / CONSOLIDATED deliverables without changing closed simulation behavior unless a named optional wording fix is approved.

**Template 2 breakdown (2026-08-12) — approved**

Recommended order: **SP1 → SP3 → SP4 → SP5 → SP6**. Park **SP7** unless you explicitly approve it later.

| ID | Goal | Must | Must not | Files | Done when |
|----|------|------|----------|-------|-----------|
| **SP1** | Audit the submission checklist and list only what is still open. | Compare Part I final checklist, CONSOLIDATED §19, and `WRITTEN_RESPONSE.MD` before-submit bullets to current repo state; write a short gap list into the spec (or writeup notes). | Mark items done. Edit reflection. Delete `waste-bin/`. Change simulation code. | `PROJECT_SPEC.MD` (and optionally checklist notes in `WRITTEN_RESPONSE.MD`) | Gap list exists; no code behavior changed. **Done.** |
| **SP3** | Prove `main.py` runs with the expected print order. | Run `python main.py`; confirm seed tables → process → updated inventory/restock/status → manager summary; record that confirmation in writeup/setup notes. | Change fulfillment/restock/summary logic to “fix” output. | Terminal evidence + `WRITTEN_RESPONSE.MD` (Project Setup / checklist) | Run succeeds; print order noted as confirmed. |
| **SP4** | Prove the unit suite passes. | Run `python -m unittest -v`; record result (e.g. 47 tests OK, or current count) in writeup/checklist notes. | Alter tests just to pass. Ignore failures. Change production logic unless Template 4 is opened for a real failure. | Terminal evidence + `WRITTEN_RESPONSE.MD` | Suite green; result recorded. **Done 2026-08-12 (49 OK).** |
| **SP5** | Keep local process scaffolding out of the submission. | Delete `waste-bin/` from the tree **or** document a hard rule that the submission zip excludes it; prefer delete if you no longer need it locally. | Delete `main.py`, `test_main.py`, `seed_data.py`, `PROJECT_SPEC.MD`, `AI_USAGE_LOG.MD`, or `WRITTEN_RESPONSE.MD`. | `waste-bin/` (removal) | `waste-bin/` gone from the project root (or explicit non-submit note you will follow). |
| **SP6** | Mark the living spec submission-ready. | Update re-anchor / where-we-are / punch list; tick checklist items that are actually true after SP1–SP5; note SP7 still parked unless approved. | Claim base gaps closed that are not. Start extra credit. Rewrite history of closed tasks. | `PROJECT_SPEC.MD` | Spec says submit polish closed; checklist matches reality. |
| **SP7** (optional) | Clarify fail-reason text when detail status is `expired`. | Named Template 3 only after your explicit approve; keep all-or-nothing; add/adjust a focused test; re-run full suite. | Bundle with writeup tasks. Change public signatures. Treat as required for submit. | `main.py`, `test_main.py` | Reason text reflects expiry without changing deduction behavior; tests green. |

**Next process step:** zip for submit. SP6 **stamped**. Do not queue SP5. Extra credit not approved.

### Assumption Closeout plan (Template 2 — 2026-08-12)

**Goal:** Leave no silent “Assumption to verify” / “Uncertain” / “Incomplete / follow-up” in `main.py`, and close §9 “Assumptions to keep verifying,” by verify+resolve, add a focused test, or write a deferral decision in this file.

**Inventory count:** ~40 comment lines in `main.py` + 5 §9 bullets → **15 one-prompt clusters (AC1–AC15)**. **AC1 done.**

**Out of this breakdown:** Stamp SP6. Extra credit. Part II extras. Waste-bin/SP5. Wholesale Task 1–9 rewrites. Changing public signatures unless a later named task you approve requires it.

**Per-task rule:** Each Template 3 does **one** AC id only. End by: updating/removing the related comments, and/or adding a test, and/or writing a §9 deferral line. Re-run `python -m unittest -v` when code/tests change.

| ID | Concern | Source comments / §9 | Path | Must | Must not | Done when |
|----|---------|----------------------|------|------|----------|-----------|
| **AC1** | Seed import + loaders | Import: seed_data.py name; Uncertain none; Incomplete import scope. `load_recipes` module lists. `load_restock` seed vs live rebuild. | (a) | Confirm against Decisions/DC1 + load tests; resolve or rewrite comments to “verified” notes (or remove). | Change loader APIs. Add DB. | Comments closed; no silent import assumptions. **Done 2026-08-12.** |
| **AC2** | Grams everywhere | `load_inventory` grams/buns; §9 “All quantities are grams, including buns.” | (a)/(b) | Confirm seed + types tests; resolve comment; add a tiny assertion if missing. | Invent unit counts. | Comment closed; grams locked. **Done 2026-08-12.** |
| **AC3** | Exact recipe name match | `load_orders` exact names; `find_recipe_by_name` exact + no case/alias; §9 exact match. | (a)/(b) | Confirm Decisions + existing hit/miss tests; add case-mismatch test if absent; resolve comments. | Add aliases/case-folding. | Comments closed; exact-match locked. **Done 2026-08-12.** |
| **AC4** | Expired vs expiring-soon | Constants note (days&lt;0 vs 5-day window); availability expired meaning; summary expiry windows. | (a) | Confirm against existing expired / expiring-soon tests + Decisions; resolve comments. | Make expiring-soon block fulfillment. | Comments closed; split locked. **Done 2026-08-12.** |
| **AC5** | Availability defaults & bad inputs | `reference_date` default; None/empty/negative; Uncertain malformed→unusable; Incomplete restock/summary unchanged. | (a) | Confirm OP7 tests + default-date tests; resolve comments (malformed→unusable is intended). | Change public `check_inventory_availability` signature. | Comments closed. **Done 2026-08-12.** |
| **AC6** | Restock raise on bad date | `_days_until_expiry`: restock raises; availability/summary catch. | (a) or (c) | Either document as intentional RF3 asymmetry in §9 **or** add a focused test that restock raises on bad date; resolve comment. | Silently “fix” restock to swallow dates without approve. | Decision written; comment closed. **Done 2026-08-12.** |
| **AC7** | Lookup last-wins + snapshot shape | `_inventory_by_name` last row wins; Incomplete: `apply_final_inventory_snapshot` qty-only map. | (a) or (c) | Confirm intended; document in §9 if seed never duplicates; resolve comments. Do not merge map shapes unless you approve a follow-on. | Change public signatures. | Comments closed; decision written. **Done 2026-08-13.** |
| **AC8** | All-or-nothing / no partial deduct | `deduct_inventory` assumption; `process_orders` rejects full order; OP15 “does not change all-or-nothing”; §9 all-or-nothing. | (a) | Confirm fulfillment/cumulative tests; resolve comments. | Implement partial fulfillment. | Comments closed. **Done 2026-08-13.** |
| **AC9** | Status seed vs append | `load_status` Uncertain; `update_status_entry` Incomplete (append new ids); §9 “Status may append”. | (a) or (c) | Confirm append behavior with a test if needed; decide seed is initial table only; resolve comments. | Require every order pre-seeded unless approved. | Comments closed; §9 decision clear. **Done 2026-08-13.** |
| **AC10** | SP7 reason labels | `_format_unavailable_ingredient_reason` labels + wording-only + signature Incomplete. | (a) | Confirm SP7 tests; resolve/remove stale assumptions. | Change public signatures. | Comments closed. **Done 2026-08-13.** |
| **AC11** | Restock rules + replace table | qty 0 not also running low; max qty_needed; Incomplete OP15 covers missing; `refresh_restock_table` replaces history; §9 live restock replaced. | (a) | Confirm RS tests + OP15 tests; resolve comments. | Restock-every-N. Preserve seed history as base rule. | Comments closed. **Done 2026-08-13.** |
| **AC12** | OP15 duplicate + par | One row per name; missing→full par; expired-at-par still requests par. | (a)/(b) | Confirm existing OP15 tests; add focused assert if par-at-expiry path thin; resolve comments. | Silent duplicates. | Comments closed. **Done 2026-08-13.** |
| **AC13** | Working inventory deepcopy | `process_orders` deepcopy vs shared ref; Incomplete persistence. | (a)/(b) | Confirm cumulative tests prove live table unchanged mid-run; optional tiny aliasing test; resolve comment; defer persistence to §9. | Add a database. | Comment closed; persistence deferred explicitly. **Done 2026-08-13.** |
| **AC14** | Missing-recipe reason path | Incomplete: formal rejection reason for missing recipe. | (a) | Confirm `process_orders` already records “No matching recipe…”; resolve Incomplete (done) or note gap. | Crash on miss. Invent ingredients. | Comment closed. **Done 2026-08-13.** |
| **AC15** | Summary + main display | Summary: fulfilled True; expiry windows; live restock passed in; SM3 Incomplete. `main`: print order + console/dict. | (a) | Confirm SM tests + SP3 evidence; resolve comments. | Markdown report (extra credit). | Comments closed; §9 bullets updated. **Done 2026-08-14.** |

**§9 “Assumptions to keep verifying” map:** exact recipe → **AC3**; grams → **AC2**; status append → **AC9**; live restock replaced → **AC11**; all-or-nothing → **AC8**.

**Recommended order:** **AC1 → AC2 → AC3 → AC4 → AC5 → AC6 → AC7 → AC8 → AC9 → AC10 → AC11 → AC12 → AC13 → AC14 → AC15**. Then SP6 (if you still want stamp).

### Remaining Gaps Closeout plan (Template 2 — 2026-08-12) — status

SP7 / SP3 / SP4 / **SP6 done**. SP5 **ignored**. Assumption Closeout **AC1–AC15 done**.

Optional extra credit (one, only after base works):

| Option | What |
|--------|------|
| A Partial fulfillment | Deliver items that can be filled; mark only unavailable items not delivered |
| B Predictive stockout | Forecast which ingredients run out in the next batch from observed consumption |
| C Dynamic item disabling | Mark menu items unavailable when a required ingredient is out or unusable |
| D Improved reporting | Polished Markdown, CSV, or HTML report |

---

## 7. Testing plan

Python `unittest` in `test_main.py`. Tests must be runnable; results visible or documented. Cover **normal, edge, and failure** cases.

| Area | Must cover | Now |
|------|------------|-----|
| Data load | Five tables, types, record counts, key fields | Done |
| Recipe lookup | Hit, miss, quantity > 1 | Done |
| Availability | All ok; missing; insufficient; expired; bad inputs | Done |
| Fulfillment | Delivered + deduct; not delivered + reason; no deduct on failure | Done (quantity fail). Expiry-fail no-deduct probed, not a dedicated test. |
| Cumulative | Shared ingredient across two orders; later fail from earlier consumption; final inventory | Done |
| Restock | Zero; ≤ 1,000g; above threshold; expiring soon; **multiple reasons**; not flagged when healthy | Done for those cases. Default date is `2026-05-10`. |

**5-point review on every AI-generated function**

1. Does it do what I asked? Run it with 3 different inputs you can verify manually.
2. Are there hidden assumptions? Hard-coded values, assumed types, or logic paths not specified.
3. Is anything hard-coded that should be a variable? (restock thresholds, par levels, expiry windows)
4. Does it handle bad inputs? `None`, empty lists, negative quantities
5. Is any part security-sensitive or business-critical? (financial deductions, expiry logic)

**Debug loop:** read the error → understand line/type/variable → Template 4 with function + full error → root cause not just patch → fix → re-run **all** tests → repeat if needed.

---

## 8. Process requirements (also in scope)

### Files / deliverables

| File | Purpose |
|------|---------|
| `main.py` | Simulation logic |
| `seed_data.py` | Seed tables (instructor file was `seed_data-1.py`) |
| `test_main.py` | Unit tests |
| `PROJECT_SPEC.md` | This file |
| `AI_USAGE_LOG.md` | Major AI interactions |
| Written reflection | 400–600 words; questions in the punch list |

Submit: `main.py`, `test_main.py`, `PROJECT_SPEC.md`, `AI_USAGE_LOG.md`, written reflection; optional extra reports. Keep seed data in the project. No private credentials.

**AI_USAGE_LOG (each major interaction):** task, the prompt you gave (exact wording—no paraphrase labels), short summary of AI response, accepted/changed/rejected, issues found. Not every tiny prompt; enough to show critical use. Full entries live in [`AI_USAGE_LOG.MD`](AI_USAGE_LOG.MD).

**Template 4 examples (debugging — root cause, not just a patch):**

These use the Template 4 form from [`docs/prompt_templates.md`](docs/prompt_templates.md). Unexpected output counts as the “error” when there is no traceback.

```text
Here is the code and the error it produces: calculate_restock_needs uses if/elif across out-of-stock / running-low / expiring-soon, so an ingredient at 500g that is also within 5 days of SIMULATION_DATE only keeps one reason. / Unexpected output vs Part I: restock must preserve all matching reasons (do not overwrite with elif). Explain what is wrong and provide a corrected version with comments.
```

```text
Here is the code and the error it produces: restock/availability default reference_date to date.today(). / Unexpected output: seed expiry_date values run 2026-01 through 2026-11; on 2026-08-11 several seed items already look expired or expiring soon against the calendar, so the operational day does not match the seed. Explain what is wrong and provide a corrected version with comments.
```

```text
Here is the code and the error it produces: process_orders status remark / fail-reason. / Unexpected output: when an ingredient detail status is expired (or unusable), the remark still says only “Missing or insufficient ingredients”. Deduction is already correct (no deduct). Explain what is wrong and provide a corrected version with comments.
```

```text
Here is the code and the error it produces: _classify_inventory_stock_flags sets expired when days_until_expiry < 0 but does not append a restock reason from that flag; calculate_restock_needs therefore returns [] for Chocolate at 10,000g with expiry_date 2026-01-10 (simulation date 2026-05-10). / Unexpected output: Part I R6 requires flagging expired or expiring soon; expired stock only reached the table if an order failed on it (seed order 3 masks this). test_expired_flag_does_not_add_restock_reason asserted the defect. Explain what is wrong and provide a corrected version with comments.
```

### Workflow (each major task)

1. Plan or breakdown (Templates 1–2) — done for base components
2. Implement only one small task (Template 3)
3. Validation hooks
4. Review (5-point checklist)
5. Write/generate unit tests immediately
6. Run tests
7. Debug failures before moving on; re-run all tests
8. Update this spec

### AI use — allowed / not allowed

**May:** plan, break down tasks, draft code, explain errors, suggest tests, suggest refactoring.

**May not:** submit code you do not understand; submit explanations you cannot explain; ignore failed tests; hide known defects; claim AI work as fully your own without documenting process.

### Written response headings

Project Setup · Data Loading · Recipe Lookup · Inventory Availability · Order Fulfillment · Cumulative Processing · Restock and Expiry Logic · Business Summary · Refactoring Notes · AI Usage Summary · Reflection

### Rubric (100)

| Area | Pts | Full credit |
|------|-----|-------------|
| Setup + data loading | 10 | Structure; import seed; access all five structures |
| Recipe lookup + calculation | 10 | Lookup, scaling, graceful miss |
| Availability | 10 | Required vs available, missing/insufficient, expired/unusable |
| Fulfillment + status | 15 | Status; deduct on deliver; no deduct on fail; reasons |
| Cumulative | 10 | Later orders use remaining stock |
| Restock + expiry | 10 | Low, out, expiring soon, multiple reasons |
| Unit testing | 15 | Normal/edge/failure; runnable; results visible/documented |
| AI process | 10 | Useful spec; AI log; iteration; reviewed not blindly accepted |
| Quality + refactor | 5 | Readable; constants; comments; less duplication |
| Reflection | 5 | Benefits, risks, limits of AI-assisted coding |

### Submission checklist

**SP6 stamp (2026-08-14):** tick only what is true. Unticked items are intentional.

- [x] `main.py` runs — **SP3** (2026-08-12)
- [x] `test_main.py` runs — **SP4** (49 OK recorded); current suite **79 OK** at SP6
- [x] Uses `seed_data.py`
- [x] Final inventory is cumulative
- [x] Restock handles low stock, expiry, and multiple reasons
- [x] Failed orders include reasons
- [x] Tests cover success and failure
- [x] This spec is complete and updated — **for base + AC + SP6 stamp** (see stamp verdict)
- [x] `AI_USAGE_LOG.md` documents the process
- [x] Reflection answers all required questions — 589 words
- [ ] We understand the code being submitted — **only you can tick this**
- [x] No credentials / API keys

**Not claimed:** SP5 `waste-bin/` deleted (exclude from zip). Extra credit.

---

## 9. Open questions, assumptions, known issues

### Error-handling map (EH1 complete — Task 10 / quiet failures)

**Policy:** Most bad inputs become **status / reason results** (quiet). One deliberate exception: `calculate_restock_needs` **raises** on malformed expiry (AC6 / EH3). Printers assume seed-shaped rows. Hardening beyond this map is **EH2** (if approved). EH3 (comments + this §9 asymmetry blurb) is **complete**.

**Availability return shape** (`check_inventory_availability`):  
`{"all_available": bool, "details": [{"ingredient", "required_qty_grams", "available_qty_grams", "is_available", "is_expired", "status"}, ...]}`.

#### At a glance (one inventory)

| Area | Functions | Quiet / result path | Raises | Primary tests |
|------|-----------|---------------------|--------|---------------|
| A — Availability / OP7 | `check_inventory_availability` | None/empty coerce; `status` = missing / insufficient / expired / unusable / invalid; expiring-soon stays `ok` | No (malformed expiry → `unusable`) | `test_none_*`, `test_missing_ingredient`, `test_insufficient_quantity`, `test_expired_*`, `test_invalid_expiry_date_is_unusable`, `test_empty_requirement_list_is_available` |
| B — Recipes / orders | `find_recipe_by_name`, `process_orders` | Miss → `None` / Not Delivered + reason; empty `order_data` → `[]`; empty `items` → vacuous Delivered | No on recipe miss | `test_find_recipe_by_name_*`, `test_process_orders_records_no_matching_recipe_reason` |
| C — Restock | `calculate_restock_needs`, `refresh_restock_table` | Empty inventory → `[]`; refresh clears + rebuilds | **Yes** — malformed expiry; also `KeyError` on missing seed keys | `test_restock_raises_on_malformed_expiry_date`, `test_refresh_restock_table_replaces_prior_rows` |
| D — Manager summary | `build_manager_summary` | None/empty orders → zeros; bad expiry **caught** → name on expired list; skip non-dicts | No on bad dates | `test_empty_or_none_processed_orders_report_zero`, summary suite |
| E — Printers | `print_*` | Empty list → header only | `KeyError` if required keys missing (`print_restock` soft on optional fields) | `test_main_prints_all_five_seed_tables_before_processing` (happy path) |

#### Detail A — `check_inventory_availability` / OP7

| Input / situation | `all_available` | Detail `status` | Notes | Tests |
|-------------------|-----------------|-----------------|-------|-------|
| `inventory_data is None` | `False` if requirements non-empty | `missing` (per required name) | Coerced to `[]`; no crash | `test_none_inventory_does_not_crash` |
| `inventory_data == []` (empty) | `False` if requirements non-empty | `missing` | Same coerce path as None | `test_missing_ingredient` (name absent) |
| `requirements is None` | `True` | `details == []` | Coerced to `[]`; vacuous success | `test_none_requirements_does_not_crash` |
| `requirements == []` | `True` | `details == []` | Vacuous success | `test_empty_requirement_list_is_available` |
| Negative `required_qty_grams` (or non-numeric) | `False` | `invalid` | `is_available=False`, `is_expired=False` | `test_negative_quantity_is_not_valid_demand` |
| Required name not in inventory | `False` | `missing` | `available_qty_grams=0` | `test_missing_ingredient` |
| Present but `available_qty < required` (unexpired) | `False` | `insufficient` | Expiry checked before qty shortfall when date present | `test_insufficient_quantity` |
| Present, `days_until_expiry < 0` | `False` | `expired` | `is_expired=True`; blocks even if qty high | `test_expired_ingredient_blocks_fulfillment` |
| Present, malformed / unparseable `expiry_date` | `False` | `unusable` | Catch `TypeError`/`ValueError` from `_days_until_expiry`; `is_expired=True` | `test_invalid_expiry_date_is_unusable` |
| Expiring soon (`0..EXPIRING_SOON_DAYS`) | `True` (if qty ok) | `ok` | Does **not** fail availability (restock/summary only) | `test_expiring_soon_does_not_block_fulfillment` |
| Omit `reference_date` | (as above) | (as above) | Defaults to `SIMULATION_DATE` via `_resolve_reference_date` | `test_availability_default_reference_date_is_simulation_date` |
| Non-dict requirement entry | `False` | `invalid` | Defensive; no dedicated unittest | (code) |

#### Detail B — `find_recipe_by_name` / `process_orders`

| Input / situation | `fulfilled` | Reason / return | Inventory | Notes | Tests |
|-------------------|-------------|-----------------|-----------|-------|-------|
| Recipe name miss (`find_recipe_by_name`) | n/a | Returns `None` | n/a | Exact `==` only; no aliases/case fold | `test_find_recipe_by_name_handles_missing_recipe_gracefully`; `test_find_recipe_by_name_requires_exact_case_match` |
| Order item with no matching recipe | `False` | `No matching recipe for item(s): …` | Unchanged (no deduct) | `recipe_found=False`, `requirements=[]`, no invented ingredients; status updated Not Delivered | `test_process_orders_records_no_matching_recipe_reason` |
| Missing recipe **and** other unavailable ingredients | `False` | Recipe reason `\|` SP7 inventory reason | Unchanged | Both parts joined when both apply | (path in code; mixed inventory fails covered elsewhere) |
| `order_data == []` (empty order list) | n/a | Returns `[]` processed | Live qty unchanged after snapshot of untouched working copy | Loop body never runs; restock still refreshed from final inventory | `test_process_orders_empty_order_data_returns_empty_list` |
| Order with `items == []` | `True` | `Delivered` | Unchanged (empty deduct) | Vacuous requirements → availability succeeds; current base behavior | No dedicated unittest — behavior from code |

**Detail B note:** Does not invent ingredients or substitute recipes (AC14). Empty-items-as-Delivered is intentional vacuous success unless a later approved task changes it.

#### Detail C — restock, manager summary, `print_*`

| Area | Input / situation | Behavior | Tests / evidence |
|------|-------------------|----------|------------------|
| `calculate_restock_needs` | Malformed `expiry_date` | **Raises** (`ValueError`/`TypeError` from bare `_days_until_expiry`) — intentional AC6 asymmetry | `test_restock_raises_on_malformed_expiry_date` |
| `calculate_restock_needs` | `inventory_data == []` | Returns `[]` | `test_calculate_restock_needs_empty_inventory_returns_empty_list` |
| `calculate_restock_needs` | Missing row keys (`qty_grams` / `expiry_date` / `ingredient`) | **Raises** `KeyError` (assumes seed-shaped rows) | No dedicated test — seed/process paths supply keys |
| `refresh_restock_table` | Any call | `clear()` then `extend(calculate_restock_needs(...))` — prior rows discarded | `test_refresh_restock_table_replaces_prior_rows` |
| `refresh_restock_table` | Empty inventory | Live table becomes `[]` (then OP15 may append) | `test_refresh_restock_table_empty_inventory_clears_recommendations` |
| `build_manager_summary` | Malformed inventory expiry | **Catches**; name listed in `expired` (no raise) | AC6 asymmetry; summary path mirrors availability catch |
| `build_manager_summary` | `processed_orders` None/empty | Counts 0; safe text | `test_empty_or_none_processed_orders_report_zero` |
| `build_manager_summary` | `inventory_data` / `restock_data` None | Coerced to `[]`; inventory/restock sections omitted when arg was None (`show_*` flags) | Summary tests pass real lists; None coerce in code |
| `build_manager_summary` | Non-dict order/inventory/restock rows | Skipped (`continue` / filter) | Defensive in code; no dedicated unittest |
| `build_manager_summary` | Missing qty / blank ingredient | `.get` defaults (`qty`→0, name→`""`) | Defensive in code |
| `print_recipes` / `print_inventory` / `print_orders` / `print_status` | Empty list | Prints section header only; no crash | Seed print order covered by `test_main_prints_all_five_seed_tables_before_processing` (non-empty seed) |
| `print_*` (most) | Missing required keys | **Raises** `KeyError` — assume well-shaped seed/live rows | No defensive `.get` on core fields (except `print_restock` optional `current_qty_grams` / `expiry_date`) |
| `print_restock` | Row without `current_qty_grams` or `expiry_date` | Skips those lines; still needs `item`, `qty_needed_grams`, `reason` | Code uses `in` / `.get` for optional fields only |

**Detail C note:** Quiet paths elsewhere + restock **raise** on bad dates is deliberate (see §9 Intentional asymmetries / EH3 — complete). Printers are thin display helpers for trusted tables.

**Known gaps vs requirements (do not treat as done)**

1. ~~Expiry not in availability.~~ **Closed OP6.**
2. ~~`calculate_restock_needs` uses `if/elif`, so an ingredient cannot carry both reasons.~~ **Closed RS3.**
3. ~~Restock rows omit current quantity and expiry information.~~ **Closed RS3.**
4. ~~Thresholds `1000` / `10000` / `5` are literals.~~ **Closed RS1:** `RUNNING_LOW_THRESHOLD_GRAMS`, `PAR_LEVEL_GRAMS`, `EXPIRING_SOON_DAYS`.
5. ~~No dedicated manager-facing business summary.~~ **Closed SM1–SM4:** content, `main()` output, and required tests.
6. ~~Module import vs `seed_data-1.py`.~~ **Closed DC1.**
7. ~~Default restock `reference_date` is `date.today()`.~~ **Closed RS4:** `SIMULATION_DATE = date(2026, 5, 10)`. Tests still pass an explicit `reference_date`.
8. ~~Failed-order restock is still rebuild-only.~~ **Closed OP15:** rebuild from final-inventory rules, then add missing/unavailable failed-order items without silent duplicates.
9. ~~Availability bad inputs.~~ **Closed OP7.**
10. ~~`AI_USAGE_LOG.md` still fill in after each major coding interaction.~~ Continue logging; file is active through SP6.
11. ~~Documented refactors.~~ **Closed RF2 + RF3** (+ DR1–DR8). Reflection complete.
12. ~~Fail-reason text still says “Missing or insufficient” when detail `status` is `expired`.~~ **Closed SP7.**
13. ~~Submit polish open (audit).~~ **SP1/SP3/SP4/SP6/SP7 done;** SP5 ignored.
14. ~~Three-source audit needed.~~ **Closed 2026-08-12.** Base complete vs Part I / CONSOLIDATED; Part II extras not required.
15. ~~Assumption Closeout.~~ **Closed AC1–AC15 (2026-08-14).** Two low-risk DR “Assumption to verify” comments remain in `main.py` (None `days_until_expiry`; restock `reasons` list shape) — documented, not blocking base submit.

**Assumptions to keep verifying**

_AC map closed. Remaining student action: “understand the code.”_

- ~~Exact string match for recipe names is enough (no aliases / case folding).~~ **Closed AC3:** `==` only; case/whitespace mismatches return None; locked by `test_find_recipe_by_name_requires_exact_case_match`.
- ~~All quantities are grams, including buns.~~ **Closed AC2:** seed inventory + recipes use `qty_grams` only (Bun included); locked by `test_all_seed_quantities_are_grams_including_buns`.
- ~~Status may append a row if `order_id` is new.~~ **Closed AC9:** `load_status` is seed baseline only; `update_status_entry` updates in place or appends for new ids. Orders need not be pre-seeded. Locked by `test_update_status_entry_updates_existing_row`, `test_update_status_entry_appends_when_order_id_is_new`, `test_seed_status_is_initial_table_matching_seed_order_ids`.
- ~~Live restock table is replaced each run (seed restock rows are not preserved as history).~~ **Closed AC11:** `refresh_restock_table` clears + rebuilds from final inventory; OP15 covers missing-from-inventory after. Qty 0 is Out of stock only; multi-reason uses max qty_needed. Restock-every-N not base. Locked by RS/OP15 tests + `test_refresh_restock_table_replaces_prior_rows`.
- ~~Base assignment stays all-or-nothing.~~ **Closed AC8:** failed orders never call `deduct_inventory`; multi-item orders reject fully (no partial item delivery). Locked by without-deduct tests + `test_multi_item_order_fails_all_or_nothing_without_partial_deduct`. Partial fulfillment remains extra credit only.

**Assumption closeout progress**

- **AC1 (2026-08-12):** Verified — `seed_data.py` direct import (DC1); `load_recipes` returns module-level seed lists; `load_restock` is seed-only for baseline print, live table rebuilt after orders. Loader APIs unchanged. Tests green.
- **AC2 (2026-08-12):** Verified — all quantities are grams, including Bun. `load_inventory` comment closed. Focused unittest added. Suite **50 OK**.
- **AC3 (2026-08-12):** Verified — exact recipe name match only. Comments on `load_orders` / `find_recipe_by_name` closed. Case-mismatch unittest added. Suite **51 OK**.
- **AC4 (2026-08-12):** Verified — fulfillment uses `days < 0` for expired; `EXPIRING_SOON_DAYS` is restock/summary only and does not block. Comments on constants / availability / summary closed. Existing expiry tests confirm. Suite **51 OK**.
- **AC5 (2026-08-12):** Verified — omit `reference_date` → `SIMULATION_DATE`; None/empty/negative OP7 behavior; malformed expiry → unusable (intended). Added `test_availability_default_reference_date_is_simulation_date`. Signature unchanged. Suite **52 OK**.
- **AC6 (2026-08-12):** Intentional RF3 asymmetry documented and locked — restock/`calculate_restock_needs` raises on malformed expiry; availability/summary catch as unusable. Comment on `_days_until_expiry` closed. Added `test_restock_raises_on_malformed_expiry_date`. Did **not** make restock swallow bad dates. Suite **53 OK**.
- **AC7 (2026-08-13):** Verified — `_inventory_by_name` last-row-wins is intentional (seed has unique names; defensive for duplicates). `apply_final_inventory_snapshot` keeps a **qty-only** map on purpose so live expiry/row identity are preserved. Shapes stay separate (do not merge without approve). Comments closed. Tests: `test_inventory_by_name_last_row_wins`, `test_seed_inventory_ingredient_names_are_unique`, `test_final_snapshot_updates_qty_only_not_expiry`. Suite **65 OK**.
- **AC8 (2026-08-13):** Verified — all-or-nothing fulfillment; no partial deduct. Comments on `deduct_inventory`, `process_orders` fail path, and OP15 closed. Confirmed cumulative/fulfillment tests; added `test_multi_item_order_fails_all_or_nothing_without_partial_deduct`. Did **not** implement partial fulfillment. Suite **66 OK**.
- **AC9 (2026-08-13):** Verified — seed status is initial table only; live updates via `update_status_entry` (update or append). Do not require every order pre-seeded. Comments closed. Suite **69 OK**.
- **AC10 (2026-08-13):** Verified — SP7 reason labels on `_format_unavailable_ingredient_reason` (Expired / Unusable / Missing or insufficient; invalid→shortage bucket). Wording-only; signatures unchanged. Confirmed SP7 tests; extended invalid-status assert. Suite **69 OK**.
- **AC11 (2026-08-13):** Verified — restock rules (0g not also running-low; max qty_needed; OP15 covers missing-from-inventory) and replace-table behavior. Comments closed. Added `test_refresh_restock_table_replaces_prior_rows`. Did **not** add restock-every-N. Suite **70 OK**.
- **AC12 (2026-08-13):** Verified — OP15 one row per name; missing→full par; expired-at-par→full par. Comments closed. Extended expired restock assert; added `TestAddFailedOrderItemsToRestock`. Suite **73 OK**.
- **AC13 (2026-08-13):** Verified — `process_orders` uses `deepcopy` working inventory; live table unchanged until `apply_final_inventory_snapshot`. Confirmed cumulative tests; added `test_live_inventory_unchanged_until_final_snapshot`. Persistence deferred to §9 (in-memory only; no database). Suite **74 OK**.
- **AC14 (2026-08-13):** Verified — missing recipe already has formal reason `No matching recipe for item(s): …`; no crash; no invented ingredients; status updated. Incomplete resolved. Added `test_process_orders_records_no_matching_recipe_reason`. Suite **79 OK**.
- **AC15 (2026-08-14):** Verified — summary: `fulfilled` True → delivered; expiry windows (AC4); live restock passed in (OP15 rows included); SM3 console print + returned dict (no Markdown). `main()` print order locked by SM/main tests + SP3 evidence in `WRITTEN_RESPONSE.MD`. Comments closed. Suite **79 OK**. **Assumption Closeout AC1–AC15 complete.**
- **SP6 (2026-08-14):** Living spec stamped for **base assignment + AC closeout**. Checklist ticks only verified items. **Not** claimed: SP5 deleted, extra credit, “understand the code.” Suite **79 OK** at stamp.

**Intentional asymmetries (do not “fix” without approve)**

- **RF3 / AC6 / EH3 — restock raise vs availability/summary catch (Task 10 “weak error handling”):**
  - `_days_until_expiry` itself **raises** on a bad/malformed date (`ValueError`/`TypeError` from parse).
  - **Catch side (quiet):** `check_inventory_availability` wraps the call → detail `status="unusable"` (no exception to the order path). `build_manager_summary` wraps the call → ingredient name goes on the expired-concern list (no raise).
  - **Raise side (strict):** `calculate_restock_needs` calls `_days_until_expiry` **bare** — malformed expiry **propagates**. This is **not** forgotten try/except or weak handling; it is locked behavior so a corrupt final-inventory date fails loudly at restock rebuild.
  - **Do not** “align” restock to swallow bad dates to match availability/summary unless explicitly approved (that would change AC6).
  - **Locks:** `test_restock_raises_on_malformed_expiry_date`; `test_invalid_expiry_date_is_unusable`. Code comments: EH3a on those call sites. Full quiet-path inventory: Error-handling map above.
- **AC7:** Full-row lookup (`_inventory_by_name`) vs qty-only snapshot map (`apply_final_inventory_snapshot`) are different shapes on purpose. Do not merge without approve.
- **AC8:** Base stays all-or-nothing. Partial fulfillment is extra credit only — do not implement without approve.

**Deferred (explicit)**

- **AC13:** External inventory persistence / transactions / database — out of base scope. Simulation is in-memory only (`deepcopy` + final snapshot).

**Open questions**

- Restock-every-N-orders: skip unless we explicitly take it as an enhancement.
- ~~SM3 output form.~~ **Closed SM3:** console print of manager text; `main()` returns the dict. No Markdown file.
- ~~Which two refactors.~~ **Closed:** A `_inventory_by_name` (RF2); B `_days_until_expiry` (RF3).

---

## 10. Design principles

- **Centralized inventory** — one shared source for all brands
- **Recipe-driven deduction** — recipes × quantities
- **Availability validation** — enough quantity and unexpired
- **Separated workflows** — consume during orders; replenish in a restock phase
- **Baseline restocking** — to par (10,000g)
- **Multi-reason tracking** — low stock and expiry can both apply; do not overwrite
- **Periodic replenishment** — optional/design note; **base requirement is restock on final inventory**

---

## 11. Post-audit changes (2026-08-16)

Three slices after the standards audit. No public signature changed in any of them.

| ID | Change | Why | Evidence |
|----|--------|-----|----------|
| **RX1** | `_classify_inventory_stock_flags` adds reason `"Expired"` at full par | Part I R6 lists "expired **or** expiring soon" as restock conditions. Part II Step 5 omits expired and the code had followed Part II, so expired stock only reached the table when an order happened to fail on it. | `test_expired_adds_restock_reason_at_full_par`, `test_expired_and_out_of_stock_keep_both_reasons`. Replaced `test_expired_flag_does_not_add_restock_reason`, which had asserted the defect. |
| **RF5** | `process_orders` 127 → 32 lines via `_resolve_order_lines`, `_decide_order_outcome`, `_process_single_order` | Task 10 "functions that do too much". Decision logic is now pure, so all-or-nothing (AC8) cannot be broken by a change to the decision branch. | Suite 79 OK; run output unchanged. |
| **RF6** | `build_manager_summary` 162 → 54 lines via `_split_orders_by_delivery`, `_summarize_inventory_health`, `_render_manager_summary_text` | Task 10, plus Part II §1 "separate logic changes from output-format changes". | Suite 79 OK; summary output byte-for-byte unchanged. |

**Preserved deliberately during RF5/RF6:**

- Missing-recipe precedence: a missing recipe rejects the order even when every ingredient is in stock; inventory wording is appended only when ingredients also failed.
- `show_inventory` / `show_restock` stay explicit parameters. An empty inventory list prints an empty block; `None` omits the block. Inferring from emptiness would change output.
- The AC6 asymmetry: `_summarize_inventory_health` still catches malformed dates; `calculate_restock_needs` still raises.

**Largest remaining function:** `check_inventory_availability` at 101 lines, roughly a third of which is the OP7/AC5/AC6 comment block. Not split — its branches are one linear decision per requirement and splitting would add indirection without reducing real complexity.
