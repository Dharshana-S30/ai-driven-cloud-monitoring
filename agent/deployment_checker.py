def check_pod_health(restarts):

    if restarts > 3:
        return "Pod restarting repeatedly."

    return "Pods healthy."