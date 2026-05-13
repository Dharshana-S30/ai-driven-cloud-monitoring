import requests
import boto3
import time
import os
from gtts import gTTS
from datetime import datetime, timedelta

# ================================
# KEYS FROM ENVIRONMENT
# ================================
GROQ_API_KEY = os.environ.get("GROQ_API_KEY", "").strip()
TELEGRAM_TOKEN = os.environ.get("TELEGRAM_TOKEN", "").strip()
TELEGRAM_CHAT_ID = os.environ.get("TELEGRAM_CHAT_ID", "").strip()
AWS_ACCESS_KEY_ID = os.environ.get("AWS_ACCESS_KEY_ID", "").strip()
AWS_SECRET_ACCESS_KEY = os.environ.get("AWS_SECRET_ACCESS_KEY", "").strip()
EC2_INSTANCE_ID = os.environ.get("EC2_INSTANCE_ID", "").strip()# ================================
# AWS CLOUDWATCH CONNECTION
# ================================
cloudwatch = boto3.client(
    'cloudwatch',
    region_name='ap-south-1',
    aws_access_key_id=AWS_ACCESS_KEY_ID,
    aws_secret_access_key=AWS_SECRET_ACCESS_KEY
)

ec2 = boto3.client(
    'ec2',
    region_name='ap-south-1',
    aws_access_key_id=AWS_ACCESS_KEY_ID,
    aws_secret_access_key=AWS_SECRET_ACCESS_KEY
)

# ================================
# GET REAL AWS METRICS
# ================================
def get_aws_metrics():
    print("📊 Fetching real AWS metrics...")

    # Get CPU usage
    cpu_response = cloudwatch.get_metric_statistics(
        Namespace='AWS/EC2',
        MetricName='CPUUtilization',
        Dimensions=[{
            'Name': 'InstanceId',
            'Value': EC2_INSTANCE_ID
        }],
        StartTime=datetime.utcnow() - timedelta(minutes=5),
        EndTime=datetime.utcnow(),
        Period=300,
        Statistics=['Average']
    )

    cpu = 0
    if cpu_response['Datapoints']:
        cpu = round(cpu_response['Datapoints'][0]['Average'], 2)

    # Get instance status
    instance_response = ec2.describe_instance_status(
        InstanceIds=[EC2_INSTANCE_ID]
    )

    instance_status = "UNKNOWN"
    system_status = "UNKNOWN"

    if instance_response['InstanceStatuses']:
        status = instance_response['InstanceStatuses'][0]
        instance_status = status['InstanceStatus']['Status']
        system_status = status['SystemStatus']['Status']

    # Check if MERN app is responding
    app_status = "DOWN"
    try:
        instance_info = ec2.describe_instances(
            InstanceIds=[EC2_INSTANCE_ID]
        )
        public_ip = instance_info['Reservations'][0]['Instances'][0].get(
            'PublicIpAddress', 'N/A'
        )
        app_response = requests.get(
            f"http://{public_ip}:30007",
            timeout=5
        )
        if app_response.status_code == 200:
            app_status = "RUNNING"
    except:
        app_status = "DOWN"

    # Build real log
    real_log = f"""
    PRE-DEPLOYMENT CHECK
    Time: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
    ─────────────────────────────
    EC2 Instance ID: {EC2_INSTANCE_ID}
    Instance Status: {instance_status}
    System Status: {system_status}
    CPU Usage: {cpu}%
    MERN App Status: {app_status}
    Port 30007: {app_status}
    Region: ap-south-1
    ─────────────────────────────
    """

    print(real_log)
    return real_log, cpu, instance_status, app_status

# ================================
# ANALYZE WITH GROQ
# ================================
def analyze_with_groq(log):
    print("🤖 Groq analyzing pre-deployment status...")

    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }

    data = {
        "model": "llama-3.3-70b-versatile",
        "messages": [
            {
                "role": "system",
                "content": """You are a pre-deployment cloud monitoring 
                AI agent for a MERN application running on AWS EC2 
                with Kubernetes. Analyze the pre-deployment metrics 
                and decide if deployment should proceed or stop."""
            },
            {
                "role": "user",
                "content": f"""
                Analyze these pre-deployment metrics and respond with:
                1. Status: CRITICAL or NORMAL
                2. Safe to Deploy: YES or NO
                3. Reason: Why you decided that
                4. Action: What should be done

                Metrics:
                {log}

                
                Rules:
                   - If CPU > 1% → CRITICAL
                   - If instance not running → CRITICAL
                   - If MERN app DOWN → CRITICAL
                   - If all OK → NORMAL

                Keep response short and clear.
                """
            }
        ]
    }

    response = requests.post(
        "https://api.groq.com/openai/v1/chat/completions",
        headers=headers,
        json=data
    )

    result = response.json()
    answer = result["choices"][0]["message"]["content"]
    print("\n🤖 Groq Analysis:")
    print(answer)
    return answer

# ================================
# SEND TELEGRAM TEXT
# ================================
def send_text_alert(message):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    data = {
        "chat_id": TELEGRAM_CHAT_ID,
        "text": message
    }
    requests.post(url, json=data)
    print("✅ Text alert sent!")

# ================================
# SEND TELEGRAM VOICE
# ================================
def send_voice_alert(message):
    print("🔊 Converting to voice...")
    tts = gTTS(text=message, lang='en')
    tts.save("alert.mp3")

    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendVoice"
    with open("alert.mp3", "rb") as audio:
        files = {"voice": audio}
        data = {"chat_id": TELEGRAM_CHAT_ID}
        requests.post(url, files=files, data=data)

    os.remove("alert.mp3")
    print("✅ Voice alert sent!")

# ================================
# ESCALATION TIMER
# ================================
def check_user_responded():
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/getUpdates"
    response = requests.get(url)
    data = response.json()
    if data["result"]:
        last_message = data["result"][-1]
        if "message" in last_message:
            text = last_message["message"].get("text", "")
            if text.upper() in ["OK", "ACKNOWLEDGED", "ACK"]:
                return True
    return False

def escalation_timer():
    print("⏳ Waiting 10 minutes for response...")
    time.sleep(600)
    if not check_user_responded():
        print("⚠️ No response! Escalating...")
        send_text_alert(
            "🔺 ESCALATION ALERT 🔺\n"
            "No response received!\n"
            "Deployment is BLOCKED!\n"
            "Immediate attention needed!"
        )

# ================================
# MAIN PRE-DEPLOYMENT CHECK
# ================================
def run_pre_deployment_check():
    print("\n" + "="*50)
    print("   PRE-DEPLOYMENT AGENT STARTING")
    print("="*50)
    print(f"Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"Repo: Dharshana-S30/ai-driven-cloud-monitoring")
    print(f"Region: ap-south-1")
    print("="*50)

    # Step 1 Get real metrics
    log, cpu, instance_status, app_status = get_aws_metrics()

    # Step 2 Analyze with Groq
    analysis = analyze_with_groq(log)

    # Step 3 Check result
    if "CRITICAL" in analysis.upper():
        print("\n🚨 CRITICAL ISSUE FOUND!")
        print("🚫 DEPLOYMENT BLOCKED!")

        # Send text alert first
        send_text_alert(
            f"🚨 PRE-DEPLOYMENT ALERT 🚨\n\n"
            f"Deployment BLOCKED!\n"
            f"EC2: {instance_status}\n"
            f"CPU: {cpu}%\n"
            f"MERN App: {app_status}\n\n"
            f"Check voice message for details!\n"
            f"Reply OK when resolved."
        )

        time.sleep(2)

        # Send voice alert
        voice_message = (
            f"Pre-deployment Alert! "
            f"Deployment has been blocked. "
            f"Your EC2 instance status is {instance_status}. "
            f"CPU usage is at {cpu} percent. "
            f"MERN application is {app_status}. "
            f"Please resolve these issues before deploying. "
            f"Reply OK on Telegram when resolved. "
            f"This is your Cloud Alert System."
        )
        send_voice_alert(voice_message)

        # Start escalation
        escalation_timer()

        # Exit with error to stop deployment
        print("\n🚫 Deployment stopped by pre-deployment agent!")
        exit(1)

    else:
        print("\n✅ ALL CHECKS PASSED!")
        print("🚀 SAFE TO DEPLOY!")

        send_text_alert(
            f"✅ PRE-DEPLOYMENT CHECK PASSED\n\n"
            f"EC2: {instance_status}\n"
            f"CPU: {cpu}%\n"
            f"MERN App: {app_status}\n\n"
            f"Deployment proceeding automatically!"
        )

        print("\n✅ Pre-deployment agent completed!")
        exit(0)

# ================================
# RUN
# ================================
if __name__ == "__main__":
    run_pre_deployment_check()
