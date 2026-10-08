#shared data & helpers
import os
import datetime

# ==============================================================================
# FILE NAMES & CONSTANTS
# ==============================================================================
SPACES_FILE = "spaces.txt"
USERS_FILE = "users.txt"
BOOKINGS_FILE = "bookings.txt"
PAYMENTS_FILE = "payments.txt"
MAINTENANCE_FILE = "maintenance.txt"
LOG_FILE = "logs.txt"

DELIMITER = ","

# Data Column Schema Indexes:
S_ID, S_NAME, S_TYPE, S_FLOOR, S_CAPACITY, S_HOURLY, S_DAILY, S_STATUS = range(8)
SPACE_FIELDS = 8

U_ID, U_NAME, U_PHONE, U_EMAIL, U_TYPE, U_PASSWORD, U_REG_DATE = range(7)
USER_FIELDS = 7

(B_ID, B_USER, B_SPACE, B_DATE, B_START, B_END, B_TYPE,
 B_HOURS, B_ATTENDEES, B_AMOUNT, B_STATUS, B_CREATED) = range(12)
BOOKING_FIELDS = 12

P_ID, P_BOOKING, P_USER, P_AMOUNT, P_STATUS, P_DATE = range(6)
PAYMENT_FIELDS = 6

M_ID, M_SPACE, M_ISSUE, M_DATE, M_STATUS = range(5)
MAINTENANCE_FIELDS = 5

OPENING_HOUR = 8
CLOSING_HOUR = 22
MAX_ADVANCE_DAYS = 60
SERVICE_TAX_RATE = 0.08
LONG_BOOKING_HOURS = 4
LONG_BOOKING_DISCOUNT = 0.10

LINE = "=" * 80
DASH = "-" * 80

# ==============================================================================
# CORE FILE I/O & SYSTEM UTILITIES
# ==============================================================================
def read_records(filename, expected_fields):
    records = []
    if not os.path.exists(filename):
        try:
            open(filename, "w").close()
        except IOError:
            print(f"  [Error] Failed to create missing file: {filename}")
        return records

    try:
        with open(filename, "r") as file:
            for line in file:
                line = line.strip()
                if not line:
                    continue
                fields = line.split(DELIMITER)
                if len(fields) != expected_fields:
                    continue
                records.append(fields)
    except IOError:
        print(f"  [Error] Failed to read file: {filename}")
    return records

def write_records(filename, records):
    try:
        with open(filename, "w") as file:
            for record in records:
                file.write(DELIMITER.join(str(f) for f in record) + "\n")
        return True
    except IOError:
        print(f"  [Error] Failed to write to file: {filename}")
        return False

def append_record(filename, record):
    try:
        with open(filename, "a") as file:
            file.write(DELIMITER.join(str(f) for f in record) + "\n")
        return True
    except IOError:
        print(f"  [Error] Failed to append data to file: {filename}")
        return False

def write_log(role, action, details):
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_entry = f"{timestamp} | Role: {role:<20} | Action: {action:<22} | Details: {details}"
    try:
        with open(LOG_FILE, "a") as file:
            file.write(log_entry + "\n")
    except IOError:
        pass

def generate_id(records, prefix, digits=3):
    highest = 0
    for rec in records:
        rec_id = rec[0]
        if rec_id.startswith(prefix):
            num_part = rec_id[len(prefix):]
            if num_part.isdigit():
                highest = max(highest, int(num_part))
    return f"{prefix}{str(highest + 1).zfill(digits)}"

def initialize_default_files():
    if not os.path.exists(SPACES_FILE) or os.path.getsize(SPACES_FILE) == 0:
        sample_spaces = [
            ["DS001", "Quiet Hot Desk A1", "Desk", "1", "1", "5.00", "35.00", "Available"],
            ["DS002", "Window Hot Desk B2", "Desk", "1", "1", "6.00", "40.00", "Available"],
            ["RM001", "Executive Conference Room", "Room", "2", "10", "30.00", "200.00", "Available"]
        ]
        write_records(SPACES_FILE, sample_spaces)

    if not os.path.exists(USERS_FILE) or os.path.getsize(USERS_FILE) == 0:
        sample_users = [
            ["U001", "Alice Tan", "0123456789", "alice@gmail.com", "Freelancer", "user123", "2026-01-10"]
        ]
        write_records(USERS_FILE, sample_users)

# ==============================================================================
# INPUT VALIDATION UTILITIES
# ==============================================================================
def get_non_empty_input(prompt):
    while True:
        val = input(prompt).strip()
        if not val:
            print("  [Error] Input cannot be empty.")
        elif DELIMITER in val or "|" in val:
            print("  [Error] Input must not contain commas (,) or vertical bars (|).")
        else:
            return val

def get_float_input(prompt, min_val=0.0):
    while True:
        val = input(prompt).strip()
        try:
            num = float(val)
            if num < min_val:
                print(f"  [Error] Value must be at least {min_val:.2f}.")
            else:
                return round(num, 2)
        except ValueError:
            print("  [Error] Invalid input. Please enter a valid decimal number.")

def get_int_input(prompt, min_val, max_val):
    while True:
        val = input(prompt).strip()
        if val.isdigit():
            num = int(val)
            if min_val <= num <= max_val:
                return num
        print(f"  [Error] Enter a whole number between {min_val} and {max_val}.")

def get_yes_no(prompt):
    while True:
        ans = input(prompt + " (Y/N): ").strip().upper()
        if ans in ("Y", "N"):
            return ans == "Y"
        print("  [Error] Please enter 'Y' for Yes or 'N' for No.")


def get_valid_date(prompt):
    import datetime
    today = datetime.date.today()
    while True:
        value = input(prompt).strip()
        
        # Check if the user wants to cancel
        if value == "0":
            return "0"
            
        try:
            chosen_date = datetime.datetime.strptime(value, "%Y-%m-%d").date()
            max_date = today + datetime.timedelta(days=MAX_ADVANCE_DAYS)
            
            if chosen_date < today:
                print("  [Error] The date cannot be in the past.")
            elif chosen_date > max_date:
                print(f"  [Error] You can only book up to {MAX_ADVANCE_DAYS} days in advance.")
            else:
                return chosen_date.strftime("%Y-%m-%d")
                
        except ValueError:
            print("  [Error] Invalid date format. Please use YYYY-MM-DD...")