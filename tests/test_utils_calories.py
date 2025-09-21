import pytest
from utils.calories import select_best_food


def test_select_best_food_exact_match():
    foods = [
        {"description": "Apple, raw"},
        {"description": "Banana, raw"},
        {"description": "Orange, raw"}
    ]
    # Test exact match
    best = select_best_food(foods, "Apple")
    assert best["description"] == "Apple, raw"


def test_select_best_food_fuzzy_match():
    foods = [
        {"description": "Apple, raw"},
        {"description": "Banana, raw"},
        {"description": "Orange, raw"}
    ]
    # Test fuzzy match with typo
    best = select_best_food(foods, "Aple")  # Typo
    assert best["description"] == "Apple, raw"


def test_select_best_food_no_good_match():
    foods = [
        {"description": "Apple, raw"},
        {"description": "Banana, raw"},
        {"description": "Orange, raw"}
    ]
    # Test no match above threshold
    best = select_best_food(foods, "Pizza")
    assert best is None  # No fallback, return None


def test_select_best_food_empty_foods():
    foods = []
    # Test with empty foods list
    best = select_best_food(foods, "Apple")
    assert best is None


def test_select_best_food_case_insensitive():
    foods = [
        {"description": "APPLE, RAW"},
        {"description": "Banana, raw"},
        {"description": "Orange, raw"}
    ]
    # Test case insensitive match
    best = select_best_food(foods, "apple")
    assert best["description"] == "APPLE, RAW"

def test_select_best_food_score_threshold():
    foods = [
        {"description": "Apple pie"},
        {"description": "Green apple"},
        {"description": "Apple, raw"}
    ]

    # Test that it finds a match above threshold
    best = select_best_food(foods, "Apple")
    # The exact match depends on fuzzywuzzy scoring, but it should find one
    assert best is not None
    assert best["description"] in ["Apple pie", "Green apple", "Apple, raw"]

def test_select_best_food_different_word_order():
    foods = [
        {"description": "Biryani, mutton"},
        {"description": "Chicken biryani"},
        {"description": "Pizza, cheese"}
    ]

    # Test matching with different word order
    best = select_best_food(foods, "mutton biryani")
    assert best["description"] == "Biryani, mutton"
