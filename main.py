from time import sleep
import discord_webhook
import dualis
from change_detection import find_changed_modules

old_grades = []
while True:
    session_id = dualis.login()
    semester_ids = dualis.get_all_semester_ids(dualis.get_grades(session_id))
    new_grades = dualis.get_all_grades_over_semesters(session_id, semester_ids)
    dualis.logout(session_id)
    
    changed_modules = find_changed_modules(new_grades, old_grades)
    message = "📢 Es gibt Notenänderungen!"
    if changed_modules != []:
        for module in changed_modules:
            discord_webhook.send_discord_notification(module, message)
            message = ""

    old_grades = new_grades
    sleep(360) # 6 Minuten
