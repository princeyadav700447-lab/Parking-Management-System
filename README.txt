PARKING MANAGEMENT SYSTEM — PS NO. 26

Files:
- one.py: Main Python program.
- parking.txt: Persistent parking-slot data.

Requirements: Python 3. No external packages required.

Run:
    python3 one.py

Menu:
1. Entry: enter vehicle number and type (car/bike).
2. Exit: enter vehicle number and parking duration in hours.
3. Status: display all five slots.

Rates:
- Car: Rs. 20 per charged hour.
- Bike: Rs. 10 per charged hour.
- Minimum charge: 1 hour.
- Partial hours are rounded up.

The program loads and saves parking data in parking.txt.
To start a fresh test case, stop the program and replace parking.txt
contents with:
[
    null,
    null,
    null,
    null,
    null
]

Test cases:
1. Entry MH12AB1234, type car -> slot 1, 4 free slots.
2. With the car parked, exit after 0.5 hours -> 1 hour, Rs. 20.
3. Duplicate entry is rejected; truck type is rejected; unknown vehicle
   exit reports vehicle not found.
4. Entry KA01AB1111, type bike; exit after 2.5 hours -> 3 hours, Rs. 30;
   status -> 5 of 5 slots free.

Entry validation accepts common Indian registration formats.
