from datetime import datetime, timezone

_DE_MONTH_ABBR = {
    1: "Jan.", 2: "Feb.", 3: "März", 4: "Apr.", 5: "Mai", 6: "Juni",
    7: "Juli", 8: "Aug.", 9: "Sept.", 10: "Okt.", 11: "Nov.", 12: "Dez."
}

def format_ts(ts: str | None) -> str:
    """Erwartet ISO-8601 (z. B. '2025-10-15T10:30:00Z' oder '+00:00')."""
    if not ts:
        return ""
    iso = ts.strip()
    if iso.endswith("Z"):
        iso = iso[:-1] + "+00:00"
    try:
        dt = datetime.fromisoformat(iso)
        return f"{dt.day}. {_DE_MONTH_ABBR[dt.month]} {dt.year}"
    except Exception:
        return ts