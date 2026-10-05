# DeskHive Hub - Shared Workspace & Meeting Room Booking System

DeskHive Hub is a command-line Python application designed to manage hot desks and meeting rooms for freelancers and small teams. This system handles space availability, user registrations, bookings, payments, and facility maintenance using text-based file storage.

## Group Members & Roles

* **Azfar**: Hub Administrator (System management and reporting)
* **Thiviya**: Booking Coordinator (User registration and booking processing)
* **Farhan**: User / Member (Space viewing and booking requests)
* **Lekshmannjeyv**: Accountant (Payment recording and financial reporting)
* **Kiruthigan**: Facilities Staff (Maintenance logging and updates)

## Features

The system supports distinct functionalities based on the logged-in role:

* **Hub Administrator:** Add, update, and remove desks and meeting rooms; view all system data; generate overall revenue and space utilisation reports.


* **Booking Coordinator:** Register new users, process daily and hourly bookings, manage cancellations, and view booking histories.


* **User / Member:** View available spaces and check personal booking and payment history.


* **Accountant:** Record and update booking payments, generate an income summary and outstanding payment list, and generate a monthly financial summary.


* **Facilities Staff:** Log new maintenance issues for spaces and update maintenance statuses to automatically toggle space availability.


* **Unique System Features:** Time-slot conflict detection to prevent double-booking, automatic ID generation, and file-based operation logging.



## Installation & Setup

1. Ensure you have Python 3 installed on your machine. No external libraries are required.


2. Clone or download this repository to your local machine.
3. Ensure all `.py` files are located in the exact same directory.
4. Open a terminal or command prompt, navigate to the folder, and run the program:
```bash
python main.py

```


5. On the first run, the system will automatically generate the required text files (`spaces.txt`, `users.txt`, `bookings.txt`, `payments.txt`, `maintenance.txt`, and `logs.txt`) and populate sample data.



## File Structure

* `main.py`: The central entry point containing the main login menu.
* `utils.py`: Shared helper functions for file handling, ID generation, and input validation.
* `admin.py`: Logic for the Hub Administrator role.
* `coordinator.py`: Logic for the Booking Coordinator role.
* `member.py`: Logic for the User/Member role.
* `accountant.py`: Logic for the Accountant role.
* `facilities.py`: Logic for the Facilities Staff role.
* `*.txt`: Automatically generated text files used for database storage.



## Academic Integrity Disclaimer

This project is submitted for an academic assignment. Copying, paraphrasing, or adapting this code without proper attribution is considered a violation of academic integrity policies.
