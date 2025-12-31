from collections import defaultdict

def balance_surveillances(prof_compteurs, profs, seuil=1):
    """
    Trie les profs par nombre de surveillances, moins surveillances d'abord
    profs : liste de dictionnaires [{'id':1,'dept_id':2}, ...]
    prof_compteurs : dict {prof_id: nb_surveillance}
    """
    sorted_profs = sorted(profs, key=lambda x: prof_compteurs.get(x["id"], 0))

    valeurs = [prof_compteurs.get(p["id"], 0) for p in profs]
    if valeurs and max(valeurs) - min(valeurs) > seuil:
        # Équilibrage minimal
        sorted_profs[0], sorted_profs[-1] = sorted_profs[-1], sorted_profs[0]

    return sorted_profs
