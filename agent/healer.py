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


def restart_pod(pod_name):

    print(
        f"\n♻️ Restarting pod: {pod_name}"
    )

    try:

        delete_command = (
            f"kubectl delete pod {pod_name}"
        )

        subprocess.run(
            delete_command,
            shell=True
        )

        print(
            "\n✅ Pod restart triggered"
        )

        send_email_alert(
            "Pod Recovery Triggered",
            f"Pod restarted automatically: {pod_name}"
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