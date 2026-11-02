"""Notify Mini: subscribers live only in the current Python process."""

subscribers: set[str] = set()


def subscribe(name: str) -> dict[str, bool]:
    """Add a trimmed nonempty name; duplicates are harmless."""
    if not name.strip():
        raise ValueError("empty name")
    subscribers.add(name.strip())
    return {"subscribed": True}


def list_subscribers() -> list[str]:
    """Return a sorted snapshot, independent of the internal set."""
    return sorted(subscribers)


def unsubscribe(name: str) -> dict[str, bool]:
    """Remove a trimmed nonempty name from subscribers."""
    if not name.strip():
        raise ValueError("empty name")
    normalized = name.strip()
    if normalized in subscribers:
        subscribers.discard(normalized)
        return {"unsubscribed": True}
    return {"unsubscribed": False}
