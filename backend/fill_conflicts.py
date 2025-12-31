from db.database import get_connection
from backend.conflicts import detect_conflicts

def remplir_table_conflits():
    conn = get_connection()
    cur = conn.cursor(dictionary=True)

    cur.execute("DELETE FROM conflits")
    conn.commit()

    conflicts = detect_conflicts(cur)

    # Étudiants
    for row in conflicts["etudiants"]:
        cur.execute("""
            INSERT INTO conflits (etudiant_id, date_heure, nb_examens, type_conflit)
            VALUES (%s, %s, %s, %s)
        """, (row["etudiant_id"], row["date_jour"], row["nb_examens"], "etudiant"))

    # Profs
    for row in conflicts["profs"]:
        cur.execute("""
            INSERT INTO conflits (prof_id, date_heure, nb_examens, type_conflit)
            VALUES (%s, %s, %s, %s)
        """, (row["prof_id"], row["date_jour"], row["nb_examens"], "prof"))

    # Salles
    for row in conflicts["salles"]:
        cur.execute("""
            INSERT INTO conflits (salle_id, date_heure, nb_examens, type_conflit)
            VALUES (%s, %s, %s, %s)
        """, (row["salle_id"], row["date_jour"], row["nb_examens"], "salle"))

    conn.commit()
    conn.close()
