stats = {
    "scripts": 0,
    "videos": 0,
    "uploads": 0
}


def script_created():
    stats["scripts"] += 1


def video_created():
    stats["videos"] += 1


def uploaded():
    stats["uploads"] += 1


def report():
    return stats
