# Part I

Overview
In this assignment, you will use AI as a coding assistant to build, test, debug, and refine a Python-based inventory simulation for a cloud kitchen.

A cloud kitchen is a delivery-only food business where multiple virtual restaurant brands share the same kitchen, staff, equipment, and ingredients. This creates operational challenges because the same ingredients may be used across many menu items and brands. If one ingredient runs out or expires, several menu items may become unavailable at the same time.

Your task is to use AI-assisted coding practices to build a simulation that processes customer orders, checks recipe-linked inventory, updates delivery status, deducts ingredient quantities, tracks expiry risk, and creates a restock plan.

The purpose of this assignment is not just to produce working code. You must also demonstrate that you can guide AI effectively, inspect AI-generated code critically, test it, debug it, and document your decisions.

Files Provided
You will receive the following files from your instructor:

AI-Assisted Cloud Kitchen Inventory Simulation.pdf
seed_data-1.pyDownload seed_data-1.py
main.pyDownload main.py
test_main.pyDownload test_main.py
You will need to create your own files,

PROJECT_SPEC.md
 

Learning Objectives
By completing this assignment, you will be able to:

Use AI tools to plan, implement, test, and debug a Python program.
Break a software problem into small implementation tasks.
Maintain a project specification file to reduce context drift when using AI.
Evaluate AI-generated code instead of accepting it uncritically.
Write and run unit tests for AI-generated functions.
Implement rule-based business logic in Python.
Explain the difference between AI-assisted coding and autonomous AI decision-making.
Reflect on the strengths and limitations of using AI as a programming partner.
Business Scenario
A cloud kitchen operates multiple virtual brands from one shared kitchen. Each menu item is linked to a recipe, and each recipe consumes ingredients from a shared inventory.

The kitchen faces several operational problems:

Ingredients may run out mid-shift.
Orders may be accepted for menu items the kitchen cannot fulfill.
Expired or soon-to-expire ingredients may create waste or quality risk.
Restocking may be inefficient if the kitchen lacks visibility into ingredient usage.
Manual menu and inventory updates can cause errors.
You will build a Python simulation that models these problems and creates a more reliable inventory workflow.

Role of AI in This Assignment
You are expected to use AI as a coding assistant, but you are responsible for the final result.

Think of AI as a fast but unreliable junior developer. It can generate code quickly, but it may misunderstand requirements, invent assumptions, duplicate logic, or produce code that only appears correct.

Throughout the assignment, you will play three roles:

Navigator
You define the goal, break the work into tasks, and decide what to ask the AI to do.
Reviewer
You inspect AI-generated code, identify assumptions, check outputs, and look for errors.
Decision-Maker
You decide what to accept, reject, revise, test, or refactor.
You may use AI tools to help write code, debug errors, generate tests, and improve explanations. However, your submitted work must show your own understanding.

Required Development Practice
You must use an incremental AI-assisted development workflow.

For each major task:

Ask AI for a plan or task breakdown.
Ask AI to implement only one small task at a time.
Review the generated code.
Ask AI to identify assumptions, uncertainty, and incomplete sections.
Write or generate unit tests.
Run the tests.
Debug failures before moving on.
Update your project specification file.
Do not ask AI to build the entire project in one prompt.

Required Project Files
Your final submission should include:

main.py
seed_data.py
test_main.py
PROJECT_SPEC.md
AI_USAGE_LOG.md
You may add additional files if useful.

main.py
This file should contain your main simulation logic.

seed_data.py
This file contains the starting data for recipes, inventory, orders, restock records, and delivery status.

test_main.py
This file should contain your unit tests.

PROJECT_SPEC.md
This file is your external memory for the project. It should summarize:

What you are building
Current components and their status
Important design decisions
Business rules
Constraints
Current task and next task
Known issues or assumptions
AI_USAGE_LOG.md
This file should document how you used AI. For each major interaction, include:

The task you were working on
The prompt you gave the AI
A short summary of the AI’s response
What you accepted, changed, or rejected
Any issues you found in the AI output
You do not need to include every minor prompt, but you should include enough evidence to show that you used AI thoughtfully and critically.

Core Data Structures
Your simulation will use five core data structures from seed_data.py:

Recipes
Inventory
Orders
Restock
Status
The exact format will be provided in the data file. Your code should inspect and use the provided structure rather than assuming a completely different schema.

Functional Requirements
Your program must implement the following functionality.

Requirement 1: Load and Display Data
Create functions that import and display all major data structures from seed_data.py.

Your program should be able to show:

Recipes
Inventory
Orders
Restock records
Delivery status records
You should use this step to confirm that your program can access all required data.

Requirement 2: Process Orders Against Recipes
For each order, your program should:

Identify the menu item or items ordered.
Look up the corresponding recipe.
Calculate the total ingredient quantity required.
Handle item quantities correctly.
Handle missing or unknown recipes gracefully.
For example, if an order contains quantity 2 of a menu item, the required ingredient quantities should be doubled.

Requirement 3: Check Inventory Availability
Before fulfilling an order, your program should check whether the required ingredients are available in sufficient quantity.

The check should account for:

Ingredient name
Quantity required
Quantity available
Expiry status, if expiry dates are included in the inventory data
The function should return clear information about whether the order can be fulfilled and, if not, what is missing or unavailable.

Requirement 4: Fulfill Orders and Deduct Inventory
If all required ingredients are available, your program should:

Mark the order as Delivered
Deduct the used ingredient quantities from inventory
If required ingredients are missing or unavailable, your program should:

Mark the order as Not Delivered
Record the reason
Add missing or unavailable ingredients to the restock list
Your code should clearly define whether failed orders deduct any partial inventory. For the base assignment, use all-or-nothing fulfillment unless your instructor states otherwise.

Requirement 5: Make Inventory Deduction Cumulative
Inventory deduction must be cumulative.

This means:

Order 1 consumes inventory.
Order 2 checks against the inventory remaining after Order 1.
Order 3 checks against the inventory remaining after Orders 1 and 2.
The final inventory table should reflect all delivered orders.
Do not reset inventory between orders unless you are running a separate test case.

Requirement 6: Apply Restock and Expiry Rules
After processing orders, apply restock logic.

Your program should identify ingredients that meet any of the following conditions:

Ingredient is out of stock.
Ingredient is running low.
Ingredient is expired or expiring soon.
Unless your instructor provides different values, use these rules:

Running low threshold: quantity ≤ 1,000g
Par level: 10,000g
Expiring soon window: within 5 days of the simulation date
Your restock output should include:

Ingredient name
Current quantity
Reason for restock
Quantity needed to reach par level
Any relevant expiry information
If an ingredient qualifies for more than one reason, your code should preserve all relevant reasons instead of silently overwriting them.

Requirement 7: Produce a Business-Friendly Summary
At the end of the simulation, produce a clear summary that includes:

Number of orders delivered
Number of orders not delivered
Final inventory levels
Restock recommendations
Any ingredients that are low, out of stock, expired, or expiring soon
Any orders that could not be fulfilled and why
This output should be understandable to a non-technical kitchen manager.

Required AI Prompt Templates
Use the following prompt patterns during the assignment.

Planning Prompt
Use this before building a major component.

I want to build [COMPONENT OR FEATURE]. Before writing any code, give me a high-level plan. What components do I need and what should I build first?
Task Breakdown Prompt
Use this after you have a plan.

Here is component [COMPONENT NAME] from our plan. Break it into individual implementation tasks. Keep each task small enough to implement in a single prompt.
Implementation Prompt
Use this for one task at a time.

Implement Task [N]: [DESCRIPTION]. Use Python. Keep the code simple and add comments explaining each section. Do not implement any other tasks yet.
Validation Hook Prompt
Use this after AI generates code.

After generating the code, add inline comments or notes that identify:
1. Any assumptions you made that I should verify
2. Any parts you are uncertain about
3. Any sections that are incomplete or require follow-up
Debugging Prompt
Use this when code fails or results are unexpected.

Here is the code and the error it produces: [PASTE CODE] / [PASTE ERROR]. Explain what is wrong and why. Then provide a corrected version with comments explaining what was changed and why.
Required Tasks
Task 1: Set Up the Project
Create or organize the following files:

main.py
seed_data.py
test_main.py
PROJECT_SPEC.md
AI_USAGE_LOG.md
Run a simple import test to confirm that main.py can access data from seed_data.py.

In your written response, explain:

How your project is organized.
How to run your program.
How to run your tests.
Any setup issues you encountered.
Task 2: Create PROJECT_SPEC.md
Create a project specification file that documents your current understanding of the project.

It should include:

Project purpose
Data structures
Business rules
Implementation plan
Testing plan
Open questions or assumptions
Update this file throughout the assignment.

Task 3: Load and Inspect Seed Data
Write functions that load and print or return the five main data structures.

Your code should show that you can access:

Recipes
Inventory
Orders
Restock
Status
Write unit tests that verify:

All required data structures are present.
Each data structure has the expected type.
Each data structure contains records.
Key fields are present.
Task 4: Implement Recipe Lookup
Write a function that looks up a recipe for an ordered item.

Your function should:

Accept an item name or order line.
Return the required ingredients and quantities.
Handle missing recipes gracefully.
Write unit tests for:

A valid item with a matching recipe.
An invalid item with no matching recipe.
A quantity greater than 1.
Task 5: Implement Inventory Availability Check
Write a function that checks whether inventory can fulfill an order.

Your function should:

Compare required ingredients against available stock.
Identify missing ingredients.
Identify ingredients with insufficient quantity.
Identify expired or unusable ingredients, if expiry data is available.
Write unit tests for:

All ingredients available.
One ingredient missing.
One ingredient with insufficient quantity.
One expired or invalid ingredient, if applicable.
Task 6: Implement Fulfillment Logic
Write a function that processes an order.

If the order can be fulfilled:

Mark it as delivered.
Deduct ingredients from inventory.
If the order cannot be fulfilled:

Mark it as not delivered.
Record the reason.
Add missing or unavailable ingredients to restock recommendations.
Write unit tests for:

Successful delivery.
Failed delivery due to missing stock.
Correct inventory deduction after delivery.
No unintended deduction after failed delivery.
Task 7: Implement Cumulative Order Processing
Write a function that processes all orders in sequence.

Your function should ensure that each order uses the inventory remaining after previous delivered orders.

Write unit tests for:

Two orders consuming the same ingredient.
An order that fails because an earlier order used the remaining stock.
Final inventory matching expected values.
Task 8: Implement Restock and Expiry Rules
Write or update a function that generates restock recommendations.

Your logic should account for:

Out-of-stock ingredients
Low-stock ingredients
Expiring soon ingredients
Multiple restock reasons for the same ingredient
Write unit tests for:

Ingredient with zero stock
Ingredient below or equal to the low-stock threshold
Ingredient above the threshold
Ingredient expiring soon
Ingredient with multiple restock reasons
Task 9: Generate Final Business Summary
Create a final output that summarizes the simulation for a business user.

The summary should include:

Delivered orders
Not delivered orders
Reasons for non-delivery
Final inventory
Restock recommendations
Expiry concerns
The output may be printed to the console, returned as a dictionary, or written to a text or Markdown file.

Task 10: Refactor and Review
After completing the core functionality, review your code for:

Duplicate logic
Hard-coded values that should be constants
Unclear function names
Missing comments
Weak error handling
Functions that do too much
Use AI to help identify possible refactoring opportunities, but you decide what to change.

Document at least two improvements you made during refactoring.

Task 11: Reflection on AI-Assisted Coding
Write a 400–600 word reflection addressing the following questions:

How did AI help you move faster?
Where did AI make mistakes or questionable assumptions?
How did testing help you evaluate AI-generated code?
What did you change or reject from the AI’s suggestions?
How did PROJECT_SPEC.md help maintain context?
What would you do differently in a future AI-assisted coding project?
Optional Enhancement
Choose one optional enhancement if you want to go beyond the base requirements.

Option A: Partial Fulfillment
Modify the logic so that if part of an order can be fulfilled, those items are delivered and only unavailable items are marked as not delivered.

Option B: Predictive Stockout Alert
Estimate which ingredients are likely to run out soon based on observed consumption across orders.

Option C: Dynamic Menu Item Disabling
Identify menu items that should be marked unavailable because one or more required ingredients are out of stock or unusable.

Option D: Improved Reporting
Generate a polished business report in Markdown, CSV, or HTML format.

Optional enhancements may earn extra credit if they are working, tested, and clearly documented.

Deliverables
Submit the following:

main.py
test_main.py
PROJECT_SPEC.md
AI_USAGE_LOG.md
Written reflection
Optional: any additional output files or reports
Do not submit files containing private credentials, API keys, or unrelated personal information.

Suggested Written Response Structure
Use the following headings:

Project Setup
Data Loading
Recipe Lookup
Inventory Availability
Order Fulfillment
Cumulative Processing
Restock and Expiry Logic
Business Summary
Refactoring Notes
AI Usage Summary
Reflection
Minimum Technical Requirements
Your submission must include:

Working Python code.
Use of the provided seed data.
Functions for data loading, recipe lookup, inventory checking, order fulfillment, cumulative processing, restock logic, and final reporting.
Unit tests for major functions.
Evidence that tests were run.
A maintained PROJECT_SPEC.md.
An AI_USAGE_LOG.md.
A written reflection on AI-assisted coding.
Grading Rubric
Total: 100 points

1. Project Setup and Data Loading — 10 points
Full credit requires a clear project structure, successful import of seed_data.py, and working functions to access the five core data structures.

2. Recipe Lookup and Ingredient Calculation — 10 points
Full credit requires correct recipe lookup, quantity scaling, and graceful handling of missing recipes.

3. Inventory Availability Logic — 10 points
Full credit requires accurate comparison of required ingredients against available inventory, including missing or insufficient ingredients.

4. Fulfillment and Status Updates — 15 points
Full credit requires correct delivery status updates, inventory deduction for delivered orders, no unintended deduction for failed orders, and meaningful failure reasons.

5. Cumulative Inventory Processing — 10 points
Full credit requires inventory to be updated across sequential orders so later orders use remaining stock.

6. Restock and Expiry Logic — 10 points
Full credit requires correct handling of low stock, out-of-stock, expiring soon, and multiple restock reasons.

7. Unit Testing — 15 points
Full credit requires meaningful tests for major functions, including normal cases, edge cases, and failure cases. Tests must be runnable and results must be visible or documented.

8. AI-Assisted Development Process — 10 points
Full credit requires a useful PROJECT_SPEC.md, meaningful AI usage documentation, evidence of prompt-based iteration, and evidence that the student reviewed rather than blindly accepted AI output.

9. Code Quality and Refactoring — 5 points
Full credit requires readable, organized code with clear function names, constants for key thresholds, comments where useful, and reduced duplication.

10. Reflection — 5 points
Full credit requires a thoughtful reflection on the benefits, risks, and limitations of AI-assisted coding.

Academic Integrity and Responsible AI Use
You are allowed and encouraged to use AI tools in this assignment. However, AI use must be documented, and you are responsible for the final work.

You may use AI to:

Plan the project
Break tasks into smaller steps
Generate draft code
Explain errors
Suggest tests
Suggest refactoring
You may not:

Submit code you do not understand
Submit AI-generated explanations you cannot explain
Ignore failed tests
Hide known defects
Claim AI-generated work as fully your own without documenting your process
Your grade is based not only on whether the program works, but also on how well you demonstrate responsible, critical, and effective AI-assisted coding practice.

Final Checklist Before Submission
Before submitting, confirm that:

main.py runs.
test_main.py runs.
The program uses seed_data.py.
The final inventory is cumulative.
Restock logic handles low stock and expiry.
Failed orders include reasons.
Tests cover both success and failure cases.
PROJECT_SPEC.md is complete and updated.
AI_USAGE_LOG.md documents your AI-assisted process.
Your reflection answers all required questions.
You understand the code you are submitting.

## Part II
Proprietary content. © Great Learning. All Rights Reserved. Page 1
Project Plan:
AI-Assisted Cloud Kitchen Inventory Simulation
Proprietary content. © Great Learning. All Rights Reserved. Page 2
1. Why AI-Assisted Coding for This Case
• Speeds up first implementation from data model to runnable logic.
• Helps quickly refactor when business rules change.
• Makes it easy to test “what if” logic through prompt iterations.
• Supports clear separation between logic changes and output-format changes.
2. Business Context
Cloud kitchens operate on tight margins. After aggregator commissions (typically 20–30% of order value), packaging costs, marketing spend, food costs, rent, labor, and utilities, contribution margins on a typical order are often only 5–15%. Even small operational inefficiencies have a meaningful impact on profitability.
Why This Problem Matters Financially
• Stockouts: Stockouts cause lost sales: every minute an ingredient is unavailable but its dependent menu items remain listed leads to order acceptances the kitchen cannot fulfill, hurting both revenue and platform ranking.
• Food waste: Food waste hurts margin: in poorly managed kitchens, 8–15% of food cost is thrown away each month due to expiry. A recipe-linked inventory system can cut this significantly.
• Customer experience: Customer experience drives ranking: rejected orders, missing items, and partial deliveries hurt aggregator ratings, reducing visibility and orders — a downward spiral.
3. Problem Statement
A cloud kitchen is a delivery-only food business where multiple virtual brands operate from the same kitchen, sharing staff, equipment, and ingredients. While this improves utilization and revenue, it creates major operational challenges in inventory and recipe management.
Key Problems Being Solved
• Silent stockouts: Ingredients run out mid-shift, causing rejected orders.
• Manual menu updates: When an ingredient is unavailable, dependent items across brands and platforms must be manually disabled.
• No expiry tracking: Lack of freshness monitoring leads to food waste and risk of expired ingredients being used.
• Inefficient restocking: Poor consumption visibility causes over-ordering or under-ordering.
• No structured procurement planning: Kitchens lack a prioritized, data-driven daily restock plan.
Proprietary content. © Great Learning. All Rights Reserved. Page 3
4. Mental Model: The Director, Not the Typist
Before writing a single prompt, learners must internalize the correct mental model for AI-assisted coding.
AI is not a software engineer. It is a probabilistic generator — an advanced autocomplete system trained on billions of lines of code. It predicts what looks plausible, not what is correct. Think of it as a confident but forgetful junior developer: writes fast, has seen a lot of examples, sometimes gets details wrong, and forgets what you told it 10 minutes ago.
Three Roles You Play Throughout This Project
• Navigator: Set the direction and goal. Break work into clear, small steps. Keep the big picture in focus.
• Reviewer: Inspect every AI-generated output. Ask: Does this do what I asked? Spot gaps, errors, or drift from intent.
• Decision-Maker: Accept, reject, or redirect AI output. Own the final quality of the work. You are always accountable.
5. Solutioning Approach: AI-Assisted Coding
We are building a Python-based simulation of a multi-brand cloud kitchen’s inventory and order management for a single operational day. The system processes orders in real time, tracks shared inventory and ingredient expiry, supports partial fulfillment, and performs periodic restocking.
Core Idea
Each menu item is linked to a recipe. When an order arrives, the system:
1. Looks up the recipe for each item and calculates the total ingredients required
2. Checks inventory for sufficient stock and valid expiry dates
3. Deducts the used ingredients and marks the order as Delivered if all stock is available
4. Flags the order as Not Delivered and adds missing or expiring items to the restock list if stock is insufficient
Restocking happens at configurable checkpoints (every N orders), not after every order.
Key Design Principles
• Centralized inventory: All brands consume from one shared inventory source.
• Recipe-driven deduction: Inventory updates happen automatically from recipes and order quantities.
• Availability validation: Ingredients must have sufficient quantity and be unexpired.
Proprietary content. © Great Learning. All Rights Reserved. Page 4
• Separated workflows: Order processing only consumes inventory; replenishment happens in dedicated checkpoint phases.
• Baseline restocking: Ingredients are replenished to predefined par levels.
• Multi-reason tracking: Ingredients can be flagged simultaneously for low stock and expiry with audit comments preserved.
• Periodic replenishment: Restocking occurs every N orders to balance operational recovery and system efficiency.
Proprietary content. © Great Learning. All Rights Reserved. Page 5
6. PROJECT_SPEC.md — Your AI’s External Memory
AI has no persistent memory between sessions. Within a session, as the conversation grows, earlier instructions degrade or disappear entirely. To prevent context drift, every learner must maintain a PROJECT_SPEC.md file and paste the relevant section at the start of each new session.
What to Include in PROJECT_SPEC.md
• What you are building and why
• Key components and their current status
• Decisions already made (e.g. restock threshold = 1,000g, par level = 10,000g)
• Constraints and rules the AI must follow
• Current task and next task
How to Use It at the Start of Each Session Session Re-anchor Prompt: Here is our project context. We are building a Python-based cloud kitchen inventory simulation using seed_data.py (Recipes, Inventory, Orders, Restock, Status). We have completed Tasks 1–3. Task 4 (cumulative deduction) is the current task. Do not modify any previously implemented functions.
When to Update It
After every session: mark completed tasks, record new decisions, and add constraints that emerged. Treat it as the single source of truth for the project.
7. Prompt Templates Library
These four templates are reused throughout the entire project. Every prompt in Section 8 is built on one of these. Learn them once, apply them everywhere.
Use Templates 1 and 2 before writing a single line of code. They are your project architecture phase. Use Template 3 strictly one task at a time — never bundle tasks. Use Template 4 every time something breaks — never skip it and move on.
Template 1 Planning Prompt When to use: At the very start of every new project or major component, before any code is written.
Proprietary content. © Great Learning. All Rights Reserved. Page 6
What it does: Gets AI thinking in components, not in code. Gives you a shared architecture to reference throughout. Template: “I want to build [PROJECT]. Before writing any code, give me a high-level plan — what components do I need and what should I build first?”
Template 2 Task Breakdown Prompt When to use: Run once per component, after the plan from Template 1 is confirmed. What it does: Converts each component into individual, small, implementable tasks. Each task then becomes one Template 3 prompt. Small tasks = small errors = fast debugging. Template: “Here is component [NAME] from our plan. Break it into individual implementation tasks. Keep each task small enough to implement in a single prompt.”
Template 3 Implementation Prompt When to use: For every individual task in the implementation phase. One task per prompt — never bundle tasks. What it does: Keeps scope tight. The phrase “Do not implement any other tasks yet” prevents scope creep. Comments make the output readable and verifiable. Template: “Implement Task [N]: [DESCRIPTION]. Use Python. Keep the code simple and add comments explaining each section. Do not implement any other tasks yet.”
Template 4 Debugging Prompt When to use: Every time a test fails or code produces unexpected output. Never skip it and move on. What it does: Forces AI to explain the root cause, not just patch the error. This builds your understanding of the code over time so you genuinely own it. Template: “Here is the code and the error it produces: [PASTE CODE] / [PASTE ERROR]. Explain what is wrong and provide a corrected version with comments.”
Correct Order of Use in Every Project 5. Template 1 — once, at the very start, before any code. 6. Template 2 — once per component, after the plan is confirmed. 7. Template 3 — for every individual task, one at a time.
Proprietary content. © Great Learning. All Rights Reserved. Page 7
8. Template 4 — whenever a test fails or an error appears. Save these 4 templates. They cover the full development cycle: plan → breakdown → implementation → debugging.
8. Step-by-Step Instructions and Prompts
We follow a structured path divided into three parts: establish data connectivity first, define the operational flow second, and refine the logic to handle complex business rules last. Each step follows the Build → Test → Inspect → Refine loop from the course.
Part 1: Creating the Orchestrator
The goal is to ensure the application can “see” all the data it needs to work with. This layer acts as the foundation for the entire system.
Step 1: Establishing Data Connectivity
Goal: Create a baseline main.py that interfaces with every data structure in seed_data.py.
Note: seed_data.py contains 5 tables — Recipes (5 items: Margherita Pizza, Chicken Burger, Caesar Salad, Pasta Alfredo, Chocolate Cake with ingredient quantities in grams), Inventory (14 ingredients with current stock and expiry dates), Orders (5 orders across 2 brands — Taco Bell and Subway), Restock (5 flagged ingredients with reason), and Status (delivery status per order).
Planning Prompt (Template 1): I want to build a Python cloud kitchen inventory simulation using seed_data.py. Before writing any code, give me a high-level plan — what components do I need and what should I build first?
Implementation Prompt (Template 3): Implement Task 1: Create a baseline main.py file that imports all data from seed_data.py. Write specific functions to load and print the contents of every data table—including Recipes, Inventory, Orders, Restock, and Status—to the console. Add comments explaining each function. Do not implement any other tasks yet.
Validation Hook Prompt: After generating the code, add inline comments that identify: (1) any assumptions you made that I should verify, (2) any parts you are uncertain about, and (3) any sections that are incomplete or require follow-up.
Proprietary content. © Great Learning. All Rights Reserved. Page 8
Test Generation Prompt (immediately after Step 1 code): Write unit tests for the load functions using Python unittest. Cover: successful import of all 5 tables, correct count of records in each table, and correct data types for key fields (e.g. qty_grams is a number, expiry_date is a string).
5-Point Code Review Checklist — Apply After Every Step Run this checklist on every function the AI generates: 9. Does it do what I asked? Run it with 3 different inputs you can verify manually. 10. Are there hidden assumptions? Look for hard-coded values, assumed data types, or logic paths you didn’t specify. 11. Is anything hard-coded that should be a variable? (e.g. restock thresholds, par levels, expiry windows). 12. Does it handle bad inputs? What happens with None values, empty lists, or negative quantities? 13. Is any part of it security-sensitive or business-critical? (e.g. financial deductions, expiry logic).
Part 2: Defining the Application Flow
Now that the data is connected, we define the “rhythm” of the kitchen: taking an order, checking ingredients, and updating the status.
Step 2: Implementing Order-to-Recipe Processing
Goal: Create the logic to pull an order, look up its recipe, and identify required ingredients.
Task Breakdown Prompt (Template 2): Here is component ‘Order Processing’ from our plan. Break it into individual implementation tasks. Keep each task small enough to implement in a single prompt.
Implementation Prompt (Template 3): Implement Task 2: Update main.py to process orders from the Orders table. For each order, the system should: 1. Look up the recipe for each item. 2. Calculate the total grams of ingredients required. 3. Check the Inventory table to see if all required ingredients are present in the necessary quantities. Add comments explaining each step. Do not implement any other tasks yet.
Proprietary content. © Great Learning. All Rights Reserved. Page 9
Validation Hook Prompt: After generating the code, add inline comments that identify: (1) any assumptions you made about how recipe lookup works, (2) what happens if an order item has no matching recipe, and (3) any sections that are incomplete.
Test Generation Prompt: Write unit tests for the order-to-recipe lookup function using Python unittest. Cover: a valid order item with a matching recipe, an order item with no matching recipe (should handle gracefully), and correct calculation of total grams for an order with quantity 2.
Step 3: Fulfillment and Inventory Deduction
Goal: Update the order status and reduce stock if ingredients are available.
Implementation Prompt (Template 3): Implement Task 3: Add fulfillment logic. If all ingredients are available, mark the order as 'Delivered' in the status table and deduct the used grams from the inventory. If ingredients are missing, mark the order as 'Not Delivered,' record the reason, and add the missing items to the Restock table. Add comments. Do not implement any other tasks yet.
Validation Hook Prompt: After generating the code, add inline comments identifying: (1) what happens if the same ingredient is missing from two consecutive orders, (2) any assumption about whether partial stock can be deducted, and (3) any incomplete sections.
Test Generation Prompt: Write unit tests for the fulfillment function. Cover: an order where all ingredients are available (expect Delivered), an order where one ingredient is missing (expect Not Delivered, missing item logged to Restock), and correct deduction from inventory after delivery.
Proprietary content. © Great Learning. All Rights Reserved. Page 10
Part 3: Refining the Logic for Correct Output
The final part ensures the inventory math is accurate across multiple orders and that restocking triggers correctly based on health rules.
Step 4: Cumulative Inventory Deduction
Goal: Ensure each order subtracts from the remaining inventory of the previous order.
Implementation Prompt (Template 3): Implement Task 4: Refine the inventory logic to be cumulative. Order 2 must check availability against the quantity remaining after Order 1 was served. Update the final inventory table only after all orders in the list have been processed to show the true remaining stock. Add comments. Do not implement any other tasks yet.
Validation Hook Prompt: After generating the code, add inline comments identifying: (1) whether a deep copy or reference is used for the working inventory state, (2) what happens if two orders compete for the same ingredient, and (3) any incomplete sections.
Test Generation Prompt: Write unit tests for cumulative deduction. Cover: two orders consuming the same ingredient (verify combined deduction), an order that fails because a prior order consumed the remaining stock, and final inventory state matching expected remaining quantities.
Step 5: Implementing Restock and Expiry Rules
Goal: Automate restock reasons based on expiry dates and low-stock thresholds.
Implementation Prompt (Template 3): Implement Task 5: Update the restock logic with these specific rules: 1. If an ingredient is within 5 days of expiry (relative to today’s date), mark it as 'Expiring soon' and set the restock quantity to 10,000g. 2. If the final stock is 0, mark as 'Out of stock' (10,000g needed). 3. If stock is ≤ 1,000g, mark as 'Running low on stock' and calculate the needed amount to reach 10,000g. Add comments. Do not implement anything beyond this task.
Validation Hook Prompt: After generating the code, add inline comments identifying: (1) how today’s date is obtained — verify this is correct for the simulation, (2) whether an ingredient can be flagged for both low stock and expiry simultaneously, and (3) any incomplete sections.
Proprietary content. © Great Learning. All Rights Reserved. Page 11
Test Generation Prompt: Write unit tests for the restock logic. Cover: an ingredient expiring within 5 days (expect 'Expiring soon', 10,000g), an ingredient with 0 stock (expect 'Out of stock', 10,000g), an ingredient with 500g remaining (expect 'Running low', 9,500g needed), and an ingredient with adequate stock and no expiry issue (expect not flagged).
Duplication Check — After Every 3–4 Tasks
After completing Steps 2–5, run the following refactoring prompt before proceeding to enhancements. AI generates code based on each prompt in isolation and has no global view of your codebase — duplicate logic will accumulate silently.
Refactoring Prompt: Review the code in main.py for duplicated logic or functions — particularly any inventory lookup, availability check, or restock flagging logic that appears more than once. Suggest how to refactor it to eliminate duplication while keeping the behaviour identical. Do not change any function signatures yet.
Debugging Loop — Template 4
When any test fails or any step produces unexpected output, do not skip ahead. Use this structured debugging loop.
Step 1: Read the error message carefully — before anything else. Step 2: Try to understand what it is saying — what line, what type of error, what variable? Step 3: Use Template 4 — paste both code AND full error. Step 4: Ask AI to explain the root cause, not just give a fix. Step 5: Apply the fix and re-run ALL tests — not just the failing one. Step 6: If still failing, paste the new error and repeat.
Debugging Prompt (Template 4): Here is the code and the error it produces: [PASTE FUNCTION CODE] / [PASTE FULL ERROR MESSAGE]. Explain what is wrong and why. Then provide a corrected version with comments explaining what was changed and why.
Proprietary content. © Great Learning. All Rights Reserved. Page 12
9. Session Exercise: Application Enhancements
Apply the full 8-step playbook independently for each enhancement. Do not skip the planning stage or jump straight to code. Each enhancement should follow: Plan → Task Breakdown → Implement one task → Validate hooks → Test → Debug → Refactor.
Enhancement 1: Partial Fulfillment Logic
Modify the order processing logic so that if a subset of items in an order can be fulfilled with remaining inventory, those items are delivered and marked separately rather than failing the entire order.
Starting Prompt (Template 1): I want to add partial fulfillment logic to the cloud kitchen simulation. Before writing any code, give me a plan — what components need to change and what should I build first?
Reminder: After each implementation prompt, request validation hooks. After each function, request unit tests. Use Template 4 when tests fail.
Enhancement 2: Predictive Stockout Alerts
Enhance the system to calculate the current per-order consumption rate and forecast which ingredients will run out within the next batch of orders, even if they are currently in stock.
Starting Prompt (Template 1): I want to add predictive stockout alerts to the cloud kitchen simulation. Before writing any code, give me a plan — what components do I need and what should I build first?
Enhancement 3: Dynamic Item Disabling
Implement a function that automatically identifies all menu items across all brands linked to a depleted ingredient and marks them as “unavailable” to prevent future order rejections.
Starting Prompt (Template 1): I want to implement dynamic item disabling in the cloud kitchen simulation. Before writing any code, give me a plan — what components do I need and what should I build first?
Proprietary content. © Great Learning. All Rights Reserved. Page 13
10. Practical Approach Followed
• Import and print all data structures (Recipes, Inventory, Orders, Restock, Status) to establish full data connectivity.
• For each order, look up its recipe and calculate the total grams of ingredients required.
• Check inventory for availability; mark as Delivered and deduct stock, or mark as Not Delivered, log the reason, and add missing items to Restock.
• Make inventory deduction cumulative — each order checks against stock remaining after the previous order.
• Update the final inventory table only after all orders are processed.
• Apply restock rules to final inventory: Expiring soon (within 5 days, 10,000g); Out of stock (qty = 0, 10,000g); Running low (qty ≤ 1,000g, top-up to 10,000g).
• Generate unit tests immediately after each function is implemented.
• Use Template 4 (debugging prompt) whenever tests fail — always ask for root cause explanation, not just a fix.
• Request validation hooks after every implementation prompt to surface hidden assumptions.
• Run a duplication check every 3–4 tasks to prevent duplicate logic accumulating across steps.
• Maintain PROJECT_SPEC.md and re-anchor at the start of each new session.
• Refine outputs to a business-friendly reporting format.
Proprietary content. © Great Learning. All Rights Reserved. Page 14
11. Key Takeaways
01 The Business Pain Point Inventory risk and delivery reliability are the real problems. Every technical decision should trace back to reducing stockouts, waste, or rejected orders. 02 The Technical Problem The order-to-inventory-to-restock pipeline must be cumulative, expiry-aware, and threshold-triggered. Each component is a single, testable task. 03 The Implementation Strategy Incremental AI prompts that evolve logic safely — with tests after every function, validation hooks after every prompt, a debugging loop when things break, and a context file to prevent drift. This is not just writing code with AI. It is structured problem-solving with AI aligned to business outcomes.