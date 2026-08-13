import os
import json
import time
import requests

from config import PEXELS_API_KEY


PEXELS_URL = "https://api.pexels.com/v1/search"

# ============================================================
# ANTI-REPEAT SETTINGS
# ============================================================

HISTORY_FILE = "data/pexels_image_history.json"

IMAGE_COOLDOWN = 20

SEARCH_RESULTS_PER_PAGE = 20

MAX_SEARCH_PAGES = 5


# ============================================================
# DIRECTORY SETUP
# ============================================================

def ensure_history_directory():

    history_dir = os.path.dirname(
        HISTORY_FILE
    )

    if history_dir:

        os.makedirs(
            history_dir,
            exist_ok=True
        )


# ============================================================
# LOAD IMAGE HISTORY
# ============================================================

def load_history():

    ensure_history_directory()

    if not os.path.exists(
        HISTORY_FILE
    ):

        return []


    try:

        with open(
            HISTORY_FILE,
            "r",
            encoding="utf-8"
        ) as f:

            data = json.load(f)


        if not isinstance(
            data,
            list
        ):

            return []


        return data


    except Exception as e:

        print(
            "=" * 60
        )

        print(
            "PEXELS HISTORY LOAD ERROR"
        )

        print(
            e
        )

        print(
            "=" * 60
        )

        return []


# ============================================================
# SAVE IMAGE HISTORY
# ============================================================

def save_history(history):

    ensure_history_directory()

    try:

        with open(
            HISTORY_FILE,
            "w",
            encoding="utf-8"
        ) as f:

            json.dump(
                history,
                f,
                indent=2,
                ensure_ascii=False
            )


    except Exception as e:

        print(
            "=" * 60
        )

        print(
            "PEXELS HISTORY SAVE ERROR"
        )

        print(
            e
        )

        print(
            "=" * 60
        )


# ============================================================
# CLEAN HISTORY
# ============================================================

def normalize_history(history):

    cleaned = []

    for item in history:

        if isinstance(
            item,
            dict
        ):

            if item.get(
                "id"
            ):

                cleaned.append(
                    item
                )

    return cleaned


# ============================================================
# GET RECENT PEXELS IDS
# ============================================================

def get_recent_ids(
    history
):

    recent = history[
        -IMAGE_COOLDOWN:
    ]


    return {
        str(
            item.get("id")
        )

        for item in recent

        if item.get("id") is not None
    }


# ============================================================
# RECORD IMAGE USAGE
# ============================================================

def record_image_usage(
    history,
    photo
):

    item = {

        "id":
            str(
                photo.get(
                    "id"
                )
            ),

        "photographer":
            photo.get(
                "photographer",
                ""
            ),

        "source":
            "pexels",

        "timestamp":
            int(
                time.time()
            )

    }


    history.append(
        item
    )


    # Keep a reasonable long-term history.
    # The newest 100 entries are enough to preserve
    # the 20-image cooldown while preventing the file
    # from growing forever.

    history = history[
        -100:
    ]


    save_history(
        history
    )


    return history


# ============================================================
# DOWNLOAD IMAGE
# ============================================================

def download_image(
    url,
    output_path
):

    response = requests.get(

        url,

        timeout=60

    )

    response.raise_for_status()


    with open(
        output_path,
        "wb"
    ) as f:

        f.write(
            response.content
        )


    return output_path


# ============================================================
# SAFE FILENAME
# ============================================================

def build_filename(
    prompt,
    photo_id
):

    safe_prompt = (
        "".join(
            c
            if c.isalnum()
            else "_"

            for c in prompt[:60]
        )
        .strip("_")
        .lower()
    )


    if not safe_prompt:

        safe_prompt = "pexels"


    return (
        f"{safe_prompt}_"
        f"{photo_id}.jpg"
    )


# ============================================================
# SEARCH PEXELS
# ============================================================

def search_pexels(
    prompt,
    page
):

    headers = {

        "Authorization":
            PEXELS_API_KEY

    }


    params = {

        "query":
            prompt,

        "per_page":
            SEARCH_RESULTS_PER_PAGE,

        "page":
            page,

        "orientation":
            "portrait"

    }


    response = requests.get(

        PEXELS_URL,

        headers=headers,

        params=params,

        timeout=60

    )


    response.raise_for_status()


    return response.json()


# ============================================================
# CHOOSE FRESH PHOTO
# ============================================================

def choose_fresh_photo(
    prompt,
    history
):

    recent_ids = get_recent_ids(
        history
    )


    print(
        "=" * 60
    )

    print(
        "PEXELS IMAGE SEARCH"
    )

    print(
        "=" * 60
    )

    print(
        "Searching:",
        prompt
    )

    print(
        "Recent image cooldown:",
        IMAGE_COOLDOWN
    )


    # --------------------------------------------------------
    # Search several pages so that a repeated first result
    # doesn't cause the factory to reuse the same image.
    # --------------------------------------------------------

    for page in range(
        1,
        MAX_SEARCH_PAGES + 1
    ):

        print(
            f"Searching Pexels page "
            f"{page}/{MAX_SEARCH_PAGES}..."
        )


        data = search_pexels(
            prompt,
            page
        )


        photos = data.get(
            "photos",
            []
        )


        if not photos:

            continue


        # ----------------------------------------------------
        # Remove recently used photos
        # ----------------------------------------------------

        fresh_photos = [

            photo

            for photo in photos

            if str(
                photo.get(
                    "id"
                )
            )

            not in recent_ids

        ]


        print(
            "Results:",
            len(photos)
        )

        print(
            "Fresh results:",
            len(fresh_photos)
        )


        if fresh_photos:

            # Prefer the first fresh result.
            return fresh_photos[0]


    # ========================================================
    # FALLBACK
    # ========================================================
    #
    # If Pexels keeps returning images we've recently used,
    # we still need to produce a video rather than fail the
    # entire content factory.
    #
    # Choose the oldest image from the first page.
    # ========================================================

    print(
        "No completely fresh Pexels image found "
        "within the search limit."
    )


    data = search_pexels(
        prompt,
        1
    )


    photos = data.get(
        "photos",
        []
    )


    if photos:

        print(
            "Using fallback Pexels image."
        )

        return photos[0]


    return None


# ============================================================
# MAIN IMAGE ENGINE
# ============================================================

def generate_ai_image(
    prompt,
    output_folder="assets/images"
):

    os.makedirs(
        output_folder,
        exist_ok=True
    )


    history = normalize_history(
        load_history()
    )


    try:

        # ====================================================
        # SELECT FRESH PHOTO
        # ====================================================

        photo = choose_fresh_photo(
            prompt,
            history
        )


        if not photo:

            print(
                "No Pexels image found."
            )

            return None


        # ====================================================
        # PHOTO INFORMATION
        # ====================================================

        photo_id = str(
            photo.get(
                "id"
            )
        )


        image_url = (
            photo
            .get("src", {})
            .get("large2x")
        )


        if not image_url:

            image_url = (
                photo
                .get("src", {})
                .get("large")
            )


        if not image_url:

            print(
                "Pexels photo has no usable image URL."
            )

            return None


        photographer = photo.get(
            "photographer",
            ""
        )


        print(
            "Selected Pexels photo:",
            photo_id
        )


        print(
            "Photographer:",
            photographer
        )


        # ====================================================
        # FILE PATH
        # ====================================================

        filename = build_filename(
            prompt,
            photo_id
        )


        image_path = os.path.join(

            output_folder,

            filename

        )


        # ====================================================
        # DOWNLOAD
        # ====================================================

        if os.path.exists(
            image_path
        ):

            print(
                "Using existing downloaded image:",
                image_path
            )

        else:

            print(
                "Downloading:",
                image_url
            )


            download_image(

                image_url,

                image_path

            )


            print(
                "Downloaded:",
                image_path
            )


        # ====================================================
        # VERIFY FILE
        # ====================================================

        if not os.path.exists(
            image_path
        ):

            print(
                "Downloaded image is missing."
            )

            return None


        file_size = os.path.getsize(
            image_path
        )


        if file_size <= 0:

            print(
                "Downloaded image is empty."
            )

            return None


        # ====================================================
        # RECORD USAGE
        # ====================================================
        #
        # Record after successful download.
        # This prevents a failed request from consuming
        # a cooldown slot.
        # ====================================================

        record_image_usage(
            history,
            photo
        )


        print(
            "=" * 60
        )

        print(
            "PEXELS IMAGE READY"
        )

        print(
            "Photo ID:",
            photo_id
        )

        print(
            "File:",
            image_path
        )

        print(
            "Cooldown:",
            f"{IMAGE_COOLDOWN} videos"
        )

        print(
            "=" * 60
        )


        return image_path


    except Exception as e:

        print(
            "=" * 60
        )

        print(
            "PEXELS FAILED"
        )

        print(
            e
        )

        print(
            "=" * 60
        )

        return None
