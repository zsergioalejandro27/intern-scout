DOMAIN_KEYWORDS = [
    "software", "developer", "engineer", "backend", "back-end",
    "frontend", "front-end", "full stack", "fullstack", "devops",
    "data engineer", "programmer", "qa engineer", "sre",
    "machine learning", "ml engineer",
]

ENTRY_LEVEL_KEYWORDS = [
    "intern", "internship", "werkstudent", "working student",
    "praktikum", "praktikant", "graduate", "junior", "entry level",
    "entry-level", "trainee", "apprentice",
]

EXCLUDE_KEYWORDS = [
    "senior", "sr.", "lead", "staff", "principal", "head of",
    "director", "manager", "chief",
]


def is_relevant_role(title: str) -> bool:
    title_lower = title.lower()

    if not any(keyword in title_lower for keyword in DOMAIN_KEYWORDS):
        return False

    if any(keyword in title_lower for keyword in EXCLUDE_KEYWORDS):
        return False

    return any(keyword in title_lower for keyword in ENTRY_LEVEL_KEYWORDS)
