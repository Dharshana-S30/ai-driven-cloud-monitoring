import os
import time
from alerts import send_email_alert

MONITORED_DIR = "../MERN-eCommerce"

known_files = set()

suspicious_extensions = [
    ".sh",
    ".exe",
    ".bat",
    ".ps1"
]


def scan_files():

    current_files = set()

    for root, dirs, files in os.walk(MONITORED_DIR):

        # Skip node_modules
        if "node_modules" in root:
            continue

        for file in files:

            full_path = os.path.join(root, file)

            current_files.add(full_path)

            # Detect suspicious extensions
            for ext in suspicious_extensions:

                if file.endswith(ext):

                    message = (
                        f"Suspicious file detected: {file}"
                    )

                    print(f"\n🚨 {message}")

                    send_email_alert(
                        "Security Threat Detected",
                        message
                    )

    return current_files


print("\n🔍 Initial File Scan Running...")

known_files = scan_files()

print("\n✅ Known Files Stored")


while True:

    time.sleep(30)

    print("\n🔄 Rescanning Files...")

    current_files = scan_files()

    # Detect unknown files
    new_files = current_files - known_files

    if new_files:

        for file in new_files:

            message = (
                f"Unknown file appeared: {file}"
            )

            print(f"\n🚨 {message}")

            send_email_alert(
                "Unknown File Alert",
                message
            )

    known_files = current_files