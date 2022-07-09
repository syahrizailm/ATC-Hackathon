def generate_matching_query(condition):
    """
    Return query string for mongodb
    condition format:
    [
        {param: <>, value: <>],
        {param: <>, value: <>],
        ...
    ]
    """
    consolidate_condition = []
    for cond in condition:
        consolidate_condition.append(
            {"$toInt": {"$in": [cond["value"], f"${cond['param']}"]}}
        )

    return [
        {
            "$addFields": {
                "matching_score": {
                    "$divide": [ 
                        {"$add": consolidate_condition},
                        len(condition)
                    ]
                }
            }
        },
        {
            "$match": {
                "$expr": {"$gt": ["$matching_score", 0]}
            }
        },
        {
            "$sort": {"matching_score": 1}
        }
    ]