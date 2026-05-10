import requests
import time


LOKI_URL = (
    "http://13.235.50.151:31830/loki/api/v1/query_range"
)


def get_recent_logs():

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

        logs = []

        results = data["data"]["result"]


        for stream in results:

            values = stream["values"]

            for value in values:

                log_line = value[1]

                logs.append(log_line)


        return logs

    except Exception as e:

        return [
            f"Loki Error: {e}"
        ]


# =========================================
# TESTING MODE
# =========================================

if __name__ == "__main__":

    while True:

        print("\n===== LOKI LOGS =====")

        logs = get_recent_logs()

        for log in logs:

            print(log)

        time.sleep(60)
