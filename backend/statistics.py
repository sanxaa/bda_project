from db.database import get_connection
from backend.conflicts import detect_conflicts

def get_exam_stats():
    conn = get_connection()
    cur = conn.cursor(dictionary=True)
    cur.execute("SELECT COUNT(*) AS total FROM examens")
    total = cur.fetchone()["total"]
    conflicts = detect_conflicts(cur)
    conn.close()

    total_conflicts = sum(len(conflicts[t]) for t in conflicts)
    return {
        "total_examens": total,
        "conflits": total_conflicts,
        "détails_conflits": conflicts
    }
