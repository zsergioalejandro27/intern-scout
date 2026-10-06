import unicodedata


def normalize_text(text: str) -> str:
    text = text.lower().replace("ß", "ss").replace("ø", "o").replace("æ", "ae")
    decomposed = unicodedata.normalize("NFKD", text)
    return "".join(char for char in decomposed if not unicodedata.combining(char))
