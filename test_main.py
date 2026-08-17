"""Unit tests for the baseline seed-data loading functions."""

from contextlib import redirect_stdout
from copy import deepcopy
from datetime import date
from io import StringIO
from unittest.mock import patch
import unittest

import seed_data
from main import (
    EXPIRING_SOON_DAYS,
    PAR_LEVEL_GRAMS,
    RUNNING_LOW_THRESHOLD_GRAMS,
    SIMULATION_DATE,
    _classify_inventory_stock_flags,
    _format_unavailable_ingredient_reason,
    _inventory_by_name,
    _make_restock_row,
    _resolve_reference_date,
    apply_final_inventory_snapshot,
    add_failed_order_items_to_restock,
    build_manager_summary,
    calculate_ingredient_requirements,
    calculate_restock_needs,
    check_inventory_availability,
    find_recipe_by_name,
    load_inventory,
    load_orders,
    load_recipes,
    load_restock,
    load_status,
    main,
    process_orders,
    refresh_restock_table,
    update_status_entry,
)


class TestLoadFunctions(unittest.TestCase):
    """Verify the Task 1 data-loading helpers return the expected seed tables."""

    def test_seed_data_module_imports_all_five_tables(self):
        """DC1: main.py must be able to import the five tables from seed_data."""
        # Assumption to verify: the module name is seed_data, matching seed_data.py.
        self.assertTrue(hasattr(seed_data, "recipes"))
        self.assertTrue(hasattr(seed_data, "inventory"))
        self.assertTrue(hasattr(seed_data, "orders"))
        self.assertTrue(hasattr(seed_data, "restock"))
        self.assertTrue(hasattr(seed_data, "status"))
        self.assertIsInstance(seed_data.recipes, list)
        self.assertIsInstance(seed_data.inventory, list)
        self.assertIsInstance(seed_data.orders, list)
        self.assertIsInstance(seed_data.restock, list)
        self.assertIsInstance(seed_data.status, list)

    def test_loads_all_five_tables_successfully(self):
        """Each load function should return a non-empty list from seed_data."""
        # Assumption to verify: Task 1 considers a successful import equivalent to
        # each loader returning the seeded module-level list without raising errors.
        self.assertIsInstance(load_recipes(), list)
        self.assertIsInstance(load_inventory(), list)
        self.assertIsInstance(load_orders(), list)
        self.assertIsInstance(load_restock(), list)
        self.assertIsInstance(load_status(), list)

        self.assertGreater(len(load_recipes()), 0)
        self.assertGreater(len(load_inventory()), 0)
        self.assertGreater(len(load_orders()), 0)
        self.assertGreater(len(load_restock()), 0)
        self.assertGreater(len(load_status()), 0)

    def test_record_counts_match_seed_data(self):
        """Each load function should return the expected number of seed records."""
        self.assertEqual(len(load_recipes()), 5)
        self.assertEqual(len(load_inventory()), 14)
        self.assertEqual(len(load_orders()), 5)
        self.assertEqual(len(load_restock()), 5)
        self.assertEqual(len(load_status()), 5)

    def test_recipe_key_field_types(self):
        """Recipe records should expose the expected identifier and ingredient types."""
        recipe = load_recipes()[0]
        ingredient = recipe["ingredients"][0]

        self.assertIsInstance(recipe["recipe_id"], int)
        self.assertIsInstance(recipe["name"], str)
        self.assertIsInstance(recipe["ingredients"], list)
        self.assertIsInstance(ingredient["name"], str)
        self.assertIsInstance(ingredient["qty_grams"], (int, float))

    def test_inventory_key_field_types(self):
        """Inventory records should provide valid quantity and expiry field types."""
        item = load_inventory()[0]

        self.assertIsInstance(item["ingredient"], str)
        self.assertIsInstance(item["qty_grams"], (int, float))
        self.assertIsInstance(item["expiry_date"], str)

    def test_all_seed_quantities_are_grams_including_buns(self):
        """AC2: every seed quantity field is qty_grams, including Bun."""
        # Inventory: Bun is stocked as grams, not unit counts.
        bun_inventory = next(
            item for item in load_inventory() if item["ingredient"] == "Bun"
        )
        self.assertIn("qty_grams", bun_inventory)
        self.assertIsInstance(bun_inventory["qty_grams"], (int, float))
        self.assertNotIn("qty", bun_inventory)
        self.assertNotIn("qty_units", bun_inventory)

        # Recipes: Bun ingredient amounts are also qty_grams.
        burger = next(
            recipe for recipe in load_recipes() if recipe["name"] == "Chicken Burger"
        )
        bun_ingredient = next(
            ingredient
            for ingredient in burger["ingredients"]
            if ingredient["name"] == "Bun"
        )
        self.assertIn("qty_grams", bun_ingredient)
        self.assertIsInstance(bun_ingredient["qty_grams"], (int, float))

        # Every inventory row uses the grams field name.
        for item in load_inventory():
            self.assertIn("qty_grams", item)
            self.assertIsInstance(item["qty_grams"], (int, float))

    def test_order_key_field_types(self):
        """Order records should expose valid identifiers, brands, and quantities."""
        order = load_orders()[0]
        item = order["items"][0]

        self.assertIsInstance(order["order_id"], int)
        self.assertIsInstance(order["brand"], str)
        self.assertIsInstance(order["items"], list)
        self.assertIsInstance(item["item"], str)
        self.assertIsInstance(item["qty"], int)

    def test_restock_key_field_types(self):
        """Restock records should provide an item name, numeric quantity, and reason."""
        item = load_restock()[0]

        self.assertIsInstance(item["item"], str)
        self.assertIsInstance(item["qty_needed_grams"], (int, float))
        self.assertIsInstance(item["reason"], str)

    def test_status_key_field_types(self):
        """Status records should provide order linkage and delivery state types."""
        item = load_status()[0]

        self.assertIsInstance(item["order_id"], int)
        self.assertIsInstance(item["delivered"], bool)
        self.assertIsInstance(item["remark"], str)
        # Incomplete / follow-up: if the project later formalizes a status enum or
        # richer state machine, these tests should be expanded beyond simple types.

    def test_main_prints_all_five_seed_tables_before_processing(self):
        """DC7: main() must print all five seed tables, including seed Restock."""
        captured = StringIO()
        with redirect_stdout(captured):
            main()
        output = captured.getvalue()

        recipes_at = output.find("=== Recipes ===")
        inventory_at = output.find("=== Inventory ===")
        orders_at = output.find("=== Orders ===")
        restock_at = output.find("=== Restock ===")
        status_at = output.find("=== Status ===")
        processing_at = output.find("=== Order Processing ===")

        self.assertNotEqual(recipes_at, -1)
        self.assertNotEqual(inventory_at, -1)
        self.assertNotEqual(orders_at, -1)
        self.assertNotEqual(restock_at, -1)
        self.assertNotEqual(status_at, -1)
        self.assertNotEqual(processing_at, -1)

        self.assertLess(recipes_at, inventory_at)
        self.assertLess(inventory_at, orders_at)
        self.assertLess(orders_at, restock_at)
        self.assertLess(restock_at, status_at)
        self.assertLess(status_at, processing_at)

        seed_restock = output[restock_at:processing_at]
        self.assertIn("Item: Flour", seed_restock)
        self.assertIn("Reason: Running low stock", seed_restock)
        self.assertIn("Reason: Out of stock", seed_restock)

    def test_main_prints_and_returns_manager_summary(self):
        """SM3: main() prints the manager summary and returns the summary dict."""
        captured = StringIO()
        with redirect_stdout(captured):
            summary = main()
        output = captured.getvalue()

        processing_at = output.find("=== Order Processing ===")
        summary_at = output.find("=== Kitchen Manager Summary ===")
        self.assertNotEqual(summary_at, -1)
        self.assertLess(processing_at, summary_at)
        self.assertIn("Orders delivered:", output)
        self.assertIn("Orders not delivered:", output)
        self.assertIn("Reasons for non-delivery:", output)
        self.assertIsInstance(summary, dict)
        self.assertIn("delivered_count", summary)
        self.assertIn("not_delivered_count", summary)
        self.assertIn("text", summary)


class TestUpdateStatusEntry(unittest.TestCase):
    """AC9: seed status is initial only; update in place or append for new ids."""

    def test_update_status_entry_updates_existing_row(self):
        status_data = [
            {"order_id": 1, "delivered": False, "remark": "Not Delivered"}
        ]
        update_status_entry(status_data, 1, True, "Delivered")
        self.assertEqual(len(status_data), 1)
        self.assertTrue(status_data[0]["delivered"])
        self.assertEqual(status_data[0]["remark"], "Delivered")

    def test_update_status_entry_appends_when_order_id_is_new(self):
        status_data = [
            {"order_id": 1, "delivered": True, "remark": "Delivered"}
        ]
        update_status_entry(status_data, 99, False, "Missing Bun")
        self.assertEqual(len(status_data), 2)
        self.assertEqual(status_data[1]["order_id"], 99)
        self.assertFalse(status_data[1]["delivered"])
        self.assertEqual(status_data[1]["remark"], "Missing Bun")

    def test_seed_status_is_initial_table_matching_seed_order_ids(self):
        """load_status returns baseline rows; it does not process orders."""
        seed_status_ids = [row["order_id"] for row in load_status()]
        seed_order_ids = [row["order_id"] for row in load_orders()]
        self.assertEqual(seed_status_ids, seed_order_ids)


class TestOrderRecipeLookup(unittest.TestCase):
    """Verify order items can be matched to recipes and scaled correctly."""

    def test_find_recipe_by_name_returns_matching_recipe(self):
        """A valid order item should return its matching recipe record."""
        recipe = find_recipe_by_name(load_recipes(), "Chicken Burger")

        self.assertIsNotNone(recipe)
        self.assertEqual(recipe["recipe_id"], 2)
        self.assertEqual(recipe["name"], "Chicken Burger")

    def test_find_recipe_by_name_handles_missing_recipe_gracefully(self):
        """A missing order item should return None instead of raising an error."""
        recipe = find_recipe_by_name(load_recipes(), "Paneer Wrap")

        self.assertIsNone(recipe)

    def test_find_recipe_by_name_requires_exact_case_match(self):
        """AC3: case/whitespace differences must not match; no folding or aliases."""
        recipes = load_recipes()
        self.assertIsNotNone(find_recipe_by_name(recipes, "Chicken Burger"))
        self.assertIsNone(find_recipe_by_name(recipes, "chicken burger"))
        self.assertIsNone(find_recipe_by_name(recipes, "CHICKEN BURGER"))
        self.assertIsNone(find_recipe_by_name(recipes, " Chicken Burger"))
        self.assertIsNone(find_recipe_by_name(recipes, "Chicken Burger "))

    def test_calculate_ingredient_requirements_scales_for_quantity_two(self):
        """Ingredient requirements should double when the order quantity is two."""
        recipe = find_recipe_by_name(load_recipes(), "Margherita Pizza")
        requirements = calculate_ingredient_requirements(recipe, 2)

        expected_requirements = [
            {"name": "Flour", "required_qty_grams": 600},
            {"name": "Tomato Sauce", "required_qty_grams": 200},
            {"name": "Mozzarella Cheese", "required_qty_grams": 300},
        ]

        self.assertEqual(requirements, expected_requirements)


class TestInventoryAvailability(unittest.TestCase):
    """Verify quantity and expiry checks for OP6. Tests pass an explicit date."""

    def test_all_ingredients_available_and_unexpired(self):
        """Enough unexpired stock should be available."""
        inventory_data = [
            {"ingredient": "Flour", "qty_grams": 1000, "expiry_date": "2026-12-31"},
        ]
        requirements = [{"name": "Flour", "required_qty_grams": 300}]
        result = check_inventory_availability(
            inventory_data, requirements, reference_date=date(2026, 5, 10)
        )

        self.assertTrue(result["all_available"])
        self.assertEqual(result["details"][0]["status"], "ok")
        self.assertFalse(result["details"][0]["is_expired"])

    def test_missing_ingredient(self):
        """A required ingredient not in inventory should be marked missing."""
        inventory_data = [
            {"ingredient": "Flour", "qty_grams": 1000, "expiry_date": "2026-12-31"},
        ]
        requirements = [{"name": "Chocolate", "required_qty_grams": 150}]
        result = check_inventory_availability(
            inventory_data, requirements, reference_date=date(2026, 5, 10)
        )

        self.assertFalse(result["all_available"])
        self.assertEqual(result["details"][0]["status"], "missing")
        self.assertFalse(result["details"][0]["is_available"])

    def test_insufficient_quantity(self):
        """Unexpired stock below the required grams should be insufficient."""
        inventory_data = [
            {"ingredient": "Bun", "qty_grams": 50, "expiry_date": "2026-12-31"},
        ]
        requirements = [{"name": "Bun", "required_qty_grams": 100}]
        result = check_inventory_availability(
            inventory_data, requirements, reference_date=date(2026, 5, 10)
        )

        self.assertFalse(result["all_available"])
        self.assertEqual(result["details"][0]["status"], "insufficient")
        self.assertFalse(result["details"][0]["is_expired"])

    def test_expired_ingredient_blocks_fulfillment(self):
        """Past expiry (days < 0) makes the ingredient unusable even if qty is high."""
        inventory_data = [
            {"ingredient": "Chocolate", "qty_grams": 10000, "expiry_date": "2026-01-15"},
        ]
        requirements = [{"name": "Chocolate", "required_qty_grams": 150}]
        result = check_inventory_availability(
            inventory_data, requirements, reference_date=date(2026, 5, 10)
        )

        self.assertFalse(result["all_available"])
        self.assertEqual(result["details"][0]["status"], "expired")
        self.assertTrue(result["details"][0]["is_expired"])
        self.assertFalse(result["details"][0]["is_available"])

    def test_expiring_soon_does_not_block_fulfillment(self):
        """Expiring soon must not fail availability; it is restock-only."""
        inventory_data = [
            {"ingredient": "Flour", "qty_grams": 10000, "expiry_date": "2026-05-12"},
        ]
        requirements = [{"name": "Flour", "required_qty_grams": 300}]
        result = check_inventory_availability(
            inventory_data, requirements, reference_date=date(2026, 5, 10)
        )

        self.assertTrue(result["all_available"])
        self.assertEqual(result["details"][0]["status"], "ok")
        self.assertFalse(result["details"][0]["is_expired"])

    def test_invalid_expiry_date_is_unusable(self):
        """A malformed expiry date should make the ingredient unusable."""
        inventory_data = [
            {"ingredient": "Flour", "qty_grams": 10000, "expiry_date": "not-a-date"},
        ]
        requirements = [{"name": "Flour", "required_qty_grams": 300}]
        result = check_inventory_availability(
            inventory_data, requirements, reference_date=date(2026, 5, 10)
        )

        self.assertFalse(result["all_available"])
        self.assertEqual(result["details"][0]["status"], "unusable")
        self.assertTrue(result["details"][0]["is_expired"])

    def test_none_inventory_does_not_crash(self):
        """None inventory should be treated as empty, not raise."""
        requirements = [{"name": "Flour", "required_qty_grams": 300}]
        result = check_inventory_availability(
            None, requirements, reference_date=date(2026, 5, 10)
        )

        self.assertFalse(result["all_available"])
        self.assertEqual(result["details"][0]["status"], "missing")

    def test_none_requirements_does_not_crash(self):
        """None requirements should be treated as an empty list, not raise."""
        inventory_data = [
            {"ingredient": "Flour", "qty_grams": 1000, "expiry_date": "2026-12-31"},
        ]
        result = check_inventory_availability(
            inventory_data, None, reference_date=date(2026, 5, 10)
        )

        self.assertTrue(result["all_available"])
        self.assertEqual(result["details"], [])

    def test_empty_requirement_list_is_available(self):
        """An empty requirement list means nothing is required."""
        inventory_data = [
            {"ingredient": "Flour", "qty_grams": 1000, "expiry_date": "2026-12-31"},
        ]
        result = check_inventory_availability(
            inventory_data, [], reference_date=date(2026, 5, 10)
        )

        self.assertTrue(result["all_available"])
        self.assertEqual(result["details"], [])

    def test_negative_quantity_is_not_valid_demand(self):
        """A negative required quantity must not pass as available."""
        inventory_data = [
            {"ingredient": "Flour", "qty_grams": 10000, "expiry_date": "2026-12-31"},
        ]
        requirements = [{"name": "Flour", "required_qty_grams": -100}]
        result = check_inventory_availability(
            inventory_data, requirements, reference_date=date(2026, 5, 10)
        )

        self.assertFalse(result["all_available"])
        self.assertEqual(result["details"][0]["status"], "invalid")
        self.assertFalse(result["details"][0]["is_available"])

    def test_availability_default_reference_date_is_simulation_date(self):
        """AC5: omitting reference_date uses SIMULATION_DATE, not date.today()."""
        inventory_data = [
            {"ingredient": "Chocolate", "qty_grams": 10000, "expiry_date": "2026-01-15"},
        ]
        requirements = [{"name": "Chocolate", "required_qty_grams": 150}]
        # No reference_date argument — must use SIMULATION_DATE (2026-05-10).
        result = check_inventory_availability(inventory_data, requirements)

        self.assertEqual(SIMULATION_DATE, date(2026, 5, 10))
        self.assertFalse(result["all_available"])
        self.assertEqual(result["details"][0]["status"], "expired")


class TestOrderFulfillment(unittest.TestCase):
    """Verify fulfillment updates status, restock, and inventory correctly."""

    def test_process_orders_records_no_matching_recipe_reason(self):
        """AC14: missing recipe rejects the order with a formal reason; no invent."""
        recipe_data = deepcopy(load_recipes())
        inventory_data = deepcopy(load_inventory())
        before = {
            item["ingredient"]: item["qty_grams"] for item in inventory_data
        }
        order_data = [
            {
                "order_id": 902,
                "brand": "Test Kitchen",
                "items": [{"item": "Unicorn Sandwich", "qty": 1}],
            }
        ]
        status_data = []
        restock_data = []

        processed = process_orders(
            recipe_data,
            inventory_data,
            order_data,
            status_data,
            restock_data,
            reference_date=date(2026, 6, 3),
        )

        self.assertFalse(processed[0]["fulfilled"])
        self.assertIn(
            "No matching recipe for item(s): Unicorn Sandwich",
            processed[0]["reason"],
        )
        self.assertFalse(processed[0]["items"][0]["recipe_found"])
        self.assertEqual(processed[0]["items"][0]["requirements"], [])
        self.assertEqual(processed[0]["order_requirements"], [])
        self.assertEqual(status_data[0]["order_id"], 902)
        self.assertFalse(status_data[0]["delivered"])
        self.assertEqual(status_data[0]["remark"], processed[0]["reason"])
        after = {
            item["ingredient"]: item["qty_grams"] for item in inventory_data
        }
        self.assertEqual(after, before)

    def test_process_orders_empty_order_data_returns_empty_list(self):
        """EH2a: empty order_data returns [] and does not raise."""
        recipe_data = deepcopy(load_recipes())
        inventory_data = deepcopy(load_inventory())
        before = {
            item["ingredient"]: item["qty_grams"] for item in inventory_data
        }
        status_data = []
        restock_data = [{"item": "seed-only", "qty_needed_grams": 1, "reason": "seed"}]

        processed = process_orders(
            recipe_data,
            inventory_data,
            [],
            status_data,
            restock_data,
            reference_date=date(2026, 5, 10),
        )

        self.assertEqual(processed, [])
        self.assertEqual(status_data, [])
        after = {
            item["ingredient"]: item["qty_grams"] for item in inventory_data
        }
        self.assertEqual(after, before)
        # Restock still rebuilt from final inventory (loop never ran).
        self.assertTrue(isinstance(restock_data, list))
        self.assertNotIn("seed-only", [row.get("item") for row in restock_data])

    def test_process_orders_marks_delivered_when_ingredients_are_available(self):
        """An order with sufficient stock should be marked as delivered."""
        recipe_data = deepcopy(load_recipes())
        inventory_data = deepcopy(load_inventory())
        status_data = deepcopy(load_status())
        restock_data = deepcopy(load_restock())
        order_data = [
            {
                "order_id": 101,
                "brand": "Test Kitchen",
                "items": [{"item": "Chicken Burger", "qty": 1}],
            }
        ]

        processed_orders = process_orders(
            recipe_data, inventory_data, order_data, status_data, restock_data
        )

        self.assertTrue(processed_orders[0]["fulfilled"])
        self.assertEqual(processed_orders[0]["reason"], "Delivered")
        self.assertEqual(status_data[-1]["order_id"], 101)
        self.assertTrue(status_data[-1]["delivered"])
        self.assertEqual(status_data[-1]["remark"], "Delivered")

    def test_process_orders_marks_not_delivered_and_adds_missing_item_to_restock(self):
        """An order with a missing ingredient should fail and log the shortage."""
        recipe_data = [
            {
                "recipe_id": 1,
                "name": "Test Wrap",
                "ingredients": [
                    {"name": "Chicken Breast", "qty_grams": 200},
                    {"name": "Bun", "qty_grams": 100},
                ],
            }
        ]
        inventory_data = [
            {"ingredient": "Chicken Breast", "qty_grams": 500, "expiry_date": "2026-12-31"},
            {"ingredient": "Bun", "qty_grams": 0, "expiry_date": "2026-12-31"},
        ]
        order_data = [
            {"order_id": 202, "brand": "Test Kitchen", "items": [{"item": "Test Wrap", "qty": 1}]}
        ]
        status_data = []
        restock_data = []

        processed_orders = process_orders(
            recipe_data,
            inventory_data,
            order_data,
            status_data,
            restock_data,
            reference_date=date(2026, 6, 3),
        )

        self.assertFalse(processed_orders[0]["fulfilled"])
        self.assertIn("Missing or insufficient ingredients: Bun", processed_orders[0]["reason"])
        self.assertEqual(status_data[0]["order_id"], 202)
        self.assertFalse(status_data[0]["delivered"])
        self.assertIn("Bun", status_data[0]["remark"])
        bun_restock = next(item for item in restock_data if item["item"] == "Bun")
        self.assertEqual(bun_restock["qty_needed_grams"], 10000)
        self.assertEqual(bun_restock["reason"], "Out of stock")
        bun_rows = [item for item in restock_data if item["item"] == "Bun"]
        self.assertEqual(len(bun_rows), 1)

    def test_failed_order_missing_inventory_item_appears_on_restock(self):
        """A failed order's missing ingredient must appear on restock once."""
        recipe_data = [
            {
                "recipe_id": 1,
                "name": "Test Wrap",
                "ingredients": [
                    {"name": "Chicken Breast", "qty_grams": 200},
                    {"name": "Pickles", "qty_grams": 50},
                ],
            }
        ]
        inventory_data = [
            {"ingredient": "Chicken Breast", "qty_grams": 10000, "expiry_date": "2026-12-31"},
        ]
        original_chicken = inventory_data[0]["qty_grams"]
        order_data = [
            {"order_id": 203, "brand": "Test Kitchen", "items": [{"item": "Test Wrap", "qty": 1}]}
        ]
        status_data = []
        restock_data = []

        processed_orders = process_orders(
            recipe_data,
            inventory_data,
            order_data,
            status_data,
            restock_data,
            reference_date=date(2026, 6, 3),
        )

        self.assertFalse(processed_orders[0]["fulfilled"])
        self.assertEqual(inventory_data[0]["qty_grams"], original_chicken)
        pickle_rows = [item for item in restock_data if item["item"] == "Pickles"]
        self.assertEqual(len(pickle_rows), 1)
        self.assertEqual(pickle_rows[0]["current_qty_grams"], 0)
        self.assertEqual(pickle_rows[0]["qty_needed_grams"], 10000)
        self.assertIn("Missing from inventory", pickle_rows[0]["reasons"])

    def test_failed_order_expired_item_appears_on_restock_without_deduct(self):
        """Expired high-qty stock that blocked fulfillment must appear on restock."""
        recipe_data = [
            {
                "recipe_id": 1,
                "name": "Chocolate Cake",
                "ingredients": [{"name": "Chocolate", "qty_grams": 150}],
            }
        ]
        inventory_data = [
            {"ingredient": "Chocolate", "qty_grams": 10000, "expiry_date": "2026-01-15"},
        ]
        order_data = [
            {"order_id": 204, "brand": "Test Kitchen", "items": [{"item": "Chocolate Cake", "qty": 1}]}
        ]
        status_data = []
        restock_data = []

        processed_orders = process_orders(
            recipe_data,
            inventory_data,
            order_data,
            status_data,
            restock_data,
            reference_date=date(2026, 5, 10),
        )

        self.assertFalse(processed_orders[0]["fulfilled"])
        self.assertEqual(inventory_data[0]["qty_grams"], 10000)
        self.assertIn("Expired ingredients: Chocolate", processed_orders[0]["reason"])
        self.assertEqual(status_data[0]["remark"], processed_orders[0]["reason"])
        chocolate_rows = [item for item in restock_data if item["item"] == "Chocolate"]
        self.assertEqual(len(chocolate_rows), 1)
        self.assertIn("Expired", chocolate_rows[0]["reasons"])
        self.assertEqual(chocolate_rows[0]["expiry_date"], "2026-01-15")
        # AC12: expired stock already at par still requests a full par replacement.
        self.assertEqual(chocolate_rows[0]["current_qty_grams"], 10000)
        self.assertEqual(chocolate_rows[0]["qty_needed_grams"], PAR_LEVEL_GRAMS)

    def test_fail_reason_names_expired_clearly_without_deduct(self):
        """SP7: expired fail-reason/status remark must say Expired, not only missing."""
        recipe_data = [
            {
                "recipe_id": 1,
                "name": "Mixed Fail Plate",
                "ingredients": [
                    {"name": "Chocolate", "qty_grams": 150},
                    {"name": "Bun", "qty_grams": 50},
                ],
            }
        ]
        inventory_data = [
            {"ingredient": "Chocolate", "qty_grams": 10000, "expiry_date": "2026-01-15"},
            {"ingredient": "Bun", "qty_grams": 0, "expiry_date": "2026-12-31"},
        ]
        order_data = [
            {
                "order_id": 207,
                "brand": "Test Kitchen",
                "items": [{"item": "Mixed Fail Plate", "qty": 1}],
            }
        ]
        status_data = []
        restock_data = []

        processed_orders = process_orders(
            recipe_data,
            inventory_data,
            order_data,
            status_data,
            restock_data,
            reference_date=date(2026, 5, 10),
        )

        reason = processed_orders[0]["reason"]
        self.assertFalse(processed_orders[0]["fulfilled"])
        self.assertIn("Expired ingredients: Chocolate", reason)
        self.assertIn("Missing or insufficient ingredients: Bun", reason)
        self.assertEqual(status_data[0]["remark"], reason)
        # Deduction behavior unchanged: no grams removed on failure.
        self.assertEqual(inventory_data[0]["qty_grams"], 10000)
        self.assertEqual(inventory_data[1]["qty_grams"], 0)

    def test_format_unavailable_reason_names_expired_and_unusable(self):
        """SP7/AC10: helper labels expired/unusable; invalid stays with shortages."""
        reason = _format_unavailable_ingredient_reason(
            [
                {"ingredient": "Chocolate", "status": "expired"},
                {"ingredient": "Flour", "status": "unusable"},
                {"ingredient": "Bun", "status": "insufficient"},
            ]
        )
        self.assertEqual(
            reason,
            "Expired ingredients: Chocolate | Unusable ingredients: Flour | "
            "Missing or insufficient ingredients: Bun",
        )
        invalid_reason = _format_unavailable_ingredient_reason(
            [{"ingredient": "Weird Qty", "status": "invalid"}]
        )
        self.assertEqual(
            invalid_reason,
            "Missing or insufficient ingredients: Weird Qty",
        )

    def test_two_failed_orders_same_missing_item_do_not_duplicate_restock(self):
        """The same missing ingredient from two failed orders is one restock row."""
        recipe_data = [
            {
                "recipe_id": 1,
                "name": "Test Wrap",
                "ingredients": [{"name": "Pickles", "qty_grams": 50}],
            }
        ]
        inventory_data = []
        order_data = [
            {"order_id": 205, "brand": "Test Kitchen", "items": [{"item": "Test Wrap", "qty": 1}]},
            {"order_id": 206, "brand": "Test Kitchen", "items": [{"item": "Test Wrap", "qty": 1}]},
        ]
        status_data = []
        restock_data = []

        process_orders(
            recipe_data,
            inventory_data,
            order_data,
            status_data,
            restock_data,
            reference_date=date(2026, 6, 3),
        )

        pickle_rows = [item for item in restock_data if item["item"] == "Pickles"]
        self.assertEqual(len(pickle_rows), 1)


class TestAddFailedOrderItemsToRestock(unittest.TestCase):
    """AC12: OP15 one-row-per-name, missing→full par, expired-at-par→full par."""

    def test_skips_name_already_on_restock_table(self):
        restock_data = [
            _make_restock_row(
                item="Pickles",
                current_qty_grams=0,
                qty_needed_grams=PAR_LEVEL_GRAMS,
                reasons=["Out of stock"],
                expiry_date=None,
            )
        ]
        add_failed_order_items_to_restock(
            restock_data,
            inventory_data=[],
            failed_items=[{"ingredient": "Pickles", "status": "missing"}],
        )
        self.assertEqual(len(restock_data), 1)
        self.assertEqual(restock_data[0]["reasons"], ["Out of stock"])

    def test_missing_from_inventory_requests_full_par(self):
        restock_data = []
        add_failed_order_items_to_restock(
            restock_data,
            inventory_data=[],
            failed_items=[{"ingredient": "Pickles", "status": "missing"}],
        )
        self.assertEqual(len(restock_data), 1)
        self.assertEqual(restock_data[0]["qty_needed_grams"], PAR_LEVEL_GRAMS)
        self.assertEqual(restock_data[0]["reasons"], ["Missing from inventory"])

    def test_expired_at_or_above_par_requests_full_par(self):
        restock_data = []
        inventory_data = [
            {
                "ingredient": "Chocolate",
                "qty_grams": PAR_LEVEL_GRAMS,
                "expiry_date": "2026-01-01",
            }
        ]
        add_failed_order_items_to_restock(
            restock_data,
            inventory_data,
            failed_items=[{"ingredient": "Chocolate", "status": "expired"}],
        )
        self.assertEqual(len(restock_data), 1)
        self.assertEqual(restock_data[0]["current_qty_grams"], PAR_LEVEL_GRAMS)
        self.assertEqual(restock_data[0]["qty_needed_grams"], PAR_LEVEL_GRAMS)
        self.assertEqual(restock_data[0]["reasons"], ["Expired"])


class TestProcessOrdersDeduction(unittest.TestCase):
    """Delivered orders deduct; kept separate from OP15 AC12 helpers."""

    def test_process_orders_deducts_inventory_after_successful_delivery(self):
        """A delivered order should reduce inventory by the required grams."""
        recipe_data = deepcopy(load_recipes())
        inventory_data = deepcopy(load_inventory())
        status_data = []
        restock_data = []
        order_data = [
            {
                "order_id": 303,
                "brand": "Test Kitchen",
                "items": [{"item": "Margherita Pizza", "qty": 2}],
            }
        ]

        original_flour_qty = next(
            item["qty_grams"] for item in inventory_data if item["ingredient"] == "Flour"
        )
        original_sauce_qty = next(
            item["qty_grams"] for item in inventory_data if item["ingredient"] == "Tomato Sauce"
        )
        original_cheese_qty = next(
            item["qty_grams"]
            for item in inventory_data
            if item["ingredient"] == "Mozzarella Cheese"
        )

        process_orders(recipe_data, inventory_data, order_data, status_data, restock_data)

        updated_flour_qty = next(
            item["qty_grams"] for item in inventory_data if item["ingredient"] == "Flour"
        )
        updated_sauce_qty = next(
            item["qty_grams"] for item in inventory_data if item["ingredient"] == "Tomato Sauce"
        )
        updated_cheese_qty = next(
            item["qty_grams"]
            for item in inventory_data
            if item["ingredient"] == "Mozzarella Cheese"
        )

        self.assertEqual(updated_flour_qty, original_flour_qty - 600)
        self.assertEqual(updated_sauce_qty, original_sauce_qty - 200)
        self.assertEqual(updated_cheese_qty, original_cheese_qty - 300)

    def test_multi_item_order_fails_all_or_nothing_without_partial_deduct(self):
        """AC8: one unavailable item rejects the whole order; pizza stock untouched."""
        recipe_data = deepcopy(load_recipes())
        inventory_data = deepcopy(load_inventory())
        for item in inventory_data:
            if item["ingredient"] == "Bun":
                item["qty_grams"] = 0
        before = {
            item["ingredient"]: item["qty_grams"] for item in inventory_data
        }
        order_data = [
            {
                "order_id": 801,
                "brand": "Test Kitchen",
                "items": [
                    {"item": "Margherita Pizza", "qty": 1},
                    {"item": "Chicken Burger", "qty": 1},
                ],
            }
        ]
        status_data = []
        restock_data = []

        processed = process_orders(
            recipe_data,
            inventory_data,
            order_data,
            status_data,
            restock_data,
            reference_date=date(2026, 6, 3),
        )

        self.assertFalse(processed[0]["fulfilled"])
        self.assertIn("Bun", processed[0]["reason"])
        after = {
            item["ingredient"]: item["qty_grams"] for item in inventory_data
        }
        self.assertEqual(after, before)


class TestCumulativeInventoryDeduction(unittest.TestCase):
    """Verify inventory is consumed cumulatively across sequential orders."""

    def test_two_orders_consuming_same_ingredient_use_combined_deduction(self):
        """Two delivered orders should deduct the combined shared ingredient total."""
        recipe_data = deepcopy(load_recipes())
        inventory_data = deepcopy(load_inventory())
        status_data = []
        restock_data = []
        order_data = [
            {"order_id": 401, "brand": "Test Kitchen", "items": [{"item": "Margherita Pizza", "qty": 1}]},
            {"order_id": 402, "brand": "Test Kitchen", "items": [{"item": "Chocolate Cake", "qty": 1}]},
        ]

        original_flour_qty = next(
            item["qty_grams"] for item in inventory_data if item["ingredient"] == "Flour"
        )

        processed_orders = process_orders(
            recipe_data,
            inventory_data,
            order_data,
            status_data,
            restock_data,
            reference_date=date(2026, 1, 1),
        )

        updated_flour_qty = next(
            item["qty_grams"] for item in inventory_data if item["ingredient"] == "Flour"
        )

        self.assertTrue(processed_orders[0]["fulfilled"])
        self.assertTrue(processed_orders[1]["fulfilled"])
        self.assertEqual(updated_flour_qty, original_flour_qty - 550)

    def test_live_inventory_unchanged_until_final_snapshot(self):
        """AC13: deepcopy — live qty stays original during deduct; snapshot updates after."""
        import main as main_module

        recipe_data = [
            {
                "recipe_id": 1,
                "name": "Cheese Dish",
                "ingredients": [{"name": "Cheese", "qty_grams": 600}],
            }
        ]
        inventory_data = [
            {"ingredient": "Cheese", "qty_grams": 1000, "expiry_date": "2026-12-31"}
        ]
        order_data = [
            {
                "order_id": 901,
                "brand": "Test Kitchen",
                "items": [{"item": "Cheese Dish", "qty": 1}],
            }
        ]
        status_data = []
        restock_data = []
        live_qty_during_deduct = []

        real_deduct = main_module.deduct_inventory

        def wrap_deduct(inv, requirements):
            live_qty_during_deduct.append(inventory_data[0]["qty_grams"])
            return real_deduct(inv, requirements)

        with patch.object(main_module, "deduct_inventory", side_effect=wrap_deduct):
            processed = process_orders(
                recipe_data,
                inventory_data,
                order_data,
                status_data,
                restock_data,
                reference_date=date(2026, 6, 3),
            )

        self.assertTrue(processed[0]["fulfilled"])
        self.assertEqual(live_qty_during_deduct, [1000])
        self.assertEqual(inventory_data[0]["qty_grams"], 400)

    def test_later_order_fails_after_prior_order_consumes_remaining_stock(self):
        """A later order should fail if an earlier order uses the remaining shared stock."""
        recipe_data = [
            {
                "recipe_id": 1,
                "name": "First Dish",
                "ingredients": [{"name": "Cheese", "qty_grams": 600}],
            },
            {
                "recipe_id": 2,
                "name": "Second Dish",
                "ingredients": [{"name": "Cheese", "qty_grams": 500}],
            },
        ]
        inventory_data = [
            {"ingredient": "Cheese", "qty_grams": 1000, "expiry_date": "2026-12-31"}
        ]
        order_data = [
            {"order_id": 501, "brand": "Test Kitchen", "items": [{"item": "First Dish", "qty": 1}]},
            {"order_id": 502, "brand": "Test Kitchen", "items": [{"item": "Second Dish", "qty": 1}]},
        ]
        status_data = []
        restock_data = []

        processed_orders = process_orders(
            recipe_data,
            inventory_data,
            order_data,
            status_data,
            restock_data,
            reference_date=date(2026, 6, 3),
        )

        self.assertTrue(processed_orders[0]["fulfilled"])
        self.assertFalse(processed_orders[1]["fulfilled"])
        self.assertIn("Cheese", processed_orders[1]["reason"])
        self.assertEqual(status_data[1]["order_id"], 502)
        self.assertFalse(status_data[1]["delivered"])
        self.assertEqual(restock_data[0]["item"], "Cheese")
        self.assertEqual(restock_data[0]["qty_needed_grams"], 9600)
        self.assertEqual(restock_data[0]["reason"], "Running low on stock")

    def test_final_inventory_matches_expected_remaining_quantities(self):
        """Final inventory should reflect all successful cumulative deductions."""
        recipe_data = deepcopy(load_recipes())
        inventory_data = deepcopy(load_inventory())
        status_data = []
        restock_data = []
        order_data = [
            {"order_id": 601, "brand": "Test Kitchen", "items": [{"item": "Margherita Pizza", "qty": 2}]},
            {"order_id": 602, "brand": "Test Kitchen", "items": [{"item": "Chocolate Cake", "qty": 1}]},
        ]

        process_orders(
            recipe_data,
            inventory_data,
            order_data,
            status_data,
            restock_data,
            reference_date=date(2026, 1, 1),
        )

        flour_qty = next(item["qty_grams"] for item in inventory_data if item["ingredient"] == "Flour")
        sauce_qty = next(
            item["qty_grams"] for item in inventory_data if item["ingredient"] == "Tomato Sauce"
        )
        cheese_qty = next(
            item["qty_grams"] for item in inventory_data if item["ingredient"] == "Mozzarella Cheese"
        )
        chocolate_qty = next(
            item["qty_grams"] for item in inventory_data if item["ingredient"] == "Chocolate"
        )
        sugar_qty = next(item["qty_grams"] for item in inventory_data if item["ingredient"] == "Sugar")

        self.assertEqual(flour_qty, 9150)
        self.assertEqual(sauce_qty, 9800)
        self.assertEqual(cheese_qty, 9700)
        self.assertEqual(chocolate_qty, 9850)
        self.assertEqual(sugar_qty, 9900)


class TestInventoryLookupAndSnapshot(unittest.TestCase):
    """AC7: last-row-wins lookup vs qty-only final snapshot (shapes stay separate)."""

    def test_inventory_by_name_last_row_wins(self):
        """Duplicate ingredient names: last row wins in the full-row lookup."""
        inventory_data = [
            {
                "ingredient": "Flour",
                "qty_grams": 100,
                "expiry_date": "2026-01-01",
            },
            {
                "ingredient": "Flour",
                "qty_grams": 999,
                "expiry_date": "2026-12-01",
            },
        ]
        lookup = _inventory_by_name(inventory_data)
        self.assertEqual(lookup["Flour"]["qty_grams"], 999)
        self.assertEqual(lookup["Flour"]["expiry_date"], "2026-12-01")

    def test_seed_inventory_ingredient_names_are_unique(self):
        """Seed table has one row per ingredient; last-wins is defensive only."""
        names = [row["ingredient"] for row in load_inventory()]
        self.assertEqual(len(names), len(set(names)))

    def test_final_snapshot_updates_qty_only_not_expiry(self):
        """Snapshot copies grams onto live rows; does not overwrite expiry."""
        live = [
            {
                "ingredient": "Flour",
                "qty_grams": 10000,
                "expiry_date": "2026-06-01",
            }
        ]
        working = [
            {
                "ingredient": "Flour",
                "qty_grams": 9000,
                "expiry_date": "2099-01-01",
            }
        ]
        apply_final_inventory_snapshot(live, working)
        self.assertEqual(live[0]["qty_grams"], 9000)
        self.assertEqual(live[0]["expiry_date"], "2026-06-01")


class TestClassifyInventoryStockFlags(unittest.TestCase):
    """DR1: private stock/expiry classifier used by restock and summary (later)."""

    def test_out_of_stock_only_requests_par(self):
        flags = _classify_inventory_stock_flags(0, days_until_expiry=None)
        self.assertTrue(flags["out_of_stock"])
        self.assertFalse(flags["running_low"])
        self.assertFalse(flags["expiring_soon"])
        self.assertFalse(flags["expired"])
        self.assertEqual(flags["restock_reasons"], ["Out of stock"])
        self.assertEqual(flags["qty_needed_grams"], PAR_LEVEL_GRAMS)

    def test_running_low_tops_up_to_par(self):
        flags = _classify_inventory_stock_flags(500, days_until_expiry=None)
        self.assertFalse(flags["out_of_stock"])
        self.assertTrue(flags["running_low"])
        self.assertEqual(flags["restock_reasons"], ["Running low on stock"])
        self.assertEqual(flags["qty_needed_grams"], PAR_LEVEL_GRAMS - 500)

    def test_expiring_soon_and_out_of_stock_take_max_par(self):
        flags = _classify_inventory_stock_flags(0, days_until_expiry=3)
        self.assertTrue(flags["out_of_stock"])
        self.assertTrue(flags["expiring_soon"])
        self.assertFalse(flags["expired"])
        self.assertEqual(
            flags["restock_reasons"], ["Out of stock", "Expiring soon"]
        )
        self.assertEqual(flags["qty_needed_grams"], PAR_LEVEL_GRAMS)

    def test_expired_adds_restock_reason_at_full_par(self):
        """RX1: expired stock is a restock condition (Part I R6), full par."""
        flags = _classify_inventory_stock_flags(10000, days_until_expiry=-1)
        self.assertTrue(flags["expired"])
        self.assertFalse(flags["expiring_soon"])
        self.assertEqual(flags["restock_reasons"], ["Expired"])
        self.assertEqual(flags["qty_needed_grams"], PAR_LEVEL_GRAMS)

    def test_expired_and_out_of_stock_keep_both_reasons(self):
        """RX1: expiry does not overwrite the quantity reason; both persist."""
        flags = _classify_inventory_stock_flags(0, days_until_expiry=-30)
        self.assertTrue(flags["out_of_stock"])
        self.assertTrue(flags["expired"])
        self.assertEqual(flags["restock_reasons"], ["Out of stock", "Expired"])
        self.assertEqual(flags["qty_needed_grams"], PAR_LEVEL_GRAMS)

    def test_none_days_means_no_expiry_flags(self):
        flags = _classify_inventory_stock_flags(10000, days_until_expiry=None)
        self.assertFalse(flags["expired"])
        self.assertFalse(flags["expiring_soon"])
        self.assertEqual(flags["restock_reasons"], [])


class TestMakeRestockRow(unittest.TestCase):
    """DR4: private restock row builder (callers wired in DR5/DR6)."""

    def test_multi_reason_joins_reason_string(self):
        row = _make_restock_row(
            item="Flour",
            current_qty_grams=0,
            qty_needed_grams=PAR_LEVEL_GRAMS,
            reasons=["Out of stock", "Expiring soon"],
            expiry_date="2026-05-12",
        )
        self.assertEqual(
            row,
            {
                "item": "Flour",
                "current_qty_grams": 0,
                "qty_needed_grams": PAR_LEVEL_GRAMS,
                "reason": "Out of stock, Expiring soon",
                "reasons": ["Out of stock", "Expiring soon"],
                "expiry_date": "2026-05-12",
            },
        )

    def test_single_reason_matches_op15_shape(self):
        row = _make_restock_row(
            item="Mystery Spice",
            current_qty_grams=0,
            qty_needed_grams=PAR_LEVEL_GRAMS,
            reasons=["Missing from inventory"],
            expiry_date=None,
        )
        self.assertEqual(row["reason"], "Missing from inventory")
        self.assertEqual(row["reasons"], ["Missing from inventory"])
        self.assertIsNone(row["expiry_date"])


class TestResolveReferenceDate(unittest.TestCase):
    """DR7: private default reference_date helper (callers wired in DR8)."""

    def test_none_resolves_to_simulation_date(self):
        self.assertEqual(_resolve_reference_date(None), SIMULATION_DATE)

    def test_explicit_date_unchanged(self):
        explicit = date(2026, 1, 1)
        self.assertEqual(_resolve_reference_date(explicit), explicit)


class TestRestockRules(unittest.TestCase):
    """Verify the Task 5 rule-based restock calculations."""

    def test_named_restock_constants_match_assignment_values(self):
        """RS1: thresholds must be named constants with the assignment values."""
        self.assertEqual(RUNNING_LOW_THRESHOLD_GRAMS, 1000)
        self.assertEqual(PAR_LEVEL_GRAMS, 10000)
        self.assertEqual(EXPIRING_SOON_DAYS, 5)
        self.assertEqual(SIMULATION_DATE, date(2026, 5, 10))

    def test_restock_default_date_is_simulation_date_not_today(self):
        """RS4: omitting reference_date must use 2026-05-10, not date.today()."""
        inventory_data = [
            {"ingredient": "Flour", "qty_grams": 10000, "expiry_date": "2026-05-12"}
        ]

        restock_data = calculate_restock_needs(inventory_data)

        self.assertEqual(len(restock_data), 1)
        self.assertIn("Expiring soon", restock_data[0]["reasons"])

    def test_restock_raises_on_malformed_expiry_date(self):
        """AC6: restock does not swallow bad dates; _days_until_expiry raises."""
        inventory_data = [
            {"ingredient": "Flour", "qty_grams": 10000, "expiry_date": "not-a-date"}
        ]
        with self.assertRaises(ValueError):
            calculate_restock_needs(
                inventory_data, reference_date=date(2026, 5, 10)
            )

    def test_calculate_restock_needs_empty_inventory_returns_empty_list(self):
        """EH2b: empty inventory → no recommendations (does not change AC6 raise)."""
        self.assertEqual(
            calculate_restock_needs([], reference_date=date(2026, 5, 10)),
            [],
        )

    def test_refresh_restock_table_empty_inventory_clears_recommendations(self):
        """EH2b: refresh with empty inventory clears prior rows to []."""
        restock_data = [
            {
                "item": "Prior Row",
                "current_qty_grams": 0,
                "qty_needed_grams": 10000,
                "reason": "Out of stock",
                "reasons": ["Out of stock"],
                "expiry_date": None,
            }
        ]
        refresh_restock_table(
            restock_data, [], reference_date=date(2026, 5, 10)
        )
        self.assertEqual(restock_data, [])

    def test_expiring_soon_sets_full_restock_quantity(self):
        """Ingredients expiring within 5 days should be marked as expiring soon."""
        # RS6: 3 days to expiry, stock above the low threshold → Expiring soon, 10,000g.
        inventory_data = [
            {"ingredient": "Cream", "qty_grams": 7000, "expiry_date": "2026-06-06"}
        ]

        restock_data = calculate_restock_needs(inventory_data, reference_date=date(2026, 6, 3))
        row = restock_data[0]

        self.assertEqual(row["item"], "Cream")
        self.assertEqual(row["current_qty_grams"], 7000)
        self.assertEqual(row["qty_needed_grams"], 10000)
        self.assertEqual(row["reasons"], ["Expiring soon"])
        self.assertEqual(row["expiry_date"], "2026-06-06")

    def test_out_of_stock_sets_full_restock_quantity(self):
        """Zero final stock should be marked as out of stock with 10,000 grams needed."""
        # RS6: 0g, not expiring soon → Out of stock, 10,000g.
        inventory_data = [
            {"ingredient": "Bun", "qty_grams": 0, "expiry_date": "2026-12-31"}
        ]

        restock_data = calculate_restock_needs(inventory_data, reference_date=date(2026, 6, 3))
        row = restock_data[0]

        self.assertEqual(row["item"], "Bun")
        self.assertEqual(row["current_qty_grams"], 0)
        self.assertEqual(row["qty_needed_grams"], 10000)
        self.assertEqual(row["reasons"], ["Out of stock"])
        self.assertEqual(row["expiry_date"], "2026-12-31")

    def test_running_low_calculates_amount_needed_to_reach_ten_thousand(self):
        """Low stock should request only the amount needed to reach 10,000 grams."""
        # RS6: 500g remaining → Running low, 9,500g needed.
        inventory_data = [
            {"ingredient": "Chicken Breast", "qty_grams": 500, "expiry_date": "2026-12-31"}
        ]

        restock_data = calculate_restock_needs(inventory_data, reference_date=date(2026, 6, 3))
        row = restock_data[0]

        self.assertEqual(row["item"], "Chicken Breast")
        self.assertEqual(row["current_qty_grams"], 500)
        self.assertEqual(row["qty_needed_grams"], 9500)
        self.assertEqual(row["reasons"], ["Running low on stock"])
        self.assertEqual(row["expiry_date"], "2026-12-31")

    def test_running_low_includes_stock_at_the_one_thousand_gram_threshold(self):
        """Stock at exactly 1,000g is at or below the low-stock threshold."""
        # Verified (AC11): running-low rule is inclusive (qty <= 1,000g).
        inventory_data = [
            {"ingredient": "Lettuce", "qty_grams": 1000, "expiry_date": "2026-12-31"}
        ]

        restock_data = calculate_restock_needs(inventory_data, reference_date=date(2026, 6, 3))
        row = restock_data[0]

        self.assertEqual(row["reasons"], ["Running low on stock"])
        self.assertEqual(row["qty_needed_grams"], 9000)
        self.assertEqual(row["current_qty_grams"], 1000)

    def test_above_low_threshold_is_not_flagged_for_low_stock(self):
        """Stock just above 1,000g must not be flagged for running low."""
        # RS6: above the threshold, far from expiry → not flagged.
        inventory_data = [
            {"ingredient": "Bun", "qty_grams": 1001, "expiry_date": "2026-12-31"}
        ]

        restock_data = calculate_restock_needs(inventory_data, reference_date=date(2026, 6, 3))

        self.assertEqual(restock_data, [])

    def test_multiple_restock_reasons_are_preserved(self):
        """Running low and expiring soon must both appear on the same row."""
        inventory_data = [
            {"ingredient": "Cream", "qty_grams": 500, "expiry_date": "2026-06-06"}
        ]

        restock_data = calculate_restock_needs(inventory_data, reference_date=date(2026, 6, 3))
        row = restock_data[0]

        self.assertEqual(row["item"], "Cream")
        self.assertEqual(row["current_qty_grams"], 500)
        self.assertEqual(row["expiry_date"], "2026-06-06")
        self.assertIn("Running low on stock", row["reasons"])
        self.assertIn("Expiring soon", row["reasons"])
        self.assertEqual(len(row["reasons"]), 2)
        self.assertEqual(row["qty_needed_grams"], 10000)

    def test_refresh_restock_table_replaces_prior_rows(self):
        """AC11: refresh clears prior (seed/history) rows, then rebuilds from inventory."""
        restock_data = [
            {
                "item": "Seed Only Item",
                "current_qty_grams": 0,
                "qty_needed_grams": 10000,
                "reason": "Out of stock",
                "reasons": ["Out of stock"],
                "expiry_date": None,
            }
        ]
        inventory_data = [
            {"ingredient": "Bun", "qty_grams": 0, "expiry_date": "2026-12-31"}
        ]

        refresh_restock_table(
            restock_data, inventory_data, reference_date=date(2026, 6, 3)
        )

        self.assertEqual(len(restock_data), 1)
        self.assertEqual(restock_data[0]["item"], "Bun")
        self.assertNotIn(
            "Seed Only Item", [row["item"] for row in restock_data]
        )

    def test_adequate_stock_without_expiry_issue_is_not_flagged(self):
        """Adequate stock with no near-expiry condition should not appear in restock."""
        # RS6: 7,000g and far from expiry → not flagged.
        inventory_data = [
            {"ingredient": "Tomato Sauce", "qty_grams": 7000, "expiry_date": "2026-12-31"}
        ]

        restock_data = calculate_restock_needs(inventory_data, reference_date=date(2026, 6, 3))

        self.assertEqual(restock_data, [])


class TestManagerSummary(unittest.TestCase):
    """Business summary: counts, reasons, restock, and manager-readable output."""

    def test_empty_or_none_processed_orders_report_zero(self):
        """None or an empty list should not crash and should report zero orders."""
        empty_summary = build_manager_summary([])
        none_summary = build_manager_summary(None)

        self.assertEqual(empty_summary["delivered_count"], 0)
        self.assertEqual(empty_summary["not_delivered_count"], 0)
        self.assertEqual(empty_summary["not_delivered_orders"], [])
        self.assertEqual(none_summary["delivered_count"], 0)
        self.assertEqual(none_summary["not_delivered_count"], 0)

    def test_all_delivered_orders_have_no_non_delivery_reasons(self):
        """When every order is delivered, not-delivered count is zero."""
        processed_orders = [
            {"order_id": 1, "brand": "A", "fulfilled": True, "reason": "Delivered"},
            {"order_id": 2, "brand": "B", "fulfilled": True, "reason": "Delivered"},
        ]

        summary = build_manager_summary(processed_orders)

        self.assertEqual(summary["delivered_count"], 2)
        self.assertEqual(summary["not_delivered_count"], 0)
        self.assertEqual(len(summary["delivered_orders"]), 2)
        self.assertIn("Orders delivered: 2", summary["text"])
        self.assertIn("None. Every processed order was delivered.", summary["text"])

    def test_failed_orders_appear_with_reasons_and_matching_counts(self):
        """Counts must match processed orders; failed orders keep their reasons."""
        recipe_data = [
            {
                "recipe_id": 1,
                "name": "Test Wrap",
                "ingredients": [
                    {"name": "Chicken Breast", "qty_grams": 200},
                    {"name": "Bun", "qty_grams": 100},
                ],
            }
        ]
        inventory_data = [
            {"ingredient": "Chicken Breast", "qty_grams": 10000, "expiry_date": "2026-12-31"},
            {"ingredient": "Bun", "qty_grams": 100, "expiry_date": "2026-12-31"},
        ]
        order_data = [
            {"order_id": 301, "brand": "Kitchen A", "items": [{"item": "Test Wrap", "qty": 1}]},
            {"order_id": 302, "brand": "Kitchen B", "items": [{"item": "Test Wrap", "qty": 1}]},
        ]
        status_data = []
        restock_data = []

        processed_orders = process_orders(
            recipe_data,
            inventory_data,
            order_data,
            status_data,
            restock_data,
            reference_date=date(2026, 6, 3),
        )
        summary = build_manager_summary(processed_orders)

        delivered = [order for order in processed_orders if order["fulfilled"]]
        not_delivered = [order for order in processed_orders if not order["fulfilled"]]
        self.assertEqual(summary["delivered_count"], len(delivered))
        self.assertEqual(summary["not_delivered_count"], len(not_delivered))
        self.assertEqual(summary["delivered_count"], 1)
        self.assertEqual(summary["not_delivered_count"], 1)
        self.assertEqual(summary["not_delivered_orders"][0]["order_id"], 302)
        self.assertIn("Bun", summary["not_delivered_orders"][0]["reason"])
        self.assertIn("Order 302", summary["text"])
        self.assertIn("Bun", summary["text"])

    def test_summary_includes_inventory_restock_and_expiry_concerns(self):
        """SM2: final inventory, restock rows, and low/out/expired/expiring-soon."""
        inventory_data = [
            {"ingredient": "Flour", "qty_grams": 7000, "expiry_date": "2026-12-31"},
            {"ingredient": "Bun", "qty_grams": 0, "expiry_date": "2026-12-31"},
            {"ingredient": "Cheese", "qty_grams": 500, "expiry_date": "2026-12-31"},
            {"ingredient": "Chocolate", "qty_grams": 10000, "expiry_date": "2026-01-15"},
            {"ingredient": "Cream", "qty_grams": 8000, "expiry_date": "2026-05-12"},
        ]
        restock_data = [
            {
                "item": "Bun",
                "qty_needed_grams": 10000,
                "reason": "Out of stock",
                "reasons": ["Out of stock"],
            }
        ]
        processed_orders = [
            {"order_id": 1, "brand": "A", "fulfilled": True, "reason": "Delivered"},
        ]

        summary = build_manager_summary(
            processed_orders,
            inventory_data=inventory_data,
            restock_data=restock_data,
            reference_date=date(2026, 5, 10),
        )

        self.assertEqual(len(summary["final_inventory"]), 5)
        flour = next(
            item for item in summary["final_inventory"] if item["ingredient"] == "Flour"
        )
        self.assertEqual(flour["qty_grams"], 7000)
        self.assertEqual(summary["out_of_stock"], ["Bun"])
        self.assertEqual(summary["low_stock"], ["Cheese"])
        self.assertEqual(summary["expired"], ["Chocolate"])
        self.assertEqual(summary["expiring_soon"], ["Cream"])
        self.assertNotIn("Flour", summary["low_stock"])
        self.assertEqual(summary["restock_recommendations"][0]["item"], "Bun")
        self.assertIn("Final inventory:", summary["text"])
        self.assertIn("Flour: 7000 grams", summary["text"])
        self.assertIn("Restock recommendations:", summary["text"])
        self.assertIn("Bun: 10000 grams needed — Out of stock", summary["text"])
        self.assertIn("Low stock: Cheese", summary["text"])
        self.assertIn("Out of stock: Bun", summary["text"])
        self.assertIn("Expired: Chocolate", summary["text"])
        self.assertIn("Expiring soon: Cream", summary["text"])

    def test_summary_counts_match_processed_orders_and_include_live_restock(self):
        """SM4: counts match processed orders; live restock rows appear in the summary."""
        # First wrap uses the only 100g of Bun and is delivered. Second wrap fails.
        # process_orders rebuilds restock from final inventory, so Bun is Out of stock.
        recipe_data = [
            {
                "recipe_id": 1,
                "name": "Test Wrap",
                "ingredients": [
                    {"name": "Chicken Breast", "qty_grams": 200},
                    {"name": "Bun", "qty_grams": 100},
                ],
            }
        ]
        inventory_data = [
            {"ingredient": "Chicken Breast", "qty_grams": 10000, "expiry_date": "2026-12-31"},
            {"ingredient": "Bun", "qty_grams": 100, "expiry_date": "2026-12-31"},
        ]
        order_data = [
            {"order_id": 401, "brand": "Kitchen A", "items": [{"item": "Test Wrap", "qty": 1}]},
            {"order_id": 402, "brand": "Kitchen B", "items": [{"item": "Test Wrap", "qty": 1}]},
        ]
        status_data = []
        restock_data = []

        processed_orders = process_orders(
            recipe_data,
            inventory_data,
            order_data,
            status_data,
            restock_data,
            reference_date=date(2026, 6, 3),
        )
        summary = build_manager_summary(
            processed_orders,
            inventory_data=inventory_data,
            restock_data=restock_data,
            reference_date=date(2026, 6, 3),
        )

        delivered = [order for order in processed_orders if order["fulfilled"]]
        not_delivered = [order for order in processed_orders if not order["fulfilled"]]
        self.assertEqual(summary["delivered_count"], len(delivered))
        self.assertEqual(summary["not_delivered_count"], len(not_delivered))
        self.assertEqual(summary["delivered_count"], 1)
        self.assertEqual(summary["not_delivered_count"], 1)
        self.assertEqual(summary["not_delivered_orders"][0]["order_id"], 402)
        self.assertIn("Bun", summary["not_delivered_orders"][0]["reason"])

        restock_names = [row["item"] for row in summary["restock_recommendations"]]
        self.assertIn("Bun", restock_names)
        bun_restock = next(
            row for row in summary["restock_recommendations"] if row["item"] == "Bun"
        )
        self.assertEqual(bun_restock["qty_needed_grams"], 10000)
        self.assertIn("Out of stock", bun_restock["reason"])
        self.assertIn("Restock recommendations:", summary["text"])
        self.assertIn("Bun: 10000 grams needed — Out of stock", summary["text"])

    def test_summary_is_dict_with_manager_readable_text(self):
        """SM4: the summary is a dict; text is a string a kitchen manager can read."""
        summary = build_manager_summary(
            [
                {"order_id": 1, "brand": "A", "fulfilled": True, "reason": "Delivered"},
                {
                    "order_id": 2,
                    "brand": "B",
                    "fulfilled": False,
                    "reason": "Missing or insufficient ingredients: Bun",
                },
            ],
            inventory_data=[
                {"ingredient": "Bun", "qty_grams": 0, "expiry_date": "2026-12-31"},
            ],
            restock_data=[
                {
                    "item": "Bun",
                    "qty_needed_grams": 10000,
                    "reason": "Out of stock",
                }
            ],
            reference_date=date(2026, 6, 3),
        )

        self.assertIsInstance(summary, dict)
        self.assertIsInstance(summary["text"], str)
        self.assertIn("=== Kitchen Manager Summary ===", summary["text"])
        self.assertIn("Orders delivered: 1", summary["text"])
        self.assertIn("Orders not delivered: 1", summary["text"])
        self.assertIn("Order 2: Missing or insufficient ingredients: Bun", summary["text"])
        self.assertIn("Restock recommendations:", summary["text"])
        self.assertIn("Bun: 10000 grams needed — Out of stock", summary["text"])


if __name__ == "__main__":
    unittest.main()
