from fuzzywuzzy import fuzz

def select_best_food(foods, query, threshold=70):
    best_food = None
    best_score = 0
    query_lower = query.lower()
    for food in foods:
        desc = food.get("description", "").lower()
        score = fuzz.partial_ratio(query_lower, desc)
        if score > best_score and score >= threshold:
            best_score = score
            best_food = food

    return best_food
