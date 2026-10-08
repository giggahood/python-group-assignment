#booking coordinator module
import datetime
from utils import *
from admin import admin_view_all_spaces, admin_view_all_data_menu

def bc_register_user():
    print("\n" + LINE)
    print("REGISTER NEW USER".center(80))
    print(LINE)
    users = read_records(USERS_FILE, USER_FIELDS)

    name = get_non_empty_input("Full Name          : ")
    phone = get_non_empty_input("Phone (e.g. 0123456789): ")
    email = get_non_empty_input("Email              : ").lower()
    
    print("User Type: 1. Freelancer   2. Team")
    utype = "Freelancer" if get_int_input("Select (1-2): ", 1, 2) == 1 else "Team"
    password = get_non_empty_input("Password (min 6 chars): ")

    user_id = generate_id(users, "U", 3)
    today = datetime.date.today().strftime("%Y-%m-%d")
    new_user = [user_id, name, phone, email, utype, password, today]

    if get_yes_no("\nConfirm registration?"):
        if append_record(USERS_FILE, new_user):
            write_log("Booking Coordinator", "REGISTER_USER", f"{user_id}")
            print(f"  [Success] User registered. ID: {user_id}")

def bc_make_booking():
    print("\n" + LINE)
    print("NEW DESK / ROOM BOOKING".center(80))
    print(LINE)
    users = read_records(USERS_FILE, USER_FIELDS)
    bookings = read_records(BOOKINGS_FILE, BOOKING_FIELDS)
    payments = read_records(PAYMENTS_FILE, PAYMENT_FIELDS)
    spaces = read_records(SPACES_FILE, SPACE_FIELDS)

    user_id = get_non_empty_input("Enter User ID (e.g. U001): ").upper()
    if not any(u[U_ID] == user_id for u in users):
        print("  [Error] User ID not found.")
        return

    admin_view_all_spaces()
    space_id = get_non_empty_input("Enter Space ID to book: ").upper()
    space = next((s for s in spaces if s[S_ID] == space_id), None)
    
    if not space or space[S_STATUS] != "Available":
        print("  [Error] Space unavailable.")
        return

    print("Booking Type: 1. Hourly   2. Daily")
    btype = "Hourly" if get_int_input("Choice (1-2): ", 1, 2) == 1 else "Daily"
    date_str = get_valid_date("Booking Date (YYYY-MM-DD) or '0' to cancel: ")
    
    # Stop the booking process if the user typed 0
    if date_str == "0":
        print("  Booking cancelled.")
        return
    
    if btype == "Daily":
        start_hr, end_hr = OPENING_HOUR, CLOSING_HOUR
        hours = end_hr - start_hr
    else:
        start_hr = get_int_input(f"Start Hour ({OPENING_HOUR}-{CLOSING_HOUR-1}): ", OPENING_HOUR, CLOSING_HOUR-1)
        hours = get_int_input("Duration in Hours (1-8): ", 1, min(8, CLOSING_HOUR - start_hr))
        end_hr = start_hr + hours

    for b in bookings:
        if b[B_SPACE] == space_id and b[B_DATE] == date_str and b[B_STATUS] == "Active":
            if start_hr < int(b[B_END][:2]) and end_hr > int(b[B_START][:2]):
                print("  [Conflict Error] Time slot overlaps with existing booking.")
                return

   # 1. Calculate base rate
    rate = float(space[S_DAILY]) if btype == "Daily" else float(space[S_HOURLY]) * hours
    
    # 2. Apply discount if it's an Hourly booking meeting the minimum hours threshold
    discount = 0.0
    if btype == "Hourly" and hours >= LONG_BOOKING_HOURS:
        discount = rate * LONG_BOOKING_DISCOUNT
        print(f"  [Info] Applied {int(LONG_BOOKING_DISCOUNT * 100)}% discount for booking {LONG_BOOKING_HOURS} or more hours!")

    # 3. Calculate final total with tax
    subtotal = rate - discount
    total = subtotal + (subtotal * SERVICE_TAX_RATE)

    b_id = generate_id(bookings, "B", 4)
    p_id = generate_id(payments, "P", 4)
    today = datetime.date.today().strftime("%Y-%m-%d")

    new_b = [b_id, user_id, space_id, date_str, f"{str(start_hr).zfill(2)}:00", f"{str(end_hr).zfill(2)}:00", btype, str(hours), "1", f"{total:.2f}", "Active", today]
    new_p = [p_id, b_id, user_id, f"{total:.2f}", "Unpaid", today]

    print(f"\nTotal Charge (incl. tax): RM {total:.2f}")
    if get_yes_no("Confirm booking?"):
        if append_record(BOOKINGS_FILE, new_b) and append_record(PAYMENTS_FILE, new_p):
            write_log("Booking Coordinator", "NEW_BOOKING", f"{b_id} for {user_id}")
            print(f"  [Success] Booking confirmed. ID: {b_id}")

def booking_coordinator_menu():
    while True:
        print("\n" + LINE)
        print("DESKHIVE HUB - BOOKING COORDINATOR MENU".center(80))
        print(LINE)
        print("  1. Register New User\n  2. Process Booking\n  3. View All Bookings\n  0. Back")
        choice = input("Enter choice (0-3): ").strip()
        if choice == "1": bc_register_user()
        elif choice == "2": bc_make_booking()
        elif choice == "3": admin_view_all_data_menu()
        elif choice == "0": break
        else: print("  [Error] Invalid choice. Please enter 0, 1, 2, or 3.")