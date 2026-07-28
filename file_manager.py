import os


def save_text(filename, content):

    with open(filename, "w", encoding="utf-8") as file:
        file.write(content)

    print(f"Saved: {filename}")

    return filename
