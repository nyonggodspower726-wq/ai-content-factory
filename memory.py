memory = []


def remember(item):
    """
    Save information into memory.
    """
    memory.append(item)


def recall():
    """
    Get all stored memories.
    """
    return memory


def clear_memory():
    """
    Remove all stored memories.
    """
    memory.clear()
