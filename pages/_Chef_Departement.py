import streamlit as st
from db.database import get_connection
import pandas as pd
from backend.api_interface import get_exam_for_dept
st.title("🏫 Chef de Département")

conn = get_connection()

dept = st.selectbox("Choisir département", ["Informatique",
    "Math",
    "Biologie",
    "Physique",
    "Chimie",
    "Agronomie",
    "STAPS"])
if conn and dept:
    query = """
    SELECT f.nom AS formation, COUNT(e.id) AS nb_exams
    FROM examens e
    JOIN modules m ON e.module_id = m.id
    JOIN formations f ON m.formation_id = f.id
    JOIN departements d ON f.dept_id = d.id
    WHERE d.nom=%s
    GROUP BY f.nom
    """
    df = pd.read_sql(query, conn, params=(dept,))
    st.subheader(f"📊 Nombre d'examens par formation pour {dept}")
    st.dataframe(df)

    if st.button("✅ Valider EDT Département"):
        df = get_exam_for_dept(dept)
        st.dataframe(df)
        st.success(f"EDT du département {dept} validé")
else:
    st.error("Impossible de se connecter à la base de données")