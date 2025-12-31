
# config.py
DB_NAME = "exam_planning"
DB_USER = "root"
DB_PASSWORD = ""
DB_HOST = "localhost"
DB_PORT = 3306

MAX_EXAMS_PROF_PAR_JOUR = 3
MAX_EXAMS_ETU_PAR_JOUR = 1

CRENEAUX_PAR_JOUR = [9, 11, 14, 16]  # heures possibles des examens
CRENEAU_HOURS = 2
DUREE_EXAM = 90

START_DATE = "2026-01-10 09:00:00"

LOG_FILE = "placement_logs.txt"
