import re

from src.processing.text import normalize_text

PLACES: dict[str, list[str]] = {
    "Austria": [
        "Austria", "Österreich", "Oesterreich",
        "Vienna", "Wien", "Graz", "Linz", "Salzburg", "Innsbruck", "Klagenfurt", "Villach",
        "Wels", "St. Pölten", "Sankt Pölten", "Dornbirn", "Steyr", "Wiener Neustadt",
        "Feldkirch", "Bregenz", "Leonding", "Krems", "Leoben", "Hagenberg", "Eisenstadt",
        "Klosterneuburg", "Schwechat", "Mödling",
        "Tyrol", "Tirol", "Styria", "Steiermark", "Carinthia", "Kärnten", "Upper Austria",
        "Oberösterreich", "Lower Austria", "Niederösterreich", "Vorarlberg", "Burgenland",
    ],
    "Switzerland": [
        "Switzerland", "Schweiz", "Suisse", "Svizzera",
        "Zurich", "Zürich", "Zuerich", "Geneva", "Genf", "Genève", "Basel", "Bâle", "Bern",
        "Berne", "Lausanne", "Winterthur", "Lucerne", "Luzern", "St. Gallen", "Sankt Gallen",
        "Lugano", "Biel", "Bienne", "Thun", "Fribourg", "Schaffhausen", "Chur", "Neuchâtel",
        "Sion", "Uster", "Zug", "Baar", "Dübendorf", "Duebendorf", "Wallisellen", "Kloten",
        "Opfikon", "Rapperswil", "Aarau", "Olten", "Solothurn", "Dietikon", "Schlieren",
        "Ticino", "Tessin", "Vaud", "Waadt", "Valais", "Wallis", "Graubünden", "Aargau",
        "Thurgau", "Schwyz", "Appenzell", "Glarus", "Basel-Stadt", "Basel-Landschaft",
    ],
    "Norway": [
        "Norway", "Norge", "Norwegen",
        "Oslo", "Bergen", "Trondheim", "Stavanger", "Drammen", "Fredrikstad", "Kristiansand",
        "Sandnes", "Tromsø", "Sarpsborg", "Skien", "Ålesund", "Sandefjord", "Haugesund",
        "Tønsberg", "Porsgrunn", "Bodø", "Arendal", "Hamar", "Larvik", "Halden",
        "Lillehammer", "Gjøvik", "Kongsberg", "Lysaker", "Fornebu", "Bærum", "Asker",
        "Lillestrøm",
    ],
    "Sweden": [
        "Sweden", "Sverige", "Schweden",
        "Stockholm", "Gothenburg", "Göteborg", "Malmö", "Uppsala", "Västerås", "Örebro",
        "Linköping", "Helsingborg", "Jönköping", "Norrköping", "Lund", "Umeå", "Gävle",
        "Borås", "Södertälje", "Eskilstuna", "Halmstad", "Växjö", "Karlstad", "Sundsvall",
        "Luleå", "Kista", "Solna", "Sundbyberg", "Nacka", "Mölndal", "Skåne",
    ],
    "Finland": [
        "Finland", "Suomi", "Finnland",
        "Helsinki", "Espoo", "Tampere", "Vantaa", "Oulu", "Turku", "Jyväskylä", "Lahti",
        "Kuopio", "Pori", "Kouvola", "Joensuu", "Lappeenranta", "Hämeenlinna", "Vaasa",
        "Seinäjoki", "Rovaniemi", "Kotka", "Kajaani", "Kerava", "Uusimaa", "Pirkanmaa",
    ],
    "Denmark": [
        "Denmark", "Danmark", "Dänemark",
        "Copenhagen", "København", "Kobenhavn", "Aarhus", "Århus", "Odense", "Aalborg",
        "Esbjerg", "Randers", "Kolding", "Horsens", "Vejle", "Roskilde", "Herning",
        "Silkeborg", "Næstved", "Fredericia", "Viborg", "Køge", "Holstebro", "Taastrup",
        "Ballerup", "Lyngby", "Glostrup", "Hellerup", "Frederiksberg", "Hovedstaden",
        "Midtjylland", "Syddanmark", "Nordjylland",
    ],
    "Germany": [
        "Germany", "Deutschland",
        "Berlin", "Hamburg", "Munich", "München", "Muenchen", "Cologne", "Köln", "Koeln",
        "Frankfurt", "Stuttgart", "Düsseldorf", "Duesseldorf", "Leipzig", "Dortmund", "Essen",
        "Bremen", "Dresden", "Hannover", "Hanover", "Nuremberg", "Nürnberg", "Nuernberg",
        "Duisburg", "Bochum", "Wuppertal", "Bielefeld", "Bonn", "Münster", "Muenster",
        "Karlsruhe", "Mannheim", "Augsburg", "Wiesbaden", "Gelsenkirchen", "Braunschweig",
        "Kiel", "Chemnitz", "Aachen", "Halle", "Magdeburg", "Freiburg", "Krefeld", "Lübeck",
        "Mainz", "Erfurt", "Rostock", "Kassel", "Potsdam", "Heidelberg", "Darmstadt",
        "Regensburg", "Ingolstadt", "Würzburg", "Wolfsburg", "Ulm", "Heilbronn", "Pforzheim",
        "Göttingen", "Osnabrück", "Oldenburg", "Jena", "Ilmenau", "Paderborn", "Saarbrücken",
        "Konstanz", "Walldorf", "Garching", "Ludwigshafen", "Leverkusen", "Neuss", "Mülheim",
        "Oberhausen", "Hagen", "Hamm", "Herne", "Solingen", "Offenbach", "Reutlingen",
        "Fürth", "Fuerth", "Erlangen", "Trier", "Siegen", "Hildesheim", "Cottbus", "Zwickau",
        "Bayreuth", "Bamberg", "Landshut", "Rosenheim", "Friedrichshafen", "Böblingen",
        "Sindelfingen", "Esslingen", "Ludwigsburg", "Offenburg", "Tübingen", "Passau",
        "Kaiserslautern", "Koblenz", "Flensburg", "Greifswald", "Schwerin", "Stralsund",
        "Bavaria", "Bayern", "Baden-Württemberg",
        "Baden-Wuerttemberg", "North Rhine-Westphalia", "Nordrhein-Westfalen", "Hesse",
        "Hessen", "Saxony", "Sachsen", "Lower Saxony", "Niedersachsen", "Thuringia",
        "Thüringen", "Brandenburg", "Mecklenburg-Vorpommern", "Schleswig-Holstein",
        "Rhineland-Palatinate", "Rheinland-Pfalz", "Saarland",
    ],
}

TARGET_COUNTRIES = frozenset(PLACES)
PRIORITY_COUNTRIES = TARGET_COUNTRIES - {"Germany"}

_PATTERNS = {
    country: re.compile(
        r"(?<![a-z])(?:" + "|".join(re.escape(normalize_text(place)) for place in places) + r")(?![a-z])"
    )
    for country, places in PLACES.items()
}


def detect_country(location: str | None) -> str | None:
    if not location:
        return None
    text = normalize_text(location)
    for country, pattern in _PATTERNS.items():
        if pattern.search(text):
            return country
    return None
