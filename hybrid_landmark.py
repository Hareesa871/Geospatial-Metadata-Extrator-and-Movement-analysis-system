def infer_landmark(city, cnn_prediction):
    if not city:
        return cnn_prediction

    # Simple heuristic rules
    if city.lower() == "mumbai" and "dome" in cnn_prediction:
        return "Possible Gateway of India (Mumbai)"

    if city.lower() == "hyderabad" and "mosque" in cnn_prediction:
        return "Possible Charminar (Hyderabad)"

    if "bridge" in cnn_prediction:
        return f"Bridge in {city}"

    if "tower" in cnn_prediction:
        return f"Tower in {city}"

    return f"{cnn_prediction} in {city}"