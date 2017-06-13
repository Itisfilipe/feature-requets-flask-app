def insert_item_by_priority(features, item):
    """ Insert an item into a ordered list of features
        in the right position"""
    features.insert(item.priority - 1, item)
    return features


def rearrange_priorities_of_ordered_list(features):
    """ Rearrange the priorities number in a ordered list"""
    for index, feature in enumerate(features, 1):
        feature.priority = index
    return features
