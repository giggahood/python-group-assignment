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

def user_member_menu(user_id):
    while True:
        print(f"\n===== User / Member Menu [{user_id}] =====")
        print("1. View Available Spaces\n2. Request Booking\n3. View History\n0. Logout")
        choice = input("Enter choice (0-3): ").strip()
        
        if choice == "1": user_view_available_spaces()
        elif choice == "2": bc_make_booking()
        elif choice == "3": user_view_history(user_id)
        elif choice == "0": break