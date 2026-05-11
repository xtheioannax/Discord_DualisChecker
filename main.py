from time import sleep
import discord_webhook
import dualis
from change_detection import find_changed_modules

old_grades = []
while True:
    session_id = dualis.login()
    new_grades = dualis.get_grades(session_id)
    parsed_grades = dualis.parse_grades(new_grades)
    dualis.logout(session_id)
    
    changed_modules = find_changed_modules(parsed_grades, old_grades)

    if changed_modules != []:
        discord_webhook.send_discord_notification(changed_modules)

    old_grades = parsed_grades
    sleep(3600) # 1 Stunde warten