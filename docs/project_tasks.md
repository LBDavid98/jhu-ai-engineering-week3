# Required Tasks

## Task 1: Set Up the Project

Create or organize the following files:

- `main.py`
- `seed_data.py`
- `test_main.py`
- `PROJECT_SPEC.md`
- `AI_USAGE_LOG.md`

Run a simple import test to confirm that `main.py` can access data from `seed_data.py`.

In your written response, explain:

- How your project is organized
- How to run your program
- How to run your tests
- Any setup issues you encountered

---

## Task 2: Create PROJECT_SPEC.md

Create a project specification file that documents your current understanding of the project.

It should include:

- Project purpose
- Data structures
- Business rules
- Implementation plan
- Testing plan
- Open questions or assumptions

Update this file throughout the assignment.

---

## Task 3: Load and Inspect Seed Data

Write functions that load and print or return the five main data structures.

Your code should show that you can access:

- Recipes
- Inventory
- Orders
- Restock
- Status

Write unit tests that verify:

- All required data structures are present
- Each data structure has the expected type
- Each data structure contains records
- Key fields are present

---

## Task 4: Implement Recipe Lookup

Write a function that looks up a recipe for an ordered item.

Your function should:

- Accept an item name or order line
- Return the required ingredients and quantities
- Handle missing recipes gracefully

Write unit tests for:

- A valid item with a matching recipe
- An invalid item with no matching recipe
- A quantity greater than 1

---

## Task 5: Implement Inventory Availability Check

Write a function that checks whether inventory can fulfill an order.

Your function should:

- Compare required ingredients against available stock
- Identify missing ingredients
- Identify ingredients with insufficient quantity
- Identify expired or unusable ingredients, if expiry data is available

Write unit tests for:

- All ingredients available
- One ingredient missing
- One ingredient with insufficient quantity
- One expired or invalid ingredient, if applicable

---

## Task 6: Implement Fulfillment Logic

Write a function that processes an order.

If the order can be fulfilled:

- Mark it as delivered
- Deduct ingredients from inventory

If the order cannot be fulfilled:

- Mark it as not delivered
- Record the reason
- Add missing or unavailable ingredients to restock recommendations

Write unit tests for:

- Successful delivery
- Failed delivery due to missing stock
- Correct inventory deduction after delivery
- No unintended deduction after failed delivery

---

## Task 7: Implement Cumulative Order Processing

Write a function that processes all orders in sequence.

Your function should ensure that each order uses the inventory remaining after previous delivered orders.

Write unit tests for:

- Two orders consuming the same ingredient
- An order that fails because an earlier order used the remaining stock
- Final inventory matching expected values

---

## Task 8: Implement Restock and Expiry Rules

Write or update a function that generates restock recommendations.

Your logic should account for:

- Out-of-stock ingredients
- Low-stock ingredients
- Expiring soon ingredients
- Multiple restock reasons for the same ingredient

Write unit tests for:

- Ingredient with zero stock
- Ingredient below or equal to the low-stock threshold
- Ingredient above the threshold
- Ingredient expiring soon
- Ingredient with multiple restock reasons

---

## Task 9: Generate Final Business Summary

Create a final output that summarizes the simulation for a business user.

The summary should include:

- Delivered orders
- Not delivered orders
- Reasons for non-delivery
- Final inventory
- Restock recommendations
- Expiry concerns

The output may be printed to the console, returned as a dictionary, or written to a text or Markdown file.

---

## Task 10: Refactor and Review

After completing the core functionality, review your code for:

- Duplicate logic
- Hard-coded values that should be constants
- Unclear function names
- Missing comments
- Weak error handling
- Functions that do too much

Use AI to help identify possible refactoring opportunities, but you decide what to change.

Document at least two improvements you made during refactoring.

---

## Task 11: Reflection on AI-Assisted Coding

Write a 400–600 word reflection addressing the following questions:

- How did AI help you move faster?
- Where did AI make mistakes or questionable assumptions?
- How did testing help you evaluate AI-generated code?
- What did you change or reject from the AI’s suggestions?
- How did `PROJECT_SPEC.md` help maintain context?
- What would you do differently in a future AI-assisted coding project?
