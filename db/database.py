import mysql.connector
from config import *

def get_connection():
    return mysql.connector.connect(
        host=DB_HOST,
        user=DB_USER,
        password=DB_PASSWORD,
        database=DB_NAME,
        port=DB_PORT
    )

# Fonctions utilitaires pour récupération des données
def get_modules(cur):
    cur.execute("""
        SELECT m.id, m.formation_id, f.dept_id, COUNT(i.etudiant_id) AS nb_etudiants
        FROM modules m
        JOIN formations f ON m.formation_id = f.id
        LEFT JOIN inscriptions i ON m.id = i.module_id
        GROUP BY m.id
        ORDER BY nb_etudiants DESC
    """)
    return cur.fetchall()

def get_salles(cur):
    cur.execute("SELECT id, capacite FROM lieu_examen ORDER BY capacite DESC")
    return cur.fetchall()

def get_professeurs(cur):
    cur.execute("SELECT id, dept_id FROM professeurs")
    return cur.fetchall()

def get_inscriptions(cur):
    cur.execute("SELECT etudiant_id, module_id FROM inscriptions")
    return cur.fetchall()
