# Requirements Checklist (PRD -> implementation)

All functions are in `main.py`. Test IDs refer to `test_cases.txt`.

## Functional requirements

| # | Requirement | Where implemented | Tests |
|---|-------------|-------------------|-------|
| 1 | Welcome screen, menu repeats until Exit, helpful error for text/unsupported choices, clean exit on 8 | `show_welcome()`, `show_menu()`, `main()` (while loop, try/except, `break`) | TC-12 |
| 2 | Routes as list of dicts; numbered table; "Fully Booked" at 0; available-only filter uses `continue`; all five starter routes | `routes`, `view_routes()` (`enumerate`, `continue`) | TC-01, TC-10 |
| 3 | Search by route ID / departure / destination; case-insensitive; city search shows all matches; unique ID search uses `break`; for-else no-match | `search_route()` | TC-02, TC-03, B-12, B-13 |
| 4 | Booking: validate name, age, route, seats, availability; unique ID via set; total fare; subtract seats once; no change on failure; confirmation screen | `book_ticket()`, `parse_positive_int()`, `find_route_by_id()`, `generate_booking_id()` | TC-04, TC-05, TC-06, B-01..B-11 |
| 5 | Booking history incl. cancelled; `enumerate`; "No bookings found." | `view_bookings()` | B-15, TC-07 |
| 6 | Cancel: find ID, only Confirmed, restore exact seats once, keep record, for-else, nested conditions, `break` | `cancel_booking()` | TC-07, TC-08, B-16, B-17 |
| 7 | Seat availability with Available / Partially Booked / Fully Booked, filter, invariant 0 <= available <= total | `view_seat_availability()`, `get_route_status()` | TC-04, TC-10 |
| 8 | Report: totals, confirmed, cancelled, reserved seats, confirmed revenue, fully booked routes; nested loops (routes outer, bookings inner); zero state; reconciliation | `generate_report()` | TC-09, TC-11, B-18 |
| 9 | Schedule by departure city: outer loop cities, inner loop routes, "No scheduled departures." | `show_route_schedule()` (menu option 9) | B-14 |

## Required menu

| Required item | Menu number | Function |
|---------------|-------------|----------|
| View Available Routes | 1 | `view_routes()` |
| Search for a Route | 2 | `search_route()` |
| Book a Ticket | 3 | `book_ticket()` |
| View My Bookings | 4 | `view_bookings()` |
| Cancel a Booking | 5 | `cancel_booking()` |
| View Seat Availability | 6 | `view_seat_availability()` |
| Generate Booking Report | 7 | `generate_report()` |
| Exit | 8 | `main()` (`break`) |
| (added) Route Schedule | 9 | `show_route_schedule()` |

## Business rules

| Rule | Where enforced |
|------|----------------|
| BR-01 name required | `book_ticket()`: `strip()` then empty check |
| BR-02 age positive integer | `parse_positive_int()` |
| BR-03 route must exist | `find_route_by_id()` check in `book_ticket()` |
| BR-04 seats positive integer | `parse_positive_int()` |
| BR-05 seats <= available | `book_ticket()` availability check |
| BR-06 unique booking IDs via set | `generate_booking_id()`, `issued_booking_ids` |
| BR-07 total fare = price x seats | `book_ticket()` |
| BR-08 subtract only after all checks, once | `book_ticket()` (all `return`s happen before the update) |
| BR-09 only Confirmed can be cancelled | `cancel_booking()` status check |
| BR-10 restore seats only once | `cancel_booking()` (Cancelled bookings are refused) |
| BR-11 cancelled records stay | `cancel_booking()` only changes `status` |
| BR-12 cancelled fares excluded from revenue | `generate_report()` (`continue` on non-Confirmed) |
| BR-13 0 <= available <= total | Validation in `book_ticket()`, cap in `cancel_booking()`, checked after every test run |
| BR-14 invalid menu choices safe | `main()` try/except and `else` branch |
| BR-15 empty lists are valid | `view_bookings()`, `generate_report()` give messages / zero totals |

## Test cases

TC-01 to TC-12 and 18 boundary tests (B-01 to B-18) are all in `test_cases.txt`. Each one was run against `main.py` from a fresh state. Result: **30 of 30 matched the expected result.**

## Python concepts used

`print()`, `input()`, variables, str / int / bool, lists, dictionaries, tuple (`SUPPORTED_CITIES`), set (`issued_booking_ids`), `if / elif / else` and nested conditions, `for` and nested `for`, `while`, for-else (`search_route`, `cancel_booking`), `break` (unique route search, cancel, menu exit), `continue` (filters, report loop, bad menu input), `enumerate()` (all numbered listings), `try / except` (safe number conversion).

## Deliverables

| Deliverable | File | Status |
|-------------|------|--------|
| main.py | `main.py` | Done, tested |
| README.md | `README.md` | Done |
| test_cases.txt | `test_cases.txt` | Done, results from real runs |
| Screenshots | not generated | Real terminal transcripts are in `sample_sessions.txt`; take screenshots yourself by following the README workflow |
| Demonstration guide | `demo_guide.md` (Roman Urdu) | Done |

## Known discrepancies / decisions

- The PRD lists Exit as option 8 and also requires a schedule feature. To avoid changing any original number, the schedule is option 9.
- On an invalid booking field the program rejects the booking and returns to the menu (it does not re-ask that single field). Nothing is changed in that case.
- Screenshots cannot be created here; `sample_sessions.txt` is the real output they should match.
