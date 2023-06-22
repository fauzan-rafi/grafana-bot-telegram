import requests
import telegram
import shutil

# Configuration Variable
# [GRAFANA]
HOST = "YOUR-HOST"
PORT = "3000"
API_KEY = "YOUR_API_GRAFANA"

# [PANEL_IMAGE]
DASHBOARD_UID = "YOUR_DASHBOARD_ID"
FROM_DATE = "now-5m"
TO_DATE = "now"
ORG_ID = "1"
WIDTH = "900"
HEIGHT = "400"
TZ = "Asia/Jakarta"

# [TELEGRAM]
BOT_TOKEN = "YOUR_BOT_TOKEN"
CHAT_ID = "YOUR_GROUP_CHAT_ID"

# [TEMP_STORAGE]
FILE_PATH = r"rendered/image.png"

# End of Configuration Variable


def handle_command(command):
    if command.startswith("/get"):
        panel_id = command.split(" ")[1]
        panel_id = check_value_message(panel_name=panel_id)
        download = get_grafana_snapshot(panel_id)
        if download:
            send_telegram_photo(FILE_PATH)
        else:
            message = "Failed to fetch snapshot from Grafana API"
            send_telegram_message(message)


def send_telegram_photo(image_path):
    bot = telegram.Bot(token=BOT_TOKEN)
    bot.send_photo(chat_id=CHAT_ID, photo=open(image_path, 'rb'))


def send_telegram_message(message):
    bot = telegram.Bot(token=BOT_TOKEN)
    bot.send_message(chat_id=CHAT_ID, text=message)


def check_value_message(panel_name):
    listPanel = {"usage_cpu": 20, "cpu_core": 14, "usage_ram": 16, "total_ram": 75, "total_fs": 2, "usage_disk": 154,
                 "network_traffic": 60, "status_server": 281, "server_uptime": 15}  # YOU MUST CUSTOMISE WITH YOUR ENVIRONMENT

    for x in listPanel:
        if x == panel_name:
            panel_id = listPanel[x]
    return panel_id


def get_grafana_snapshot(panel_id):
    try:
        response = requests.get(
            url=f"http://{HOST}:{PORT}/render/d-solo/"
                f"{DASHBOARD_UID}?from={FROM_DATE}&to={TO_DATE}"
                f"&orgId={ORG_ID}&panelId={panel_id}"
                f"&width={WIDTH}&height={HEIGHT}"
                f"&tz={TZ}",
            headers={"Authorization": f"Bearer {API_KEY}"},
            stream=True
        )

        if response.status_code == 200:
            with open(FILE_PATH, 'wb') as image_file:
                response.raw.decode_content = True
                shutil.copyfileobj(response.raw, image_file)
            return True
        else:
            print(
                f"Error fetching snapshot from Grafana API: {response.status_code}")
            return None

    except requests.exceptions.RequestException as e:
        print(f"Error fetching snapshot from Grafana API: {e}")
        return None


# Main Function
if __name__ == '__main__':
    last_update_id = None
    while True:
        try:
            response = requests.get(f"https://api.telegram.org/bot{BOT_TOKEN}/getUpdates",
                                    params={"offset": last_update_id})
            response_json = response.json()
            for update in response_json["result"]:
                last_update_id = update["update_id"] + 1
                if "message" in update and "text" in update["message"]:
                    handle_command(update["message"]["text"])
        except Exception as e:
            print(f"An error occurred: {e}")
