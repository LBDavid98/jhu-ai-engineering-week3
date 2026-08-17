"""Baseline entry point for loading and printing cloud kitchen seed data."""

from copy import deepcopy
from datetime import date, datetime

# DC1 (verified): import the five tables from seed_data.py.
# Instructor file was seed_data-1.py; renamed so a direct import works (no fallback).
# Covered by test_seed_data_module_imports_all_five_tables and the load_* tests.
# This import only supplies seed tables; lookup/fulfillment/restock live elsewhere.
from seed_data import inventory, orders, recipes, restock, status

# RS1: restock thresholds as named constants. Values are unchanged.
# Verified (AC4): EXPIRING_SOON_DAYS is restock/summary only. Fulfillment treats
# past expiry as days < 0 (see check_inventory_availability). Covered by
# test_expired_ingredient_blocks_fulfillment and
# test_expiring_soon_does_not_block_fulfillment.
RUNNING_LOW_THRESHOLD_GRAMS = 1000
PAR_LEVEL_GRAMS = 10000
EXPIRING_SOON_DAYS = 5

# RS4: one operational day for this simulation. Seed expiries are 2026-01 through
# 2026-11. Do not use date.today() — on 2026-08-11 that would already mark
# Flour, Romaine Lettuce, Fettuccine Pasta, Chocolate, and Sugar as past expiry.
# Approved 2026-08-11 20:52 -0400.
SIMULATION_DATE = date(2026, 5, 10)


def load_recipes():
    """Return the seeded recipe records for use in the application."""
    # Verified (AC1): returning the module-level seed list is acceptable for Task 1.
    # Callers that mutate (e.g. main/process_orders) deepcopy before changing data.
    # No database or file loader is required for this assignment.
    return recipes


def print_recipes(recipe_data):
    """Print every recipe and its ingredient requirements to the console."""
    print("\n=== Recipes ===")
    for recipe in recipe_data:
        print(f"Recipe ID: {recipe['recipe_id']}")
        print(f"Name: {recipe['name']}")
        print("Ingredients:")
        for ingredient in recipe["ingredients"]:
            print(f"  - {ingredient['name']}: {ingredient['qty_grams']} grams")
        print()


def load_inventory():
    """Return the seeded inventory records for the simulation."""
    # Verified (AC2): seed schema stores every stock quantity in qty_grams,
    # including Bun (not piece counts). Part I / seed_data use grams only.
    return inventory


def print_inventory(inventory_data):
    """Print every inventory item with quantity and expiry information."""
    print("\n=== Inventory ===")
    for item in inventory_data:
        print(f"Ingredient: {item['ingredient']}")
        print(f"Quantity: {item['qty_grams']} grams")
        print(f"Expiry Date: {item['expiry_date']}")
        print()


def load_orders():
    """Return the seeded customer order records."""
    # Verified (AC3): Orders.item must match Recipes.name with exact string equality
    # (Decision: no aliases / case folding). find_recipe_by_name enforces that.
    return orders


def print_orders(order_data):
    """Print every order, including its brand and requested items."""
    print("\n=== Orders ===")
    for order in order_data:
        print(f"Order ID: {order['order_id']}")
        print(f"Brand: {order['brand']}")
        print("Items:")
        for item in order["items"]:
            print(f"  - {item['item']}: {item['qty']}")
        print()


def load_restock():
    """Return the seeded restock recommendations."""
    # Verified (AC1): load_restock returns the seed Restock table for baseline
    # load/print (DC7). After orders, refresh_restock_table replaces the live
    # table from final inventory (+ OP15). Seed rows are not kept as history.
    return restock


def print_restock(restock_data):
    """Print every restock item with quantity needed and reason."""
    print("\n=== Restock ===")
    for item in restock_data:
        print(f"Item: {item['item']}")
        if "current_qty_grams" in item:
            print(f"Current Quantity: {item['current_qty_grams']} grams")
        print(f"Quantity Needed: {item['qty_needed_grams']} grams")
        print(f"Reason: {item['reason']}")
        if item.get("expiry_date"):
            print(f"Expiry Date: {item['expiry_date']}")
        print()


def load_status():
    """Return the seeded delivery status records."""
    # Verified (AC9): seed status is the initial baseline table for Task 1 print
    # only (like load_restock). Live fulfillment writes via update_status_entry
    # on a working copy in main()/process_orders — not re-derived by load_status.
    return status


def print_status(status_data):
    """Print every order status with delivery result and remark."""
    print("\n=== Status ===")
    for entry in status_data:
        print(f"Order ID: {entry['order_id']}")
        print(f"Delivered: {entry['delivered']}")
        print(f"Remark: {entry['remark']}")
        print()


def find_recipe_by_name(recipe_data, item_name):
    """Return the recipe that matches an order item name, or None if missing."""
    # Verified (AC3): exact Orders.item ↔ Recipes.name match only.
    # No case folding, trimming, aliases, or brand-specific variants (Decision).
    for recipe in recipe_data:
        if recipe["name"] == item_name:
            return recipe
    return None


def calculate_ingredient_requirements(recipe, quantity):
    """Return the total grams required for each ingredient in an order item."""
    requirements = []

    # Step 2: multiply each recipe ingredient quantity by the ordered item count
    # so we know the total grams needed to prepare that order item.
    for ingredient in recipe["ingredients"]:
        requirements.append(
            {
                "name": ingredient["name"],
                "required_qty_grams": ingredient["qty_grams"] * quantity,
            }
        )

    return requirements


def _inventory_by_name(inventory_data):
    """Return a dict of inventory rows keyed by ingredient name."""
    # RF2 / Verified (AC7): one lookup builder for availability, deduct, and OP15.
    # Last row wins if the same ingredient appears twice (dict comprehension).
    # Seed inventory has unique names; last-wins is locked by
    # test_inventory_by_name_last_row_wins for defensive clarity.
    # Verified (AC7): apply_final_inventory_snapshot keeps a separate qty-only map
    # on purpose — it copies remaining grams onto the live table and must not
    # replace full rows or expiry. Do not merge the two shapes without approve.
    return {item["ingredient"]: item for item in inventory_data}


def _days_until_expiry(expiry_value, reference_date):
    """Return days from reference_date until expiry_value. Raises on a bad date."""
    # RF3 / Verified (AC6) / EH3a: shared parse only — callers choose raise vs catch.
    # Intentional asymmetry (do not “fix” without approve):
    # - check_inventory_availability + build_manager_summary: try/except → quiet status
    # - calculate_restock_needs: bare call → malformed date raises
    # Locked by: test_restock_raises_on_malformed_expiry_date,
    # test_invalid_expiry_date_is_unusable (availability catch → status "unusable").
    expiry_date = datetime.strptime(expiry_value, "%Y-%m-%d").date()
    return (expiry_date - reference_date).days


def _classify_inventory_stock_flags(current_qty_grams, days_until_expiry=None):
    """Classify qty/expiry flags and restock need from already-parsed inputs.

    Returns a dict with:
    - out_of_stock, running_low, expiring_soon, expired (bools)
    - restock_reasons (list of labels matching calculate_restock_needs strings)
    - qty_needed_grams (max of applicable restock rules; 0 if none apply)

    Callers pass days_until_expiry (int) or None. This helper does not parse
    dates and does not catch malformed-date errors.
    """
    # DR1: shared classifier for restock + manager summary (DR2/DR3 wired).
    # Thresholds match RUNNING_LOW_THRESHOLD_GRAMS / PAR_LEVEL_GRAMS / EXPIRING_SOON_DAYS.
    # Restock reasons use the exact strings already in calculate_restock_needs.
    # Verified (AC11): qty 0 is out-of-stock only (not also running-low).
    # Assumption to verify: days_until_expiry is None means "no expiry signal here"
    # (caller skipped parse or had no date) — not expired and not expiring soon.
    out_of_stock = current_qty_grams == 0
    running_low = 0 < current_qty_grams <= RUNNING_LOW_THRESHOLD_GRAMS
    expired = days_until_expiry is not None and days_until_expiry < 0
    expiring_soon = (
        days_until_expiry is not None
        and 0 <= days_until_expiry <= EXPIRING_SOON_DAYS
    )

    restock_reasons = []
    qty_needed_grams = 0

    # Same max-of-rules logic as calculate_restock_needs (not elif across reasons).
    if out_of_stock:
        restock_reasons.append("Out of stock")
        qty_needed_grams = max(qty_needed_grams, PAR_LEVEL_GRAMS)

    if running_low:
        restock_reasons.append("Running low on stock")
        qty_needed_grams = max(
            qty_needed_grams, PAR_LEVEL_GRAMS - current_qty_grams
        )

    if expiring_soon:
        restock_reasons.append("Expiring soon")
        qty_needed_grams = max(qty_needed_grams, PAR_LEVEL_GRAMS)

    # RX1: Part I R6 lists "expired or expiring soon" as restock conditions, so
    # already-expired stock must be flagged by the rule engine, not only when an
    # order happens to fail on it. Part II Step 5 omits Expired; Part I wins.
    # Full par because expired grams cannot be used and must be replaced, not
    # topped up. OP15 still skips names already on the table (no duplicates).
    if expired:
        restock_reasons.append("Expired")
        qty_needed_grams = max(qty_needed_grams, PAR_LEVEL_GRAMS)
    return {
        "out_of_stock": out_of_stock,
        "running_low": running_low,
        "expiring_soon": expiring_soon,
        "expired": expired,
        "restock_reasons": restock_reasons,
        "qty_needed_grams": qty_needed_grams,
    }


def _make_restock_row(
    item,
    current_qty_grams,
    qty_needed_grams,
    reasons,
    expiry_date,
):
    """Build one restock-table row dict with the shared field shape.

    Keys: item, current_qty_grams, qty_needed_grams, reason, reasons, expiry_date.
    reason is ", ".join(reasons) so multi-reason restock and single-reason OP15
    rows share one builder.
    """
    # DR4: shared row shape for calculate_restock_needs and
    # add_failed_order_items_to_restock (DR5/DR6 wired).
    # Assumption to verify: reasons is always a list of strings (possibly one
    # element for OP15 labels like "Expired" / "Missing from inventory").
    # Skip-if-name-exists and label selection stay in the callers.
    if reasons is None:
        reasons = []
    return {
        "item": item,
        "current_qty_grams": current_qty_grams,
        "qty_needed_grams": qty_needed_grams,
        "reason": ", ".join(reasons),
        "reasons": reasons,
        "expiry_date": expiry_date,
    }


def _resolve_reference_date(reference_date):
    """Return SIMULATION_DATE when reference_date is None; otherwise unchanged."""
    # DR7/DR8: shared default for availability, restock, and manager summary.
    # RS4: default is SIMULATION_DATE (2026-05-10), not date.today().
    if reference_date is None:
        return SIMULATION_DATE
    return reference_date


def check_inventory_availability(inventory_data, requirements, reference_date=None):
    """Check quantity and expiry. Past expiry blocks; expiring soon does not."""
    # OP6: an order is not fulfillable if a required ingredient is missing,
    # short on grams, expired, or otherwise unusable.
    # OP7 / Verified (AC5):
    # - Omit reference_date → SIMULATION_DATE (2026-05-10), not date.today().
    # - None inventory / None requirements → empty lists; empty requirements succeed.
    # - Negative (or non-numeric) required qty → status "invalid", not available.
    # - Malformed expiry string → catch here → status "unusable" (AC6 catch side).
    #   Locked by test_invalid_expiry_date_is_unusable. Restock does NOT catch (EH3a).
    # This function only returns availability; restock and summary are separate.
    # Verified (AC4): "expired" means days_until_expiry < 0 only. Expiring soon
    # (0..EXPIRING_SOON_DAYS) is restock/summary only and does not fail this check.
    # DR8: default reference_date via _resolve_reference_date (still SIMULATION_DATE).
    reference_date = _resolve_reference_date(reference_date)

    if inventory_data is None:
        inventory_data = []
    if requirements is None:
        requirements = []

    inventory_lookup = _inventory_by_name(inventory_data)
    availability_results = []
    all_available = True

    # Compare each required ingredient: present, enough grams, and not past expiry.
    for requirement in requirements:
        if not isinstance(requirement, dict):
            availability_results.append(
                {
                    "ingredient": None,
                    "required_qty_grams": None,
                    "available_qty_grams": 0,
                    "is_available": False,
                    "is_expired": False,
                    "status": "invalid",
                }
            )
            all_available = False
            continue

        inventory_item = inventory_lookup.get(requirement.get("name"))
        required_qty = requirement.get("required_qty_grams")
        is_expired = False
        status = "ok"
        ingredient_name = requirement.get("name")

        # Negative (or non-numeric) demand is not a valid order quantity.
        if not isinstance(required_qty, (int, float)) or required_qty < 0:
            availability_results.append(
                {
                    "ingredient": ingredient_name,
                    "required_qty_grams": required_qty,
                    "available_qty_grams": (
                        inventory_item["qty_grams"] if inventory_item else 0
                    ),
                    "is_available": False,
                    "is_expired": False,
                    "status": "invalid",
                }
            )
            all_available = False
            continue

        if inventory_item is None:
            available_qty = 0
            status = "missing"
            is_available = False
        else:
            available_qty = inventory_item["qty_grams"]
            expiry_value = inventory_item.get("expiry_date")

            # Only inspect expiry when the inventory row has a date.
            # Verified (AC6) / EH3a: wrap _days_until_expiry — do not let bad dates raise
            # here (restock calls it bare). Locked by test_invalid_expiry_date_is_unusable.
            if expiry_value:
                try:
                    days_until_expiry = _days_until_expiry(
                        expiry_value, reference_date
                    )
                    if days_until_expiry < 0:
                        is_expired = True
                        status = "expired"
                except (TypeError, ValueError):
                    # Intentional catch: quiet "unusable", not an exception to the caller.
                    is_expired = True
                    status = "unusable"

            if is_expired:
                is_available = False
            elif available_qty < required_qty:
                status = "insufficient"
                is_available = False
            else:
                status = "ok"
                is_available = True

        availability_results.append(
            {
                "ingredient": ingredient_name,
                "required_qty_grams": required_qty,
                "available_qty_grams": available_qty,
                "is_available": is_available,
                "is_expired": is_expired,
                "status": status,
            }
        )

        if not is_available:
            all_available = False

    return {"all_available": all_available, "details": availability_results}


def combine_requirements(requirement_groups):
    """Merge repeated ingredient requirements into a single total per ingredient."""
    combined_requirements = {}

    # Step 2: combine ingredient demand across all items in the same order so
    # fulfillment is checked against the total grams needed for the entire order.
    for requirements in requirement_groups:
        for requirement in requirements:
            ingredient_name = requirement["name"]
            combined_requirements.setdefault(ingredient_name, 0)
            combined_requirements[ingredient_name] += requirement["required_qty_grams"]

    return [
        {"name": ingredient_name, "required_qty_grams": required_qty}
        for ingredient_name, required_qty in combined_requirements.items()
    ]


def deduct_inventory(inventory_data, requirements):
    """Subtract the used ingredient grams from inventory after a successful order."""
    inventory_lookup = _inventory_by_name(inventory_data)

    # Step 4 / Verified (AC8): deduct only after the full order passes availability.
    # Failed orders never call this; no partial stock is consumed. Locked by
    # all-or-nothing / without-deduct tests (including multi-item AC8 test).
    for requirement in requirements:
        inventory_lookup[requirement["name"]]["qty_grams"] -= requirement["required_qty_grams"]


def apply_final_inventory_snapshot(inventory_data, final_inventory_data):
    """Copy the final cumulative inventory quantities back into the main table."""
    # Verified (AC7): qty-only map by design. Working inventory may carry the same
    # fields, but this step only writes qty_grams onto matching live rows so seed
    # row order and expiry_date stay intact. Different shape from
    # _inventory_by_name (full rows) — do not merge without approve.
    # Locked by test_final_snapshot_updates_qty_only_not_expiry.
    final_inventory_lookup = {
        item["ingredient"]: item["qty_grams"] for item in final_inventory_data
    }

    # Step 6: update the final inventory table only after all orders have been
    # processed so the printed inventory reflects the true remaining stock.
    for item in inventory_data:
        if item["ingredient"] in final_inventory_lookup:
            item["qty_grams"] = final_inventory_lookup[item["ingredient"]]


def update_status_entry(status_data, order_id, delivered, remark):
    """Update or create a status-table entry for a processed order."""
    # Verified (AC9): if order_id exists, update in place; otherwise append.
    # Seed is initial table only — orders need not be pre-seeded. Locked by
    # test_update_status_entry_updates_existing_row and
    # test_update_status_entry_appends_when_order_id_is_new.
    for entry in status_data:
        if entry["order_id"] == order_id:
            entry["delivered"] = delivered
            entry["remark"] = remark
            return

    status_data.append({"order_id": order_id, "delivered": delivered, "remark": remark})


def _format_unavailable_ingredient_reason(unavailable_details):
    """Build a fail-reason that names expired/unusable separately from shortages."""
    # SP7 / Verified (AC10): label by availability detail status —
    # expired → "Expired ingredients"; unusable → "Unusable ingredients";
    # missing / insufficient / invalid / other → "Missing or insufficient ingredients".
    # Wording only: callers still reject the whole order and do not deduct
    # (AC8). Public process_orders signature unchanged. Locked by
    # test_format_unavailable_reason_names_expired_and_unusable and
    # test_fail_reason_names_expired_clearly_without_deduct.
    expired_names = []
    unusable_names = []
    missing_or_short_names = []

    for detail in unavailable_details:
        name = detail.get("ingredient")
        if name is None:
            name = "(unknown)"
        status = detail.get("status")
        if status == "expired":
            expired_names.append(str(name))
        elif status == "unusable":
            unusable_names.append(str(name))
        else:
            missing_or_short_names.append(str(name))

    reason_parts = []
    if expired_names:
        reason_parts.append("Expired ingredients: " + ", ".join(expired_names))
    if unusable_names:
        reason_parts.append("Unusable ingredients: " + ", ".join(unusable_names))
    if missing_or_short_names:
        reason_parts.append(
            "Missing or insufficient ingredients: " + ", ".join(missing_or_short_names)
        )

    if not reason_parts:
        return "Unavailable ingredients"
    return " | ".join(reason_parts)


def calculate_restock_needs(inventory_data, reference_date=None):
    """Build restock recommendations from final inventory using the Task 5 rules."""
    # RS3 / DR2: multi-reason + qty_needed come from _classify_inventory_stock_flags.
    # DR5: row dict shape comes from _make_restock_row (same keys as before).
    # Verified (AC6) / EH3a: call _days_until_expiry bare so malformed dates raise.
    # Do not add try/except here — availability/summary catch; restock must not.
    # Locked by test_restock_raises_on_malformed_expiry_date.
    # Verified (AC11): qty 0 → "Out of stock" only (not also "Running low");
    # multi-rule qty_needed_grams is max of applicable rules (RS3).
    # RX1: expired stock is flagged here too (reason "Expired", full par), so an
    # expired ingredient no longer depends on a failed order to reach the table.
    # Verified (AC11): inventory-only rebuild; names missing from inventory are
    # added afterward by OP15 (not here). Restock-every-N is not base.
    # DR8 / RS4: default reference_date via _resolve_reference_date (SIMULATION_DATE).
    reference_date = _resolve_reference_date(reference_date)

    restock_recommendations = []

    for item in inventory_data:
        current_qty = item["qty_grams"]
        expiry_value = item["expiry_date"]
        # Bare call on purpose (AC6 raise side) — do not wrap in try/except here.
        days_until_expiry = _days_until_expiry(expiry_value, reference_date)
        flags = _classify_inventory_stock_flags(current_qty, days_until_expiry)
        reasons = flags["restock_reasons"]
        qty_needed_grams = flags["qty_needed_grams"]

        if reasons:
            restock_recommendations.append(
                _make_restock_row(
                    item=item["ingredient"],
                    current_qty_grams=current_qty,
                    qty_needed_grams=qty_needed_grams,
                    reasons=reasons,
                    expiry_date=expiry_value,
                )
            )

    return restock_recommendations


def refresh_restock_table(restock_data, inventory_data, reference_date=None):
    """Replace the live restock table with recommendations from final inventory."""
    # Step 7 / Verified (AC11): clear + rebuild from final inventory each run.
    # Seed/historical restock rows are not preserved as base history. OP15 may
    # append after this. Locked by test_refresh_restock_table_replaces_prior_rows.
    # Restock-every-N is not part of the base assignment.
    restock_data.clear()
    restock_data.extend(calculate_restock_needs(inventory_data, reference_date))


def add_failed_order_items_to_restock(restock_data, inventory_data, failed_items):
    """Add failed-order missing/unavailable items that final-inventory rules missed."""
    # OP15 / DR6 / Verified (AC12):
    # - One row per ingredient name (skip if already on the live table).
    # - Missing-from-inventory → full PAR_LEVEL_GRAMS.
    # - Present but failed at/above par (e.g. expired) → still request full par
    #   so unusable stock can be replaced; below par → top up to par.
    # Verified (AC8): OP15 only appends restock rows; it does not deduct inventory
    # or enable partial fulfillment. Base assignment stays all-or-nothing.
    # Locked by OP15 process_orders tests + TestAddFailedOrderItemsToRestock.
    if not failed_items:
        return
    if inventory_data is None:
        inventory_data = []

    existing_names = {row["item"] for row in restock_data}
    inventory_lookup = _inventory_by_name(inventory_data)

    for failed in failed_items:
        if not isinstance(failed, dict) or "ingredient" not in failed:
            continue
        name = failed["ingredient"]
        if name in existing_names:
            continue

        inventory_item = inventory_lookup.get(name)
        if inventory_item is None:
            current_qty = 0
            expiry_value = None
            reason_label = "Missing from inventory"
            qty_needed_grams = PAR_LEVEL_GRAMS
        else:
            current_qty = inventory_item["qty_grams"]
            expiry_value = inventory_item.get("expiry_date")
            status = failed.get("status", "unavailable")
            if status == "expired":
                reason_label = "Expired"
            elif status == "unusable":
                reason_label = "Unusable"
            elif status == "insufficient":
                reason_label = "Insufficient stock"
            else:
                reason_label = "Unavailable"
            if current_qty >= PAR_LEVEL_GRAMS:
                qty_needed_grams = PAR_LEVEL_GRAMS
            else:
                qty_needed_grams = PAR_LEVEL_GRAMS - current_qty

        restock_data.append(
            _make_restock_row(
                item=name,
                current_qty_grams=current_qty,
                qty_needed_grams=qty_needed_grams,
                reasons=[reason_label],
                expiry_date=expiry_value,
            )
        )
        existing_names.add(name)


def _resolve_order_lines(recipe_data, order):
    """Turn one order's item lines into per-item results and ingredient demand.

    Returns a 3-tuple:
    - item_results: one dict per ordered line (item, qty, recipe_found, requirements)
    - requirement_groups: scaled requirement lists, one per line that found a recipe
    - missing_recipe_items: item names with no matching recipe

    Pure lookup and arithmetic. Touches no inventory and no status table.
    """
    # RF5 (Task 10 "functions that do too much"): extracted from process_orders.
    # Behaviour unchanged — this is the former Step 1 / Step 2 inner loop verbatim.
    item_results = []
    requirement_groups = []
    missing_recipe_items = []

    for item in order["items"]:
        # Step 1: find the recipe for the ordered menu item.
        recipe = find_recipe_by_name(recipe_data, item["item"])

        if recipe is None:
            # Verified (AC14): no crash, no substitution, no invented ingredients.
            # Record recipe_found=False and skip this line's demand. The caller
            # turns a non-empty missing_recipe_items into the formal rejection
            # reason "No matching recipe for item(s): …". Locked by
            # test_process_orders_records_no_matching_recipe_reason.
            item_results.append(
                {
                    "item": item["item"],
                    "qty": item["qty"],
                    "recipe_found": False,
                    "requirements": [],
                }
            )
            missing_recipe_items.append(item["item"])
            continue

        # Step 2: total grams for this line = recipe grams × ordered quantity.
        requirements = calculate_ingredient_requirements(recipe, item["qty"])
        requirement_groups.append(requirements)

        item_results.append(
            {
                "item": item["item"],
                "qty": item["qty"],
                "recipe_found": True,
                "requirements": requirements,
            }
        )

    return item_results, requirement_groups, missing_recipe_items


def _decide_order_outcome(missing_recipe_items, inventory_check, unavailable_details):
    """Return (fulfilled, reason) for one order. Pure — decides, does not act.

    Precedence matches the original if/elif/else chain:
    1. Any missing recipe rejects the order, and the inventory wording is appended
       only when ingredients also failed.
    2. Otherwise, everything available → Delivered.
    3. Otherwise → rejected with the SP7 status-aware ingredient wording.
    """
    # RF5: extracted from process_orders. No deduction, no status write, no
    # mutation of any argument — so the all-or-nothing rule (AC8) cannot be
    # broken here by accident. The caller owns every side effect.
    if missing_recipe_items:
        reason_parts = [
            "No matching recipe for item(s): " + ", ".join(missing_recipe_items)
        ]
        # SP7: include inventory fail wording by detail status when both apply.
        if unavailable_details:
            reason_parts.append(
                _format_unavailable_ingredient_reason(unavailable_details)
            )
        return False, " | ".join(reason_parts)

    if inventory_check["all_available"]:
        return True, "Delivered"

    return False, _format_unavailable_ingredient_reason(unavailable_details)


def _process_single_order(
    recipe_data,
    working_inventory,
    order,
    status_data,
    reference_date,
):
    """Process one order against the working inventory.

    Returns (order_result, failed_details). failed_details is empty for a
    delivered order and otherwise carries the unavailable availability details,
    which the caller merges into restock after all orders (OP15).

    Side effects, deliberately all in this one place:
    - deducts from working_inventory, and only when the whole order is fulfillable
    - writes one row to status_data
    """
    # RF5: extracted from process_orders so the outer function is just the
    # cumulative loop plus the final publish step.
    item_results, requirement_groups, missing_recipe_items = _resolve_order_lines(
        recipe_data, order
    )
    order_requirements = combine_requirements(requirement_groups)

    # Step 3: check the total ingredient demand for the whole order, not per item.
    # Because this reads working_inventory, order 2 is checked against whatever
    # stock remains after order 1 was served. If two orders compete for the same
    # ingredient, the earlier delivered order consumes it first and the later
    # order is evaluated against the reduced quantity that remains.
    inventory_check = check_inventory_availability(
        working_inventory, order_requirements, reference_date
    )
    unavailable_details = [
        detail for detail in inventory_check["details"] if not detail["is_available"]
    ]

    fulfilled, reason = _decide_order_outcome(
        missing_recipe_items, inventory_check, unavailable_details
    )

    if fulfilled:
        # Step 4: deduct the used grams, from the working copy only.
        deduct_inventory(working_inventory, order_requirements)

    # Step 5 / Verified (AC8): a rejected order reaches this line without ever
    # having called deduct_inventory, so no partial stock is consumed. Locked by
    # the without-deduct tests + test_multi_item_order_fails_all_or_nothing.
    update_status_entry(status_data, order["order_id"], fulfilled, reason)

    order_result = {
        "order_id": order["order_id"],
        "brand": order["brand"],
        "items": item_results,
        "order_requirements": order_requirements,
        "inventory_check": inventory_check,
        "fulfilled": fulfilled,
        "reason": reason,
    }
    return order_result, ([] if fulfilled else unavailable_details)


def process_orders(
    recipe_data,
    inventory_data,
    order_data,
    status_data,
    restock_data,
    reference_date=None,
):
    """Process orders, update fulfillment status, deduct inventory, and add restocks."""
    # Step 0 / Verified (AC13): deepcopy working inventory so interim deductions do
    # not mutate the live inventory_data until apply_final_inventory_snapshot.
    # Locked by cumulative tests + test_live_inventory_unchanged_until_final_snapshot.
    # Deferred (AC13 / §9): in-memory simulation only — no database or external
    # persistence in the base assignment.
    # RF5: per-order work now lives in _process_single_order. This function is the
    # cumulative loop and the after-all-orders publish step, nothing else.
    working_inventory = deepcopy(inventory_data)
    processed_orders = []
    failed_unavailable_items = []

    for order in order_data:
        order_result, failed_details = _process_single_order(
            recipe_data, working_inventory, order, status_data, reference_date
        )
        processed_orders.append(order_result)
        failed_unavailable_items.extend(failed_details)

    # Step 6: publish the cumulative result exactly once, after every order, so the
    # live table shows true remaining stock rather than a mid-run figure.
    apply_final_inventory_snapshot(inventory_data, working_inventory)
    # Rebuild from Task 8 final-inventory rules, then merge failed-order gaps (OP15).
    refresh_restock_table(restock_data, inventory_data, reference_date)
    add_failed_order_items_to_restock(restock_data, inventory_data, failed_unavailable_items)

    return processed_orders


def print_order_processing_results(processed_orders):
    """Print recipe lookup, ingredient demand, inventory checks, and fulfillment."""
    print("\n=== Order Processing ===")
    for order in processed_orders:
        print(f"Order ID: {order['order_id']}")
        print(f"Brand: {order['brand']}")

        for item in order["items"]:
            print(f"Item: {item['item']}")
            print(f"Quantity Ordered: {item['qty']}")
            print(f"Recipe Found: {item['recipe_found']}")

            if not item["recipe_found"]:
                print("Inventory Check: Skipped because the recipe was not found.")
                print()
                continue

            print("Required Ingredients:")
            for requirement in item["requirements"]:
                print(
                    f"  - {requirement['name']}: "
                    f"{requirement['required_qty_grams']} grams required"
                )

            print()

        print("Combined Order Requirements:")
        for requirement in order["order_requirements"]:
            print(f"  - {requirement['name']}: {requirement['required_qty_grams']} grams required")

        print(f"All Ingredients Available: {order['inventory_check']['all_available']}")
        print("Inventory Details:")
        for detail in order["inventory_check"]["details"]:
            print(
                f"  - {detail['ingredient']}: "
                f"required={detail['required_qty_grams']} grams, "
                f"available={detail['available_qty_grams']} grams, "
                f"enough={detail['is_available']}"
            )

        print(f"Fulfilled: {order['fulfilled']}")
        print(f"Reason: {order['reason']}")
        print()


def _split_orders_by_delivery(processed_orders):
    """Split processed orders into (delivered, not_delivered) manager-facing entries.

    Not-delivered entries carry a "reason"; delivered entries do not.
    Non-dict rows are skipped defensively.
    """
    # RF6 (Task 10 "functions that do too much"): extracted from build_manager_summary.
    # SM1 / Verified (AC15): fulfilled True → delivered; anything else → not delivered.
    delivered_orders = []
    not_delivered_orders = []

    for order in processed_orders:
        if not isinstance(order, dict):
            continue
        entry = {
            "order_id": order.get("order_id"),
            "brand": order.get("brand", ""),
        }
        if order.get("fulfilled"):
            delivered_orders.append(entry)
        else:
            entry["reason"] = order.get("reason") or "No reason recorded"
            not_delivered_orders.append(entry)

    return delivered_orders, not_delivered_orders


def _summarize_inventory_health(inventory_data, reference_date):
    """Build the final-inventory snapshot and the four attention lists.

    Returns a dict with final_inventory, low_stock, out_of_stock, expired, and
    expiring_soon. Quantity and expiry classification come from
    _classify_inventory_stock_flags so restock and this summary cannot drift apart.
    """
    # RF6: extracted from build_manager_summary.
    # Verified (AC4): expired is days < 0; expiring soon is 0 through
    # EXPIRING_SOON_DAYS inclusive. Expiring soon does not block fulfillment.
    # Verified (AC6) / EH3a: this function CATCHES bad dates. calculate_restock_needs
    # deliberately does not — see §9 "Intentional asymmetries". Do not align them.
    final_inventory = []
    low_stock = []
    out_of_stock = []
    expired = []
    expiring_soon = []

    for item in inventory_data:
        if not isinstance(item, dict):
            continue
        name = item.get("ingredient", "")
        current_qty = item.get("qty_grams", 0)
        if current_qty is None:
            current_qty = 0
        expiry_value = item.get("expiry_date")
        final_inventory.append(
            {
                "ingredient": name,
                "qty_grams": current_qty,
                "expiry_date": expiry_value,
            }
        )

        # Verified (AC6) / EH3a: try/except so a bad date is listed as expired here
        # without raising. Restock still uses a bare call — do not “align” them.
        days_until_expiry = None
        if expiry_value:
            try:
                days_until_expiry = _days_until_expiry(expiry_value, reference_date)
            except (TypeError, ValueError):
                # Intentional catch (summary catch side): quiet expired list entry.
                days_until_expiry = None
                expired.append(name)

        flags = _classify_inventory_stock_flags(current_qty, days_until_expiry)

        # Match prior if/elif: out-of-stock and low-stock are mutually exclusive.
        if flags["out_of_stock"]:
            out_of_stock.append(name)
        elif flags["running_low"]:
            low_stock.append(name)

        # Parsed-date flags only. Bad dates already appended above; classifier
        # received None so it will not add expired/expiring-soon again.
        if days_until_expiry is not None:
            if flags["expired"]:
                expired.append(name)
            elif flags["expiring_soon"]:
                expiring_soon.append(name)

    return {
        "final_inventory": final_inventory,
        "low_stock": low_stock,
        "out_of_stock": out_of_stock,
        "expired": expired,
        "expiring_soon": expiring_soon,
    }


def _render_manager_summary_text(
    delivered_orders,
    not_delivered_orders,
    health,
    restock_recommendations,
    show_inventory,
    show_restock,
):
    """Render the kitchen-manager report text from already-computed results.

    Presentation only — no parsing, no classification, no business rules. The
    inventory and restock blocks are omitted when the caller passed None for
    those arguments (show_* flags), which is why they are parameters and not
    inferred from the lists being empty.
    """
    # RF6: extracted from build_manager_summary. Keeping formatting separate from
    # the rules means output wording can change without touching expiry logic —
    # the "separate logic changes from output-format changes" idea in Part II §1.
    lines = [
        "=== Kitchen Manager Summary ===",
        f"Orders delivered: {len(delivered_orders)}",
        f"Orders not delivered: {len(not_delivered_orders)}",
        "",
        "Reasons for non-delivery:",
    ]
    if not not_delivered_orders:
        lines.append("  None. Every processed order was delivered.")
    else:
        for item in not_delivered_orders:
            lines.append(f"  Order {item['order_id']}: {item['reason']}")

    if show_inventory:
        lines.extend(["", "Final inventory:"])
        if not health["final_inventory"]:
            lines.append("  None recorded.")
        else:
            for item in health["final_inventory"]:
                expiry_label = item["expiry_date"] or "no expiry date"
                lines.append(
                    f"  {item['ingredient']}: {item['qty_grams']} grams "
                    f"(expires {expiry_label})"
                )

        lines.extend(["", "Ingredients that need attention:"])
        for label, names in (
            ("Low stock", health["low_stock"]),
            ("Out of stock", health["out_of_stock"]),
            ("Expired", health["expired"]),
            ("Expiring soon", health["expiring_soon"]),
        ):
            lines.append(f"  {label}: " + (", ".join(names) if names else "none"))

    if show_restock:
        lines.extend(["", "Restock recommendations:"])
        if not restock_recommendations:
            lines.append("  None.")
        else:
            for row in restock_recommendations:
                item_name = row.get("item", "")
                qty_needed = row.get("qty_needed_grams", 0)
                reason = row.get("reason", "")
                lines.append(f"  {item_name}: {qty_needed} grams needed — {reason}")

    return "\n".join(lines)


def build_manager_summary(
    processed_orders,
    inventory_data=None,
    restock_data=None,
    reference_date=None,
):
    """Summarize orders, final inventory, restock, and expiry for a kitchen manager."""
    # SM1 / Verified (AC15): fulfilled True → delivered; anything else → not delivered.
    # SM2 / DR3: final inventory, restock, and low / out / expired / expiring-soon
    # lists. Qty and parsed-expiry flags come from _classify_inventory_stock_flags.
    # Verified (AC4): expired is days < 0; expiring soon is 0 through
    # EXPIRING_SOON_DAYS inclusive. Expiring soon does not block fulfillment.
    # Verified (AC6) / EH3a: summary catches bad dates (quiet expired list); restock
    # does not. Same asymmetry as availability. See try/except on parse below.
    # Raise-side lock: test_restock_raises_on_malformed_expiry_date.
    # Verified (AC15): caller passes the live restock table so OP15 rows are
    # included — this function does not rebuild restock. Locked by
    # test_summary_counts_match_processed_orders_and_include_live_restock.
    # Verified (AC15 / SM3): main() prints summary["text"] and returns the dict;
    # do not print here. No Markdown report file.
    if not processed_orders:
        processed_orders = []
    show_inventory = inventory_data is not None
    show_restock = restock_data is not None
    if inventory_data is None:
        inventory_data = []
    if restock_data is None:
        restock_data = []
    # DR8: default reference_date via _resolve_reference_date (still SIMULATION_DATE).
    reference_date = _resolve_reference_date(reference_date)

    delivered_orders, not_delivered_orders = _split_orders_by_delivery(processed_orders)
    health = _summarize_inventory_health(inventory_data, reference_date)
    restock_recommendations = [row for row in restock_data if isinstance(row, dict)]

    text = _render_manager_summary_text(
        delivered_orders,
        not_delivered_orders,
        health,
        restock_recommendations,
        show_inventory,
        show_restock,
    )

    return {
        "delivered_count": len(delivered_orders),
        "not_delivered_count": len(not_delivered_orders),
        "delivered_orders": delivered_orders,
        "not_delivered_orders": not_delivered_orders,
        "final_inventory": health["final_inventory"],
        "restock_recommendations": restock_recommendations,
        "low_stock": health["low_stock"],
        "out_of_stock": health["out_of_stock"],
        "expired": health["expired"],
        "expiring_soon": health["expiring_soon"],
        "text": text,
    }


def main():
    """Load and print seed tables, process orders, then show the manager summary."""
    # DC7 / Verified (AC15): print Recipes, Inventory, Orders, Restock, and Status
    # from the loaders before any processing (Decision-Maker display order).
    # Verified (AC15 / SM3): after processing, print updated inventory / restock /
    # status, then print the manager summary text and return the summary dict.
    # No Markdown/text report file (extra-credit option D only). Locked by
    # test_main_prints_all_five_seed_tables_before_processing,
    # test_main_prints_and_returns_manager_summary, and SP3 evidence in
    # WRITTEN_RESPONSE.MD.
    recipe_data = load_recipes()
    inventory_data = load_inventory()
    order_data = load_orders()
    restock_data = load_restock()
    status_data = load_status()

    print_recipes(recipe_data)
    print_inventory(inventory_data)
    print_orders(order_data)
    print_restock(restock_data)
    print_status(status_data)

    working_inventory = deepcopy(inventory_data)
    working_status = deepcopy(status_data)
    live_restock = []
    processed_orders = process_orders(
        recipe_data,
        working_inventory,
        order_data,
        working_status,
        live_restock,
        reference_date=SIMULATION_DATE,
    )

    print_order_processing_results(processed_orders)
    print_inventory(working_inventory)
    print_restock(live_restock)
    print_status(working_status)

    summary = build_manager_summary(
        processed_orders,
        inventory_data=working_inventory,
        restock_data=live_restock,
        reference_date=SIMULATION_DATE,
    )
    print()
    print(summary["text"])
    return summary


if __name__ == "__main__":
    main()
