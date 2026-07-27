# content/product_reader.py

from config import WEBSITE_URL


def get_products():
    """
    Returns information about your products.
    Later, this will automatically read your website.
    """

    products = {
        "website": WEBSITE_URL,
        "brand": "AI Content Factory",
        "products": [
            "ChatGPT Prompt Guide",
            "AI Prompt Templates",
            "Business Prompt Bundle",
            "Marketing Prompt Pack",
            "Freelancer AI Toolkit"
        ]
    }

    return products
