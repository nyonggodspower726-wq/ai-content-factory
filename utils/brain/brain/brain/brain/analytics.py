memory = []

def remember(item):
    """
    Save something into memory.
    """
    memory.append(item)


def recall():
    """
    Return everything stored in memory.
    """
    return memory


def clear_memory():
    """
    Clear all stored memory.
    """
    memory.clear()
