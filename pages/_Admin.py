import streamlit as st
from db.database import get_connection
import pandas as pd
from backend.api_interface import generate_edt, get_conflicts
st.title("⚙️ Administrateur Examens")

conn = get_connection()

if st.button("🚀 Générer l'emploi du temps"):
    generate_edt()# Ici on appelle la fonction Python de génération de l'EDT
    st.success("EDT généré avec succès")

# Afficher les conflits
    conflicts = get_conflicts()
    st.subheader("⚠ Conflits détectés")
    st.dataframe(conflicts)
# Affichage du nombre d'examens par département
if conn:
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
    st.dataframe(df_exams)
else:
    st.error("Impossible de se connecter à la base de données")
