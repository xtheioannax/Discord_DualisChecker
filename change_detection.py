def find_changed_modules(new_grades, old_grades=None):
    changed_modules = []
    if old_grades is None:
        return new_grades
    old_lookup = {
        module["module_number"]: module
        for module in old_grades
    }

    for new_module in new_grades:
        module_number = new_module["module_number"]

        old_module = old_lookup.get(module_number)

        # Falls Modul vorher noch nicht existierte → direkt als geändert
        if not old_module:
            changed_modules.append(new_module)
            continue

        module_changed = False

        # Endnote prüfen
        old_final = old_module.get("final_grade", "")
        new_final = new_module.get("final_grade", "")

        if old_final != new_final:
            module_changed = True

        # Detailnoten prüfen
        old_details = {
            detail["exam_name"]: detail["exam_grade"]
            for detail in old_module.get("detail_grades", [])
        }

        for new_detail in new_module.get("detail_grades", []):
            exam_name = new_detail["exam_name"]
            exam_grade = new_detail["exam_grade"]

            old_grade = old_details.get(exam_name)

            if old_grade != exam_grade:
                module_changed = True
                break

        if module_changed:
            changed_modules.append(new_module)

    return changed_modules