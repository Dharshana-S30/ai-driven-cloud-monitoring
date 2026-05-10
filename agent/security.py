import os
import time

from alerts import send_email_alert
from analyzer import analyze_security_threat
from healer import suggested_actions


MONITORED_DIR = "../MERN-eCommerce"

known_files = {}

suspicious_extensions = [
    ".sh",
    ".exe",
    ".bat",
    ".ps1"
]


def scan_files():

    current_files = {}

    for root, dirs, files in os.walk(MONITORED_DIR):

        if "node_modules" in root:
            continue

        for file in files:

            full_path = os.path.join(root, file)

            modified_time = os.path.getmtime(
                full_path
            )

            current_files[full_path] = modified_time

            # Detect suspicious extensions
            for ext in suspicious_extensions:

                if file.endswith(ext):

                    message = (
                        f"Suspicious file detected: {file}"
                    )

                    print(f"\n🚨 {message}")

                    # AI Threat Analysis
                    try:

                        ai_analysis = (
                            analyze_security_threat(
                                file,
                                "Suspicious file detected during scan."
                            )
                        )

                        print(
                            "\n🤖 AI THREAT ANALYSIS:\n"
                        )

                        print(ai_analysis)

                        print(
                            "\n🛠️ Suggested Actions:\n"
                        )

                        actions = suggested_actions()

                        for action in actions:
                            print(action)

                        actions_text = "\n".join(actions)

                        full_alert = f"""

🚨 SECURITY THREAT DETECTED

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

                    except Exception as e:

                        print(
                            "\n⚠️ AI Analysis Failed:",
                            e
                        )

                        send_email_alert(
                            "Security Threat Detected",
                            message
                        )

    return current_files


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


def start_security_monitor():

    global known_files

    print("\n🔍 Initial File Scan Running...")

    known_files = scan_files()

    print("\n✅ Known Files Stored")

    while True:

        time.sleep(30)

        print("\n🔄 Rescanning Files...")

        current_files = scan_files()

        # Detect new files
        for file in current_files:

            if file not in known_files:

                message = (
                    f"Unknown file appeared: {file}"
                )

                print(f"\n🚨 {message}")

                send_email_alert(
                    "Unknown File Alert",
                    message
                )

            else:

                # Detect modified files
                if (
                    current_files[file]
                    != known_files[file]
                ):

                    message = (
                        f"File modified unexpectedly: {file}"
                    )

                    print(f"\n⚠️ {message}")

                    send_email_alert(
                        "File Modification Alert",
                        message
                    )

        known_files = current_files