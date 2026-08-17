# Cloud Kitchen Inventory Simulation

Python simulation of **one operational day** in a delivery-only cloud kitchen. Several virtual brands share one inventory. The program looks up recipes, checks stock and expiry, fulfills orders all-or-nothing, rebuilds a restock plan, and prints a manager summary.

Simulation date is **2026-05-10** (`SIMULATION_DATE` in `main.py`). It does not use today’s calendar date.

```bash
python3 main.py
python3 -m unittest -v
```

Requires Python 3. No extra packages.

---

## How to navigate the codebase

Start with the three files that actually run:

| Start here | Why |
|------------|-----|
| `seed_data.py` | The five tables the program reads |
| `main.py` | All simulation logic; `main()` is the run order |
| `test_main.py` | Unit tests for loaders, fulfillment, restock, and the summary |

Then, if you need assignment context rather than code:

| Then read | Why |
|-----------|-----|
| `PROJECT_SPEC.MD` | Decisions, punch list, business rules, error-handling map |
| `WRITTEN_RESPONSE.MD` | Task writeup and reflection |
| `AI_USAGE_LOG.MD` | Major AI prompts, responses, and approvals |
| `docs/` | Assignment instructions and prompt templates |

In `main.py`, follow this path:

1. Constants at the top (`SIMULATION_DATE`, par / low-stock / expiry window)
2. `load_*` / `print_*` — seed tables
3. `find_recipe_by_name` → `check_inventory_availability` → `process_orders`
4. `calculate_restock_needs` / `refresh_restock_table` / `add_failed_order_items_to_restock`
5. `build_manager_summary`
6. `main()` — print seed → process → print updates → print summary

Private helpers are prefixed with `_` (inventory lookup, expiry math, stock flags, order split). Public function names were kept stable for tests.

---

## What each file is

### Run these

| File | Role |
|------|------|
| `main.py` | Entire simulation: load, print, process orders, restock, manager summary |
| `seed_data.py` | Instructor seed tables (renamed from `seed_data-1.py`). Five lists: `recipes`, `inventory`, `orders`, `restock`, `status` |
| `test_main.py` | `unittest` suite (79 tests). Isolates mutable tables with `deepcopy` |

### Assignment writeup

| File | Role |
|------|------|
| `PROJECT_SPEC.MD` | Living spec (Task 2): rules, decisions, punch list, known issues |
| `WRITTEN_RESPONSE.MD` | Written response headings plus the 400–600 word reflection |
| `AI_USAGE_LOG.MD` | Major AI interactions: prompt, response, decision, issues |

### Supporting

| File | Role |
|------|------|
| `README.md` | This file |
| `.gitignore` | Ignores `__pycache__/`, `*.pyc`, `.DS_Store` |
| `AGENTS.MD` | Local agent notes for this repo (not a graded deliverable) |
| `docs/INSTRUCTIONS.MD` | Course brief (Part I graded assignment + Part II project plan) |
| `docs/CONSOLIDATED_INSTRUCTIONS.MD` | Merged standard; Part I wins conflicts |
| `docs/prompt_templates.md` | Templates 1–4 (plan, breakdown, implement, debug) |
| `docs/project_tasks.md` | Numbered task list from the plan |
| `docs/problem_statement.md` | Cloud-kitchen problem framing |
| `docs/business_context.md` | Margin / waste / stockout context |
| `docs/AI-Assisted Cloud Kitchen Inventory Simulation.pdf` | Original assignment PDF |

---

## How the program works

One shared inventory. Orders are processed **in list order**. Later orders see stock remaining after earlier **delivered** orders.

For each order:

1. **Look up** each line item by exact recipe name (`Orders.item` == `Recipes.name`). No aliases or case folding.
2. **Scale** ingredients by line quantity (qty 2 doubles every gram) and **combine** shared ingredients in the same order.
3. **Check availability** — enough grams **and** not past expiry (`days < 0` vs 2026-05-10). Expiring soon (within 5 days) does **not** block fulfillment; it only flags restock.
4. **All-or-nothing:** if every required ingredient is usable, mark **Delivered** and deduct grams. Otherwise mark **Not Delivered**, record a reason, deduct **nothing**.
5. After **all** orders: copy remaining grams onto the live inventory table, rebuild restock from final stock, then add failed-order missing/unusable items that the rebuild missed (no duplicate names).

Restock flags (any that apply; multiple reasons are kept):

| Condition | Qty needed |
|-----------|------------|
| Out of stock (0 g) | 10,000 g (par) |
| Running low (≤ 1,000 g) | grams to reach 10,000 |
| Expiring soon (within 5 days) | 10,000 g |
| Expired (already past date) | 10,000 g (replace, not top up) |

Healthy stock above 1,000 g and not expiring/expired is not flagged.

---

## What it reads

Nothing from disk except the Python modules. `main.py` imports five in-memory lists from `seed_data.py`:

| Table | Count | Fields |
|-------|-------|--------|
| **Recipes** | 5 items | `recipe_id`, `name`, `ingredients[{name, qty_grams}]` |
| **Inventory** | 14 ingredients | `ingredient`, `qty_grams`, `expiry_date` (`YYYY-MM-DD`) |
| **Orders** | 5 orders | `order_id`, `brand`, `items[{item, qty}]` |
| **Restock** | 5 seed rows | Baseline print only; **replaced** after processing |
| **Status** | 5 rows | `order_id`, `delivered`, `remark` — seed is initial; live rows update or append |

All quantities are grams, including buns. Brands in the seed are Taco Bell and Subway.

The first Restock and Status blocks you see are **seed baselines**, not the day’s result. Seed status even disagrees with the processed day (for example seed order 2 is “Not Delivered”; after processing it is delivered).

---

## What it outputs

Console only. No report file is written. `main()` also **returns** a summary dict (`summary["text"]` is what gets printed).

Print order:

1. `=== Recipes ===` — seed recipes
2. `=== Inventory ===` — seed stock (all 10,000 g in this seed)
3. `=== Orders ===` — the five incoming orders
4. `=== Restock ===` — **seed** restock (ignore for the day’s plan)
5. `=== Status ===` — **seed** status (ignore for the day’s results)
6. `=== Order Processing ===` — per-order lookup, scaled grams, availability, fulfilled/reason
7. `=== Inventory ===` — **final** grams after delivered orders
8. `=== Restock ===` — **live** plan (current qty, qty needed, reason(s), expiry)
9. `=== Status ===` — **live** delivered / remark per order
10. `=== Kitchen Manager Summary ===` — counts, reasons, final inventory, attention lists, restock

---

## How to read the final run

Run `python3 main.py` and treat the output as **before → during → after**.

### 1. Seed block (before)

Use Recipes, Inventory, and Orders to see demand vs starting stock. Skip seed Restock and seed Status; they are not the result of this run.

Starting inventory is 10,000 g per ingredient. Simulation date is 2026-05-10, so:

- **Already expired:** Fettuccine Pasta (2026-01-31), Chocolate (2026-01-15)
- **Expiring soon (within 5 days):** Flour, Romaine Lettuce, Sugar (all 2026-05-12)

### 2. Order Processing (during)

Read each `Order ID` for `Fulfilled` and `Reason`.

| Order | What was ordered | Result | Why |
|-------|------------------|--------|-----|
| 1 | 2× Margherita Pizza, 1× Caesar Salad | Delivered | Stock and dates OK |
| 2 | 1× Chicken Burger | Delivered | Stock and dates OK |
| 3 | Pasta Alfredo + Chocolate Cake | **Not Delivered** | Expired ingredients: Fettuccine Pasta, Chocolate. **No grams deducted** |
| 4 | 1× Margherita Pizza | Delivered | Sees stock left after order 1 |
| 5 | 45× Chicken Burger, 1× Caesar Salad | Delivered | Large burger batch; chicken falls to 800 g |

Order 3 is the important failure: both pasta and cake need expired ingredients, so the whole order is rejected. Cream, parmesan, flour, and sugar on that order are **not** used.

### 3. Updated tables (after)

**Inventory** — remaining grams. Delivered orders deducted; order 3 did not. Fettuccine and Chocolate stay at 10,000 g because they were never consumed.

**Restock** — the procurement plan. In the seed run you should see:

| Item | Why it is on the list |
|------|------------------------|
| Flour, Romaine Lettuce, Sugar | Expiring soon |
| Chicken Breast | Running low (800 g after order 5) → 9,200 g needed to reach par |
| Fettuccine Pasta, Chocolate | Expired (rule engine, not only because order 3 failed) |

**Status** — this is the day’s delivery board. Compare it to seed Status; they are not the same. Order 3’s remark names the expired ingredients.

### 4. Kitchen Manager Summary (the one-page read)

If you only read one section, read this.

- **Orders delivered / not delivered** — 4 delivered, 1 not (order 3)
- **Reasons for non-delivery** — expired pasta and chocolate
- **Final inventory** — same numbers as the second Inventory block
- **Ingredients that need attention** — low / out / expired / expiring soon
- **Restock recommendations** — same live restock table in shorter form

A successful run exits 0. Tests: `python3 -m unittest -v` should report **Ran 79 tests — OK**.
