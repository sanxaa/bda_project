import streamlit as st
from db.database import get_connection
import pandas as pd
from backend.api_interface import get_exam_for_etudiant, get_exam_for_prof

st.title("🎓 Étudiant / Professeur")

conn = get_connection()
user_type = st.radio("Vous êtes :", ["Étudiant", "Professeur"])

if conn:
    if user_type == "Étudiant":
        matricule = st.text_input("Matricule étudiant")
        if matricule:
            query = """
            SELECT e.date_heure, m.nom AS module, l.nom AS salle
            FROM examens e
            JOIN modules m ON e.module_id = m.id
            JOIN lieu_examen l ON e.salle_id = l.id
            JOIN inscriptions i ON i.module_id = m.id
            WHERE i.etudiant_id=%s
            ORDER BY e.date_heure
            """
            df = pd.read_sql(query, conn, params=(matricule,))
            df = get_exam_for_etudiant(matricule)
            st.subheader("📅 Votre emploi du temps")
            st.dataframe(df)
    else:
        prof_id = st.text_input("ID Professeur")
        if prof_id:
            query = """
            SELECT e.date_heure, m.nom AS module, l.nom AS salle
            FROM examens e
            JOIN modules m ON e.module_id = m.id
            JOIN lieu_examen l ON e.salle_id = l.id
            WHERE e.prof_id=%s
            ORDER BY e.date_heure
            """
            df = pd.read_sql(query, conn, params=(prof_id,))
            df = get_exam_for_prof(prof_id)
            st.subheader("📅 Votre emploi du temps")
            st.dataframe(df)
else:
    st.error("Impossible de se connecter à la base de données")