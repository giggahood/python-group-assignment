#facilities staff module
import datetime
from utils import *
from admin import admin_view_all_data_menu

def facilities_log_maintenance():
    spaces = read_records(SPACES_FILE, SPACE_FIELDS)
    maint = read_records(MAINTENANCE_FILE, MAINTENANCE_FIELDS)

    space_id = get_non_empty_input("Enter Space ID for Maintenance: ").upper()
    target_space = next((s for s in spaces if s[S_ID] == space_id), None)

    if not target_space:
        print(f"  [Error] Space ID '{space_id}' not found.")
        return

    issue = get_non_empty_input("Enter issue description: ")
    rec_id = generate_id(maint, "MT", 4)
    today = datetime.date.today().strftime("%Y-%m-%d")

    append_record(MAINTENANCE_FILE, [rec_id, space_id, issue, today, "Pending"])
    target_space[S_STATUS] = "Maintenance"
    write_records(SPACES_FILE, spaces)
    write_log("Facilities Staff", "LOG_MAINTENANCE", rec_id)
    print(f"\n  [Success] Logged {rec_id}. Space {space_id} set to 'Maintenance'.")

def facilities_update_status():
    maint = read_records(MAINTENANCE_FILE, MAINTENANCE_FIELDS)
    rec_id = get_non_empty_input("Enter Record ID (e.g. MT0001): ").upper()
    rec = next((m for m in maint if m[M_ID] == rec_id), None)

    if not rec:
        print("  [Error] Record ID not found.")
        return

    print(f"Current Status: {rec[M_STATUS]}\n1. Pending   2. Done")
    rec[M_STATUS] = "Pending" if get_int_input("Select (1-2): ", 1, 2) == 1 else "Done"
    write_records(MAINTENANCE_FILE, maint)

    if rec[M_STATUS] == "Done":
        spaces = read_records(SPACES_FILE, SPACE_FIELDS)
        for sp in spaces:
            if sp[S_ID] == rec[M_SPACE]:
                sp[S_STATUS] = "Available"
                write_records(SPACES_FILE, spaces)
                break
        print(f"  [Success] Space restored to 'Available'.")

def facilities_staff_menu():
    while True:
        print("\n" + LINE)
        print("DESKHIVE HUB - FACILITIES STAFF MENU".center(80))
        print(LINE)
        print("  1. Log Maintenance\n  2. Update Status\n  3. View Maintenance Logs\n  0. Back")
        choice = input("Enter choice (0-3): ").strip()
        
        if choice == "1": facilities_log_maintenance()
        elif choice == "2": facilities_update_status()
        elif choice == "3": admin_view_all_data_menu()
        elif choice == "0": break