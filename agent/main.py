from alerts import send_email_alert

from security import detect_suspicious_activity

from deployment_checker import check_pod_health

from traffic_manager import (
    analyze_traffic,
    monitor_resources
)


# TEST VALUES

cpu_usage = 92
memory_usage = 88
pod_restarts = 5
traffic_rate = 1200


# SECURITY ANALYSIS

security_result = detect_suspicious_activity(
    cpu_usage,
    memory_usage
)


# POD HEALTH ANALYSIS

deployment_result = check_pod_health(
    pod_restarts
)


# TRAFFIC ANALYSIS

traffic_result = analyze_traffic(
    traffic_rate
)


# RESOURCE ANALYSIS

resource_result = monitor_resources(
    cpu_usage=92,
    memory_usage=90,
    pod_name="mern-app"
)


print("\n===== AI CLOUD AGENT =====\n")


print("Security Analysis:")
print(security_result)


print("\nDeployment Analysis:")
print(deployment_result)


print("\nTraffic Analysis:")
print(traffic_result)


print("\nResource Analysis:")
print(resource_result)


# EMAIL ALERTS

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


if "spike" in traffic_result.lower():

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