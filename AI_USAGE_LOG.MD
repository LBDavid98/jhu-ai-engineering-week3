# AI Usage Log

Major interactions only: task, prompt used, short summary of the AI response, what I accepted/changed/rejected, and issues found. Enough to show critical use of AI on this assignment—not every chat message.

---

## 2026-08-11 — High-level plan (Template 1) — REJECTED

- **Task:** Plan the project before more code.
- **Prompt:** High-level plan for a cloud kitchen inventory simulation using `seed_data.py`, with constraints on all-or-nothing fulfillment, cumulative inventory, restock rules, multiple restock reasons, and the provided seed schema.
- **AI response:** Five coarse components only (data, orders, restock, summary, quality). No slice-level tasks, tests, or gap vs existing code.
- **Decision:** **Rejected.** Too coarse.
- **Issues found:** Not useful as a build plan. Asked for a much more granular plan saved to a file.

---

## 2026-08-11 — Granular plan (Template 1 revision)

- **Task:** Replace the rejected plan with a detailed implementation plan.
- **Prompt:** Save the plan to an `.MD` and make it a lot more granular.
- **AI response:** Slice-level plan (components, must/must-not, tests, known gaps such as expiry in availability, multi-reason restock, named constants, seed filename, manager summary, simulation date).
- **Decision:** **Approved** as the planning deliverable (later merged into `PROJECT_SPEC.MD`).
- **Issues found:** Open product decisions still needed (simulation date; whether expiring-soon blocks fulfillment; failed-order restock vs rebuild-only).

---

## 2026-08-11 — Task breakdowns (Template 2)

- **Task:** Break Data Connectivity, Order Processing, Restock, Business Summary, Refactor, and Writeup into one-prompt tasks.
- **Prompt:** Template 2 per component (import/display five tables; order lookup through cumulative; restock fields and multi-reason; manager summary; refactor; writeup).
- **AI response:** Task lists for each component. Recommended inspecting existing loaders/fulfillment instead of rewriting working code; restock multi-reason as one focused change; extra credit after base.
- **Decision:** **Approved** for the base assignment (through writeup). Extra credit not approved.
- **Issues found:** Rewriting already-working lookup/fulfillment would have wasted time. Expiry in availability and multi-reason restock were the real code gaps.

---

## 2026-08-11 — Inspect loaders; fix seed import

- **Task:** Confirm load/print of five tables; fix import of `seed_data`.
- **Prompt:** Inspect load/print against the spec (gaps only). Then make `main.py` import seed data as `seed_data` (instructor file had been `seed_data-1.py`).
- **AI response:** Loaders and tests largely OK. Gaps: filename mismatch; `main()` did not print seed Restock. After I renamed the file to `seed_data.py`, AI documented the import and added an import test.
- **Decision:** **Approved**. I renamed the file; AI did not invent a fallback importer.
- **Issues found:** Import failed until the file was renamed. Seed Restock still not shown until a later `main()` change.

---

## 2026-08-11 — `main()` prints all five seed tables

- **Task:** Show access to Recipes, Inventory, Orders, Restock, and Status.
- **Prompt:** Update `main()` to load and print all five tables via the load/print functions. One task only.
- **AI response:** Print seed tables first, then process orders, then print updated inventory / restock / status. Added a test for that order.
- **Decision:** **Approved** (seed tables first).
- **Issues found:** None. Tests OK.

---

## 2026-08-11 — Expiry in availability; bad inputs

- **Task:** Availability must consider expiry; handle None / empty / negative demand safely.
- **Prompt:** Update only `check_inventory_availability` for expired/unusable ingredients with an explicit `reference_date`. Then harden bad inputs. Do not change restock or summary in the first prompt.
- **AI response:** Past expiry (`days < 0`) and bad dates block; expiring soon does not. Default simulation date `2026-05-10`. None/empty/negatives handled without crashing.
- **Decision:** **Approved.** Past expiry blocks; expiring soon is restock-only. Simulation date `2026-05-10` (not `date.today()`).
- **Issues found:** Seed expiries vs “today” would have broken the sim if we had used the system date. Fail-reason text can still say “Missing or insufficient” when the detail status is `expired` (wording only; no wrong deduction).

---

## 2026-08-11 — Re-check fulfillment after expiry

- **Task:** Confirm failed orders (including expiry) do not deduct inventory; re-run tests.
- **Prompt:** Trace the failed-order path after expiry was added; list any test failures.
- **AI response:** No test failures. Inventory unchanged on expiry fail. No production patch required for deduction.
- **Decision:** **Approved** for deduction behavior.
- **Issues found:** Fail-reason wording for expired ingredients still generic. Not treated as a deduction bug.

---

## 2026-08-11 — Template 4: restock `if/elif` drops a second reason

- **Task:** Debug restock so one ingredient can keep more than one reason (RS3).
- **Prompt:** Here is the code and the error it produces: calculate_restock_needs uses if/elif across out-of-stock / running-low / expiring-soon, so an ingredient at 500g that is also within 5 days of SIMULATION_DATE only keeps one reason. / Unexpected output vs Part I: restock must preserve all matching reasons (do not overwrite with elif). Explain what is wrong and provide a corrected version with comments.
- **AI response:** Root cause: `elif` makes the branches mutually exclusive, so the first matching rule wins and later reasons never attach. Independent `if` checks plus a `reasons` list (joined into `reason`) keep both labels; `qty_needed_grams` uses max-of-rules. Locked by a multi-reason unittest (500g and expiring soon → both reasons).
- **Decision:** **Approved.**
- **Issues found:** Qty 0 should stay “Out of stock” only (not also running-low). That exclusivity is a quantity tier, not a reason overwrite.

---

## 2026-08-11 — Template 4: `date.today()` vs seed expiries

- **Task:** Debug default restock/availability date after unexpected expiry flags (RS4).
- **Prompt:** Here is the code and the error it produces: restock/availability default reference_date to date.today(). / Unexpected output: seed expiry_date values run 2026-01 through 2026-11; on 2026-08-11 several seed items already look expired or expiring soon against the calendar, so the operational day does not match the seed. Explain what is wrong and provide a corrected version with comments.
- **AI response:** Root cause: the seed is a frozen kitchen day, not “whatever day the file is run.” Default to `SIMULATION_DATE = date(2026, 5, 10)`; tests pass an explicit `reference_date`. Do not use `date.today()` as the silent production default.
- **Decision:** **Approved.**
- **Issues found:** None after the named constant.

---

## 2026-08-11 — Business summary

- **Task:** Manager-facing summary: delivered / not delivered / reasons; then inventory, restock, expiry concerns; show from `main()`; tests.
- **Prompt:** Four small prompts (counts/reasons; inventory/restock/expiry; console or dict from `main()`; unit tests).
- **AI response:** `build_manager_summary` returns a dict plus readable `text`. `main()` prints the text and returns the dict (no Markdown file). Tests for counts, reasons, restock, and readable output.
- **Decision:** **Approved.** Console print + returned dict. Extra-credit-style Markdown report not used.
- **Issues found:** None blocking Task 9.

---

## 2026-08-11 — Refactor suggest, then two improvements

- **Task:** Suggest duplication/quality issues; then apply two accepted refactors without changing public signatures.
- **Prompt:** Review for duplicated lookup/availability/restock logic (suggest only). Broader quality review (suggest only). Then extract `_inventory_by_name` and `_days_until_expiry` as the two accepted changes.
- **AI response:** Suggested several internals. User chose the shared inventory dict and shared expiry-day calculation. Restock still raises on a bad expiry date; availability and the summary still catch bad dates.
- **Decision:** **Approved.** Applied those two only. Did not rename public APIs, collapse loaders, or change restock’s bad-date behavior.
- **Issues found:** Incomplete placeholder refactor prompt was refused until I named the improvement. Tests still OK after both changes.

---

## 2026-08-12 — Three-source audit (no code)

- **Task:** Judge current project state against the graded instructions and the project plan, without changing simulation code.
- **Prompt:** Evaluate the current state of the project against `docs/CONSOLIDATED_INSTRUCTIONS.MD`. I think we have completed the base assignment and are at a stage where we should do individual plan and execute loops for the last sections. We may have planned them individually and executed them all. Do not log this request or code—just answer the question. Then: we have the consolidated instructions, and also the copy-paste instructions vs. the PDF instructions—evaluate the project against those standards individually.
- **AI response:** Mapped sources: Part I (`docs/INSTRUCTIONS.MD` Part I) = graded assignment; Part II = Project Plan PDF; CONSOLIDATED = merge with Part I winning conflicts. Verdict: Tasks 1–10 / R1–R7 met in code (47 tests OK; `main.py` runs). RS/SM/RF planned and executed as slices. Remaining is submit polish, not new feature plan/execute loops.
- **Decision:** **Approved** the audit. No re-open of Tasks 1–9 or extra credit. Capture gaps in `PROJECT_SPEC.MD` as a submit-polish plan; next step is Template 2 to break that plan into punch-list tasks.
- **Issues found:** (1) WR3 checklist not walked. (2) Fail-reason text can still say “Missing or insufficient” when detail status is `expired` (wording only). (3) Do not treat Part II partial / every-N restock as base gaps.

---

## 2026-08-12 — SP1 checklist gaps only

- **Task:** SP1 — submission checklist audit; list gaps only.
- **Prompt:** Implement Task SP1: compare repo to Part I final checklist, CONSOLIDATED §19, and WRITTEN_RESPONSE before-submit bullets; write a short gap list into PROJECT_SPEC (mirror in writeup if useful); mark open vs already true but do not tick items done; keep SP2–SP6 as closers; SP7 optional/parked; must not edit reflection, run/fix main or tests, delete waste-bin, stamp submission-ready, or change simulation files; add validation hooks; no other tasks.
- **AI response:** Open gaps: reflection voice (SP2); `main.py` run not recorded (SP3); unittest not recorded (SP4); `waste-bin/` present (SP5); spec/checklists not stamped + student “understand the code” (SP6). Optional: expired fail-reason wording (SP7 parked). Already-true items listed without ticking boxes. Mirrored notes in `WRITTEN_RESPONSE.MD` checklist.
- **Decision:** **Approved** for SP1. Next is Template 3 for SP2 only.
- **Issues found:** Historical “47 tests OK” / prior `main.py` run are not a substitute for SP3/SP4 re-record. `__pycache__` / `.DS_Store` are local junk to exclude from zip (not an SP task).

---

## 2026-08-12 — Template 1 assumptions + documented gaps plan

- **Task:** High-level plan only — audit `main.py` / `test_main.py` / `seed_data.py` vs `PROJECT_SPEC.MD` §9 and Part I; no code.
- **Prompt:** I want to audit the existing cloud kitchen inventory simulation in main.py, test_main.py, and seed_data.py against PROJECT_SPEC.MD (especially §9 open questions / assumptions / known issues) and the Part I assignment requirements. Before writing any code, give me a high-level plan — what components or gap areas still need work, which documented assumptions still need verification in the code, which known gaps are still open vs already closed, and what I should build or fix first? Do not change code in this step.
- **AI response:** §9 gaps 1–9 and 14 closed in code; open: continuous AI log (#10), reflection voice (#11 partial), optional expired fail-reason wording (#12/SP7), submit polish SP2–SP6 (#13). Assumptions spot-checked in code (exact recipe match, grams, status append, restock rebuild, all-or-nothing). Plan components: (1) optional SP7 code polish, (2) run evidence SP3–SP4, (3) submit hygiene SP5–SP6, (4) solo SP2 voice, (5) extra credit only if approved. Recommended first: decide SP7, then SP3/SP4, then SP5/SP6; SP2 offline.
- **Decision:** **Approved.** Next: Template 2 for Remaining Gaps Closeout.
- **Issues found:** None new beyond documented SP7 wording asymmetry; restock still raises on bad dates while availability/summary catch (intentional RF3).

---

## 2026-08-12 — Template 2 Remaining Gaps Closeout (breakdown only)

- **Task:** Break Remaining Gaps Closeout into one-prompt tasks from the approved Template 1 findings.
- **Prompt:** Here is component Remaining Gaps Closeout from our plan. Break it into individual implementation tasks. Keep each task small enough to implement in a single prompt. Cover only these findings from the approved Template 1 audit: (1) optional fail-reason wording when an ingredient detail status is expired or unusable instead of only “Missing or insufficient” (SP7 — keep optional until I explicitly approve implementing it); (2) record a fresh python main.py run with seed tables → process → updated inventory/restock/status → manager summary (SP3); (3) record a fresh python -m unittest -v result (SP4); (4) remove waste-bin/ from the project tree or document a hard rule that the submission zip excludes it (SP5); (5) stamp PROJECT_SPEC.MD submission-ready and tick checklist items that are actually true (SP6). Must not: reopen Tasks 1–9; treat Part II extras (partial fulfillment, restock-every-N) as required; change public function signatures; take extra credit; include reflection voice edit (SP2 is solo offline); invent new simulation features beyond SP7.
- **AI response:** Five tasks — SP7 (optional, parked until explicit approve) → SP3 record main.py → SP4 record unittest → SP5 waste-bin → SP6 stamp spec. SP1 done / SP2 solo / extra credit excluded. Written into `PROJECT_SPEC.MD` Remaining Gaps Closeout plan. No code.
- **Decision:** **Approved** the breakdown; ran Template 3 for SP7 first, then SP3.
- **Issues found:** None in the breakdown itself.

---

## 2026-08-12 — Template 4: expired fail-reason wording

- **Task:** Debug fail-reason text when availability status is `expired` (SP7).
- **Prompt:** Here is the code and the error it produces: process_orders status remark / fail-reason. / Unexpected output: when an ingredient detail status is expired (or unusable), the remark still says only “Missing or insufficient ingredients”. Deduction is already correct (no deduct). Explain what is wrong and provide a corrected version with comments.
- **AI response:** Root cause: the remark used a single shortage phrase for every unavailable path. Map `expired` → “Expired ingredients”, `unusable` → “Unusable ingredients”; keep shortage wording for missing/insufficient. Wording only; all-or-nothing unchanged.
- **Decision:** **Approved.** Then ran Template 3 SP7 to apply it.
- **Issues found:** Restock still raises on a bad expiry date (intentional RF3). Unusable wording covered via helper unit test.

---

## 2026-08-12 — SP7 fail-reason wording

- **Task:** SP7 — clearer fail-reason / status remark for expired and unusable details.
- **Prompt:** Implement Task SP7: When an order fails because an ingredient detail status is expired (or unusable), the fail-reason / status remark must say so clearly instead of only “Missing or insufficient”. Keep all-or-nothing fulfillment and do not change deduction behavior. Add or adjust a focused unittest. Use Python. Keep the code simple and add comments explaining each section. Do not implement any other tasks yet.
- **AI response:** Added `_format_unavailable_ingredient_reason` and wired it into `process_orders` (recipe-miss + inventory-fail paths). Labels: Expired / Unusable / Missing or insufficient. Public signatures unchanged; no deduct change. Tests: expired process path + helper unit test for unusable (restock still raises on bad dates — not changed). Full suite **49 OK**.
- **Decision:** **Approved.**
- **Issues found:** A process_orders fixture with `expiry_date: not-a-date` still blows up in `calculate_restock_needs` (intentional RF3); unusable wording covered via helper unit test instead.

---

## 2026-08-12 — SP3 record main.py run

- **Task:** SP3 — run `python main.py`; confirm print order; record in writeup.
- **Prompt:** Do not change code. Run python main.py. Confirm the five seed tables print first, then processing, then updated inventory / restock / status, then the manager summary. Record that confirmation in WRITTEN_RESPONSE.MD (Project Setup / before-submit checklist). Do not implement any other tasks yet.
- **AI response:** Exit 0. Order confirmed: seed Recipes → Inventory → Orders → Restock → Status, then Order Processing, then updated Inventory / Restock / Status, then Kitchen Manager Summary. Recorded in `WRITTEN_RESPONSE.MD` checklist + Project Setup. Spec/punch list updated. No code changes.
- **Decision:** **Approved.**
- **Issues found:** None in the run itself.

---

## 2026-08-12 — SP4 record unittest run

- **Task:** SP4 — run `python -m unittest -v`; record result in writeup.
- **Prompt:** Do not change code. Run python -m unittest -v. Record the result (pass/fail and test count) in WRITTEN_RESPONSE.MD (Project Setup / before-submit checklist). Do not change tests or production logic. Do not implement any other tasks yet.
- **AI response:** Ran 49 tests in 0.003s — OK (exit 0). Recorded in `WRITTEN_RESPONSE.MD` checklist + Project Setup. Spec/punch list updated. No code or test changes.
- **Decision:** **Approved.**
- **Issues found:** None.

---

## 2026-08-12 — Template 2 Assumption Closeout (breakdown only)

- **Task:** Inventory all assumption/uncertain/incomplete comments + §9 assumptions; break into one-prompt tasks.
- **Prompt:** Here is component Assumption Closeout from our plan. Break it into individual implementation tasks. Keep each task small enough to implement in a single prompt. Inventory every “Assumption to verify”, “Uncertain”, and “Incomplete / follow-up” comment in main.py, plus the “Assumptions to keep verifying” list in PROJECT_SPEC.MD §9. For each item, make one task that either (a) verifies it against PROJECT_SPEC.MD / Part I and existing tests and resolves the comment (keep / rewrite / remove), or (b) adds a focused unittest that locks the intended behavior, or (c) marks it as deferred with a written decision in PROJECT_SPEC.MD — never leave silent. Group tasks by function or concern so each Template 3 stays one slice. Must not: stamp submission-ready; reopen Tasks 1–9 wholesale; treat Part II extras as required; change public function signatures unless a named task explicitly requires it after my approve; take extra credit; queue waste-bin / SP5; invent new simulation features.
- **AI response:** ~40 `main.py` comment lines + 5 §9 bullets → **AC1–AC15** clusters (seed/loaders, grams, exact recipe match, expired vs expiring-soon, availability bad inputs, restock raise asymmetry, lookup/snapshot, all-or-nothing, status append, SP7 labels, restock replace, OP15, deepcopy, missing-recipe reason, summary/main). Each task path (a)/(b)/(c). SP6 stays blocked. Written into `PROJECT_SPEC.MD`. No code.
- **Decision:** **Approved** AC1–AC15; ran Template 3 for AC1 only.
- **Issues found:** Prior “ready” framing was wrong while these comments remained open.

---

## 2026-08-12 — AC1 seed import + loader comments

- **Task:** AC1 — close seed import / load_recipes / load_restock assumption comments.
- **Prompt:** Implement Task AC1: Close the seed import and loader assumption comments in main.py only (seed_data.py filename / direct import; load_recipes module-level lists; load_restock seed vs live rebuild note). Verify against PROJECT_SPEC.MD Decisions/DC1 and existing load tests. Resolve each related Assumption/Uncertain/Incomplete comment (rewrite to verified, remove, or record a deferral in PROJECT_SPEC.MD §9). Do not change loader APIs. Use Python only if a tiny comment-only clarification in code is needed. Keep comments clear. Do not implement any other tasks yet.
- **AI response:** Comment-only. Import block → verified DC1/`seed_data.py`. `load_recipes` → verified module-level seed lists (callers deepcopy when mutating). `load_restock` → verified seed for baseline print; live rebuild after orders. Left `load_inventory` / `load_orders` / `load_status` for AC2/AC3/AC9. Load tests + full suite OK. Spec §9 AC1 progress noted. No API changes.
- **Decision:** **Approved.** Template 2 Assumption Closeout approved by executing AC1.
- **Issues found:** None.

---

## 2026-08-12 — AC2 grams including buns

- **Task:** AC2 — close “all quantities are grams, including buns.”
- **Prompt:** Implement Task AC2: Close the “all quantities are grams, including buns” assumption (load_inventory comment + PROJECT_SPEC.MD §9). Verify against seed_data and existing type tests; add a focused unittest only if coverage is missing. Resolve the comment. Do not invent unit counts. Do not implement any other tasks yet.
- **AI response:** Seed uses `qty_grams` for Bun in inventory and Chicken Burger recipe. Resolved `load_inventory` comment to verified. Added `test_all_seed_quantities_are_grams_including_buns`. No unit-count fields invented. Suite **50 OK**. §9 AC2 closed.
- **Decision:** **Approved.**
- **Issues found:** None.

---

## 2026-08-12 — AC3 exact recipe name match

- **Task:** AC3 — close exact recipe-name-match assumptions.
- **Prompt:** Implement Task AC3: Close exact recipe-name-match assumptions (load_orders, find_recipe_by_name, §9). Verify against Decisions and existing hit/miss tests; add a case-mismatch unittest if absent. Resolve related comments. Do not add aliases or case-folding. Do not implement any other tasks yet.
- **AI response:** Verified Decisions + hit/miss tests. Resolved `load_orders` / `find_recipe_by_name` comments. Added `test_find_recipe_by_name_requires_exact_case_match` (case + leading/trailing space → None). No aliases/case-folding. Suite **51 OK**. §9 AC3 closed.
- **Decision:** **Approved.**
- **Issues found:** None.

---

## 2026-08-12 — AC4 expired vs expiring-soon

- **Task:** AC4 — close expired vs expiring-soon assumptions.
- **Prompt:** Implement Task AC4: Close expired vs expiring-soon assumptions (named-constants comment that days < 0 blocks fulfillment while the 5-day window is restock-only; matching notes in availability/summary). Verify against PROJECT_SPEC.MD Decisions and existing expired / expiring-soon tests. Resolve related comments. Do not make expiring-soon block fulfillment. Do not implement any other tasks yet.
- **AI response:** Verified Decisions + existing tests (expired blocks; expiring soon does not; restock flags soon). Resolved RS1 constants, availability AC4 lines, and summary expiry-window comments to Verified (AC4). Left AC5 bad-input assumptions in place. No behavior change. Suite **51 OK**.
- **Decision:** **Approved.**
- **Issues found:** None.

---

## 2026-08-12 — AC5 availability defaults and bad inputs

- **Task:** AC5 — close availability default/bad-input assumptions.
- **Prompt:** Implement Task AC5: Close availability default and bad-input assumptions in check_inventory_availability (SIMULATION_DATE default; None/empty/negative handling; malformed expiry as unusable). Verify against existing OP7 tests. Resolve related Assumption/Uncertain/Incomplete comments. Do not change the public function signature. Do not implement any other tasks yet.
- **AI response:** Verified OP7 tests (None/empty/negative/unusable). Resolved remaining availability Assumption/Uncertain/Incomplete comments to Verified (AC5). Added `test_availability_default_reference_date_is_simulation_date`. Public signature unchanged. Suite **52 OK**.
- **Decision:** **Approved.**
- **Issues found:** None.

---

## 2026-08-12 — AC6 restock raise on bad date

- **Task:** AC6 — close `_days_until_expiry` asymmetry (restock raises; availability/summary catch).
- **Prompt:** Implement Task AC6: Close the _days_until_expiry asymmetry (restock raises on a bad date; availability/summary catch and treat as unusable). Either document as intentional RF3 in PROJECT_SPEC.MD §9 or add a focused test that restock raises; resolve the comment. Do not silently make restock swallow bad dates without my approve. Do not implement any other tasks yet.
- **AI response:** Documented intentional RF3 asymmetry in §9. Resolved `_days_until_expiry` comment to Verified (AC6). Added `test_restock_raises_on_malformed_expiry_date`. Did not change restock to swallow bad dates. Suite **53 OK**.
- **Decision:** **Approved.**
- **Issues found:** None.

---

## 2026-08-12 — Duplication review (suggest-only plan)

- **Task:** Review main.py for duplicated logic; suggest refactor plan; no signature changes; Template 1-style plan.
- **Prompt:** Review the code in main.py for duplicated logic or functions — particularly any inventory lookup, availability check, or restock flagging logic that appears more than once. Suggest how to refactor it to eliminate duplication while keeping the behaviour identical. Do not change any function signatures yet. Output should be in the format of a plan that can be broken into tasks. See Prompt Template 1 for more information
- **AI response:** Noted RF2/RF3 already closed. Remaining components: (1) shared stock-flag classifier for restock vs summary, (2) restock row builder for calculate_restock_needs vs OP15, (3) default reference_date helper, (4) optional snapshot/lookup alignment (document first). Build order and must-nots listed. No code changed.
- **Decision:** **Approved** components 1–3 for a Template 2 breakdown; component 4 routed to AC7.
- **Issues found:** None new; AC7 overlaps component 4.

---

## 2026-08-13 — Template 2: Duplication-refactor task breakdown (DR)

- **Task:** Break approved duplication-refactor build order into Template-3-sized tasks. Task list only; no code.
- **Prompt:** Here is the approved duplication-refactor build order from our plan. Treat it as confirmed. Break it into individual implementation tasks for components in this exact order: (1) Shared stock-flag classifier for calculate_restock_needs and build_manager_summary, (2) Restock row builder shared by calculate_restock_needs and add_failed_order_items_to_restock, (3) Default reference_date helper. Keep each task small enough to implement in a single Template 3 prompt. Must not change public function signatures unless I explicitly approve that in a later task. Must not invent new simulation features, change restock bad-date behavior, or take extra credit. Do not implement any tasks yet — task list only. Component 4 (snapshot vs full-row lookup) stays out of this breakdown; handle it under AC7 separately.
- **AI response:** Tasks DR1–DR8 listed (Component 1: DR1–DR3; Component 2: DR4–DR6; Component 3: DR7–DR8). Component 4 deferred to AC7. No code changed.
- **Decision:** **Approved**; ran Template 3 for DR1.
- **Issues found:** None — noted intentional asymmetry: summary catches bad dates / lists expired; restock raises and does not use Expired as a restock reason.

---

## 2026-08-13 — Template 3: DR1 stock-flag classifier

- **Task:** DR1 — add private `_classify_inventory_stock_flags`; do not wire callers; no public signature changes.
- **Prompt:** Implement Task DR1: Add a private helper in main.py that classifies inventory stock/expiry flags from current_qty_grams and days_until_expiry using the same thresholds as calculate_restock_needs and build_manager_summary (RUNNING_LOW_THRESHOLD_GRAMS, PAR_LEVEL_GRAMS, EXPIRING_SOON_DAYS). It must return enough information for both callers: out-of-stock / running-low / expiring-soon / expired booleans, restock reason labels matching current restock strings, and restock qty_needed_grams using the current max-of-rules logic. Do not wire callers yet. Do not catch malformed dates inside this helper (caller passes days_until_expiry or None). Do not change any public function signatures. Use Python. Add comments. Do not implement any other tasks yet.
- **AI response:** Added `_classify_inventory_stock_flags` after `_days_until_expiry`. Returns booleans + restock_reasons + qty_needed_grams matching existing restock strings/max-of-rules. Expired does not add a restock reason. No date parsing/catching. Callers unchanged. Added 5 unit tests. Suite 58 OK.
- **Decision:** **Approved** for DR1.
- **Issues found:** None.

---

## 2026-08-13 — Template 3: DR2 wire classifier into restock

- **Task:** DR2 — refactor calculate_restock_needs to use DR1 helper; bare _days_until_expiry; no summary change; no public signature changes.
- **Prompt:** Implement Task DR2: Refactor only calculate_restock_needs to use the DR1 stock-flag helper for out-of-stock, running-low, and expiring-soon reason/qty logic. Keep behaviour identical, including bare _days_until_expiry (malformed dates still raise). Do not change build_manager_summary or public signatures. Use Python. Add comments. Do not implement any other tasks yet.
- **AI response:** calculate_restock_needs now calls _classify_inventory_stock_flags for reasons/qty_needed. Still calls _days_until_expiry bare. Row shape unchanged. build_manager_summary untouched. Suite 58 OK.
- **Decision:** **Approved** for DR2.
- **Issues found:** None.

---

## 2026-08-13 — Template 3: DR3 wire classifier into summary

- **Task:** DR3 — refactor build_manager_summary inventory flag lists to use DR1 helper; keep try/except bad-date → expired; no public signature / restock bad-date changes.
- **Prompt:** Implement Task DR3: Refactor only build_manager_summary inventory flag lists to use the DR1 stock-flag helper where safe. Keep behaviour identical: try/except around _days_until_expiry still treats bad dates as expired/unusable for the summary lists; expired and expiring-soon lists unchanged in meaning. Do not change public signatures or restock bad-date behavior. Use Python. Add comments. Do not implement any other tasks yet.
- **AI response:** Summary now uses _classify_inventory_stock_flags for out/low/expired/expiring-soon after a caught parse. Bad dates still append to expired before classify(None). Restock untouched. Suite 58 OK. Component 1 complete.
- **Decision:** **Approved** for DR3.
- **Issues found:** None.

---

## 2026-08-13 — Template 3: DR4 restock row builder

- **Task:** DR4 — add private `_make_restock_row`; do not wire callers; no public signature changes.
- **Prompt:** Implement Task DR4: Add a private helper in main.py that builds one restock-table row dict with keys item, current_qty_grams, qty_needed_grams, reason, reasons, expiry_date — matching the shape used by calculate_restock_needs and add_failed_order_items_to_restock (reason is the joined reasons list). Do not wire callers yet. Do not change public signatures. Use Python. Add comments. Do not implement any other tasks yet.
- **AI response:** Added `_make_restock_row` after `_classify_inventory_stock_flags`. Joins reasons into reason. Callers unchanged. 2 helper tests. Suite 60 OK.
- **Decision:** **Approved** for DR4.
- **Issues found:** None.

---

## 2026-08-13 — Template 3: DR5 wire row builder into restock

- **Task:** DR5 — refactor calculate_restock_needs to append via _make_restock_row; leave OP15 alone; no public signature changes.
- **Prompt:** Implement Task DR5: Refactor only calculate_restock_needs to append rows via the DR4 restock row builder. Keep behaviour identical. Do not change add_failed_order_items_to_restock or public signatures. Use Python. Add comments. Do not implement any other tasks yet.
- **AI response:** calculate_restock_needs now appends _make_restock_row(...). add_failed_order_items_to_restock untouched. Suite 60 OK.
- **Decision:** **Approved** for DR5.
- **Issues found:** None.

---

## 2026-08-13 — Template 3: DR6 wire row builder into OP15

- **Task:** DR6 — refactor add_failed_order_items_to_restock to append via _make_restock_row; keep skip/label logic outside; no public signature changes.
- **Prompt:** Implement Task DR6: Refactor only add_failed_order_items_to_restock to append rows via the DR4 restock row builder. Keep skip-if-name-exists and reason-label selection logic outside the helper. Keep behaviour identical. Do not change public signatures. Use Python. Add comments. Do not implement any other tasks yet.
- **AI response:** OP15 append now uses _make_restock_row with reasons=[reason_label]. Skip-existing and label selection unchanged. Suite 60 OK. Component 2 complete.
- **Decision:** **Approved** for DR6.
- **Issues found:** None.

---

## 2026-08-13 — Template 3: DR7 reference_date helper

- **Task:** DR7 — add private `_resolve_reference_date`; do not wire callers; no public signature changes.
- **Prompt:** Implement Task DR7: Add a private helper in main.py that returns SIMULATION_DATE when reference_date is None, otherwise returns reference_date unchanged. Do not wire callers yet. Do not change public signatures. Use Python. Add comments. Do not implement any other tasks yet.
- **AI response:** Added `_resolve_reference_date`. Callers still use inline None checks. 2 helper tests. Suite 62 OK.
- **Decision:** **Approved** for DR7.
- **Issues found:** None.

---

## 2026-08-13 — Template 3: DR8 wire reference_date helper

- **Task:** DR8 — wire _resolve_reference_date into availability, restock, and summary; keep SIMULATION_DATE default; no public signature / restock bad-date changes.
- **Prompt:** Implement Task DR8: Refactor check_inventory_availability, calculate_restock_needs, and build_manager_summary to resolve default reference_date via the DR7 helper. Keep behaviour identical (default remains SIMULATION_DATE). Do not change public signatures or restock bad-date behavior. Use Python. Add comments. Do not implement any other tasks yet.
- **AI response:** All three call sites now use _resolve_reference_date. Public signatures unchanged. Restock still bare-raises on bad dates. Suite 62 OK. DR Components 1–3 complete.
- **Decision:** **Approved** for DR8.
- **Issues found:** None.

---

## 2026-08-13 — Template 3: AC7 lookup last-wins + snapshot shape

- **Task:** AC7 — close _inventory_by_name last-row-wins and apply_final_inventory_snapshot qty-only map; document; resolve comments; no signature/merge.
- **Prompt:** Implement Task AC7: Close _inventory_by_name last-row-wins and apply_final_inventory_snapshot qty-only map comments. Verify intended behavior; document in PROJECT_SPEC.MD §9 if needed; resolve comments. Do not change public signatures or merge map shapes unless I approve a follow-on. Do not implement any other tasks yet.
- **AI response:** Verified last-row-wins intentional; seed names unique. Qty-only snapshot intentional (preserves live expiry). Comments → Verified (AC7). §9 + intentional asymmetries updated. Added 3 tests. Suite 65 OK. Did not merge map shapes.
- **Decision:** **Approved** for AC7.
- **Issues found:** None.

---

## 2026-08-13 — Template 3: AC8 all-or-nothing / no partial deduct

- **Task:** AC8 — close all-or-nothing assumptions in deduct_inventory, process_orders, OP15, §9; confirm tests; no partial fulfillment.
- **Prompt:** Implement Task AC8: Close all-or-nothing / no partial deduct assumptions in deduct_inventory, process_orders, OP15, and PROJECT_SPEC.MD §9. Confirm fulfillment/cumulative tests; resolve comments. Do not implement partial fulfillment. Do not change public signatures unless I approve. Do not implement any other tasks yet.
- **AI response:** Comments → Verified (AC8). Confirmed existing without-deduct / cumulative tests. Added multi-item pizza+burger fail with inventory unchanged. §9 closed. Suite 66 OK. No partial fulfillment.
- **Decision:** **Approved** for AC8.
- **Issues found:** None.

---

## 2026-08-13 — Template 3: AC9 status seed vs append

- **Task:** AC9 — close load_status / update_status_entry / §9 status append assumptions; confirm with test; seed is initial only; do not require pre-seeded orders.
- **Prompt:** Implement Task AC9: Close status seed vs append assumptions in load_status, update_status_entry, and PROJECT_SPEC.MD §9. Confirm append behavior with a test if needed; decide seed is initial table only; resolve comments. Do not require every order pre-seeded unless I approve. Do not implement any other tasks yet.
- **AI response:** Seed status = baseline print only. update_status_entry updates in place or appends. Comments → Verified (AC9). Added 3 tests. §9 closed. Suite 69 OK. Did not require pre-seeded orders.
- **Decision:** **Approved** for AC9.
- **Issues found:** None.

---

## 2026-08-13 — Template 3: AC10 SP7 reason labels

- **Task:** AC10 — close SP7 reason-label assumptions on _format_unavailable_ingredient_reason; confirm SP7 tests; no public signature changes.
- **Prompt:** Implement Task AC10: Close SP7 reason-label assumptions on _format_unavailable_ingredient_reason. Confirm SP7 tests; resolve/remove stale assumptions. Do not change public signatures. Do not implement any other tasks yet.
- **AI response:** Comments → Verified (AC10). Confirmed SP7 helper + fail-reason-without-deduct tests. Extended helper test for invalid→Missing or insufficient. Signatures unchanged. Suite 69 OK.
- **Decision:** **Approved** for AC10.
- **Issues found:** None.

---

## 2026-08-13 — Template 3: AC11 restock rules + replace table

- **Task:** AC11 — close restock rules + replace-table assumptions; confirm RS/OP15 tests; no restock-every-N.
- **Prompt:** Implement Task AC11: Close restock rules + replace-table assumptions (qty 0 not also running low; max qty_needed; OP15 covers missing; refresh_restock_table replaces history) and PROJECT_SPEC.MD §9. Confirm RS + OP15 tests; resolve comments. Do not add restock-every-N. Do not implement any other tasks yet.
- **AI response:** Comments → Verified (AC11) on classifier/restock/refresh. Confirmed existing RS (out-of-stock-only reasons, multi-reason max qty) and OP15 missing-item tests. Added refresh-replaces-prior-rows test. §9 closed. Suite 70 OK. No restock-every-N. Left OP15 duplicate/par details for AC12.
- **Decision:** **Approved** for AC11.
- **Issues found:** None.

---

## 2026-08-13 — Template 3: AC12 OP15 duplicate + par

- **Task:** AC12 — close OP15 one-row-per-name, missing→full par, expired-at-par→par; confirm tests; no silent duplicates.
- **Prompt:** Implement Task AC12: Close OP15 duplicate + par assumptions (one row per name; missing→full par; expired-at-par still requests par). Confirm existing OP15 tests; add focused assert if needed; resolve comments. Do not allow silent duplicates. Do not implement any other tasks yet.
- **AI response:** Comments → Verified (AC12). Confirmed existing OP15 duplicate/missing tests. Asserted expired-at-par qty_needed. Added TestAddFailedOrderItemsToRestock (skip/missing/expired-at-par). Suite 73 OK.
- **Decision:** **Approved** for AC12.
- **Issues found:** None.

---

## 2026-08-13 — Template 3: AC13 working inventory deepcopy

- **Task:** AC13 — close deepcopy assumptions; confirm cumulative tests; optional aliasing test; defer persistence to §9; no database.
- **Prompt:** Implement Task AC13: Close working-inventory deepcopy assumptions in process_orders. Confirm cumulative tests; optional tiny aliasing test; resolve comment; defer persistence to PROJECT_SPEC.MD §9. Do not add a database. Do not implement any other tasks yet.
- **AI response:** Comments → Verified (AC13); persistence deferred in §9. Added test_live_inventory_unchanged_until_final_snapshot (live qty intact during deduct; snapshot afterward). Confirmed cumulative tests. Suite 74 OK. No database.
- **Decision:** **Approved** for AC13.
- **Issues found:** None.

---

## 2026-08-13 — Template 3: AC14 missing-recipe reason path

- **Task:** AC14 — close missing-recipe Incomplete; confirm “No matching recipe…”; no crash; no invent ingredients.
- **Prompt:** Implement Task AC14: Close missing-recipe reason path Incomplete in process_orders. Confirm “No matching recipe…” is recorded; resolve Incomplete. Do not crash on miss or invent ingredients. Do not implement any other tasks yet.
- **AI response:** Formal reason already present; Incomplete → Verified (AC14). Added test_process_orders_records_no_matching_recipe_reason (reason, status, no inventory change, empty requirements). Suite 75 OK.
- **Decision:** **Approved** for AC14.
- **Issues found:** None.

---

## 2026-08-14 — Template 3: AC15 summary + main display

- **Task:** AC15 — close summary + main display assumptions; confirm SM tests + SP3 evidence; no Markdown report.
- **Prompt:** Implement Task AC15: Close summary + main display assumptions (fulfilled True; expiry windows; live restock passed in; SM3; main print order + console/dict). Confirm SM tests + SP3 evidence; resolve comments. Do not add a Markdown report. Do not implement any other tasks yet.
- **AI response:** Comments on build_manager_summary and main() → Verified (AC15). Confirmed SM/main tests + SP3 writeup evidence. No Markdown. Suite 75 OK. AC1–AC15 complete; SP6 unblocked.
- **Decision:** **Approved** for AC15.
- **Issues found:** Two unrelated DR “Assumption to verify” comments remain on `_classify_inventory_stock_flags` (None days) and `_make_restock_row` (reasons list) — outside AC15 scope.

---

## 2026-08-14 — Template 3: SP6 stamp PROJECT_SPEC

- **Task:** SP6 — update PROJECT_SPEC only; mark AC complete; re-anchor; stamp submission-ready only if reality matches; no SP5/extra credit claims.
- **Prompt:** Do not change simulation code. Update PROJECT_SPEC.MD only: mark Assumption Closeout complete if AC1–AC15 are done, re-anchor where-we-are, and stamp submission-ready only if that matches reality. Do not claim SP5 or extra credit. Do not implement any other tasks yet.
- **AI response:** Stamped living spec for base + AC1–AC15 with honest caveats. Ticked only true checklist items. Left SP2 voice and “understand the code” open/unticked. SP5 ignored (exclude from zip), not claimed deleted. Extra credit not claimed. Noted suite 75 OK. No simulation code changes.
- **Decision:** **Approved** SP6 stamp with caveats.
- **Issues found:** Full “submit polish closed” would be false while SP2 is open — stamp wording reflects that.

---

## 2026-08-14 — Template 1: Error handling + Task 10 checklist plan

- **Task:** Plan-only review of error handling + project_tasks Task 10 checklist (dupes, constants, names, comments, error handling, oversized functions); include repairs in plan; no code; no signature changes.
- **Prompt:** (user send) error-handling Template 1 + “IN addition, look for project_tasks 180-185 and include their repair in the plan.”
- **AI response:** Delivered component plan EH1–EH4 + T10 repairs (comments, optional size, names); noted already-done RF/DR/constants; intentional restock raise; build-order; must-nots. No code changed.
- **Decision:** **Approved**; ran Template 2 per component (EH1+EH3 first).
- **Issues found:** Error handling is mostly result-status based (quiet); two leftover “Assumption to verify” comments; process_orders / build_manager_summary still large.

---

## 2026-08-14 — Template 2: EH1+EH3 task breakdown

- **Task:** Break EH1+EH3 (error-handling inventory + intentional raise/catch docs) into Template-3-sized tasks. Task list only.
- **Prompt:** Here is component EH1+EH3 from our error-handling / Task 10 plan: Error-handling inventory and intentional raise/catch documentation. Break it into individual implementation tasks. Keep each task small enough to implement in a single prompt. Must not change public function signatures or restock bad-date raise behavior. Must not invent new simulation features or take extra credit. Do not implement any tasks yet — task list only.
- **AI response:** Tasks EH1a–EH1d + EH3a–EH3b listed (inventory table in PROJECT_SPEC/WRITTEN_RESPONSE; comment/§9 intentional asymmetry; no behavior change). No code logic changed in this pass by design.
- **Decision:** **Approved**; ran Template 3 for EH1a.
- **Issues found:** None.

---

## 2026-08-14 — Template 3: EH1a availability/OP7 error map

- **Task:** EH1a — document only check_inventory_availability / OP7 paths in PROJECT_SPEC §9; no behavior or signature changes.
- **Prompt:** Implement Task EH1a: Do not change simulation behavior or public signatures. Document only — in PROJECT_SPEC.MD §9 (or a clearly marked Error-handling map subsection) — how check_inventory_availability / OP7 paths handle: None or empty inventory, None or empty requirements, negative required qty, missing ingredient, insufficient grams, expired (days < 0), and unusable/malformed expiry. For each, note the result shape (status / all_available) and cite existing tests where possible. Do not implement any other tasks yet.
- **AI response:** Added §9 “Error-handling map” EH1a table with return shape + rows for None/empty inventory & requirements, invalid/missing/insufficient/expired/unusable, expiring-soon note, default reference_date; cited existing unittest names. No main.py changes.
- **Decision:** **Approved** for EH1a.
- **Issues found:** None.

---

## 2026-08-14 — Template 3: EH1b recipes/orders error map

- **Task:** EH1b — document process_orders / find_recipe_by_name missing recipe, empty orders, empty items in PROJECT_SPEC §9; no behavior/signature changes.
- **Prompt:** Implement Task EH1b: Do not change simulation behavior or public signatures. Document only in PROJECT_SPEC.MD §9 Error-handling map — how process_orders / find_recipe_by_name handle missing recipes, empty order lists, and orders with empty items (reason strings, fulfilled flag, inventory unchanged, no invented ingredients). Cite existing tests where possible. Do not implement any other tasks yet.
- **AI response:** Added EH1b table: recipe None; missing-recipe reject + reason; empty order_data → []; empty items → vacuous Delivered (documented from code, no dedicated test). Cited AC14 / find_recipe tests. No main.py changes.
- **Decision:** **Approved** for EH1b.
- **Issues found:** Empty-items Delivered and empty order_data lack dedicated unit tests — noted in map.

---

## 2026-08-14 — Template 3: EH1c restock/summary/print error map

- **Task:** EH1c — document restock raise vs summary catch, empty tables, odd/missing fields for restock/summary/print_*; docs only.
- **Prompt:** Implement Task EH1c: Do not change simulation behavior or public signatures. Document only in PROJECT_SPEC.MD §9 Error-handling map — how calculate_restock_needs / refresh_restock_table, build_manager_summary, and the print_* helpers behave on malformed expiry (raise vs catch), empty tables, and odd/missing row fields. Cite existing tests where possible. Do not implement any other tasks yet.
- **AI response:** Added EH1c table covering restock bare-raise, refresh clear+rebuild, summary catch/None coerce/skip non-dicts, print_* empty vs KeyError on bad shape. Cited AC6/refresh/summary empty tests. No main.py changes.
- **Decision:** **Approved** for EH1c.
- **Issues found:** None new — printers trust seed shape by design.

---

## 2026-08-14 — Template 3: EH1d consolidate error-handling map

- **Task:** EH1d — consolidate §9 Error-handling map (EH1a–EH1c) + optional WRITTEN_RESPONSE pointer; docs only.
- **Prompt:** Implement Task EH1d: Do not change simulation behavior or public signatures. Consolidate the §9 Error-handling map (EH1a–EH1c) so it is easy to scan as one inventory, and optionally add a short pointer in WRITTEN_RESPONSE.MD under Task 10 / quality to that map. No new behaviors. Do not implement any other tasks yet.
- **AI response:** Added “At a glance” inventory table (areas A–E) above detail subsections; folded EH1a non-dict note into Detail A; marked EH1 complete; pointer in WRITTEN_RESPONSE Refactoring Notes → PROJECT_SPEC §9 map. No main.py changes.
- **Decision:** **Approved** for EH1d.
- **Issues found:** None.

---

## 2026-08-14 — Template 3: EH3a AC6 raise/catch comments

- **Task:** EH3a — strengthen Verified/intentional comments on AC6 asymmetry; point at locking tests; no behavior/signature change.
- **Prompt:** Implement Task EH3a: Do not change simulation behavior or public signatures. Strengthen Verified / intentional comments on the AC6 raise vs catch asymmetry: bare `_days_until_expiry` in `calculate_restock_needs`, and try/except catch in availability + `build_manager_summary`. Point comments at locking tests where helpful. Do not implement any other tasks yet.
- **AI response:** Comment-only updates on `_days_until_expiry`, availability header + try/except, `calculate_restock_needs` bare call, `build_manager_summary` catch path. Named locking tests. No logic/signature changes.
- **Decision:** **Approved** for EH3a.
- **Issues found:** None.

---

## 2026-08-14 — Template 3: EH3b intentional-asymmetry blurb

- **Task:** EH3b — expand §9 Intentional asymmetries for Task 10 “weak error handling” readers; docs only.
- **Prompt:** Implement Task EH3b: Do not change simulation behavior or public signatures. Ensure PROJECT_SPEC.MD §9 “Intentional asymmetries” (or equivalent) explicitly covers restock raise vs availability/summary catch for Task 10 “weak error handling” readers. Docs only. Do not implement any other tasks yet.
- **AI response:** Expanded RF3/AC6/EH3 bullet: catch vs raise sides, “not weak handling,” do-not-align warning, locking tests, pointer to error-handling map; marked EH3 complete in map policy. No main.py changes.
- **Decision:** **Approved** for EH3b. EH1+EH3 component complete.
- **Issues found:** None.

---

## 2026-08-14 — Template 2: EH2 harden quiet/weak paths task breakdown

- **Task:** Break EH2 into Template-3-sized tasks. Task list only. No restock bad-date swallow; no signature changes.
- **Prompt:** Here is component EH2 from our error-handling / Task 10 plan: Harden quiet/weak paths only where we already documented gaps (without changing public signatures or making restock swallow bad dates). Break it into individual implementation tasks. Keep each task small enough to implement in a single prompt. Do not implement any tasks yet — task list only.
- **AI response:** Tasks EH2a–EH2g listed (test-locks first; empty-items decision gate; optional printer soften; restock KeyError lock without catching expiry; map update). Must-nots restated. No code changed.
- **Decision:** **Approved** EH2a–EH2b only; the rest of EH2 left unqueued as optional hardening.
- **Issues found:** Most “gaps” are missing tests for already-correct quiet behavior, not missing try/except.

---

## 2026-08-14 — Template 3: EH2a empty order_data test

- **Task:** EH2a — dedicated unittest empty order_data → []; update §9 Detail B cite; no behavior/signature change.
- **Prompt:** Implement Task EH2a: Do not change simulation behavior or public signatures. Add a dedicated unittest that empty order_data passed to process_orders returns [] and does not raise. Cite/update PROJECT_SPEC.MD §9 Detail B if needed. Do not implement any other tasks yet.
- **AI response:** Added test_process_orders_empty_order_data_returns_empty_list (empty return, no status rows, qty unchanged, restock rebuilt not seed-only). Updated §9 Detail B citation. No main.py logic changes.
- **Decision:** **Approved** for EH2a.
- **Issues found:** None.

---

## 2026-08-14 — Template 3: EH2b empty-inventory restock tests

- **Task:** EH2b — unittests for empty inventory restock/refresh; AC6 raise unchanged; §9 cites; no behavior/signature change.
- **Prompt:** Implement Task EH2b: Do not change simulation behavior or public signatures. Add dedicated unittests that calculate_restock_needs([]) returns [] and refresh_restock_table clears to empty recommendations when inventory is empty (malformed expiry must still raise — do not catch). Update §9 citations if needed. Do not implement any other tasks yet.
- **AI response:** Added test_calculate_restock_needs_empty_inventory_returns_empty_list and test_refresh_restock_table_empty_inventory_clears_recommendations. Updated §9 Detail C cites. Confirmed test_restock_raises_on_malformed_expiry_date still OK. No main.py logic changes.
- **Decision:** **Approved** for EH2b.
- **Issues found:** None.

---

## 2026-08-16 — Requirements audit vs Part I / Part II (no code)

- **Task:** Re-derive the full requirement set from every supplied document and audit the code, tests, and Markdown against it.
- **Prompt:** Audit the week-3 assignment, build one consolidated standard from all documents, then audit the code against it including the MD files.
- **AI response:** Confirmed the PDF duplicates `INSTRUCTIONS.MD` Part II and that the three lecture transcripts contain no assignment requirements. Produced a deduplicated standard plus nine Part I / Part II conflicts. Found one functional gap: **expired stock produced no restock recommendation** because `_classify_inventory_stock_flags` computed an `expired` flag and then declined to use it. Root cause: the implementation followed Part II Step 5, which lists only out-of-stock / running-low / expiring-soon, while Part I R6 explicitly says "expired **or** expiring soon". Part I governs.
- **Decision:** **Approved** the finding. Confirmed the defect by probe before agreeing to change code: 10,000g of Chocolate four months past expiry returned `[]` from `calculate_restock_needs`. Masked in the seed run only because order 3 happens to fail on those ingredients, so OP15 added them as a side effect.
- **Issues found:** `docs/CONSOLIDATED_INSTRUCTIONS.MD` §6 had propagated the same omission — its restock table also drops "expired". The consolidation error and the code defect were the same error.

---

## 2026-08-16 — Template 4: expired stock returns no restock row

- **Task:** Debug expired inventory producing no restock recommendation (RX1 / Part I R6).
- **Prompt:** Here is the code and the error it produces: _classify_inventory_stock_flags sets expired when days_until_expiry < 0 but does not append a restock reason from that flag; calculate_restock_needs therefore returns [] for Chocolate at 10,000g with expiry_date 2026-01-10 (simulation date 2026-05-10). / Unexpected output: Part I R6 requires flagging expired or expiring soon; expired stock only reached the table if an order failed on it (seed order 3 masks this). test_expired_flag_does_not_add_restock_reason asserted the defect. Explain what is wrong and provide a corrected version with comments.
- **AI response:** Root cause: the classifier followed Part II Step 5 (out-of-stock / running-low / expiring-soon only) and ignored Part I’s “expired or expiring soon.” Part I governs. Add `"Expired"` at full par (`max(..., PAR_LEVEL_GRAMS)`), compose with other reasons, and replace the test that had locked the defect.
- **Decision:** **Approved.** 
- **Issues found:** A green suite can lock a wrong requirement. Verified `add_failed_order_items_to_restock` still skips names already on the table.

---

## 2026-08-16 — Template 3: RX1 expired stock must trigger restock

- **Task:** RX1 — close the Part I R6 gap so expired inventory is flagged by the rule engine, not only when an order fails on it.
- **Prompt:** Implement Task RX1: In `_classify_inventory_stock_flags`, add "Expired" as a restock reason at full par when `expired` is true, so Part I R6 ("expired or expiring soon") is satisfied without depending on a failed order. Keep multi-reason behaviour: expiry must not overwrite an existing quantity reason. Do not change public signatures. Do not change the availability or summary catch/raise behaviour. Add unit tests. Use Python. Add comments explaining each section. Do not implement any other tasks yet.
- **AI response:** Added the `expired` branch after `expiring_soon`, using `max(..., PAR_LEVEL_GRAMS)` so it composes with the existing rules. Updated the stale comment that had justified the omission and added an RX1 note on `calculate_restock_needs`. Replaced `test_expired_flag_does_not_add_restock_reason` (which locked the buggy behaviour) with `test_expired_adds_restock_reason_at_full_par`, and added `test_expired_and_out_of_stock_keep_both_reasons`.
- **Decision:** **Approved.** Full par rather than a top-up is the right quantity: expired grams cannot be used, so they need replacing, not topping up.
- **Issues found:** The existing test actively asserted the wrong behaviour, so the suite was green *because* of the defect — a reminder that a passing suite only locks in whatever the author believed at the time. Verified `add_failed_order_items_to_restock` still skips names already on the table, so expired items appear exactly once. Suite **79 OK**; `python main.py` exit 0, with Fettuccine Pasta and Chocolate now flagged by the rule engine instead of arriving via the failed-order path.

---

## 2026-08-16 — Template 3: RF5 split `process_orders`

- **Task:** RF5 — Task 10 "functions that do too much". `process_orders` was 127 lines carrying four jobs at once: per-line recipe lookup, the fulfil/reject decision, the side effects (deduct + status), and the cumulative loop.
- **Prompt:** Implement Task RF5: Split `process_orders` in main.py into smaller functions without changing behaviour or the public signature. Extract (1) the per-item recipe lookup and scaled-requirement build, (2) the fulfilled/reason decision as a pure function, and (3) the per-order side effects (deduct on success, status write) so that `process_orders` itself is only the cumulative loop plus the after-all-orders publish step. Keep all-or-nothing fulfilment and the cumulative deepcopy behaviour identical. Use Python. Keep the code simple and add comments explaining each section. Do not implement any other tasks yet.
- **AI response:** Added `_resolve_order_lines` (item results, requirement groups, missing-recipe names — pure), `_decide_order_outcome` (returns `(fulfilled, reason)`, pure, no mutation), and `_process_single_order` (the only place that deducts and writes status). `process_orders` dropped from 127 to 32 lines and now reads as: deepcopy → loop → snapshot → refresh restock → merge failed items. Public signature unchanged.
- **Decision:** **Approved.** The decision logic being pure is the part worth keeping: `_decide_order_outcome` cannot break all-or-nothing (AC8) even by accident, because it holds no reference to the inventory. Every side effect is now in one function I can point at during review.
- **Issues found:** Had to preserve the original `if/elif/else` precedence exactly — a missing recipe rejects the order *even when every ingredient is in stock*, and the inventory wording is appended only when ingredients also failed. Writing it as two independent checks would have changed the reason string for mixed failures. Verified against `test_process_orders_records_no_matching_recipe_reason`. Suite **79 OK**; `python3 main.py` output unchanged.

---

## 2026-08-16 — Template 3: RF6 split `build_manager_summary`

- **Task:** RF6 — Task 10 "functions that do too much". `build_manager_summary` was 162 lines mixing order classification, expiry parsing, stock classification, and report formatting in one body.
- **Prompt:** Implement Task RF6: Split `build_manager_summary` in main.py into smaller functions without changing behaviour or the public signature. Extract (1) splitting processed orders into delivered / not-delivered entries, (2) building the final-inventory snapshot and the low / out-of-stock / expired / expiring-soon lists, and (3) rendering the manager-readable text from already-computed results. Keep the summary's catch of malformed expiry dates — do not make restock swallow bad dates. Keep the `show_inventory` / `show_restock` behaviour when the caller passes None. Use Python. Keep the code simple and add comments explaining each section. Do not implement any other tasks yet.
- **AI response:** Added `_split_orders_by_delivery`, `_summarize_inventory_health` (returns the snapshot plus the four attention lists), and `_render_manager_summary_text` (presentation only). `build_manager_summary` dropped from 162 to 54 lines and is now argument-normalisation, three calls, and the returned dict. The four "needs attention" lines became a loop over `(label, names)` pairs rather than four near-identical appends.
- **Decision:** **Approved.** Separating rendering from rules matches the Part II §1 point about keeping logic changes and output-format changes apart — the report wording can now change without touching expiry logic.
- **Issues found:** `show_inventory` / `show_restock` had to stay explicit parameters rather than being inferred from the lists being empty. A caller passing an empty inventory list is not the same as passing `None`: the first prints an empty "Final inventory" block, the second omits the block entirely. Inferring from emptiness would have silently changed output for the empty-list case. Also confirmed the summary's `try/except` around `_days_until_expiry` moved intact into `_summarize_inventory_health`, so the deliberate AC6 asymmetry against `calculate_restock_needs` still holds. Suite **79 OK**; seed-run summary output byte-for-byte unchanged.

---

## 2026-08-17 — Template 3: README

- **Task:** Add a README that explains how to navigate the codebase, what each file is, how the program works, what it reads, what it outputs, and how to read the final run.
- **Prompt:** Implement Task README: Add a README that explains how to navigate the codebase, what each file is, how the program works, what it reads, what it outputs, and how to read the final run. Use Python. Keep the code simple and add comments explaining each section. Do not implement any other tasks yet.
- **AI response:** Added `README.md` at the repo root. Sections: navigate the codebase (`seed_data.py` / `main.py` / tests first, then spec and writeup); file-by-file table including `docs/`; all-or-nothing order loop and restock rules; five seed tables as input; console print order (seed tables → processing → updated tables → manager summary); how to read the seed run (ignore seed Restock/Status; use orders 1–5, final inventory/restock/status, and the Kitchen Manager Summary). No simulation code changes.
- **Decision:** **Approved.**
- **Issues found:** None. `python3 main.py` and 79 tests were already green; this task is docs only.

---

## 2026-08-17 — Final review and acceptance

- **Task:** Record the Decision-Maker’s final review and acceptance of the submitted code.
- **Prompt:** Document my final review and acceptance of the code in the AI_USAGE_LOG, then push it to github one last time. Good job.
- **AI response:** Logged this closing decision. No simulation, test, or README changes in this step.
- **Decision:** **Approved.** I reviewed the code and accept it as the submission: `main.py`, `seed_data.py`, `test_main.py` (79 tests OK), `PROJECT_SPEC.MD`, `WRITTEN_RESPONSE.MD`, `AI_USAGE_LOG.MD`, and `README.md`. Extra credit not taken.
- **Issues found:** None blocking submit. Student self-check “I understand the code” remains a personal affirmation, not an AI decision.
