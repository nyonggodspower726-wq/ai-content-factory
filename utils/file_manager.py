import os
from datetime import datetime

def save_text(filename, content):

    today = datetime.now().strftime("%Y-%m-%d")

    folder = os.path.join("output", today)

    os.makedirs(folder, exist_ok=True)

    path = os.path.join(folder, filename)

    with open(path, "w", encoding="utf-8") as f:
        f.write(content)

    print(f"Saved: {path}")

    return path
