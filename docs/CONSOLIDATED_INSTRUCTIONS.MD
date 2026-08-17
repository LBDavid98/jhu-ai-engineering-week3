# Consolidated Instructions

AI-Assisted Cloud Kitchen Inventory Simulation

This document merges the two instruction sets (assignment brief + project plan) into one de-duplicated source of truth. Where the two sources disagree, the **base assignment** wins; extra plan details are marked as design notes or optional.

---

## 1. Purpose

Use AI as a coding assistant to build, test, debug, and refine a Python inventory simulation for a **cloud kitchen** (delivery-only; multiple virtual brands share one kitchen, staff, equipment, and ingredients).

The simulation models a **single operational day**. It must:

- Process customer orders
- Look up recipe-linked ingredients
- Check shared inventory (quantity + expiry)
- Update delivery status
- Deduct ingredient quantities
- Track expiry risk
- Produce a restock plan
- Produce a business-friendly summary

The assignment is not only working code. You must show that you can **guide AI, inspect its output, test it, debug it, and document decisions**.

### Why this problem matters

Cloud kitchens run on tight margins. After aggregator commissions (typically 20–30%), packaging, marketing, food cost, rent, labor, and utilities, contribution margins are often **5–15%**. Small operational misses hurt profit.

| Pain | Why it matters |
|------|----------------|
| Stockouts | Lost sales; orders accepted that cannot be fulfilled; worse platform ranking |
| Food waste | Poor kitchens throw away **8–15%** of food cost per month from expiry |
| Customer experience | Rejected orders, missing items, and partial deliveries hurt ratings → fewer orders |

### Operational problems to model

- Silent stockouts mid-shift → rejected orders
- Orders accepted for items the kitchen cannot fulfill
- No expiry tracking → waste and quality risk
- Inefficient restocking from poor usage visibility
- Manual menu/inventory updates → errors
- No prioritized, data-driven restock plan
- One missing ingredient can disable many items across brands

Every technical decision should trace back to reducing **stockouts, waste, or rejected orders**.

---

## 2. Learning objectives

By completing this assignment, you will be able to:

- Use AI tools to plan, implement, test, and debug a Python program
- Break a software problem into small implementation tasks
- Maintain a project specification file to reduce context drift
- Evaluate AI-generated code instead of accepting it uncritically
- Write and run unit tests for AI-generated functions
- Implement rule-based business logic in Python
- Explain the difference between AI-assisted coding and autonomous AI decision-making
- Reflect on the strengths and limitations of AI as a programming partner

---

## 3. Role of AI — you remain accountable

AI is a fast but unreliable junior developer: a probabilistic generator that predicts what looks plausible, not what is correct. It may misunderstand requirements, invent assumptions, duplicate logic, forget earlier instructions, or produce code that only appears correct.

You are **not** the typist. You play three roles:

| Role | What you do |
|------|-------------|
| **Navigator** | Define the goal, break work into tasks, decide what to ask AI |
| **Reviewer** | Inspect every AI output. Ask: does this do what I asked? Spot gaps, errors, drift |
| **Decision-Maker** | Accept, reject, revise, test, or refactor. Own final quality |

### You may use AI to

- Plan the project
- Break tasks into smaller steps
- Generate draft code
- Explain errors
- Suggest tests
- Suggest refactoring

### You may not

- Submit code you do not understand
- Submit AI-generated explanations you cannot explain
- Ignore failed tests
- Hide known defects
- Claim AI-generated work as fully your own without documenting your process

Grade is based on whether the program works **and** on responsible, critical, effective AI-assisted practice.

---

## 4. Files

### Provided by instructor

- `AI-Assisted Cloud Kitchen Inventory Simulation.pdf`
- `seed_data.py` (received as `seed_data-1.py`)
- `main.py`
- `test_main.py`

### Required in the repo / submission

| File | Purpose |
|------|---------|
| `main.py` | Main simulation logic |
| `seed_data.py` | Starting data: recipes, inventory, orders, restock, status |
| `test_main.py` | Unit tests |
| `PROJECT_SPEC.md` | External memory for you and the AI (update throughout) |
| `AI_USAGE_LOG.md` | How you used AI (see §12) |
| Written reflection | 400–600 words (Task 11) |

You may add extra files if useful. Do **not** submit credentials, API keys, or unrelated personal information.

### Deliverables to submit

- `main.py`
- `test_main.py`
- `PROJECT_SPEC.md`
- `AI_USAGE_LOG.md`
- Written reflection
- Optional: extra output files or reports

(`seed_data.py` is used by the program; keep it in the project even if the submit list names the files above.)

---

## 5. Data model

Inspect and use the **provided** structures. Do not assume a different schema.

Five core structures in `seed_data.py`:

| Structure | Role | Seed-file shape (as described in the project plan) |
|-----------|------|-----------------------------------------------------|
| **Recipes** | Menu item → ingredients + quantities (grams) | 5 items: Margherita Pizza, Chicken Burger, Caesar Salad, Pasta Alfredo, Chocolate Cake |
| **Inventory** | Shared stock + expiry | 14 ingredients with current stock and expiry dates |
| **Orders** | Incoming orders | 5 orders across 2 brands (Taco Bell, Subway) |
| **Restock** | Flagged ingredients + reason | 5 flagged ingredients with reason |
| **Status** | Delivery status per order | One status record per order |

Key field types called out for tests: `qty_grams` is a number; `expiry_date` is a string. Confirm against the actual file.

**Centralized inventory:** all brands consume from one shared inventory.

---

## 6. Business rules

These are the rules the code must follow. Constants (not magic numbers) for thresholds.

### Fulfillment (base assignment)

- **All-or-nothing** unless the instructor says otherwise.
- If **all** required ingredients are available (enough quantity, not expired/unusable):
  - Mark the order **Delivered**
  - Deduct used ingredient quantities from inventory
- If anything is missing, insufficient, or unusable:
  - Mark the order **Not Delivered**
  - Record the reason
  - Add missing/unavailable ingredients to the restock list (avoid silent duplicates if already present)
  - **Do not** deduct partial inventory on failed orders

Partial fulfillment is an **optional enhancement**, not the base.

### Quantity scaling

If an order line has quantity 2, required ingredient grams are doubled. Scale linearly with quantity.

### Missing recipes

Handle missing or unknown recipes gracefully (do not crash). Surface a clear failure reason.

### Cumulative inventory

Deduction is sequential. Do not reset inventory between orders except in isolated test cases.

1. Order 1 consumes inventory (if delivered)
2. Order 2 checks stock **remaining after** Order 1
3. Order 3 checks stock remaining after Orders 1 and 2
4. Final inventory reflects **all delivered** orders
5. Update the displayed final inventory table after **all** orders have been processed

If two orders compete for the same ingredient, the earlier delivered order wins the stock.

### Restock and expiry (apply after orders are processed)

Flag an ingredient if **any** of these hold. Preserve **all** reasons; do not overwrite.

| Condition | Default rule | Restock quantity |
|-----------|--------------|------------------|
| Out of stock | quantity = 0 | 10,000g (par) |
| Running low | quantity ≤ 1,000g | amount needed to reach 10,000g (e.g. 500g remaining → 9,500g) |
| Expiring soon | within 5 days of the simulation date | 10,000g |

Restock output must include:

- Ingredient name
- Current quantity
- Reason(s) for restock
- Quantity needed to reach par
- Relevant expiry information

Verify how “today” / simulation date is obtained. Do not silently assume system `today()` is correct for the seed data.

### Design notes from the project plan (not extra base requirements)

- **Separated workflows:** order processing only consumes inventory; replenishment is a distinct phase.
- **Periodic replenishment:** the plan describes restocking every N orders. The graded base requirement is restock logic on **final** inventory after processing. Configurable checkpoints are a design principle / possible extension, not a substitute for the base restock rules.
- Recipe-driven deduction: inventory updates from recipes × order quantities.

---

## 7. Functional requirements

Implement all of the following.

### R1 — Load and display data

Functions that import and show Recipes, Inventory, Orders, Restock, and Status. Confirms the program can access all required data.

### R2 — Process orders against recipes

For each order:

1. Identify menu item(s) ordered
2. Look up the recipe
3. Calculate total ingredient quantity required (scale by line quantity)
4. Handle missing/unknown recipes gracefully

### R3 — Check inventory availability

Before fulfilling, compare required ingredients to stock. Account for:

- Ingredient name
- Quantity required vs available
- Expiry / unusable status if dates exist

Return clear information: can the order be fulfilled, and if not, what is missing or unavailable.

### R4 — Fulfill orders and deduct inventory

Apply the fulfillment rules in §6. Define clearly that failed orders do not deduct inventory (all-or-nothing).

### R5 — Cumulative inventory deduction

Each order uses inventory remaining after previous **delivered** orders. See §6.

### R6 — Restock and expiry rules

After processing orders, apply the restock rules in §6 (out of stock, running low, expiring soon, multiple reasons).

### R7 — Business-friendly summary

End-of-run summary a non-technical kitchen manager can understand:

- Number (or list) of orders delivered
- Number (or list) of orders not delivered
- Reasons for non-delivery
- Final inventory levels
- Restock recommendations
- Ingredients that are low, out of stock, expired, or expiring soon

Output may be console, a dictionary, or a text/Markdown file.

---

## 8. Required tasks

Do **one task at a time**. Do not ask AI to build the entire project in one prompt.

**Numbering warning:** the assignment brief (Part I) uses Tasks 1–11 below. The project plan (Part II) numbers implementation steps differently (its “Task 4” is cumulative deduction = **assignment Task 7**). Use **this table** as the canonical task numbers.

| Task | Maps to | What to build |
|------|---------|----------------|
| 1 | Setup | Organize files; import test `main.py` ↔ `seed_data.py` |
| 2 | Spec | Create `PROJECT_SPEC.md` and keep it updated |
| 3 | R1 | Load/print/return the five data structures |
| 4 | R2 | Recipe lookup |
| 5 | R3 | Inventory availability check |
| 6 | R4 | Fulfill one order (status + deduct or fail + restock) |
| 7 | R5 | Process all orders in sequence (cumulative) |
| 8 | R6 | Restock + expiry recommendations |
| 9 | R7 | Final business summary |
| 10 | Quality | Refactor and review |
| 11 | Process | Written reflection (400–600 words) |

### Task 1 — Set up the project

Create or organize: `main.py`, `seed_data.py`, `test_main.py`, `PROJECT_SPEC.md`, `AI_USAGE_LOG.md`.

Run a simple import test so `main.py` can access `seed_data.py`.

In the written response, explain: project organization, how to run the program, how to run tests, any setup issues.

### Task 2 — Create PROJECT_SPEC.md

Document current understanding. Include:

- Project purpose
- Data structures
- Business rules
- Implementation plan
- Testing plan
- Open questions or assumptions

Also keep (see §11): component status, decisions made, constraints, current/next task, known issues. Update after every session.

### Task 3 — Load and inspect seed data

Show access to Recipes, Inventory, Orders, Restock, Status.

**Tests:** all five structures present; expected types; each contains records; key fields present. Plan also asks: correct record counts; `qty_grams` numeric; `expiry_date` string.

### Task 4 — Recipe lookup

Accept an item name or order line. Return required ingredients and quantities. Handle missing recipes gracefully.

**Tests:** valid item with matching recipe; invalid item with no recipe; quantity greater than 1 (grams scaled).

### Task 5 — Inventory availability check

Compare required ingredients to stock. Identify missing, insufficient, and expired/unusable ingredients.

**Tests:** all available; one missing; one insufficient; one expired/invalid if applicable.

### Task 6 — Fulfillment logic

Process one order per §6.

**Tests:** successful delivery; failed delivery due to missing stock (reason + restock); correct deduction after delivery; **no** deduction after failed delivery.

Also think through: same ingredient missing on two consecutive failed orders (restock list should not silently break).

### Task 7 — Cumulative order processing

Process all orders in sequence. Each uses inventory remaining after previous delivered orders.

**Tests:** two orders consuming the same ingredient; an order that fails because an earlier order used remaining stock; final inventory matches expected values.

Clarify in code/comments whether the working inventory is a **deep copy** or a shared reference.

### Task 8 — Restock and expiry rules

Account for out-of-stock, low-stock, expiring soon, and multiple reasons on one ingredient.

**Tests:** zero stock; at or below 1,000g; above threshold (not flagged for low stock); expiring soon; multiple reasons. Plan example: 500g remaining → “Running low”, 9,500g needed; adequate stock and no expiry → not flagged.

### Task 9 — Final business summary

Include delivered / not delivered, reasons, final inventory, restock recommendations, expiry concerns. Console, dict, or Markdown/text file.

### Task 10 — Refactor and review

Review for: duplicate logic; hard-coded values that should be constants; unclear names; missing comments; weak error handling; functions that do too much.

Use AI to **suggest**; you decide what to change. Document **at least two** improvements.

After every 3–4 tasks, run a duplication check (especially inventory lookup, availability, restock flagging). Do not change function signatures in that pass unless you choose to later.

### Task 11 — Reflection (400–600 words)

Answer all of:

- How did AI help you move faster?
- Where did AI make mistakes or questionable assumptions?
- How did testing help you evaluate AI-generated code?
- What did you change or reject from the AI’s suggestions?
- How did `PROJECT_SPEC.md` help maintain context?
- What would you do differently in a future AI-assisted coding project?

---

## 9. Development workflow

Use incremental AI-assisted development. **Build → Test → Inspect → Refine.** Never bundle the whole project into one prompt.

For each major task:

1. Ask AI for a plan or task breakdown (Templates 1–2)
2. Ask AI to implement **only one** small task (Template 3)
3. Request **validation hooks** (assumptions, uncertainty, incomplete sections)
4. Review the generated code (5-point checklist below)
5. Write or generate unit tests (`unittest`) **immediately after** the function
6. Run the tests
7. Debug failures with Template 4 **before** moving on; re-run **all** tests, not only the failing one
8. Update `PROJECT_SPEC.md`

### Why this workflow (from the project plan)

- Speeds first implementation from data model to runnable logic
- Makes rule changes easier to refactor
- Supports “what if” via prompt iteration
- Keeps logic changes separate from output-format changes
- Small tasks → small errors → faster debugging

### 5-point code review — every AI-generated function

1. Does it do what I asked? Run it with 3 different inputs you can verify manually.
2. Are there hidden assumptions? Look for hard-coded values, assumed data types, or logic paths you didn’t specify.
3. Is anything hard-coded that should be a variable? (e.g. restock thresholds, par levels, expiry windows).
4. Does it handle bad inputs? What happens with None values, empty lists, or negative quantities?
5. Is any part of it security-sensitive or business-critical? (e.g. financial deductions, expiry logic).

### Debugging loop (never skip a failure)

1. Read the error message carefully — before anything else
2. Understand it — what line, what type, what variable?
3. Use Template 4 — paste **function code** and the **full** error
4. Ask AI to explain the **root cause**, not just a patch
5. Apply the fix and re-run **all** tests
6. If still failing, paste the new error and repeat

---

## 10. Prompt templates

Use Templates 1 and 2 before writing code for a project or major component. Template 3 is one task per prompt. Template 4 on every failure. Validation hook after every implementation.

**Order of use**

1. Template 1 — once, at the very start, before any code
2. Template 2 — once per component, after the plan is confirmed
3. Template 3 — every individual task, one at a time
4. Validation hook — after AI generates code
5. Tests — immediately after each function
6. Template 4 — whenever a test fails or output is unexpected

### Template 1 — Planning

**When:** Start of a new project or major component, before code.

```text
I want to build [PROJECT / COMPONENT OR FEATURE]. Before writing any code, give me a high-level plan — what components do I need and what should I build first?
```

### Template 2 — Task breakdown

**When:** Once per component, after Template 1 is confirmed.

```text
Here is component [NAME] from our plan. Break it into individual implementation tasks. Keep each task small enough to implement in a single prompt.
```

### Template 3 — Implementation

**When:** One task per prompt. Never bundle tasks.

```text
Implement Task [N]: [DESCRIPTION]. Use Python. Keep the code simple and add comments explaining each section. Do not implement any other tasks yet.
```

### Validation hook

**When:** After every implementation prompt.

```text
After generating the code, add inline comments or notes that identify:
1. Any assumptions you made that I should verify
2. Any parts you are uncertain about
3. Any sections that are incomplete or require follow-up
```

Specialize the three bullets per step when useful (recipe lookup, partial stock, deep copy vs reference, simulation date, multi-reason flags, etc.).

### Template 4 — Debugging

**When:** Every test failure or unexpected output. Never skip and move on.

```text
Here is the code and the error it produces: [PASTE FUNCTION CODE] / [PASTE FULL ERROR MESSAGE]. Explain what is wrong and why. Then provide a corrected version with comments explaining what was changed and why.
```

### Test generation (after each function)

```text
Write unit tests for [FUNCTION] using Python unittest. Cover: [success case], [failure/edge cases listed for that task].
```

### Duplication / refactoring (after every 3–4 tasks)

```text
Review the code in main.py for duplicated logic or functions — particularly any inventory lookup, availability check, or restock flagging logic that appears more than once. Suggest how to refactor it to eliminate duplication while keeping the behaviour identical. Do not change any function signatures yet.
```

---

## 11. PROJECT_SPEC.md — external memory

AI has no reliable memory across sessions; within a session, early instructions fade. `PROJECT_SPEC.md` is the single source of truth. Paste the relevant section at the start of each new session.

### Must include

- What you are building and why
- Key components and current status
- Decisions already made (e.g. restock threshold = 1,000g, par = 10,000g, all-or-nothing fulfillment)
- Constraints and rules the AI must follow
- Current task and next task
- Data structures, business rules, implementation plan, testing plan
- Open questions, known issues, assumptions

### Session re-anchor (adapt the completed/current task)

```text
Here is our project context. We are building a Python-based cloud kitchen inventory simulation using seed_data.py (Recipes, Inventory, Orders, Restock, Status). We have completed [TASKS]. [CURRENT TASK] is the current task. Do not modify any previously implemented functions.
```

### When to update

After **every** session: mark completed tasks, record new decisions, add constraints that emerged.

---

## 12. AI_USAGE_LOG.md

For each **major** interaction (not every tiny prompt), record:

- The task you were working on
- The prompt you gave the AI
- A short summary of the AI’s response
- What you accepted, changed, or rejected
- Any issues you found in the AI output

Enough evidence to show thoughtful, critical use.

---

## 13. Recommended implementation prompts (project plan)

These are the plan’s concrete Template 3 prompts. They **bundle** some assignment tasks (e.g. Step 2 mixes lookup + availability). Prefer **assignment Tasks 4 then 5** as separate prompts if you want stricter incrementality; use these when you want the plan’s wording.

**Step 1 — Data connectivity (Tasks 1 & 3)**

```text
Implement Task 1: Create a baseline main.py file that imports all data from seed_data.py. Write specific functions to load and print the contents of every data table—including Recipes, Inventory, Orders, Restock, and Status—to the console. Add comments explaining each function. Do not implement any other tasks yet.
```

**Step 2 — Order-to-recipe (+ availability) (Tasks 4–5)**

```text
Implement Task 2: Update main.py to process orders from the Orders table. For each order, the system should: 1. Look up the recipe for each item. 2. Calculate the total grams of ingredients required. 3. Check the Inventory table to see if all required ingredients are present in the necessary quantities. Add comments explaining each step. Do not implement any other tasks yet.
```

Validation extras: assumptions about recipe lookup; missing recipe behavior; incomplete sections.

**Step 3 — Fulfillment (Task 6)**

```text
Implement Task 3: Add fulfillment logic. If all ingredients are available, mark the order as 'Delivered' in the status table and deduct the used grams from the inventory. If ingredients are missing, mark the order as 'Not Delivered,' record the reason, and add the missing items to the Restock table. Add comments. Do not implement any other tasks yet.
```

Validation extras: same ingredient missing on two consecutive orders; whether partial stock can be deducted; incomplete sections.

**Step 4 — Cumulative deduction (Task 7)**

```text
Implement Task 4: Refine the inventory logic to be cumulative. Order 2 must check availability against the quantity remaining after Order 1 was served. Update the final inventory table only after all orders in the list have been processed to show the true remaining stock. Add comments. Do not implement any other tasks yet.
```

Validation extras: deep copy vs reference; two orders competing for the same ingredient; incomplete sections.

**Step 5 — Restock and expiry (Task 8)**

```text
Implement Task 5: Update the restock logic with these specific rules: 1. If an ingredient is within 5 days of expiry (relative to today’s date), mark it as 'Expiring soon' and set the restock quantity to 10,000g. 2. If the final stock is 0, mark as 'Out of stock' (10,000g needed). 3. If stock is ≤ 1,000g, mark as 'Running low on stock' and calculate the needed amount to reach 10,000g. Add comments. Do not implement anything beyond this task.
```

Validation extras: how today’s date is obtained; whether an ingredient can be flagged for both low stock and expiry; incomplete sections.

Then: Task 9 summary, Task 10 refactor, Task 11 reflection.

---

## 14. Testing requirements (minimum)

Use Python `unittest` in `test_main.py`. Tests must be runnable; results visible or documented.

Cover major functions with **normal, edge, and failure** cases, including:

- Data load: five tables, types, record counts, key fields
- Recipe lookup: hit, miss, quantity > 1
- Availability: all ok; missing; insufficient; expired if applicable
- Fulfillment: delivered + deduction; not delivered + reason + restock; no deduction on failure
- Cumulative: shared ingredient across two orders; later order fails from earlier consumption; final inventory
- Restock: zero; ≤ 1,000g; above threshold; expiring soon; multiple reasons; not flagged when healthy

---

## 15. Optional enhancements (extra credit)

Choose **one** if going beyond the base. Must be working, tested, and documented. Apply the full playbook: Plan → breakdown → implement one task → validation hooks → test → debug → refactor. Do not skip planning.

| Option | What to build |
|--------|----------------|
| **A. Partial fulfillment** | If a subset of items can be filled, deliver those; mark only unavailable items as not delivered |
| **B. Predictive stockout alerts** | From observed consumption, forecast which ingredients will run out in the next batch of orders |
| **C. Dynamic menu disabling** | Mark menu items unavailable when a required ingredient is out of stock or unusable |
| **D. Improved reporting** | Polished report in Markdown, CSV, or HTML |

Starting planning prompt pattern:

```text
I want to add [ENHANCEMENT] to the cloud kitchen simulation. Before writing any code, give me a plan — what components need to change and what should I build first?
```

---

## 16. Written response structure

Use these headings:

1. Project Setup
2. Data Loading
3. Recipe Lookup
4. Inventory Availability
5. Order Fulfillment
6. Cumulative Processing
7. Restock and Expiry Logic
8. Business Summary
9. Refactoring Notes
10. AI Usage Summary
11. Reflection

---

## 17. Minimum technical requirements

- Working Python code
- Use of the provided seed data
- Functions for: data loading, recipe lookup, inventory checking, order fulfillment, cumulative processing, restock logic, final reporting
- Unit tests for major functions
- Evidence that tests were run
- Maintained `PROJECT_SPEC.md`
- `AI_USAGE_LOG.md`
- Written reflection on AI-assisted coding

---

## 18. Grading rubric (100 points)

| # | Area | Points | Full credit means |
|---|------|--------|-------------------|
| 1 | Project setup and data loading | 10 | Clear structure; successful import of `seed_data.py`; functions access all five structures |
| 2 | Recipe lookup and ingredient calculation | 10 | Correct lookup, quantity scaling, graceful missing recipes |
| 3 | Inventory availability logic | 10 | Accurate required vs available, including missing/insufficient |
| 4 | Fulfillment and status updates | 15 | Correct status; deduct on deliver; no unintended deduct on fail; meaningful reasons |
| 5 | Cumulative inventory processing | 10 | Later orders use remaining stock |
| 6 | Restock and expiry logic | 10 | Low stock, out of stock, expiring soon, multiple reasons |
| 7 | Unit testing | 15 | Meaningful tests (normal, edge, failure); runnable; results visible or documented |
| 8 | AI-assisted development process | 10 | Useful spec; meaningful AI log; prompt-based iteration; reviewed rather than blindly accepted |
| 9 | Code quality and refactoring | 5 | Readable; clear names; constants for thresholds; useful comments; less duplication |
| 10 | Reflection | 5 | Thoughtful on benefits, risks, and limits of AI-assisted coding |

---

## 19. Final checklist before submission

- [ ] `main.py` runs
- [ ] `test_main.py` runs
- [ ] Program uses `seed_data.py`
- [ ] Final inventory is cumulative
- [ ] Restock logic handles low stock and expiry (and multiple reasons)
- [ ] Failed orders include reasons
- [ ] Tests cover success and failure cases
- [ ] `PROJECT_SPEC.md` is complete and updated
- [ ] `AI_USAGE_LOG.md` documents the AI-assisted process
- [ ] Reflection answers all required questions
- [ ] You understand the code you are submitting
- [ ] No private credentials or API keys in the submission

---

## 20. Practical path (short)

1. Import and print all five data structures
2. For each order, look up recipe and total grams required
3. Check availability; Delivered + deduct, or Not Delivered + reason + restock
4. Make deduction cumulative
5. Show final inventory only after all orders
6. Apply restock rules to final inventory
7. Unit tests after every function
8. Template 4 on every failure (root cause, not just a patch)
9. Validation hooks after every implementation
10. Duplication check every 3–4 tasks
11. Maintain `PROJECT_SPEC.md` and re-anchor each session
12. Refine output to a business-friendly report

---

## 21. Key takeaways

1. **Business pain:** inventory risk and delivery reliability. Tech choices should reduce stockouts, waste, or rejected orders.
2. **Technical problem:** order → inventory → restock must be cumulative, expiry-aware, and threshold-triggered. Each piece is one testable task.
3. **Implementation strategy:** incremental AI prompts; tests after every function; validation hooks after every prompt; debugging loop when things break; spec file to prevent drift.

This is structured problem-solving with AI aligned to business outcomes — not just writing code with AI.
