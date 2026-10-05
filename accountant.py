#accountant module
import datetime
from utils import *

def acc_record_and_update_payments():
    print("\n" + LINE)
    print("RECORD AND UPDATE BOOKING PAYMENTS".center(80))
    print(LINE)
    payments = read_records(PAYMENTS_FILE, PAYMENT_FIELDS)

    print("\n--- UNPAID PAYMENTS ---")
    found_unpaid = False
    for p in payments:
        if p[P_STATUS] == "Unpaid":
            print(f"Payment ID: {p[P_ID]} | Booking ID: {p[P_BOOKING]} | User: {p[P_USER]} | RM {p[P_AMOUNT]}")
            found_unpaid = True
            
    if not found_unpaid:
        print("  No unpaid payments found.")

    p_id = get_non_empty_input("\nEnter Payment ID to update (or '0' to cancel): ").upper()
    if p_id == "0": return

    target = next((p for p in payments if p[P_ID] == p_id), None)
    if not target:
        print("  [Error] Payment ID not found.")
        return

    print(f"\nCurrent Status: {target[P_STATUS]}")
    print("1. Mark as Paid   2. Mark as Unpaid")
    choice = get_int_input("Select new status (1-2): ", 1, 2)
    target[P_STATUS] = "Paid" if choice == 1 else "Unpaid"

    if write_records(PAYMENTS_FILE, payments):
        write_log("Accountant", "UPDATE_PAYMENT", f"Set {p_id} to {target[P_STATUS]}")
        print(f"  [Success] Payment {p_id} updated to {target[P_STATUS]}.")

def acc_generate_income_and_outstanding():
    print("\n" + LINE)
    print("INCOME SUMMARY AND OUTSTANDING PAYMENT LIST".center(80))
    print(LINE)
    payments = read_records(PAYMENTS_FILE, PAYMENT_FIELDS)

    paid = [p for p in payments if p[P_STATUS] == "Paid"]
    unpaid = [p for p in payments if p[P_STATUS] == "Unpaid"]

    print("\n--- OUTSTANDING PAYMENTS LIST ---")
    if unpaid:
        for p in unpaid:
            print(f"{p[P_ID]:<8} | Booking: {p[P_BOOKING]:<8} | User: {p[P_USER]:<6} | RM {p[P_AMOUNT]}")
    else:
        print("  No outstanding payments.")
    print(f"Total Outstanding: RM {sum(float(p[P_AMOUNT]) for p in unpaid):.2f}")

    print("\n--- INCOME SUMMARY (PAID) ---")
    if paid:
        for p in paid:
            print(f"{p[P_ID]:<8} | Booking: {p[P_BOOKING]:<8} | User: {p[P_USER]:<6} | RM {p[P_AMOUNT]}")
    else:
        print("  No income recorded yet.")
    print(f"Total Income: RM {sum(float(p[P_AMOUNT]) for p in paid):.2f}\n")

def acc_generate_monthly_summary():
    print("\n" + LINE)
    print("MONTHLY FINANCIAL SUMMARY".center(80))
    print(LINE)
    payments = read_records(PAYMENTS_FILE, PAYMENT_FIELDS)
    
    monthly_data = {}
    for p in payments:
        month = p[P_DATE][:7] 
        amount = float(p[P_AMOUNT])
        
        if month not in monthly_data:
            monthly_data[month] = {"income": 0.0, "outstanding": 0.0}
            
        if p[P_STATUS] == "Paid":
            monthly_data[month]["income"] += amount
        elif p[P_STATUS] == "Unpaid":
            monthly_data[month]["outstanding"] += amount

    if not monthly_data:
        print("  No financial data available.")
        return

    print(f"{'Month':<10} | {'Total Income (RM)':<20} | {'Total Outstanding (RM)':<20}")
    print(DASH)
    for month in sorted(monthly_data.keys()):
        inc = monthly_data[month]["income"]
        out = monthly_data[month]["outstanding"]
        print(f"{month:<10} | {inc:<20.2f} | {out:<20.2f}")
    print(DASH)

def accountant_menu():
    while True:
        print("\n" + LINE)
        print("DESKHIVE HUB - ACCOUNTANT MENU".center(80))
        print(LINE)
        print("  1. Record and update booking payments")
        print("  2. Generate an income summary and outstanding payment list")
        print("  3. Generate a monthly financial summary")
        print("  0. Logout")
        choice = input("Enter choice (0-3): ").strip()

        if choice == "1":
            acc_record_and_update_payments()
        elif choice == "2":
            acc_generate_income_and_outstanding()
        elif choice == "3":
            acc_generate_monthly_summary()
        elif choice == "0":
            break