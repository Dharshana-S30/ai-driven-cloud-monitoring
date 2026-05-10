from alerts import send_email_alert
from security import detect_suspicious_activity
from deployment_checker import check_pod_health
from traffic_manager import analyze_traffic


cpu_usage = 92
memory_usage = 88
pod_restarts = 5
traffic_rate = 1200


security_result = detect_suspicious_activity(
    cpu_usage,
    memory_usage
)

deployment_result = check_pod_health(
    pod_restarts
)

traffic_result = analyze_traffic(
    traffic_rate
)


print("\n===== AI CLOUD AGENT =====\n")

print("Security Analysis:")
print(security_result)

print("\nDeployment Analysis:")
print(deployment_result)

print("\nTraffic Analysis:")
print(traffic_result)


if security_result:

    send_email_alert(
        "Security Alert",
        security_result
    )


if "restarting" in deployment_result:

    send_email_alert(
        "Pod Crash Alert",
        deployment_result
    )


if "spike" in traffic_result:

    send_email_alert(
        "Traffic Spike Alert",
        traffic_result
    )


if cpu_usage > 80:

    send_email_alert(
        "CPU Overload Alert",
        f"CPU usage critically high: {cpu_usage}%"
    )


if memory_usage > 85:

    send_email_alert(
        "Memory Overload Alert",
        f"Memory usage critically high: {memory_usage}%"
    )