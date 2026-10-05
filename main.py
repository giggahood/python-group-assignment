#the entry point
from utils import *
import admin
import coordinator
import member
import facilities

def main_menu():
    initialize_default_files()

    while True:
        print("\n" + LINE)
        print("WELCOME TO DESKHIVE HUB BOOKING & MANAGEMENT SYSTEM".center(80))
        print(LINE)
        print("  1. Hub Administrator\n  2. Booking Coordinator\n  3. User / Member\n  4. Facilities Staff\n  0. Exit")
        role_choice = input("Enter option (0-4): ").strip()

        if role_choice == "1":
            if input("Enter Admin Password: ").strip() == "admin123":
                write_log("Hub Administrator", "LOGIN", "Logged in.")
                admin.hub_administrator_menu()
            else:
                print("  [Access Denied]")
                
        elif role_choice == "2":
            coordinator.booking_coordinator_menu()
            
        elif role_choice == "3":
            users = read_records(USERS_FILE, USER_FIELDS)
            uid = get_non_empty_input("Enter User ID (e.g. U001): ").upper()
            pwd = input("Enter Password: ").strip()
            
            if any(u[U_ID] == uid and u[U_PASSWORD] == pwd for u in users):
                member.user_member_menu(uid)
            else:
                print("  [Access Denied] Invalid ID or Password.")
                
        elif role_choice == "4":
            facilities.facilities_staff_menu()
            
        elif role_choice == "0":
            break

if __name__ == "__main__":
    main_menu()