import os

OUTPUT_DIR = "output"

os.makedirs(OUTPUT_DIR, exist_ok=True)


def save_text(filename, content):

    path = os.path.join(OUTPUT_DIR, filename)

    with open(path, "w", encoding="utf-8") as f:
        f.write(content)

    print(f"Saved: {path}")

    return path
