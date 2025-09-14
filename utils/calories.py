from fuzzywuzzy import fuzz

def select_best_food(foods, query, threshold=80):
    best_food = None
    best_score = 0
    query_lower = query.lower()
    for food in foods:
        desc = food.get("description", "").lower()
        score = fuzz.ratio(query_lower, desc)
        if score > best_score and score >= threshold:
            best_score = score
            best_food = food

    if best_food is None and foods:
        best_food = foods[0]

    return best_food
