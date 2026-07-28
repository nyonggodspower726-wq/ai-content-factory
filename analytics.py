def track_event(event_name, data=None):

    """
    Track AI Content Factory events.
    """

    event = {
        "event": event_name,
        "data": data
    }

    print("Analytics:", event)

    return event
