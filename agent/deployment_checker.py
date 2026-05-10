import os

from alerts import send_email_alert


def validate_deployment():

    print(
        "\n===== PRE DEPLOYMENT VALIDATION ====="
    )

    required_files = [

        "../Dockerfile",

        "../k8s/deployment.yaml",

        "../k8s/service.yaml"
    ]

    missing_files = []


    for file in required_files:

        if not os.path.exists(file):

            missing_files.append(file)


    if missing_files:

        message = f"""

❌ Deployment Validation Failed

Missing Files:
{missing_files}

Deployment stopped.

"""

        print(message)

        send_email_alert(
            "Deployment Validation Failed",
            message
        )

        return False


    print(
        "\n✅ Deployment validation successful"
    )

    send_email_alert(
        "Deployment Validation Success",
        "All required deployment files exist."
    )

    return True


def check_pod_health(pod_restarts):

    if pod_restarts > 3:

        return (
            "Pod restarting repeatedly."
        )

    return "Pod healthy."