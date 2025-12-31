# backend/scheduler.py
import time
from datetime import datetime, timedelta
from collections import defaultdict
from db.database import get_connection
from backend.logger import log_message, clear_log
from backend.balance_surveillances import balance_surveillances
from config import CRENEAUX_PAR_JOUR, MAX_EXAMS_PROF_PAR_JOUR, MAX_EXAMS_ETU_PAR_JOUR, DUREE_EXAM, START_DATE

MAX_JOURS = 30

def generer_examens():
    clear_log()
    start_time = time.time()
    log_message("🚀 Début génération EDT avancée")

    conn = get_connection()
    cur = conn.cursor(dictionary=True)

    # Charger modules, salles, profs, inscriptions
    cur.execute("SELECT m.id AS module_id, f.dept_id FROM modules m JOIN formations f ON m.formation_id=f.id")
    modules = cur.fetchall()

    cur.execute("SELECT id, capacite FROM lieu_examen ORDER BY capacite DESC")
    salles = cur.fetchall()

    cur.execute("SELECT id, dept_id FROM professeurs")
    profs = cur.fetchall()

    cur.execute("SELECT module_id, etudiant_id FROM inscriptions")
    inscriptions = cur.fetchall()

    # Map module -> étudiants
    module_etudiants = defaultdict(list)
    for r in inscriptions:
        module_etudiants[r["module_id"]].append(r["etudiant_id"])

    # Disponibilités
    etu_jour = defaultdict(int)      # (etudiant_id, date) -> 0/1
    prof_jour = defaultdict(int)     # (prof_id, date) -> nb exams
    salle_jour = defaultdict(int)    # (salle_id, date) -> 0/1

    # Tri modules par nb étudiants décroissant
    modules.sort(key=lambda m: -len(module_etudiants[m["module_id"]]))

    date_depart = datetime.strptime(START_DATE, "%Y-%m-%d %H:%M:%S")
    placed, conflicts = 0, 0

    for mod in modules:
        module_id = mod["module_id"]
        dept_id = mod["dept_id"]
        etudiants_module = module_etudiants[module_id]
        nb_etudiants = len(etudiants_module)

        best_choice = None
        best_cost = float("inf")

        # Chercher meilleur jour/créneau/salle/prof
        for j in range(MAX_JOURS):
            jour = date_depart + timedelta(days=j)
            for h in CRENEAUX_PAR_JOUR:
                date_exam = jour.replace(hour=h, minute=0)

                # Vérifier étudiants
                if any(etu_jour[(etu, date_exam.date())] >= MAX_EXAMS_ETU_PAR_JOUR for etu in etudiants_module):
                    continue

                # Vérifier salle
                for salle in salles:
                    if salle["capacite"] < nb_etudiants:  # trop petit
                        continue
                    if salle_jour.get((salle["id"], date_exam.date()), 0) == 1:
                        continue

                    # Trier profs par équilibrage et priorité département
                    profs_sorted = balance_surveillances(prof_jour, profs)
                    for prof in profs_sorted:
                        if prof_jour[(prof["id"], date_exam.date())] >= MAX_EXAMS_PROF_PAR_JOUR:
                            continue

                        # Calcul coût simple
                        cost = abs(salle["capacite"] - nb_etudiants) + prof_jour[(prof["id"], date_exam.date())]*5
                        if cost < best_cost:
                            best_cost = cost
                            best_choice = (date_exam, salle["id"], prof["id"])
                    if best_choice:
                        break
                if best_choice:
                    break
            if best_choice:
                break

        if not best_choice:
            log_message(f"❌ Module {module_id} non placé")
            conflicts += 1
            continue

        # Placement final
        date_exam, salle_id, prof_id = best_choice
        try:
            cur.execute(
                "INSERT INTO examens (module_id, prof_id, salle_id, date_heure, duree_minutes) VALUES (%s,%s,%s,%s,%s)",
                (module_id, prof_id, salle_id, date_exam, DUREE_EXAM)
            )
            conn.commit()
        except Exception as e:
            log_message(f"❌ Erreur placement module {module_id}: {e}")
            conflicts += 1
            continue

        # Mettre à jour disponibilités
        for etu in etudiants_module:
            etu_jour[(etu, date_exam.date())] = 1
        prof_jour[(prof_id, date_exam.date())] += 1
        salle_jour[(salle_id, date_exam.date())] = 1

        placed += 1
        log_message(f"✔ Module {module_id} → {date_exam} | Salle {salle_id} | Prof {prof_id}")

    conn.close()
    elapsed = time.time() - start_time
    log_message("===================================")
    log_message(f"📊 Examens placés : {placed}")
    log_message(f"⚠ Conflits : {conflicts}")
    log_message(f"⏱ Temps total : {elapsed:.2f} s")
    log_message("✅ Génération EDT terminée")
