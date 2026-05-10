def detect_suspicious_activity(cpu, memory):

    if cpu > 80:
        return "High CPU usage detected. Possible traffic spike."

    if memory > 85:
        return "High memory usage detected. Possible memory leak."

    return None