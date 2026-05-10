import subprocess

from alerts import send_email_alert


def suggested_actions():

    actions = [

        "1. Restart affected pod",

        "2. Stop suspicious container",

        "3. Delete suspicious file",

        "4. Continue monitoring"
    ]

    return actions


def restart_pod(deployment_name):

    print(
        f"\n♻️ Restarting deployment: {deployment_name}"
    )

    try:

        command = (
            f"kubectl rollout restart deployment/{deployment_name}"
        )

        subprocess.run(
            command,
            shell=True
        )

        print(
            "\n✅ Deployment restart triggered"
        )

        send_email_alert(
            "Self-Healing Triggered",
            f"Deployment restarted automatically: {deployment_name}"
        )

    except Exception as e:

        print(
            "\n❌ Restart Failed:",
            e
        )


def collect_pod_logs(pod_name):

    try:

        command = (
            f"kubectl logs {pod_name}"
        )

        result = subprocess.check_output(
            command,
            shell=True,
            text=True
        )

        return result

    except Exception as e:

        return (
            f"Log collection failed: {e}"
        )


def detect_failed_pod():

    try:

        command = (
            "kubectl get pods --no-headers"
        )

        output = subprocess.check_output(
            command,
            shell=True,
            text=True
        )

        lines = output.splitlines()

        for line in lines:

            if (
                "CrashLoopBackOff" in line
                or "Error" in line
            ):

                pod_name = line.split()[0]

                return pod_name

        return None

    except Exception as e:

        print(
            "\n❌ Detection Failed:",
            e
        )

        return None
    

    def rollback_deployment(deployment_name):

    print(
        f"\n⏪ Rolling back deployment: {deployment_name}"
    )

    try:

        command = (
            f"kubectl rollout undo deployment/{deployment_name}"
        )

        subprocess.run(
            command,
            shell=True
        )

        print(
            "\n✅ Rollback completed"
        )

        send_email_alert(
            "Deployment Rollback Triggered",
            f"Deployment rolled back automatically: {deployment_name}"
        )

    except Exception as e:

        print(
            "\n❌ Rollback Failed:",
            e
        )