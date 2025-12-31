import streamlit as st
from db.database import get_connection
import pandas as pd
from backend.api_interface import get_exam_stats, get_conflicts


st.title("📊 Vice-Doyen / Doyen")

conn = get_connection()

if conn:
    # Nombre total d'examens
    total_exams = pd.read_sql("SELECT COUNT(*) AS total FROM examens", conn).iloc[0,0]
    st.metric("Nombre total d'examens", total_exams)

    # Capacité totale des salles
    occupancy = pd.read_sql("SELECT SUM(capacite) AS total_salles FROM lieu_examen", conn).iloc[0,0]
    st.metric("Capacité totale salles", occupancy)

    # Nombre d'examens par département
    query = """
    SELECT d.nom AS departement, COUNT(e.id) AS nb_exams
    FROM examens e
    JOIN modules m ON e.module_id = m.id
    JOIN formations f ON m.formation_id = f.id
    JOIN departements d ON f.dept_id = d.id
    GROUP BY d.nom
    """
    df_exams = pd.read_sql(query, conn)
    
    st.subheader("📊 Nombre d'examens par département")
    st.bar_chart(df_exams.set_index("departement"))

    # Affichage des conflits via API
    conflicts_df = get_conflicts()
    st.subheader("⚠ Conflits détectés")
    st.dataframe(conflicts_df)
else:
    st.error("Impossible de se connecter à la base de données")