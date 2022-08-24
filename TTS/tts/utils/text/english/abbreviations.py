import re

# List of (regular expression, replacement) pairs for abbreviations in english:
abbreviations_en = [
    (re.compile("\\b%s\\." % x[0], re.IGNORECASE), x[1])
    for x in [
        ("np", "na przykład"),
        ("itp", "i tym podobne"),
        ("itd", "i tak dalej"),
        ("płd", "południe"),
        ("pln", "północ"),
        ("cd", "ciąg dalszy"),
        ("inż", "inżynier"),
        ("mgr", "magister"),
        ("dr", "doktor"),
        ("dra", "doktora"),
        ("lic","licencjat"),
        ("nr", "numer"),
        ("św.","święty"),
        ("pl.","plac"),
        ("tzn.","to znaczy"),
        ("tzw.", "tak zwany"),
        ("ul.","ulica"),
        ("zob", "zobacz"),
        ("wsch.","wschód"),
        ("zach.", "zachód"),
    ]
]
