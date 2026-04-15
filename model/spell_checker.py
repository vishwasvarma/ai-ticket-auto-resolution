from symspellpy import SymSpell, Verbosity
import pkg_resources

_sym_spell = None

def get_spell_checker():
    global _sym_spell
    if _sym_spell is None:
        _sym_spell = SymSpell(max_dictionary_edit_distance=2, prefix_length=7)
        dict_path = pkg_resources.resource_filename(
            "symspellpy", "frequency_dictionary_en_82_765.txt"
        )
        _sym_spell.load_dictionary(dict_path, term_index=0, count_index=1)
        # Add IT-specific terms so they are never "corrected" away
        it_terms = [
            "vpn", "sql", "api", "cpu", "gpu", "dns", "dhcp",
            "lan", "wan", "ssh", "rdp", "smtp", "imap", "saml",
            "ldap", "oauth", "jwt", "dockerfile", "kubernetes",
            "postgres", "postgresql", "mongodb", "redis", "nginx",
        ]
        for term in it_terms:
            _sym_spell.create_dictionary_entry(term, 10_000)
    return _sym_spell


def correct_spelling(text: str) -> str:
    """
    Returns spell-corrected text.
    Falls back to original word if no suggestion found.
    """
    checker = get_spell_checker()
    words = text.split()
    corrected = []
    for word in words:
        # Keep tokens that look like IDs, codes, or numbers unchanged
        if any(c.isdigit() for c in word) or len(word) <= 2:
            corrected.append(word)
            continue
        suggestions = checker.lookup(
            word.lower(), Verbosity.CLOSEST, max_edit_distance=2
        )
        if suggestions:
            corrected.append(suggestions[0].term)
        else:
            corrected.append(word)
    return " ".join(corrected)