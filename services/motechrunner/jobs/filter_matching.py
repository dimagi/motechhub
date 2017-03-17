def filter_matches_message(filter_json, message):
    return all(message.get(key) == value for key, value in filter_json.items())
