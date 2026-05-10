import requests
import time

PROMETHEUS_URL = "http://13.235.50.151:32250/api/v1/query"
def query_prometheus(query):
    try:
        response = requests.get(
            PROMETHEUS_URL,
            params={"query": query}
        )

        data = response.json()

        print(data)
        return data["data"]["result"]

    except Exception as e:
        print("Prometheus Error:", e)
        return []


def get_cpu_usage():
    query = '100 - (avg by(instance)(rate(node_cpu_seconds_total{mode="idle"}[2m])) * 100)'
    result = query_prometheus(query)

    print("\nCPU Usage:")
    print(result)


def get_memory_usage():
    query = '(1 - (node_memory_MemAvailable_bytes / node_memory_MemTotal_bytes)) * 100'
    result = query_prometheus(query)

    print("\nMemory Usage:")
    print(result)


def get_pod_restarts():
    query = 'kube_pod_container_status_restarts_total'
    result = query_prometheus(query)

    print("\nPod Metrics:")
    print(result)


def get_request_rate():
    query = 'rate(container_network_receive_bytes_total[1m])'
    result = query_prometheus(query)

    print("\nRequest Rate:")
    print(result)


while True:
    print("\n===== PROMETHEUS METRICS =====")

    get_cpu_usage()
    get_memory_usage()
    get_pod_restarts()
    get_request_rate()

    time.sleep(60)