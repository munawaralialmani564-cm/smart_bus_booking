# Smart Bus Ticket Booking & Reservation System

A beginner-friendly **Python 3 console application** for a small bus service. A passenger or operator uses a text menu to browse and search routes, book seats, view booking history, cancel bookings, check seat availability, see route schedules and generate a booking report.

## Requirements

- Python 3 (tested with Python 3.12; the code uses nothing newer than f-strings, so any modern Python 3 should work)
- **No external packages.** Only built-in Python features are used.

## How to run

1. Save `main.py` in a folder, for example `smart_bus`.
2. Open a terminal in that folder (in VS Code: *Terminal > New Terminal*).
3. Run:

```
python main.py
```

On some systems the command is `python3 main.py`.

## Files in this project

| File | Purpose |
|------|---------|
| `main.py` | The complete application (routes, menu, validation, booking, cancellation, availability, schedule, report) |
| `README.md` | This guide |
| `test_cases.txt` | The 12 required tests (TC-01 to TC-12) plus 18 boundary tests, with expected and actual results |
| `sample_sessions.txt` | Real terminal transcripts of each feature |
| `demo_guide.md` | Step-by-step explanation of the program in simple Roman Urdu |
| `requirements_checklist.md` | PRD requirement -> function mapping, BR-01..BR-15, TC-01..TC-12 |
| `run_tests.py` | Optional helper that re-runs all tests and rewrites `test_cases.txt` and `sample_sessions.txt` |

## Menu guide

```
1. View Available Routes
2. Search for a Route
3. Book a Ticket
4. View My Bookings
5. Cancel a Booking
6. View Seat Availability
7. Generate Booking Report
8. Exit
9. View Route Schedule by Departure City
```

Options 1 to 8 are exactly the menu required by the PRD (8 is Exit). Option 9 was added so the required route-schedule feature is reachable without changing any of the original numbers.

| Option | What it does |
|--------|--------------|
| 1 | Lists all routes with number, route ID, journey, departure time, fare, seats left and status. You can choose to hide fully booked routes. |
| 2 | Searches by route ID, departure city or destination city (not case-sensitive). A city search shows **all** matches. |
| 3 | Asks for passenger name, age, route ID and number of seats; validates everything; creates a booking with an ID like `B1001`. |
| 4 | Shows every booking made in this run, including cancelled ones. |
| 5 | Cancels a **Confirmed** booking by ID and gives its seats back to the route. |
| 6 | Shows available seats and capacity per route with status *Available*, *Partially Booked* or *Fully Booked*, with an optional filter. |
| 7 | Report: total / confirmed / cancelled bookings, seats currently reserved, confirmed revenue, fully booked routes, plus a per-route breakdown. |
| 8 | Exits the program. |
| 9 | Shows departures city by city (Mirpur Khas and Lahore show "No scheduled departures."). |

## Starter routes

| Route | Journey | Departs | Fare | Seats |
|-------|---------|---------|------|-------|
| R101 | Karachi -> Hyderabad | 08:00 AM | Rs. 1,200 | 40 |
| R102 | Karachi -> Sukkur | 09:30 AM | Rs. 2,000 | 36 |
| R103 | Hyderabad -> Mirpur Khas | 11:00 AM | Rs. 800 | 32 |
| R104 | Karachi -> Lahore | 07:00 PM | Rs. 5,000 | 45 |
| R105 | Sukkur -> Hyderabad | 02:00 PM | Rs. 1,500 | 30 |

## Sample workflow

1. Run `python main.py`.
2. Choose **1** (answer `n`) to see all five routes.
3. Choose **3** and enter: `Ahmed`, `25`, `R101`, `2`. You get booking `B1001`, total **Rs. 2,400**.
4. Choose **6** (answer `n`): R101 now shows 38 of 40 seats, *Partially Booked*.
5. Choose **5** and enter `B1001`: the booking becomes *Cancelled* and 2 seats are restored.
6. Choose **5** and enter `B1001` again: the program refuses (already cancelled) and restores nothing.
7. Choose **7** to see the report: 1 total booking, 0 confirmed, 1 cancelled, Rs. 0 revenue.
8. Choose **8** to exit.

## Business rules the program enforces

Passenger name cannot be blank. Age must be a positive whole number. The route must exist. Seats must be a positive whole number and cannot exceed the seats available. Booking IDs are unique within a run (checked against a set). Total fare = price x seats. Seats are subtracted only after every check passes, and only once. Only *Confirmed* bookings can be cancelled, and seats are restored only once. Cancelled records stay in the history, and their fares are excluded from revenue. Seats always stay between 0 and the route capacity.

If any booking check fails, the program prints the reason, creates **no** booking and changes **no** seat count.

## Important limitations

- **Data is stored in memory only.** All bookings are lost when you exit. Routes reset to their starting seat counts on every run. This is by design.
- There is no login, file saving, database, payment, or graphical interface.
- Booking IDs (`B1001`, `B1002`, ...) are unique only within one run of the program.

## Testing

`test_cases.txt` contains the 12 required tests (TC-01 to TC-12) and 18 extra boundary tests: zero seats, exactly all remaining seats, one more than available, empty booking list, unknown route ID, invalid age text, zero/negative age, blank name and unsupported menu choices. The results in that file were produced by actually running the program with `run_tests.py`, which checks both the printed messages and the resulting data. To repeat the tests:

```
python run_tests.py
```

## Screenshots

Screenshots are not included in the generated files, because they have to be taken from your own screen. Follow the sample workflow above and capture:

1. the route listing (menu option 1),
2. a successful booking (option 3),
3. a cancellation (option 5),
4. the report (option 7).

`sample_sessions.txt` shows exactly what each of these screens should look like.

## Streamlit UI — polished demo version

The project includes a modern, responsive Streamlit interface. The UI uses a deep navy and teal colour theme, consistent headings, a styled sidebar, dashboard cards, route cards, readable tables, status labels, booking confirmation details, and seat-capacity progress bars. The console backend remains in `main.py`; the UI is in `app.py`.

### Pages included

1. **Dashboard** — overview metrics, featured routes, and shortcuts to common actions.
2. **View Routes** — filter routes by departure and destination city.
3. **Search Route** — search by route ID and select origin/destination cities.
4. **Book a Ticket** — passenger form, fare calculation, available-seat validation, and booking confirmation.
5. **My Bookings** — all confirmed and cancelled records, with a status filter.
6. **Cancel Booking** — explicit confirmation, seat restoration, and protection against repeated cancellation.
7. **Seat Availability** — available/total seat counts, progress bars, route status, and an available-only filter.
8. **Booking Reports** — total, confirmed, and cancelled bookings; reserved seats; confirmed revenue; fully booked routes; and route-wise breakdown.
9. **Route Schedule** — schedule grouped by each supported departure city, including cities with no departures.

### Install and run in VS Code

1. Extract the ZIP file.
2. Open the extracted `smart_bus` folder in VS Code.
3. Open **Terminal → New Terminal**.
4. Install the UI dependency:

```bash
python -m pip install -r requirements.txt
```

5. Start the app:

```bash
python -m streamlit run app.py
```

6. Streamlit will print a local URL (usually `http://localhost:8501`). Open it in your browser. Keep the terminal open while using the app.

If the `python` command is not recognised on your computer, try `py -m pip install -r requirements.txt` and `py -m streamlit run app.py` on Windows.

### Demo limitations

- **Bookings are stored in memory only.** They remain available while the app process is running, but reset when the process restarts. The sample routes also return to their starting seat counts on restart.
- This project does not include login/accounts, database or file persistence, online payments, real operators, or live schedules.
- The travel timetable is fixed sample data, not live transport information.

### Final UI checklist

- [x] All nine pages are reachable from the sidebar.
- [x] Booking validates a non-empty passenger name, positive age, available route, and seat quantity against current availability.
- [x] Seats decrease only after a booking passes validation.
- [x] Booking confirmation shows the booking ID, passenger, journey, departure, seats, fare per seat, total fare, and status.
- [x] Booking history retains cancelled records.
- [x] Cancellation requires confirmation, restores seats once, and marks the booking as cancelled.
- [x] Seat availability shows exact available/total counts and route status.
- [x] Reports exclude cancelled fares and seats from confirmed totals.
- [x] Schedule includes every supported city and shows an empty state where no departures exist.
- [x] The demo-only in-memory limitation is disclosed in the UI and this guide.

The Python UI file was syntax-checked and the existing backend test suite passed 30/30 tests in the build environment. Streamlit's browser UI should still be opened and clicked through on your computer for final visual verification.
