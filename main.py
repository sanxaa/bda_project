from backend.api_interface import generate_edt, get_exam_for_etudiant, get_exam_for_prof, get_conflicts
from backend.statistics import get_exam_stats

if __name__ == "__main__":
    print("Début génération EDT...")
    generate_edt()

    stats = get_exam_stats()
    print("\n--- Statistiques ---")
    print(f"Examens placés : {stats['total_examens']}")
    print(f"Conflits totaux : {stats['conflits']}")
