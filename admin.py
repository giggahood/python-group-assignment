#hub administrator module
import os
from utils import *

def admin_manage_spaces_menu():
    while True:
        print("\n" + LINE)
        print("HUB ADMINISTRATOR - DESK & ROOM MANAGEMENT".center(80))
        print(LINE)
        print("  1. Add New Desk / Meeting Room")
        print("  2. Update Desk / Meeting Room Details")
        print("  3. Remove / Deactivate Desk / Meeting Room")
        print("  4. View All Spaces")
        print("  0. Back to Main Admin Menu")
        print(LINE)
        choice = input("Select option (0-4): ").strip()

        if choice == "1":
            admin_add_space()
        elif choice == "2":
            admin_update_space()
        elif choice == "3":
            admin_remove_space()
        elif choice == "4":
            admin_view_all_spaces()
        elif choice == "0":
            break
        else:
            print("  [Error] Invalid choice.")

def admin_add_space():
    print("\n" + DASH)
    print("ADD NEW SPACE".center(80))
    print(DASH)
    spaces = read_records(SPACES_FILE, SPACE_FIELDS)

    space_name = get_non_empty_input("Enter Space Name / Label (e.g. Quiet Desk C1): ")
    print("Select Space Type:\n  1. Desk\n  2. Room")
    type_choice = get_int_input("Choice (1-2): ", 1, 2)
    space_type = "Desk" if type_choice == 1 else "Room"

    floor = str(get_int_input("Enter Floor Level (1-10): ", 1, 10))
    capacity = "1" if space_type == "Desk" else str(get_int_input("Enter Seating Capacity (2-50): ", 2, 50))

    hourly_rate = f"{get_float_input('Enter Hourly Rate (RM): ', 1.0):.2f}"
    daily_rate = f"{get_float_input('Enter Daily Rate (RM): ', 5.0):.2f}"

    prefix = "DS" if space_type == "Desk" else "RM"
    space_id = generate_id(spaces, prefix, 3)

    new_space = [space_id, space_name, space_type, floor, capacity, hourly_rate, daily_rate, "Available"]

    print(f"\n  Summary: {space_id} | {space_name} | {space_type} | Floor: {floor}")
    if get_yes_no("Confirm adding this space?"):
        if append_record(SPACES_FILE, new_space):
            write_log("Hub Administrator", "ADD_SPACE", f"Created space {space_id}")
            print("  [Success] Space added successfully.")

def admin_update_space():
    spaces = read_records(SPACES_FILE, SPACE_FIELDS)
    admin_view_all_spaces()
    space_id = get_non_empty_input("\nEnter Space ID to update (or '0' to cancel): ").upper()
    if space_id == "0": return

    target_idx = next((i for i, s in enumerate(spaces) if s[S_ID] == space_id), None)
    if target_idx is None:
        print("  [Error] Space ID not found.")
        return

    sp = spaces[target_idx]
    print(f"\nUpdating [{sp[S_ID]}] {sp[S_NAME]}")
    print("  1. Name  2. Hourly Rate  3. Daily Rate  4. Capacity  5. Status  0. Cancel")
    opt = get_int_input("Select field to update (0-5): ", 0, 5)
    
    if opt == 1: sp[S_NAME] = get_non_empty_input("New Space Name: ")
    elif opt == 2: sp[S_HOURLY] = f"{get_float_input('New Hourly Rate (RM): ', 1.0):.2f}"
    elif opt == 3: sp[S_DAILY] = f"{get_float_input('New Daily Rate (RM): ', 5.0):.2f}"
    elif opt == 4: sp[S_CAPACITY] = str(get_int_input("New Capacity: ", 1, 100))
    elif opt == 5:
        print("1. Available  2. Maintenance  3. Disabled")
        s_choice = get_int_input("Choice (1-3): ", 1, 3)
        sp[S_STATUS] = {1: "Available", 2: "Maintenance", 3: "Disabled"}[s_choice]
    elif opt == 0: return

    if write_records(SPACES_FILE, spaces):
        write_log("Hub Administrator", "UPDATE_SPACE", f"Updated space {space_id}")
        print("  [Success] Space updated.")

def admin_remove_space():
    spaces = read_records(SPACES_FILE, SPACE_FIELDS)
    bookings = read_records(BOOKINGS_FILE, BOOKING_FIELDS)
    admin_view_all_spaces()
    
    space_id = get_non_empty_input("\nEnter Space ID to remove (or '0' to cancel): ").upper()
    if space_id == "0": return

    target = next((s for s in spaces if s[S_ID] == space_id), None)
    if not target:
        print("  [Error] Space ID not found.")
        return

    active_b = [b for b in bookings if b[B_SPACE] == space_id and b[B_STATUS] == "Active"]
    if active_b:
        print(f"  [Warning] Space has {len(active_b)} active booking(s). Marking as 'Disabled'.")
        target[S_STATUS] = "Disabled"
        write_records(SPACES_FILE, spaces)
        return

    if get_yes_no(f"Permanently delete space {space_id}?"):
        new_spaces = [s for s in spaces if s[S_ID] != space_id]
        if write_records(SPACES_FILE, new_spaces):
            print("  [Success] Space deleted.")

def admin_view_all_spaces():
    spaces = read_records(SPACES_FILE, SPACE_FIELDS)
    print("\n" + DASH)
    print(f"{'ID':<7}{'Name':<25}{'Type':<7}{'Floor':<7}{'Cap':<5}{'RM/Hr':>9}{'RM/Day':>9}  {'Status':<12}")
    print(DASH)
    for s in spaces:
        print(f"{s[S_ID]:<7}{s[S_NAME]:<25}{s[S_TYPE]:<7}{s[S_FLOOR]:<7}{s[S_CAPACITY]:<5}{float(s[S_HOURLY]):>9.2f}{float(s[S_DAILY]):>9.2f}  {s[S_STATUS]:<12}")
    print(DASH)

def admin_view_all_data_menu():
    while True:
        print("\n" + LINE)
        print("HUB ADMINISTRATOR - VIEW ALL SYSTEM DATA".center(80))
        print(LINE)
        print("  1. View Users\n  2. View Bookings\n  3. View Payments\n  4. View Maintenance\n  0. Back")
        choice = input("Select option (0-4): ").strip()

        if choice == "1":
            users = read_records(USERS_FILE, USER_FIELDS)
            print("\n" + DASH)
            for u in users: print(f"{u[U_ID]:<8}{u[U_NAME]:<22}{u[U_PHONE]:<13}{u[U_EMAIL]:<25}{u[U_TYPE]:<12}")
        elif choice == "2":
            bookings = read_records(BOOKINGS_FILE, BOOKING_FIELDS)
            print("\n" + DASH)
            for b in bookings: print(f"{b[B_ID]:<7}{b[B_USER]:<7}{b[B_SPACE]:<7}{b[B_DATE]:<12}{b[B_TYPE]:<8}{b[B_STATUS]:<10}")
        elif choice == "3":
            payments = read_records(PAYMENTS_FILE, PAYMENT_FIELDS)
            print("\n" + DASH)
            for p in payments: print(f"{p[P_ID]:<8}{p[P_BOOKING]:<12}{p[P_USER]:<10}RM{float(p[P_AMOUNT]):>8.2f}  {p[P_STATUS]:<15}")
        elif choice == "4":
            maint = read_records(MAINTENANCE_FILE, MAINTENANCE_FIELDS)
            print("\n" + DASH)
            for m in maint: print(f"{m[M_ID]:<11}{m[M_SPACE]:<10}{m[M_ISSUE]:<30}{m[M_STATUS]:<10}")
        elif choice == "0": break

def admin_generate_overall_report():
    print("\n" + LINE)
    print("OVERALL HUB MANAGEMENT REPORT".center(80))
    print(LINE)
    bookings = read_records(BOOKINGS_FILE, BOOKING_FIELDS)
    payments = read_records(PAYMENTS_FILE, PAYMENT_FIELDS)
    
    total_rev = sum(float(p[P_AMOUNT]) for p in payments if p[P_STATUS] == "Paid")
    unpaid_rev = sum(float(p[P_AMOUNT]) for p in payments if p[P_STATUS] == "Unpaid")

    print(f"  Total Bookings: {len(bookings)}")
    print(f"  Total Confirmed Revenue : RM {total_rev:.2f}")
    print(f"  Total Unpaid Amount     : RM {unpaid_rev:.2f}\n")

def admin_view_audit_logs():
    print("\n" + LINE)
    print("SYSTEM OPERATION LOGS".center(80))
    print(LINE)
    if os.path.exists(LOG_FILE):
        with open(LOG_FILE, "r") as f:
            logs = f.readlines()
            for log in logs[-15:]: print("  " + log.strip())
    else:
        print("  No logs found.")

def admin_view_space_utilisation():
    print("\n" + LINE)
    print("SPACE UTILISATION & DEMAND TRACKING".center(80))
    print(LINE)
    
    spaces = read_records(SPACES_FILE, SPACE_FIELDS)
    bookings = read_records(BOOKINGS_FILE, BOOKING_FIELDS)
    
    if not spaces:
        print("  No spaces found in the system.")
        return
        
    usage_data = {s[S_ID]: {"name": s[S_NAME], "type": s[S_TYPE], "hours": 0} for s in spaces}
    
    for b in bookings:
        if b[B_STATUS] != "Cancelled": 
            s_id = b[B_SPACE]
            if s_id in usage_data:
                if b[B_TYPE] == "Daily":
                    # Daily bookings cover opening to closing (14 hours)
                    usage_data[s_id]["hours"] += (CLOSING_HOUR - OPENING_HOUR) 
                else:
                    # Hourly bookings add their specific duration
                    usage_data[s_id]["hours"] += int(b[B_HOURS])
    
    sorted_usage = sorted(usage_data.items(), key=lambda x: x[1]["hours"], reverse=True)
    
    print(f"{'Space ID':<10} | {'Name':<25} | {'Type':<10} | {'Total Hours Booked':<15}")
    print(DASH)
    for s_id, data in sorted_usage:
        print(f"{s_id:<10} | {data['name']:<25} | {data['type']:<10} | {data['hours']} hr(s)")
    print(DASH)
    
    if len(sorted_usage) >= 2:
        top_space = sorted_usage[0]
        bottom_space = sorted_usage[-1]
        
        print("\n📈 HIGH DEMAND SPACE:")
        if top_space[1]["hours"] > 0:
            print(f"   {top_space[1]['name']} ({top_space[0]}) is your most popular asset with {top_space[1]['hours']} total hours booked.")
        else:
            print("   Not enough booking data to determine high demand.")
            
        print("\n📉 LOW DEMAND SPACE:")
        print(f"   {bottom_space[1]['name']} ({bottom_space[0]}) is underutilized with only {bottom_space[1]['hours']} total hours booked.")
    print(LINE + "\n")

def hub_administrator_menu():
    while True:
        print("\n" + LINE)
        print("DESKHIVE HUB - HUB ADMINISTRATOR MENU".center(80))
        print(LINE)
        # Added Option 4 and shifted logs to Option 5
        print("  1. Manage Desks & Rooms\n  2. View All System Data\n  3. Generate Report\n  4. Space Utilisation & Demand\n  5. View Logs\n  0. Logout")
        choice = input("Enter choice (0-5): ").strip()

        if choice == "1": admin_manage_spaces_menu()
        elif choice == "2": admin_view_all_data_menu()
        elif choice == "3": admin_generate_overall_report()
        elif choice == "4": admin_view_space_utilisation() # Calls new function
        elif choice == "5": admin_view_audit_logs()
        elif choice == "0": break
        else: print("  [Error] Invalid choice. Please enter a number between 0 and 5.")