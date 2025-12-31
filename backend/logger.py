from config import LOG_FILE

def log_message(message):
    print(message)
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(message + "\n")

def clear_log():
    with open(LOG_FILE, "w", encoding="utf-8") as f:
        f.write("")
