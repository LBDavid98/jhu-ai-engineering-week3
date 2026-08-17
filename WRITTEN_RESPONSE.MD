# Written Response

AI-Assisted Cloud Kitchen Inventory Simulation. Facts from `PROJECT_SPEC.MD`. Assignment numbering is Tasks 1–11.

Project Setup -> AI Usage Summary AI Generated and reviewed by me. Personal reflection is from me, David Hook. 

**Before submit (my checklist):**
- [x] Run `python main.py` and confirm seed tables print first, then processing, then updates and the manager summary. *(SP3 done 2026-08-12 — exit 0; order confirmed below)*
- [x] Run `python -m unittest -v`. *(re-run 2026-08-16 — Ran 79 tests, OK)*
- [x] Confirm setup: instructor file was `seed_data-1.py`, renamed to `seed_data.py`.
- [x] Extra credit: not taken.

---

## Project Setup

- Files in the repo: `main.py` (simulation), `seed_data.py` (five tables), `test_main.py` (unittest), `PROJECT_SPEC.MD` (living spec / Task 2), `AI_USAGE_LOG.MD` (process log).
- Simulation logic stays in `main.py`. Seed schema was not replaced.
- Import: `from seed_data import inventory, orders, recipes, restock, status`.
- Setup issue: the instructor file was `seed_data-1.py`; it was renamed to `seed_data.py` so the import works (DC1).
- How to run the program: `python main.py`.
- **SP3 run evidence (2026-08-12):** `python main.py` exit 0. Print order confirmed: five **seed** tables first (`Recipes` → `Inventory` → `Orders` → `Restock` → `Status`), then `Order Processing`, then updated `Inventory` / `Restock` / `Status`, then `Kitchen Manager Summary`.
- How to run tests: `python -m unittest -v`.
- **Test evidence (re-run 2026-08-16):** `python -m unittest -v` → **Ran 79 tests — OK** (exit 0). No failures or errors. *(Earlier checkpoints: 49 at SP4 on 2026-08-12, 75 after the AC closeout on 2026-08-14; the suite grew as tasks added coverage, and RX1 added the last two.)*
- `main()` order (approved and confirmed): print all five **seed** tables first, then `process_orders`, then updated inventory / restock / status, then the manager summary.
- Simulation date is explicit: `SIMULATION_DATE = date(2026, 5, 10)`. Production does not use `date.today()` (on 2026-08-11 that would already mark several seed items past expiry).
- First Template 1 plan (five coarse components, chat only) was **rejected**. The granular plan now lives in `PROJECT_SPEC.MD`.

## Data Loading

- Loaders: `load_recipes`, `load_inventory`, `load_orders`, `load_restock`, `load_status`.
- Printers for each table. Seed Restock is printed before processing (DC7); live restock is rebuilt after orders.
- Five seed structures: Recipes (5), Inventory (14), Orders (5), Restock (5 seed rows), Status (5).
- Key fields: `qty_grams` is numeric; `expiry_date` is a string `YYYY-MM-DD`.
- Tests cover presence, types, record counts, and key fields.
- Live restock table is replaced each run; seed restock rows are not kept as history.

## Recipe Lookup

- `find_recipe_by_name`: exact `Orders.item` ↔ `Recipes.name`. No aliases or case folding.
- Miss returns `None`; the program does not crash.
- Missing recipe: record a clear reason, skip that item’s demand, do not invent ingredients.
- `calculate_ingredient_requirements`: line qty 2 doubles every ingredient gram (linear scale).
- `combine_requirements`: shared ingredients across items in one order become one gram total.
- Tests: hit, miss, quantity 2.

## Inventory Availability

- `check_inventory_availability` checks name, grams, and expiry.
- Past expiry (`days < 0`) blocks fulfillment. Expiring soon does **not**; that is restock-only.
- Details include missing, insufficient, expired, unusable (bad date), invalid (negative / non-numeric demand).
- Default `reference_date` is `SIMULATION_DATE` (2026-05-10), not `date.today()`.
- Bad inputs: `None` inventory or requirements treated as empty; empty requirements succeed; negatives do not crash (`status: invalid`).
- Tests: all ok; missing; insufficient; expired; expiring soon does not block; bad inputs.

## Order Fulfillment

- All-or-nothing. Partial fulfillment is extra credit only and was not implemented.
- All required ingredients available (enough grams, not expired/unusable) → Delivered; deduct used grams; status remark “Delivered”.
- Otherwise → Not Delivered; record the reason; **no** inventory deduction (including expiry fail).
- Failed-order missing/unavailable items go on restock after a final-inventory rebuild, without silent duplicates (OP15).
- `update_status_entry` may append a row if `order_id` is new.
- Known limitation: none for expired fail-reason wording — **SP7** names Expired / Unusable clearly; shortage label kept for missing/insufficient. Deduction unchanged.

## Cumulative Processing

- `process_orders` uses a `deepcopy` working inventory during the run.
- Live inventory is updated only after **all** orders (`apply_final_inventory_snapshot`).
- Later orders see stock remaining after earlier **delivered** orders.
- If two orders compete for the same ingredient, the earlier delivered order wins.
- Tests: two orders sharing an ingredient; later order fails because an earlier order used remaining stock; final inventory matches expected remaining quantities.

## Restock and Expiry Logic

- Applied to **final** inventory after all orders (`refresh_restock_table`: clear + extend). Restock-every-N is not the base rule.
- Named constants: `RUNNING_LOW_THRESHOLD_GRAMS = 1000`, `PAR_LEVEL_GRAMS = 10000`, `EXPIRING_SOON_DAYS = 5`.
- Independent `if` checks (not `elif`): an ingredient can carry more than one reason.
- Qty 0 → “Out of stock”, 10,000g. Running low is `0 < qty ≤ 1,000g` only (qty 0 is not also running low).
- Running low → grams needed to reach par (e.g. 500g → 9,500g; exactly 1,000g → 9,000g). 1,001g is not flagged for low stock.
- Expiring soon (`0 ≤ days ≤ 5`) → 10,000g.
- Expired (`days < 0`) → 10,000g. Part I lists "expired **or** expiring soon" as restock conditions, so already-expired stock is flagged by the rule engine rather than only when an order happens to fail on it. Full par, not a top-up, because expired grams cannot be used and must be replaced (RX1).
- When multiple rules match, `qty_needed_grams` is the max of those rules.
- Each row: item, `current_qty_grams`, reason string plus `reasons` list, qty needed, `expiry_date`.
- Healthy stock (above 1,000g, not expiring soon) is not flagged.
- OP15 then adds failed-order missing/unusable names that the rebuild missed, skipping names already on the table.
- Tests: zero; 500g; ≤1,000g; above threshold; expiring soon; expired; expired + out of stock together; multiple reasons; healthy not flagged; default date 2026-05-10.

## Business Summary

- `build_manager_summary` is for a non-technical kitchen manager.
- Reports delivered count, not-delivered count, lists, and reasons for non-delivery.
- Also: final inventory, restock recommendations, low / out of stock / expired / expiring soon.
- Output form (approved): console print of `summary["text"]` from `main()`, and `main()` returns the dict. No Markdown file (that would overlap extra-credit reporting).
- Tests: counts match processed orders; failed orders appear with reasons; restock included; dict plus readable `text`.

## Refactoring Notes

- Task 10 required AI to **suggest** and the student to choose. RF1 (duplication) and RF4 (quality sweep) were suggest-only; signatures were not changed in those passes.
- **Improvement 1 (RF2):** `_inventory_by_name` — one ingredient-name lookup dict used by `check_inventory_availability`, `deduct_inventory`, and `add_failed_order_items_to_restock`. Public signatures unchanged. `apply_final_inventory_snapshot` still uses a qty-only map (different shape).
- **Improvement 2 (RF3):** `_days_until_expiry` — one expiry-day calculation used by availability, `calculate_restock_needs`, and `build_manager_summary`. Restock still raises on a bad date; availability and the summary still catch. Public signatures unchanged.
- **Improvement 3 (RF5):** `process_orders` went from 127 lines to 32 by extracting `_resolve_order_lines` (per-item recipe lookup and scaling), `_decide_order_outcome` (a pure function returning fulfilled + reason), and `_process_single_order` (the one place that deducts inventory and writes status). Making the decision pure means the all-or-nothing rule cannot be broken by a change to the decision branch — that function holds no reference to inventory.
- **Improvement 4 (RF6):** `build_manager_summary` went from 162 lines to 54 by extracting `_split_orders_by_delivery`, `_summarize_inventory_health`, and `_render_manager_summary_text`. Report wording can now change without touching expiry logic.
- Thresholds were already named constants (RS1) before these refactors.
- Rejected as this pair: collapsing `load_*`/`print_*`; making restock swallow bad dates (behavior change); renaming public functions; extra credit.
- **Error handling / quality (Task 10):** Quiet failures and the intentional restock raise-vs-catch asymmetry are inventoried in `PROJECT_SPEC.MD` §9 **Error-handling map** (at-a-glance table + details). No public signature changes for that map.

## AI Usage Summary

- I used AI as a draft assistant, not as the final authority. I reviewed, tested, and decided what to keep.
- Workflow followed the course idea of plan → small implement → test → fix before moving on.
- I rejected the first high-level plan as too coarse, then accepted a granular plan that later lived in `PROJECT_SPEC.MD`.
- I preferred inspecting existing lookup/fulfillment over rewriting it.
- I did not take extra credit; I did not use restock-every-N or partial fulfillment as substitutes for the base rules.
- Evidence: `PROJECT_SPEC.MD` (decisions, punch list, gaps) and `AI_USAGE_LOG.MD` (major prompts, responses, accept/reject, issues).

## Reflection

AI sped up planning and execution. Once I had a clear slice—loaders, expiry in availability, multi-reason restock, the manager summary—I could ask for a small Python change with comments and a matching unittest case, and the rounds were quick instead of long thinking sessions. The same pattern helped with task breakdowns: the AI drafted lists so I could keep each change small. Drafting the written-response skeleton beat starting from a blank page, as long as I treated the draft as notes to edit.

AI also made mistakes and questionable assumptions. The first high-level plan was five coarse components with no tests, no must/must-not rules, and no map of what already worked versus what was missing; I rejected it and required a granular plan written in the repo for review. Early restock logic used if/elif, so an ingredient could not keep both “running low” and “expiring soon”. Restock also defaulted toward date.today(), which did not match this seed set, whose expiries sit in 2026 while the calendar can already be past several of them.

Testing was how I decided whether generated code was real or only plausible. After each major function I ran unit tests and expanded cases and the summary. Tests at exactly 1,000g and 1,001g checked the threshold edge, and re-running the suite after expiry entered availability confirmed inventory was not deducted on failure. I also ran de-duplication and integration passes rather than trusting that separately-prompted functions would fit together; those passes produced the shared inventory lookup, the shared expiry helper, and the shared restock row builder.

I used Template 4 when tests failed, but not as cleanly as the course describes, and that is the process lesson I am taking away. The agents usually noticed a failing unit test and began debugging on their own before I could paste the code and the full error into the debugging prompt, so the fix often arrived before the root-cause explanation which was backwards from the intent of the template, since the explanation is the part that makes the code fix durable. 

I changed or rejected several AI suggestions on purpose. I rejected the first Template 1 plan, and I did not rewrite working recipe lookup and fulfillment just because a breakdown listed them. For refactoring the AI offered several options; I accepted two small internals—a shared inventory name lookup and a shared days-until-expiry helper—and kept public signatures unchanged.

PROJECT_SPEC.MD was the external memory that kept the project from drifting. Splitting requirements across a plan file and the spec caused confusion, so I merged the plan into the spec and one document held status, decisions, punch list, and sequence. When the AI forgot an earlier decision—simulation date, past expiry versus expiring soon, rebuild-plus-failed-order restock—I pointed it at the written decision instead of re-arguing it.

I had planned to test my own harness on this project after watching the week 3 videos, but reading the instructions I decided that would be both a poor reflection of the task and a missed learning opportunity, so I worked inside VS Code where diffs and in-IDE approvals make inspection quick. I still experimented a little bit, including adding context to planning prompts in the IDE.  Next time I would do more experimentation with hooks, rules, and subagents, starting with a hook that stops an agent at a failing test instead of letting it debug unprompted, which is the one habit that most weakened my process this week. 
