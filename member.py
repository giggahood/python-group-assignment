#user / member module
from utils import *
from coordinator import bc_make_booking

def user_view_available_spaces():
    spaces = read_records(SPACES_FILE, SPACE_FIELDS)
    print("\n===== Available Desks & Meeting Rooms =====")
    found = False
    for s in spaces:
        if s[S_STATUS] == "Available":
            print(f"ID: {s[S_ID]} | Name: {s[S_NAME]} | Type: {s[S_TYPE]} | RM{s[S_HOURLY]}/hr")
            found = True
    if not found:
        print("No spaces currently available.")

def user_view_history(user_id):
    bookings = read_records(BOOKINGS_FILE, BOOKING_FIELDS)
    payments = read_records(PAYMENTS_FILE, PAYMENT_FIELDS)

    print(f"\n===== Booking History for [{user_id}] =====")
    for b in [b for b in bookings if b[B_USER] == user_id]:
        print(f"ID: {b[B_ID]} | Space: {b[B_SPACE]} | Date: {b[B_DATE]} | Status: {b[B_STATUS]}")

    print(f"\n===== Payment History for [{user_id}] =====")
    for p in [p for p in payments if p[P_USER] == user_id]:
        print(f"ID: {p[P_ID]} | Booking: {p[P_BOOKING]} | RM{p[P_AMOUNT]} | Status: {p[P_STATUS]}")


def user_extend_booking(user_id):
    """Extend the end time of one of the user's own active, hourly bookings."""
    print("\n===== Extend an Existing Booking =====")
    bookings = read_records(BOOKINGS_FILE, BOOKING_FIELDS)
    spaces = read_records(SPACES_FILE, SPACE_FIELDS)
    payments = read_records(PAYMENTS_FILE, PAYMENT_FIELDS)

    # Show only this user's active bookings
    my_bookings = [b for b in bookings if b[B_USER] == user_id and b[B_STATUS] == "Active"]
    if not my_bookings:
        print("You have no active bookings to extend.")
        return

    print(f"\n===== Active Bookings for [{user_id}] =====")
    for b in my_bookings:
        print(f"ID: {b[B_ID]} | Space: {b[B_SPACE]} | Date: {b[B_DATE]} | Time: {b[B_START]}-{b[B_END]} | Type: {b[B_TYPE]}")

    booking_id = get_non_empty_input("\nEnter Booking ID to extend: ").upper()

    # Find the booking's position in the list (must belong to this user)
    target_idx = None
    for i, b in enumerate(bookings):
        if b[B_ID] == booking_id and b[B_USER] == user_id:
            target_idx = i
            break

    if target_idx is None:
        print("  [Error] Booking not found, or it doesn't belong to you.")
        return

    booking = bookings[target_idx]

    if booking[B_STATUS] != "Active":
        print("  [Error] Only active bookings can be extended.")
        return

    if booking[B_TYPE] == "Daily":
        print("  [Error] Daily bookings already cover the full day and cannot be extended.")
        return

    current_end_hr = int(booking[B_END][:2])
    max_extra = CLOSING_HOUR - current_end_hr
    if max_extra <= 0:
        print("  [Error] This booking already ends at closing time. Cannot extend.")
        return

    extra_hours = get_int_input(f"Extend by how many hours? (1-{max_extra}): ", 1, max_extra)
    new_end_hr = current_end_hr + extra_hours

    # Check the extended time doesn't overlap with another active booking
    for i, b in enumerate(bookings):
        if i == target_idx:
            continue
        if b[B_SPACE] == booking[B_SPACE] and b[B_DATE] == booking[B_DATE] and b[B_STATUS] == "Active":
            if int(booking[B_START][:2]) < int(b[B_END][:2]) and new_end_hr > int(b[B_START][:2]):
                print("  [Conflict Error] The extended time overlaps with another booking.")
                return

    # Look up the space to get its hourly rate for the extra charge
    space = next((s for s in spaces if s[S_ID] == booking[B_SPACE]), None)
    if space is None:
        print("  [Error] Space details not found.")
        return

    hourly_rate = float(space[S_HOURLY])
    extra_cost = (hourly_rate * extra_hours) * (1 + SERVICE_TAX_RATE)

    print(f"\nExtending by {extra_hours} hour(s). Additional charge: RM {extra_cost:.2f}")
    if not get_yes_no("Confirm extension?"):
        print("  Extension cancelled.")
        return

    # Update the booking record in memory, then save
    booking[B_END] = f"{str(new_end_hr).zfill(2)}:00"
    booking[B_HOURS] = str(int(booking[B_HOURS]) + extra_hours)
    booking[B_AMOUNT] = f"{float(booking[B_AMOUNT]) + extra_cost:.2f}"
    bookings[target_idx] = booking

    # Keep the linked payment amount in sync, if it hasn't been paid yet
    for p in payments:
        if p[P_BOOKING] == booking_id and p[P_STATUS] == "Unpaid":
            p[P_AMOUNT] = f"{float(p[P_AMOUNT]) + extra_cost:.2f}"
            break

    if write_records(BOOKINGS_FILE, bookings) and write_records(PAYMENTS_FILE, payments):
        write_log("User/Member", "EXTEND_BOOKING", f"{booking_id} extended by {extra_hours}h")
        print(f"  [Success] Booking {booking_id} extended. New end time: {booking[B_END]}")


def user_member_menu(user_id):
    while True:
        print(f"\n===== User / Member Menu [{user_id}] =====")
        print("1. View Available Spaces")
        print("2. Request New Booking")
        print("3. Extend an Existing Booking")  # <-- New Option
        print("4. View History")
        print("0. Logout")
        choice = input("Enter choice (0-4): ").strip()
        
        if choice == "1": 
            user_view_available_spaces()
        elif choice == "2": 
            bc_make_booking()
        elif choice == "3": 
            user_extend_booking(user_id)      # <-- Calls teammate's new function
        elif choice == "4": 
            user_view_history(user_id)
        elif choice == "0": 
            break
        else:
            print("  [Error] Invalid choice. Please enter a number between 0 and 4.")
