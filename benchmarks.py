import time
from backend.scheduler import generer_examens
from backend.statistics import get_exam_stats

def run_benchmarks():
    start = time.time()
    generer_examens()
    end = time.time()
    stats = get_exam_stats()
    print(f"Temps total d'exécution: {end-start:.2f}s")
    print(f"Total examens placés: {stats['total_examens']}")
    print(f"Conflits détectés: {stats['conflits']}")
    return end-start, stats
