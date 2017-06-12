def insert_item_by_priority(features, item):
    features.insert(item.priority - 1, item)
    return features


def rearrange_priorities_of_ordered_list(features):
    for index, feature in enumerate(features, 1):
        feature.priority = index
    return features