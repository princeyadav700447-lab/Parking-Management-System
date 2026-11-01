"""
PS No. 26 - Parking Management System
Run: python3 one.py
No external Python packages are required.
"""

import json
import math
import re
from pathlib import Path

TOTAL_SLOTS = 5
RATES = {"car": 20, "bike": 10}
DATA_FILE = Path(__file__).with_name("parking.txt")

# A free slot is None; an occupied slot is a dictionary.
parking_slots = [None] * TOTAL_SLOTS


def load_data():
    """Load saved parking slots from parking.txt."""
    global parking_slots
    if not DATA_FILE.exists():
        parking_slots = [None] * TOTAL_SLOTS
        return

    try:
        with DATA_FILE.open("r", encoding="utf-8") as file:
            saved = json.load(file)
        if not isinstance(saved, list) or len(saved) != TOTAL_SLOTS:
            raise ValueError("Invalid parking data format.")

        loaded = [None] * TOTAL_SLOTS
        for i, vehicle in enumerate(saved):
            if vehicle is None:
                continue
            if not isinstance(vehicle, dict):
                raise ValueError("Invalid vehicle record.")
            number = str(vehicle.get("vehicle_number", "")).strip().upper()
            kind = str(vehicle.get("type", "")).strip().lower()
            if not number or kind not in RATES:
                raise ValueError("Invalid vehicle record.")
            loaded[i] = {"vehicle_number": number, "type": kind}
        parking_slots = loaded
    except (OSError, json.JSONDecodeError, ValueError, TypeError) as error:
        print(f"Warning: Could not load saved data ({error}). Starting empty.")
        parking_slots = [None] * TOTAL_SLOTS


def save_data():
    """Save all slots after every successful parking change."""
    try:
        with DATA_FILE.open("w", encoding="utf-8") as file:
            json.dump(parking_slots, file, indent=4)
    except OSError as error:
        print(f"Error saving parking data: {error}")


def normalize_vehicle_number(value):
    """Validate a common Indian vehicle registration format."""
    number = value.strip().upper().replace(" ", "").replace("-", "")
    pattern = r"^[A-Z]{2}[0-9]{1,2}[A-Z]{1,3}[0-9]{1,4}$"
    return number if re.fullmatch(pattern, number) else ""


def find_vehicle(number):
    for index, vehicle in enumerate(parking_slots):
        if vehicle is not None and vehicle["vehicle_number"] == number:
            return index
    return None


def vehicle_entry():
    number = normalize_vehicle_number(input("Enter vehicle number: "))
    if not number:
        print("Invalid vehicle number. Please enter a valid registration number.")
        return

    if find_vehicle(number) is not None:
        print(f"Vehicle {number} is already parked.")
        return

    kind = input("Enter vehicle type (car/bike): ").strip().lower()
    if kind not in RATES:
        print("Invalid type. Enter car or bike.")
        return

    free_index = None
    for index, vehicle in enumerate(parking_slots):
        if vehicle is None:
            free_index = index
            break

    if free_index is None:
        print("Parking lot is full. No slots available.")
        return

    parking_slots[free_index] = {"vehicle_number": number, "type": kind}
    save_data()
    print(f"Vehicle {number} parked in slot {free_index + 1}.")
    print(f"Slots free: {parking_slots.count(None)}")


def vehicle_exit():
    number = input("Enter vehicle number: ").strip().upper()
    number = number.replace(" ", "").replace("-", "")
    index = find_vehicle(number)

    if index is None:
        print(f"Vehicle {number} not found.")
        return

    try:
        hours = float(input("Enter parking hours: ").strip())
    except ValueError:
        print("Invalid parking time. Please enter a positive number.")
        return

    if not math.isfinite(hours) or hours <= 0:
        print("Invalid parking time. Please enter a positive number.")
        return

    vehicle = parking_slots[index]
    charged_hours = max(1, math.ceil(hours))
    fee = charged_hours * RATES[vehicle["type"]]

    parking_slots[index] = None
    save_data()
    print(f"Hours charged: {charged_hours} (rounded up)")
    print(f"Fee: {fee}")
    print(f"Slot {index + 1} is now free.")


def parking_status():
    print("\nPARKING STATUS")
    print("-" * 32)
    for index, vehicle in enumerate(parking_slots):
        if vehicle is None:
            print(f"Slot {index + 1}: Free")
        else:
            print(f"Slot {index + 1}: {vehicle['vehicle_number']} ({vehicle['type']})")

    free = parking_slots.count(None)
    print(f"Slots free: {free} of {TOTAL_SLOTS}")
    print(f"Slots occupied: {TOTAL_SLOTS - free} of {TOTAL_SLOTS}")


def main():
    load_data()
    print("=" * 38)
    print("       PARKING MANAGEMENT SYSTEM")
    print("=" * 38)

    while True:
        print("\nMENU")
        print("1. Entry")
        print("2. Exit")
        print("3. Status")
        choice = input("Enter your choice (1-3): ").strip()

        if choice == "1":
            vehicle_entry()
        elif choice == "2":
            vehicle_exit()
        elif choice == "3":
            parking_status()
        else:
            print("Invalid menu option. Please choose 1, 2, or 3.")


if __name__ == "__main__":
    main()
