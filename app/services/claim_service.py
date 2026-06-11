def normalize_category(category: str) -> str:
    category = category.lower().strip().replace(" ", "_")

    if any(word in category for word in ["vehicle", "car", "auto"]):
        return "vehicle"
    elif any(word in category for word in ["water", "flood", "flooding", "leak"]):
        return "water_damage"
    elif any(word in category for word in ["fire", "burn", "smoke"]):
        return "fire_damage"
    else:
        return "unknown"