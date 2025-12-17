def safe_text(s: object) -> str:
    """
    Postgres cannot store NUL bytes in TEXT.
    Also trims whitespace.
    """
    return str(s).replace("\x00", "").strip()
