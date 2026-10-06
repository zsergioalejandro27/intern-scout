import re

from src.processing.text import normalize_text


def _compile(words: tuple[str, ...] = (), stems: tuple[str, ...] = ()) -> re.Pattern:
    # Words match whole tokens ("internal" is not "intern"); stems also match inside German/Nordic compounds.
    parts = []
    if words:
        alternatives = "|".join(re.escape(normalize_text(word)) for word in words)
        parts.append(rf"(?<![a-z0-9])(?:{alternatives})s?(?![a-z0-9])")
    if stems:
        parts.append("|".join(re.escape(normalize_text(stem)) for stem in stems))
    return re.compile("|".join(parts))


DOMAIN = _compile(
    words=(
        "developer", "programmer", "engineer", "backend", "back-end", "frontend", "front-end",
        "full stack", "full-stack", "fullstack", "devops", "sre", "site reliability",
        "data engineer", "data engineering", "data scientist", "machine learning", "ml engineer",
        "ai engineer", "cloud engineer", "platform engineer", "security engineer", "cybersecurity",
        "cyber security", "qa", "test automation", "embedded", "firmware", "android", "ios",
        "sysadmin", "system administrator", "mlops", "computer science", "informatics",
    ),
    stems=(
        "software", "entwickler", "programmierer", "informatik", "informatiker",
        "mjukvaru", "utvecklare", "programmerare", "utvikler", "udvikler", "programmor",
        "ohjelmisto", "ohjelmoija", "kehittaja", "tietotekniik", "tietojenkasittely",
        "ingenieur", "ingenjor", "ingenior", "insinoori",
    ),
)

EXCLUDE = _compile(
    words=(
        "senior", "sr", "staff", "principal", "vp", "experienced", "business developer",
        "sales", "gtm", "go-to-market", "mechanical", "electrical", "electrician", "civil",
        "chemical", "structural", "manufacturing", "industrial", "hvac", "construction",
    ),
    stems=(
        "senior", "lead", "leiter", "chef", "leder", "johtaja", "paallik", "head of", "director",
        "direktor", "manager", "chief", "erfaren", "erfahren", "berufserfahren",
        "ausbildung", "azubi", "lehrling", "duales studium", "dual studium", "apprentice",
        "fachinformatik",
        "maschinenbau", "elektro", "bauingenieur", "verfahrenstechnik", "fertigung", "vertrieb",
        "maskin", "bygg", "mechatronic", "mechanic",
    ),
)

ROLE_TYPES = (
    (
        "internship",
        _compile(
            words=("intern", "internship", "working student", "student", "stagiaire", "stage"),
            stems=(
                "werkstudent", "praktik", "studentisch", "studentermedhjalp", "studiejob",
                "studentjobb", "sommerjobb", "sommarjobb", "ferial", "harjoittel", "kesatyo",
                "opiskelija", "tirocin", "praksis",
            ),
        ),
    ),
    (
        "graduate",
        _compile(
            words=("graduate", "new grad"),
            stems=(
                "trainee", "absolvent", "nyexaminerad", "nyutdannet", "nyuddannet", "dimittend",
                "vastavalmistunut",
            ),
        ),
    ),
    (
        "entry_level",
        _compile(
            words=("entry level", "entry-level", "early career", "early-career", "young professional"),
            stems=("junior", "berufseinsteig", "einsteiger"),
        ),
    ),
)


def classify_role(title: str) -> str | None:
    text = normalize_text(title)
    if not DOMAIN.search(text) or EXCLUDE.search(text):
        return None
    for role_type, pattern in ROLE_TYPES:
        if pattern.search(text):
            return role_type
    return None
