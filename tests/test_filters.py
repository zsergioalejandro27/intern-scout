import pytest

from src.processing.filters import classify_role


@pytest.mark.parametrize(
    "title, expected",
    [
        ("Working Student Software Engineer (f/m/d)", "internship"),
        ("Werkstudent (m/w/d) | Fullstack Developer", "internship"),
        ("Security Engineer Intern", "internship"),
        ("Data Engineering Intern", "internship"),
        ("Praktikum Softwareentwicklung (m/w/d)", "internship"),
        ("Ferialpraktikum Software Developer", "internship"),
        ("Praktikant Backend-Entwickler", "internship"),
        ("Praktikplats systemutvecklare", "internship"),
        ("Harjoittelija ohjelmistokehittäjä", "internship"),
        ("Praktikant softwareudvikler", "internship"),
        ("Sommerjobb systemutvikler student", "internship"),
        ("Student Assistant Software Development", "internship"),
        ("Graduate Software Engineer (Supply Chain + Operations)", "graduate"),
        ("Trainee Softwareentwickler", "graduate"),
        ("Absolvent Informatik (m/w/d)", "graduate"),
        ("Nyexaminerad systemutvecklare", "graduate"),
        ("Junior Backend Developer", "entry_level"),
        ("Junior Computational Geometry Engineer", "entry_level"),
        ("Berufseinsteiger Softwareentwickler", "entry_level"),
    ],
)
def test_relevant_roles_are_classified(title, expected):
    assert classify_role(title) == expected


@pytest.mark.parametrize(
    "title",
    [
        "Senior Software Engineer",
        "Senior Software Engineer Intern",
        "Software Engineer",
        "Internal Software Engineer",
        "International Sales Engineer",
        "Praktikum Marketing",
        "Mechanical Engineering Intern Engineer",
        "Praktikum Maschinenbau Ingenieur",
        "Junior Business Developer",
        "Ausbildung Fachinformatiker Anwendungsentwicklung",
        "Duales Studium Informatik",
        "Traumpraktikum: Werde Fachinformatiker für Anwendungsentwicklung (m/w/d)",
        "Junior GTM Engineer - 100% remote",
        "Teamleiter Softwareentwicklung Junior",
        "Lead Developer Graduate Program",
    ],
)
def test_irrelevant_roles_are_rejected(title):
    assert classify_role(title) is None
