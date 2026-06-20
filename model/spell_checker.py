from spellchecker import SpellChecker

spell = SpellChecker()

IT_TERMS = {
    "vpn", "sql", "api", "cpu", "gpu", "dns", "dhcp",
    "lan", "wan", "ssh", "rdp", "smtp", "imap", "saml",
    "ldap", "oauth", "jwt", "dockerfile", "kubernetes",
    "postgres", "postgresql", "mongodb", "redis", "nginx"
}


def correct_spelling(text: str) -> str:

    corrected = []

    for word in text.split():

        clean_word = word.lower()

        if (
            clean_word in IT_TERMS
            or any(c.isdigit() for c in word)
            or len(word) <= 2
        ):
            corrected.append(word)
            continue

        suggestion = spell.correction(clean_word)

        corrected.append(suggestion if suggestion else word)

    return " ".join(corrected)