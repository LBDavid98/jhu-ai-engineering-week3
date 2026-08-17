# Prompt Templates

## Order of Use

1. **Template 1** — once, at the very start, before any code.
2. **Template 2** — once per component, after the plan is confirmed.
3. **Template 3** — for every individual task, one at a time.
4. **Template 4** — whenever a test fails or an error appears.

---

## Template 1 — Planning Prompt

**When to use:** At the very start of every new project or major component, before any code is written.

**What it does:** Gets AI thinking in components, not in code. Gives you a shared architecture to reference throughout.

**Template:**

```text
I want to build [PROJECT]. Before writing any code, give me a high-level plan — what components do I need and what should I build first?
```

---

## Template 2 — Task Breakdown Prompt

**When to use:** Run once per component, after the plan from Template 1 is confirmed.

**What it does:** Converts each component into individual, small, implementable tasks. Each task then becomes one Template 3 prompt. Small tasks = small errors = fast debugging.

**Template:**

```text
Here is component [NAME] from our plan. Break it into individual implementation tasks. Keep each task small enough to implement in a single prompt.
```

---

## Template 3 — Implementation Prompt

**When to use:** For every individual task, one at a time.

**What it does:** Keeps scope tight. The phrase “Do not implement any other tasks yet” prevents scope creep. Comments make the output readable and verifiable.

**Template:**

```text
Implement Task [N]: [DESCRIPTION]. Use Python. Keep the code simple and add comments explaining each section. Do not implement any other tasks yet.
```

---

## Template 4 — Debugging Prompt

**When to use:** Every time a test fails or code produces unexpected output. Never skip it and move on.

**What it does:** Forces AI to explain the root cause, not just patch the error. This builds your understanding of the code over time so you genuinely own it.

**Template:**

```text
Here is the code and the error it produces: [PASTE CODE] / [PASTE ERROR]. Explain what is wrong and provide a corrected version with comments.
```



## Additional Templates

Test Generation Prompt (immediately after Step 1 code): Write unit tests for the load functions using Python unittest. Cover: successful import of all 5 tables, correct count of records in each table, and correct data types for key fields (e.g. qty_grams is a number, expiry_date is a string).

Validation Hook Prompt: After generating the code, add inline comments that identify: (1) any assumptions you made that I should verify, (2) any parts you are uncertain about, and (3) any sections that are incomplete or require follow-up.
