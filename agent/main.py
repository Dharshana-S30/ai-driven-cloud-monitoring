from alerts import send_email_alert

from security import detect_suspicious_activity

from deployment_checker import (
    check_pod_health,
    validate_deployment
)

from traffic_manager import (
    analyze_traffic,
    monitor_resources
)

from healer import (
    detect_failed_pod,
    collect_pod_logs,
    restart_pod,
    rollback_deployment,
    check_application_health
)


# =========================================
# PRE DEPLOYMENT VALIDATION
# =========================================

deployment_ready = validate_deployment()

if not deployment_ready:

    print(
        "\n❌ Deployment blocked"
    )

    exit()


# =========================================
# TEST VALUES
# =========================================

cpu_usage = 92
memory_usage = 88
pod_restarts = 5
traffic_rate = 1200


# =========================================
# SECURITY ANALYSIS
# =========================================

security_result = detect_suspicious_activity(
    cpu_usage,
    memory_usage
)


# =========================================
# POD HEALTH ANALYSIS
# =========================================

deployment_result = check_pod_health(
    pod_restarts
)


# =========================================
# TRAFFIC ANALYSIS
# =========================================

traffic_result = analyze_traffic(
    traffic_rate
)


# =========================================
# RESOURCE ANALYSIS
# =========================================

resource_result = monitor_resources(
    cpu_usage=92,
    memory_usage=90,
    pod_name="mern-app"
)


# =========================================
# MAIN OUTPUT
# =========================================

print("\n===== AI CLOUD AGENT =====\n")


print("Security Analysis:")
print(security_result)


print("\nDeployment Analysis:")
print(deployment_result)


print("\nTraffic Analysis:")
print(traffic_result)


print("\nResource Analysis:")
print(resource_result)


# =========================================
# EMAIL ALERTS
# =========================================

if security_result:

    send_email_alert(
        "Security Alert",
        security_result
    )


if "restarting" in deployment_result.lower():

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


# =========================================
# DEPLOYMENT HEALTH CHECK
# =========================================

print("\n===== DEPLOYMENT HEALTH CHECK =====")


deployment_unhealthy = True


if deployment_unhealthy:

    print(
        "\n🚨 Deployment unhealthy detected"
    )

    rollback_deployment("mern-app")

else:

    print(
        "\n✅ Deployment healthy"
    )


# =========================================
# APPLICATION HEALTH CHECK
# =========================================

print("\n===== APPLICATION HEALTH CHECK =====")


app_url = (
    "http://13.235.50.151:30007"
)


app_healthy = check_application_health(
    app_url
)


if not app_healthy:

    print(
        "\n🚨 Application Down Detected"
    )

    send_email_alert(
        "Application Recovery Alert",
        "Application unavailable. Restarting deployment."
    )

    restart_pod("mern-app")

else:

    print(
        "\n✅ Application Healthy"
    )


# =========================================
# FAILED POD DETECTION
# =========================================

print("\n===== SELF HEALING CHECK =====")


failed_pod = detect_failed_pod()


if failed_pod:

    print(
        f"\n🚨 Failed Pod Detected: {failed_pod}"
    )

    logs = collect_pod_logs(
        failed_pod
    )

    print("\n📄 POD LOGS:\n")

    print(logs[:1000])

    restart_pod("mern-app")

else:

    print(
        "\n✅ No failed pods detected"
    )
