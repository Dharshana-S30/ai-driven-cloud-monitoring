import time

from alerts import send_email_alert

from prometheus_reader import (
    get_cpu_usage,
    get_memory_usage,
    get_pod_metrics,
    get_request_rate
)

from loki_reader import (
    get_recent_logs
)

from security import (
    detect_suspicious_activity
)

from deployment_checker import (
    check_pod_health,
    validate_deployment,
    verify_deployment
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


print("\n🚀 AI CLOUD AGENT STARTED")


# =========================================
# MAIN CONTINUOUS LOOP
# =========================================

while True:

    print(
        "\n=================================="
    )

    print(
        "🤖 RUNNING AI MONITORING CYCLE"
    )

    print(
        "=================================="
    )


    # =====================================
    # READ PROMETHEUS METRICS
    # =====================================

    cpu_metrics = get_cpu_usage()

    memory_metrics = get_memory_usage()

    pod_metrics = get_pod_metrics()

    request_metrics = get_request_rate()


    # =====================================
    # EXTRACT REAL VALUES
    # =====================================

    try:

        cpu_usage = float(
            cpu_metrics[0]["value"][1]
        )

    except:

        cpu_usage = 0


    try:

        memory_usage = float(
            memory_metrics[0]["value"][1]
        )

    except:

        memory_usage = 0


    try:

        traffic_rate = float(
            request_metrics[0]["value"][1]
        )

    except:

        traffic_rate = 0


    # simulated for now
    pod_restarts = 5


    print(f"\nCPU Usage: {cpu_usage}%")

    print(f"Memory Usage: {memory_usage}%")

    print(f"Traffic Rate: {traffic_rate}")


    # =====================================
    # SECURITY ANALYSIS
    # =====================================

    security_result = (
        detect_suspicious_activity(
            cpu_usage,
            memory_usage
        )
    )

    print(
        "\n🔐 SECURITY ANALYSIS:"
    )

    print(security_result)


    # =====================================
    # POD HEALTH ANALYSIS
    # =====================================

    deployment_result = (
        check_pod_health(
            pod_restarts
        )
    )

    print(
        "\n📦 DEPLOYMENT ANALYSIS:"
    )

    print(deployment_result)


    # =====================================
    # TRAFFIC ANALYSIS
    # =====================================

    traffic_result = (
        analyze_traffic(
            traffic_rate
        )
    )

    print(
        "\n🌐 TRAFFIC ANALYSIS:"
    )

    print(traffic_result)


    # =====================================
    # RESOURCE ANALYSIS
    # =====================================

    resource_result = (
        monitor_resources(
            cpu_usage,
            memory_usage,
            "mern-app"
        )
    )

    print(
        "\n💻 RESOURCE ANALYSIS:"
    )

    print(resource_result)


    # =====================================
    # READ LOKI LOGS
    # =====================================

    print(
        "\n📄 READING LOGS:"
    )

    logs = get_recent_logs()

    print(logs)


    # =====================================
    # APPLICATION HEALTH CHECK
    # =====================================

    app_url = (
        "http://13.235.50.151:30007"
    )

    app_healthy = (
        check_application_health(
            app_url
        )
    )

    if not app_healthy:

        print(
            "\n🚨 APPLICATION DOWN"
        )

        send_email_alert(
            "Application Down",
            "Application unavailable."
        )

        restart_pod("mern-app")

    else:

        print(
            "\n✅ APPLICATION HEALTHY"
        )


    # =====================================
    # DEPLOYMENT VERIFICATION
    # =====================================

    verification_result = (
        verify_deployment(
            app_url
        )
    )

    if verification_result[0]:

        print(
            "\n✅ DEPLOYMENT VERIFIED"
        )

    else:

        print(
            "\n🚨 DEPLOYMENT FAILURE"
        )

        print(
            verification_result[1]
        )

        rollback_deployment(
            "mern-app"
        )


    # =====================================
    # FAILED POD DETECTION
    # =====================================

    print(
        "\n===== SELF HEALING CHECK ====="
    )

    failed_pod = detect_failed_pod()

    if failed_pod:

        print(
            f"\n🚨 FAILED POD: {failed_pod}"
        )

        logs = collect_pod_logs(
            failed_pod
        )

        print(
            "\n📄 POD LOGS:\n"
        )

        print(logs[:1000])

        restart_pod("mern-app")

    else:

        print(
            "\n✅ NO FAILED PODS"
        )


    # =====================================
    # WAIT 60 SECONDS
    # =====================================

    print(
        "\n⏳ Waiting 60 seconds..."
    )

    time.sleep(60)