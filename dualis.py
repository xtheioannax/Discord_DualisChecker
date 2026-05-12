from bs4 import BeautifulSoup
from dotenv import load_dotenv
import os
import requests

load_dotenv()

session = requests.Session()
BASE_URL = "https://dualis.dhbw.de"
DUALIS_URL = "https://dualis.dhbw.de/scripts/mgrqispi.dll"

def login():
    LOGIN_REQUEST_URL = DUALIS_URL
    payload = {
        "usrname": f"{os.getenv("DUALIS_USERNAME").strip()}",
        "pass": f"{os.getenv("DUALIS_PASSWORD").strip()}",
        "APPNAME": "CampusNet",
        "PRGNAME": "LOGINCHECK",
        "ARGUMENTS": "clino,usrname,pass,menuno,menu_type,browser,platform",
        "clino": "000000000000001",
        "menuno": "000324",
        "menu_type": "classic",
        "browser": "",
        "platform": ""
    }
    response = session.post(LOGIN_REQUEST_URL, data=payload)
    SESSION_ID = response.headers['REFRESH'].split("&ARGUMENTS=")[1].split(",")[0]

    return(SESSION_ID)

def get_grades(SESSION_ID):
    GRADES_REQUEST_URL = DUALIS_URL
    payload = {
        "APPNAME": "CampusNet",
        "PRGNAME": "COURSERESULTS",
        "ARGUMENTS": f"{SESSION_ID},-N000307,"
    }
    response = session.get(GRADES_REQUEST_URL, params=payload)
    return response.text

def get_all_grades_over_semesters(SESSION_ID, semester_ids):
    all_grades = []
    for semester_id in semester_ids:
        payload = {
            "APPNAME": "CampusNet",
            "PRGNAME": "COURSERESULTS",
            "ARGUMENTS": f"{SESSION_ID},-N000307,-N{semester_id}"
        }
        response = session.get(DUALIS_URL, params=payload)
        parsed_grades_of_semester = parse_grades(response.text)
        all_grades.extend(parsed_grades_of_semester)
    return all_grades

def parse_grades(html):
    soup = BeautifulSoup(html, "html.parser")
    rows = soup.select("table.nb.list tbody tr")

    grades = []

    for row in rows:
        cols = row.find_all("td")

        # skip empty rows
        if len(cols) < 6:
            continue

        module_number = cols[0].get_text(strip=True)
        module_name = cols[1].get_text(strip=True)
        final_grade = cols[2].get_text(strip=True)
        credits = cols[3].get_text(strip=True)
        status = cols[4].get_text(strip=True)

        details_link_tag = cols[5].find("a")
        details_link = None

        if details_link_tag:
            details_link = details_link_tag.get("href")

        detail_grades = []

        # only check if "unvollständig" or "noch nicht gesetzt"
        if (
            "unvollständig" in status.lower()
            or "noch nicht gesetzt" in final_grade.lower()
        ):
            detail_grades = parse_detail_grades(
                requests.get(BASE_URL + details_link, cookies=session.cookies).text
            )

        grades.append({
            "module_number": module_number,
            "module_name": module_name,
            "final_grade": final_grade,
            "credits": credits,
            "status": status,
            "detail_grades": detail_grades
        })

    return grades

def parse_detail_grades(detail_html):
    soup = BeautifulSoup(detail_html, "html.parser")

    detail_grades = []

    table = soup.find("table", class_="tb")

    if table is None:
        print("Keine Detail-Tabelle gefunden")
        return []

    rows = table.find_all("tr")

    for row in rows:
        cols = row.find_all("td")
        if len(cols) < 5:
            continue

        exam_name = cols[1].get_text(" ", strip=True)
        exam_grade = cols[3].get_text(" ", strip=True)

        if not exam_name or not exam_grade:
            continue

        if exam_name in ["Prüfung", "Modulabschlussleistungen", "Versuch 1"]:
            continue

        if exam_grade == "Bewertung":
            continue

        detail_grades.append({
            "exam_name": exam_name,
            "exam_grade": exam_grade
        })

    return detail_grades

def get_all_semester_ids(html):
    soup = BeautifulSoup(html, "html.parser")
    semester_select = soup.find("select", {"id": "semester"})

    if not semester_select:
        print("Keine Semester-Auswahl gefunden")
        return []
    
    semester_ids = []
    for option in semester_select.find_all("option"):
        semester_id = option.get("value")

        if semester_id:
            semester_ids.append(semester_id)

    return semester_ids

def logout(SESSION_ID):
    LOGOUT_URL = DUALIS_URL
    payload = {
        "APPNAME": "CampusNet",
        "PRGNAME": "LOGOUT",
        "ARGUMENTS": f"{SESSION_ID},-N000307,"
    }
    session.get(LOGOUT_URL, params=payload)
