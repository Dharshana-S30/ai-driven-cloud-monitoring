import requests
import time

LOKI_URL = "http://13.235.50.151:31830/loki/api/v1/query_range"


def read_logs():
    try:
        query = '{namespace="default"}'

        response = requests.get(
            LOKI_URL,
            params={
                "query": query,
                "limit": 5
            }
        )

        data = response.json()

        print("\n===== LOKI LOGS =====")
        print(data)

    except Exception as e:
        print("Loki Error:", e)


while True:
    read_logs()
    time.sleep(60)