# backend/api_interface.py
from db.database import get_connection
import pandas as pd
from backend.scheduler import generer_examens
from backend.statistics import get_exam_stats
from backend.fill_conflicts import remplir_table_conflits
from backend.conflicts import resolve_conflicts

def generate_edt():
    generer_examens()
    resolve_conflicts()
    remplir_table_conflits()

def get_exam_for_etudiant(etudiant_id):
    conn = get_connection()
    df = pd.read_sql(f"""
        SELECT e.date_heure, m.nom AS module, l.nom AS salle
        FROM examens e
        JOIN modules m ON e.module_id = m.id
        JOIN lieu_examen l ON e.salle_id = l.id
        JOIN inscriptions i ON i.module_id = m.id
        WHERE i.etudiant_id = %s
        ORDER BY e.date_heure
    """, conn, params=(etudiant_id,))
    conn.close()
    return df

def get_exam_for_prof(prof_id):
    conn = get_connection()
    df = pd.read_sql(f"""
        SELECT e.date_heure, m.nom AS module, l.nom AS salle
        FROM examens e
        JOIN modules m ON e.module_id = m.id
        JOIN lieu_examen l ON e.salle_id = l.id
        WHERE e.prof_id = %s
        ORDER BY e.date_heure
    """, conn, params=(prof_id,))
    conn.close()
    return df

def get_conflicts():
    conn = get_connection()
    df = pd.read_sql("SELECT * FROM conflits ORDER BY date_heure", conn)
    conn.close()
    return df

def get_exam_for_dept(dept_name):
    conn = get_connection()
    df = pd.read_sql("""
        SELECT f.nom AS formation, COUNT(e.id) AS nb_exams
        FROM examens e
        JOIN modules m ON e.module_id = m.id
        JOIN formations f ON m.formation_id = f.id
        JOIN departements d ON f.dept_id = d.id
        WHERE d.nom=%s
        GROUP BY f.nom
    """, conn, params=(dept_name,))
    conn.close()
    return df
