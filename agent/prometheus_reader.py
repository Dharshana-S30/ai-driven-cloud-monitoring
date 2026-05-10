import requests


PROMETHEUS_URL = (
    "http://13.235.50.151:32250"
)


def query_prometheus(query):

    url = (
        f"{PROMETHEUS_URL}/api/v1/query"
    )

    response = requests.get(
        url,
        params={"query": query}
    )

    data = response.json()

    return data["data"]["result"]


# =========================================
# CPU USAGE
# =========================================

def get_cpu_usage():

    query = (
        '100 - (avg by(instance)'
        '(rate(node_cpu_seconds_total'
        '{mode="idle"}[1m])) * 100)'
    )

    return query_prometheus(query)


# =========================================
# MEMORY USAGE
# =========================================

def get_memory_usage():

    query = (
        '(1 - (node_memory_MemAvailable_bytes '
        '/ node_memory_MemTotal_bytes)) * 100'
    )

    return query_prometheus(query)


# =========================================
# POD RESTARTS
# =========================================

def get_pod_metrics():

    query = (
        'kube_pod_container_status_restarts_total'
    )

    return query_prometheus(query)


# =========================================
# REQUEST RATE
# =========================================

def get_request_rate():

    query = (
        'rate(container_network_receive_bytes_total[1m])'
    )

    return query_prometheus(query)
