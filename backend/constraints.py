from config import MAX_EXAMS_PROF_PAR_JOUR, MAX_EXAMS_ETU_PAR_JOUR

def salle_disponible(cur, salle_id, date_heure, nb_etudiants, capacite):
    if nb_etudiants > capacite:
        return False
    cur.execute("SELECT 1 FROM examens WHERE salle_id=%s AND DATE(date_heure)=%s LIMIT 1",
                (salle_id, date_heure.date()))
    return cur.fetchone() is None

def prof_disponible(cur, prof_id, date_heure):
    cur.execute("SELECT COUNT(*) FROM examens WHERE prof_id=%s AND DATE(date_heure)=%s",
                (prof_id, date_heure.date()))
    return cur.fetchone()[0] < MAX_EXAMS_PROF_PAR_JOUR

def etudiant_disponible(cur, etudiants, date_heure):
    if not etudiants:
        return []
    placeholders = ','.join(['%s'] * len(etudiants))
    query = f"""
        SELECT DISTINCT etudiant_id FROM examens
        JOIN inscriptions USING(module_id)
        WHERE etudiant_id IN ({placeholders}) AND DATE(date_heure)=%s
    """
    cur.execute(query, etudiants + [date_heure.date()])
    result = cur.fetchall()
    indisponibles = {r[0] for r in result}
    return [e for e in etudiants if e not in indisponibles]
