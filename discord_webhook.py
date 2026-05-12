import requests
import os
from dotenv import load_dotenv

load_dotenv()

def send_discord_notification(module, message):
    if not module or 'W3WI' in module['module_number']:
        return

    message += f"\n\n**{module['module_name']}** ({module['module_number']}, {module['credits']} Credits)\n"

    for grade in module['detail_grades']:
        message += (
            f"{grade['exam_name']}: **{grade['exam_grade']}**\n"
        )
    
    payload = {
        "content": message
    }

    response = requests.post(f"{os.getenv("DISCORD_WEBHOOK_URL").strip()}", json=payload)
    if not response.status_code in [200, 204]:
        print(
            f"Fehler beim Senden: "
            f"{response.status_code}"
        )
        print(response.text)


