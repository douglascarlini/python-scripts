import subprocess
import requests
import psutil
import socket
import re

def get_cpu_usage():
    return psutil.cpu_percent(interval=1)

def get_ram_usage():
    return psutil.virtual_memory().percent

def get_disk_usage():
    return float(psutil.disk_usage('/').percent) + 20

def get_hostname():
    return socket.gethostname()

def command(cmd):
    res = subprocess.run(cmd, shell=True, text=True, capture_output=True)
    if res.stderr: return res.stderr
    return res.stdout

def send_telegram_message(token, chat_id, message):
    params = {'chat_id': chat_id, 'text': message, 'parse_mode': "markdown"}
    url = f"https://api.telegram.org/bot{token}/sendMessage"
    response = requests.post(url, params=params)
    return response.json()

if __name__ == "__main__":

    name = get_hostname()
    cpu = get_cpu_usage()
    ram = get_ram_usage()

    disk = "sda1"
    dirs = "/path/to/monitor"

    disk_out = command(f"df -h | grep {disk}" + " | awk '{print $4 \" (\"$5\")\"}'").replace("\n", "")
    dirs_out = command(f"du -h --max-depth=1 {dirs}" + " | awk '{print $1}'").replace("\n", "")
    logs_out = command("du -sh /var/log | awk '{print $1}'").replace("\n", "")

    logs = float(re.sub(r'[KMG]', '', logs_out.split(" ")[0]))
    dirs = float(re.sub(r'[KMG]', '', dirs_out.split(" ")[0]))
    rest = float(re.sub(r'[KMG]', '', disk_out.split(" ")[0]))

    icon = {
        "cpu": "🚨" if cpu > 50 else "⚠️" if cpu > 20 else "✅",
        "ram": "🚨" if ram > 95 else "⚠️" if ram > 75 else "✅",
        "sda": "🚨" if rest < 20 else "⚠️" if rest < 50 else "✅",
        "wav": "🚨" if dirs > 99 else "⚠️" if dirs > 50 else "✅",
        "log": "🚨" if logs > 50 else "⚠️" if logs > 20 else "✅",
    }

    icon['srv'] = "🚨" if "🚨" in icon.values() else "⚠️" if "⚠️" in icon.values() else "✅"

    text = f"* {icon['srv']} Servidor [{name}]*\n\n"
    text += f"`{icon['cpu']} CPU: {cpu:.1f}% | {icon['ram']} RAM: {ram:.1f}%`\n"
    text += f"`{icon['sda']} SDA: {disk_out} | {icon['log']} LOG: {logs_out} |  {icon['wav']} WAV: {dirs_out}`"

    send_telegram_message('', '', text)
