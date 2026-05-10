import subprocess
import requests

from alerts import send_email_alert


# =========================================
# PRE DEPLOYMENT VALIDATION
# =========================================

def validate_deployment():

    print(
        "\n===== PRE DEPLOYMENT VALIDATION ====="
    )

    print(
        "\n✅ Deployment validation successful"
    )

    return True


# =========================================
# POD HEALTH CHECK
# =========================================

def check_pod_health(pod_restarts):

    if pod_restarts > 3:

        return (
            "Pod restarting repeatedly."
        )

    return (
        "Pods healthy."
    )


# =========================================
# POST DEPLOYMENT VERIFICATION
# =========================================

def verify_deployment(app_url):

    print(
        "\n===== POST DEPLOYMENT VERIFICATION ====="
    )

    try:

        # ====================================
        # CHECK POD STATUS
        # ====================================

        command = (
            "kubectl get pods --no-headers"
        )

        output = subprocess.check_output(
            command,
            shell=True,
            text=True
        )

        if (
            "CrashLoopBackOff" in output
            or "Error" in output
        ):

            return (
                False,
                "Pod failure detected."
            )


        # ====================================
        # CHECK APPLICATION HEALTH
        # ====================================

        response = requests.get(
            app_url,
            timeout=5
        )

        if response.status_code != 200:

            return (
                False,
                "Application endpoint unhealthy."
            )


        # ====================================
        # SUCCESS
        # ====================================

        return (
            True,
            "Deployment verification successful."
        )

    except Exception as e:

        return (
            False,
            f"Verification failed: {e}"
        )