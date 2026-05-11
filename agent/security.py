import subprocess
import time

from alerts import send_email_alert
from analyzer import analyze_security_threat
from healer import suggested_actions


# =========================================
# SUSPICIOUS FILE TYPES
# =========================================

suspicious_extensions = [

    ".sh",

    ".exe",

    ".bat",

    ".ps1"
]


# =========================================
# DETECT SUSPICIOUS FILES INSIDE MERN POD
# =========================================

def scan_files():

    try:

        # ====================================
        # GET MERN POD NAME
        # ====================================

        command = (
            "kubectl get pods --no-headers"
        )

        output = subprocess.check_output(
            command,
            shell=True,
            text=True
        )

        lines = output.splitlines()

        mern_pod = None

        for line in lines:

            if "mern-app" in line:

                mern_pod = line.split()[0]

                break


        if not mern_pod:

            return (
                "MERN pod not found."
            )


        # ====================================
        # READ FILES INSIDE MERN CONTAINER
        # ====================================

        command = (
            f"kubectl exec {mern_pod} -- ls /app"
        )

        files_output = subprocess.check_output(
            command,
            shell=True,
            text=True
        )


        detected_files = []


        # ====================================
        # CHECK SUSPICIOUS FILES
        # ====================================

        for line in files_output.splitlines():

            for ext in suspicious_extensions:

                if line.endswith(ext):

                    detected_files.append(line)


        # ====================================
        # ALERT IF FOUND
        # ====================================

        if detected_files:

            for file in detected_files:

                print(
                    f"\n🚨 Suspicious file detected: {file}"
                )

                # ================================
                # AI ANALYSIS
                # ================================

                ai_analysis = (
                    analyze_security_threat(
                        file,
                        "Suspicious file detected inside MERN application."
                    )
                )

                print(
                    "\n🤖 AI THREAT ANALYSIS:\n"
                )

                print(ai_analysis)

                actions = suggested_actions()

                print(
                    "\n🛠️ Suggested Actions:\n"
                )

                for action in actions:

                    print(action)


                actions_text = "\n".join(actions)


                full_alert = f"""

🚨 SECURITY THREAT DETECTED

Pod:
{mern_pod}

Suspicious File:
{file}

AI Analysis:
{ai_analysis}

Suggested Actions:
{actions_text}

"""


                send_email_alert(
                    "AI Security Threat Alert",
                    full_alert
                )

            return (
                "Suspicious files detected."
            )


        return (
            "No suspicious files detected."
        )


    except Exception as e:

        return (
            f"Security Scan Failed: {e}"
        )


# =========================================
# SECURITY ANALYSIS
# =========================================

def detect_suspicious_activity(
    cpu,
    memory
):

    if cpu > 80:

        return (
            "High CPU usage detected. "
            "Possible traffic spike."
        )

    if memory > 85:

        return (
            "High memory usage detected. "
            "Possible memory leak."
        )

    return None


# =========================================
# CONTINUOUS SECURITY MONITOR
# =========================================

def start_security_monitor():

    print(
        "\n🔍 Security Monitoring Started..."
    )

    while True:

        print(
            "\n🔄 Scanning MERN Application Files..."
        )

        result = scan_files()

        print(result)

        time.sleep(30)