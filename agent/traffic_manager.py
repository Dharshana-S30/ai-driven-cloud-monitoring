from healer import restart_pod
from alerts import send_email_alert


def analyze_traffic(rate):

    if rate > 5000:

        print(
            "\n🚨 ABNORMAL TRAFFIC SPIKE DETECTED"
        )

        emergency_message = f"""

Emergency Traffic Alert

Traffic spike detected.

Current Request Rate:
{rate} requests

Possible Causes:
- DDoS attack
- Bot traffic
- Abnormal request flood

Temporary Actions Taken:
- Scaling pods
- Enabling rate limiting

"""

        print(emergency_message)

        send_email_alert(
            "Emergency Traffic Spike Alert",
            emergency_message
        )

        return (
            "Abnormal traffic spike detected."
        )

    elif rate > 1000:

        print(
            "\n⚠️ HIGH TRAFFIC DETECTED"
        )

        return "Traffic increasing gradually."

    return "Traffic normal."


def monitor_resources(
    cpu_usage,
    memory_usage,
    pod_name
):

    if (
        cpu_usage > 85
        or memory_usage > 85
    ):

        overload_message = f"""

🚨 RESOURCE OVERLOAD DETECTED

Pod:
{pod_name}

CPU Usage:
{cpu_usage}%

Memory Usage:
{memory_usage}%

Action:
Restarting unhealthy pod.

"""

        print(overload_message)

        send_email_alert(
            "CPU/Memory Overload Alert",
            overload_message
        )

        restart_pod(pod_name)

        return (
            "Overloaded pod restarted."
        )

    return "Resources normal."