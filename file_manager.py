import json
import os


def save_text(filename, content):
    """
    Save either text or dictionaries automatically.
    """

    folder = os.path.dirname(filename)

    if folder:
        os.makedirs(folder, exist_ok=True)

    with open(filename, "w", encoding="utf-8") as file:

        if isinstance(content, (dict, list)):
            json.dump(
                content,
                file,
                indent=4,
                ensure_ascii=False
            )

        else:
            file.write(str(content))

    print(f"Saved: {filename}")

    return filename
