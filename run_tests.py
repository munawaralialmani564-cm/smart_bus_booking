"""
run_tests.py - runs the Smart Bus test plan against main.py and writes:
    test_cases.txt      (scenario, input, expected, actual, PASS/FAIL)
    sample_sessions.txt (real terminal transcripts)

How it works: for every test we reload main.py (a fresh, empty in-memory state),
feed it the scripted keyboard answers, capture what it prints, and then check both
the printed messages AND the data left in main.routes / main.bookings.

Run it with:   python run_tests.py
"""

import builtins
import contextlib
import importlib
import io
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import main  # the program under test


def run_script(answers_list):
    """Run main.py from a fresh state, typing the given answers. Returns the printed text."""
    importlib.reload(main)  # fresh routes, empty bookings, empty issued_booking_ids
    answers = iter(answers_list)
    captured = io.StringIO()

    def fake_input(prompt=""):
        try:
            answer = next(answers)
        except StopIteration:
            raise EOFError
        print(prompt + answer)  # echo the typed answer, like a real terminal
        return answer

    original_input = builtins.input
    builtins.input = fake_input
    try:
        with contextlib.redirect_stdout(captured):
            main.main()
    finally:
        builtins.input = original_input
    return captured.getvalue()


def seats_left(route_id):
    return main.find_route_by_id(route_id)["available_seats"]


def invariant_holds():
    """BR-13: 0 <= available_seats <= total_seats for every route."""
    for route in main.routes:
        if not (0 <= route["available_seats"] <= route["total_seats"]):
            return False
    return True


def last_number(label, text):
    """Find 'label : 123' or 'label : Rs. 6,000' in text and return the value as text."""
    match = re.findall(re.escape(label) + r"\s*:\s*([^\n(]+)", text)
    return match[-1].strip() if match else None


# Menu navigation answers used in many scripts
BOOK_AHMED_R101_2 = ["3", "Ahmed", "25", "R101", "2"]

# ---------------------------------------------------------------------------
# TEST DEFINITIONS
# Each test: id, scenario, action (text), expected (text), answers, check(out) -> (actual, ok)
# ---------------------------------------------------------------------------
tests = []


def add_test(test_id, scenario, action, expected, answers, check):
    tests.append({"id": test_id, "scenario": scenario, "action": action,
                  "expected": expected, "answers": answers, "check": check})


# TC-01
def check_tc01(out):
    ids = re.findall(r"^\d+\s+(R\d+)", out, re.M)
    available_rows = len(re.findall(r"^\d+\s+R\d+.*Available$", out, re.M))
    ok = ids == ["R101", "R102", "R103", "R104", "R105"] and available_rows == 5
    return f"Rows shown: {', '.join(ids)}; {available_rows} rows have status 'Available'.", ok


add_test("TC-01", "View all routes",
         "Menu 1, answer 'n' to the available-only filter, then Exit",
         "All five routes appear with their seat status (all 'Available' at the start).",
         ["1", "n", "8"], check_tc01)


# TC-02
def check_tc02(out):
    ids = re.findall(r"Route ID\s+: (R\d+)", out)
    ok = ids == ["R101", "R103", "R105"]
    return f"Routes shown: {', '.join(ids)}.", ok


add_test("TC-02", "Search Hyderabad",
         "Menu 2, search text 'Hyderabad', then Exit",
         "R101 (arrives), R103 (departs) and R105 (arrives) appear; R102 and R104 do not.",
         ["2", "Hyderabad", "8"], check_tc02)


# TC-03
def check_tc03(out):
    ok = "No route found for 'atlantis'" in out and "Goodbye" in out
    return ("No-match message shown: " + str("No route found for 'atlantis'" in out)
            + "; program kept running and exited normally: " + str("Goodbye" in out) + "."), ok


add_test("TC-03", "Unknown city",
         "Menu 2, search text 'Atlantis', then Exit",
         "A no-match message is shown and the program keeps running (menu returns, Exit works).",
         ["2", "Atlantis", "8"], check_tc03)


# TC-04
def check_tc04(out):
    booking = main.bookings[0] if main.bookings else {}
    ok = (len(main.bookings) == 1 and booking.get("total_fare") == 2400
          and booking.get("status") == "Confirmed" and seats_left("R101") == 38
          and "Rs. 2,400" in out and invariant_holds())
    return (f"Booking {booking.get('booking_id')} created, total_fare={booking.get('total_fare')}, "
            f"status={booking.get('status')}; R101 available seats = {seats_left('R101')} of 40."), ok


add_test("TC-04", "Book two seats",
         "Menu 3: name Ahmed, age 25, route R101, seats 2",
         "Booking confirmed, total Rs. 2,400, R101 availability drops from 40 to 38.",
         BOOK_AHMED_R101_2 + ["8"], check_tc04)


# TC-05
def check_tc05(out):
    ok = (len(main.bookings) == 0 and seats_left("R101") == 40
          and "Booking was NOT created" in out and invariant_holds())
    return (f"Rejection message shown: {'Booking was NOT created' in out}; bookings stored = {len(main.bookings)}; "
            f"R101 available seats = {seats_left('R101')}."), ok


add_test("TC-05", "Zero seats",
         "Menu 3: name Ahmed, age 25, route R101, seats 0",
         "Rejected; no booking is created and no seat count changes.",
         ["3", "Ahmed", "25", "R101", "0", "8"], check_tc05)


# TC-06
def check_tc06(out):
    ok = (len(main.bookings) == 0 and seats_left("R101") == 40
          and "only 40 seat(s) are available" in out and invariant_holds())
    lowest = min(r["available_seats"] for r in main.routes)
    return (f"Rejection message shown: {'only 40 seat(s) are available' in out}; bookings stored = {len(main.bookings)}; "
            f"R101 available seats = {seats_left('R101')}; lowest seat count on any route = {lowest}."), ok


add_test("TC-06", "Too many seats",
         "Menu 3: name Ahmed, age 25, route R101, seats 41 (capacity is 40)",
         "Rejected; availability stays 40 and never becomes negative.",
         ["3", "Ahmed", "25", "R101", "41", "8"], check_tc06)


# TC-07
def check_tc07(out):
    booking = main.bookings[0] if main.bookings else {}
    ok = (len(main.bookings) == 1 and booking.get("status") == "Cancelled"
          and seats_left("R101") == 40 and "Seats restored : 2" in out and invariant_holds())
    return (f"Booking record kept: {len(main.bookings)}; status={booking.get('status')}; "
            f"'Seats restored : 2' shown: {'Seats restored : 2' in out}; R101 available seats = {seats_left('R101')}."), ok


add_test("TC-07", "Cancel a confirmed booking",
         "Book 2 seats on R101 (B1001), then Menu 5 with B1001",
         "Status becomes Cancelled, exactly 2 seats are restored (R101 back to 40), record is kept.",
         BOOK_AHMED_R101_2 + ["5", "B1001", "8"], check_tc07)


# TC-08
def check_tc08(out):
    ok = (seats_left("R101") == 40 and out.count("Seats restored :") == 1
          and "is already Cancelled" in out and invariant_holds())
    return (f"'already Cancelled' error shown: {'is already Cancelled' in out}; 'Seats restored' printed "
            f"{out.count('Seats restored :')} time(s); R101 available seats = {seats_left('R101')}."), ok


add_test("TC-08", "Cancel the same booking again",
         "Book 2 seats (B1001), cancel B1001, cancel B1001 a second time",
         "Second cancellation is rejected and seats are NOT restored a second time.",
         BOOK_AHMED_R101_2 + ["5", "B1001", "5", "B1001", "8"], check_tc08)


# TC-09
def check_tc09(out):
    ok = (last_number("Total bookings created", out) == "0"
          and last_number("Confirmed bookings", out) == "0"
          and last_number("Cancelled bookings", out) == "0"
          and last_number("Seats currently reserved", out) == "0"
          and last_number("Confirmed revenue", out) == "Rs. 0"
          and last_number("Fully booked routes", out) == "0")
    return (f"Total={last_number('Total bookings created', out)}, Confirmed={last_number('Confirmed bookings', out)}, "
            f"Cancelled={last_number('Cancelled bookings', out)}, Reserved seats={last_number('Seats currently reserved', out)}, "
            f"Revenue={last_number('Confirmed revenue', out)}, Fully booked routes={last_number('Fully booked routes', out)}."), ok


add_test("TC-09", "Report with no bookings",
         "Menu 7 on a fresh run",
         "All booking counts, reserved seats and revenue are 0; fully booked routes is still calculated (0).",
         ["7", "8"], check_tc09)


# TC-10
def check_tc10(out):
    last_part = out.split("Show only routes")[-1]  # the final availability screen (filter = y)
    ok = (seats_left("R101") == 0 and main.get_route_status(main.find_route_by_id("R101")) == "Fully Booked"
          and len(main.bookings) == 2 and "Fully Booked" in out and "R101" not in last_part
          and invariant_holds())
    return (f"R101 available seats = {seats_left('R101')}; status = "
            f"{main.get_route_status(main.find_route_by_id('R101'))}; 'Fully Booked' shown in listing: "
            f"{'Fully Booked' in out}; hidden when the available-only filter is on: {'R101' not in last_part}."), ok


add_test("TC-10", "Book all remaining seats",
         "Book 2 seats on R101, then book the remaining 38; view routes; view availability with filter 'y'",
         "Second booking succeeds, R101 shows 0 seats and 'Fully Booked', and the filter hides R101.",
         BOOK_AHMED_R101_2 + ["3", "Sara", "30", "R101", "38", "1", "n", "6", "y", "8"], check_tc10)


# TC-11
def check_tc11(out):
    ok = (last_number("Total bookings created", out) == "2"
          and last_number("Confirmed bookings", out) == "1"
          and last_number("Cancelled bookings", out) == "1"
          and last_number("Seats currently reserved", out) == "3"
          and last_number("Confirmed revenue", out) == "Rs. 6,000"
          and "report totals agree" in out)
    return (f"Total={last_number('Total bookings created', out)}, Confirmed={last_number('Confirmed bookings', out)}, "
            f"Cancelled={last_number('Cancelled bookings', out)}, Reserved seats={last_number('Seats currently reserved', out)}, "
            f"Revenue={last_number('Confirmed revenue', out)}; reconciliation check printed OK: {'report totals agree' in out}."), ok


add_test("TC-11", "Report after cancellation",
         "Book 2 seats on R101 (Rs. 2,400), book 3 seats on R102 (Rs. 6,000), cancel B1001, Menu 7",
         "Total 2, confirmed 1, cancelled 1, reserved seats 3, revenue Rs. 6,000 (cancelled fare excluded).",
         BOOK_AHMED_R101_2 + ["3", "Sara", "30", "R102", "3", "5", "B1001", "7", "8"], check_tc11)


# TC-12
def check_tc12(out):
    invalid_count = out.count("Invalid")
    ok = invalid_count == 5 and "Goodbye" in out
    return f"'Invalid ...' message shown {invalid_count} time(s) for 5 bad entries; program still exited normally: {'Goodbye' in out}.", ok


add_test("TC-12", "Invalid menu option",
         "Type 'abc', '0', '10', '-3' and an empty line at the menu, then 8",
         "Each bad entry gives a helpful error and returns to the menu without crashing.",
         ["abc", "0", "10", "-3", "", "8"], check_tc12)


# ---------------- Boundary and extra tests ----------------

def no_change_check(message_text):
    def check(out):
        ok = (message_text in out and len(main.bookings) == 0
              and all(r["available_seats"] == r["total_seats"] for r in main.routes))
        return (f"Message shown: {message_text in out}; bookings stored = {len(main.bookings)}; "
                f"all routes still at full availability: {all(r['available_seats'] == r['total_seats'] for r in main.routes)}."), ok
    return check


add_test("B-01", "Invalid age text", "Menu 3: name Ahmed, age 'abc'",
         "Rejected with an age error; no booking; no seat change.",
         ["3", "Ahmed", "abc", "8"], no_change_check("age must be a positive whole number"))

add_test("B-02", "Zero age", "Menu 3: name Ahmed, age 0",
         "Rejected with an age error; no booking; no seat change.",
         ["3", "Ahmed", "0", "8"], no_change_check("age must be a positive whole number"))

add_test("B-03", "Negative age", "Menu 3: name Ahmed, age -5",
         "Rejected with an age error; no booking; no seat change.",
         ["3", "Ahmed", "-5", "8"], no_change_check("age must be a positive whole number"))

add_test("B-04", "Blank passenger name (spaces only)", "Menu 3: name '   '",
         "Rejected with a name error; no booking; no seat change.",
         ["3", "   ", "8"], no_change_check("passenger name cannot be empty"))

add_test("B-05", "Unknown route ID", "Menu 3: name Ahmed, age 25, route R999",
         "Rejected: route does not exist; no booking; no seat change.",
         ["3", "Ahmed", "25", "R999", "8"], no_change_check("route 'R999' does not exist"))

add_test("B-06", "Seat quantity is text", "Menu 3: name Ahmed, age 25, route R101, seats 'two'",
         "Rejected with a seats error; no booking; no seat change.",
         ["3", "Ahmed", "25", "R101", "two", "8"], no_change_check("number of seats must be a positive whole number"))

add_test("B-07", "Negative seat quantity", "Menu 3: name Ahmed, age 25, route R101, seats -2",
         "Rejected with a seats error; no booking; no seat change.",
         ["3", "Ahmed", "25", "R101", "-2", "8"], no_change_check("number of seats must be a positive whole number"))


def check_b08(out):
    ok = (len(main.bookings) == 1 and seats_left("R103") == 1
          and "only 1 seat(s) are available" in out and invariant_holds())
    return (f"Bookings stored = {len(main.bookings)}; R103 available seats = {seats_left('R103')}; "
            f"over-request rejected: {'only 1 seat(s) are available' in out}."), ok


add_test("B-08", "One more than available",
         "Book 31 seats on R103 (leaves 1), then request 2 seats on R103",
         "Second request is rejected; R103 still has 1 seat; only 1 booking exists.",
         ["3", "Ali", "40", "R103", "31", "3", "Sana", "22", "R103", "2", "8"], check_b08)


def check_b09(out):
    ok = (seats_left("R103") == 0 and main.get_route_status(main.find_route_by_id("R103")) == "Fully Booked"
          and len(main.bookings) == 1 and main.bookings[0]["total_fare"] == 25600)
    return (f"R103 available seats = {seats_left('R103')}; status = "
            f"{main.get_route_status(main.find_route_by_id('R103'))}; total_fare = {main.bookings[0]['total_fare']}."), ok


add_test("B-09", "Exactly all seats of a route",
         "Book 32 seats (the full capacity) on R103",
         "Booking succeeds (32 x 800 = 25,600); availability becomes 0; status Fully Booked.",
         ["3", "Ali", "40", "R103", "32", "8"], check_b09)


def check_b10(out):
    ok = (len(main.bookings) == 1 and "is Fully Booked" in out and seats_left("R101") == 0)
    return (f"Bookings stored = {len(main.bookings)}; 'Fully Booked' error shown: {'is Fully Booked' in out}; "
            f"R101 available seats = {seats_left('R101')}."), ok


add_test("B-10", "Book on a fully booked route",
         "Book all 40 seats on R101, then try to book 1 more seat on R101",
         "Second booking is rejected with a 'Fully Booked' message; availability stays 0.",
         ["3", "Ali", "40", "R101", "40", "3", "Sana", "22", "R101", "1", "8"], check_b10)


def check_b11(out):
    ids = [b["booking_id"] for b in main.bookings]
    ok = (ids == ["B1001", "B1002"] and len(set(ids)) == 2 and main.issued_booking_ids == {"B1001", "B1002"})
    return f"Booking IDs issued: {ids}; issued_booking_ids set = {sorted(main.issued_booking_ids)}.", ok


add_test("B-11", "Unique booking IDs",
         "Make two valid bookings in one run",
         "Two different IDs (B1001, B1002), both recorded in the issued-IDs set.",
         BOOK_AHMED_R101_2 + ["3", "Sara", "30", "R102", "1", "8"], check_b11)


def check_b12(out):
    ids = re.findall(r"Route ID\s+: (R\d+)", out)
    ok = ids == ["R101"]
    return f"Routes shown: {', '.join(ids)}.", ok


add_test("B-12", "Search by route ID (lower case)",
         "Menu 2, search text 'r101'",
         "Only route R101 is shown (search stops at the unique match).",
         ["2", "r101", "8"], check_b12)


def check_b13(out):
    ids = re.findall(r"Route ID\s+: (R\d+)", out)
    ok = ids == ["R103"]
    return f"Routes shown: {', '.join(ids)}.", ok


add_test("B-13", "Search by destination city (mixed case)",
         "Menu 2, search text 'MiRpUr KhAs'",
         "Only R103 (Hyderabad -> Mirpur Khas) is shown.",
         ["2", "MiRpUr KhAs", "8"], check_b13)


def check_b14(out):
    ok = out.count("No scheduled departures.") == 2
    return (f"'No scheduled departures.' shown {out.count('No scheduled departures.')} time(s) "
            f"(Mirpur Khas and Lahore)."), ok


add_test("B-14", "Route schedule for all supported cities",
         "Menu 9",
         "All five cities are listed; Mirpur Khas and Lahore show 'No scheduled departures.'.",
         ["9", "8"], check_b14)


def check_b15(out):
    ok = "No bookings found." in out
    return f"'No bookings found.' shown: {ok}.", ok


add_test("B-15", "View bookings with an empty list", "Menu 4 on a fresh run",
         "'No bookings found.' is shown.",
         ["4", "8"], check_b15)


def check_b16(out):
    ok = ("no booking found with ID 'B9999'" in out and len(main.bookings) == 0
          and all(r["available_seats"] == r["total_seats"] for r in main.routes))
    return f"Error shown: {'no booking found with ID' in out}; bookings = {len(main.bookings)}; seats unchanged.", ok


add_test("B-16", "Cancel an unknown booking ID", "Menu 5 with B9999",
         "Error shown; nothing changes.",
         ["5", "B9999", "8"], check_b16)


def check_b17(out):
    ok = (seats_left("R101") == 39 and len(main.bookings) == 2
          and main.bookings[0]["status"] == "Cancelled" and main.bookings[1]["status"] == "Confirmed"
          and invariant_holds())
    return (f"R101 available seats = {seats_left('R101')}; statuses = "
            f"{[b['status'] for b in main.bookings]}."), ok


add_test("B-17", "Rebook after a cancellation",
         "Book all 40 seats on R101, cancel it, then book 1 seat on R101",
         "Cancel restores 40 seats, the new booking uses 1: R101 has 39 left; both records kept.",
         ["3", "Ali", "40", "R101", "40", "5", "B1001", "3", "Sana", "22", "R101", "1", "8"], check_b17)


def check_b18(out):
    ok = (last_number("Seats currently reserved", out) == "1"
          and last_number("Confirmed revenue", out) == "Rs. 1,200"
          and last_number("Fully booked routes", out) == "1"
          and "report totals agree" in out)
    return (f"Reserved seats={last_number('Seats currently reserved', out)}, "
            f"Revenue={last_number('Confirmed revenue', out)}, "
            f"Fully booked routes={last_number('Fully booked routes', out)}."), ok


add_test("B-18", "Report reconciles with seat counts (mixed activity)",
         "Fill R103 completely (32 seats), book 1 seat on R101, book then cancel 2 seats on R102, Menu 7",
         "Reserved seats 33 is the sum of Confirmed seats, which matches capacity minus available; "
         "revenue excludes the cancelled booking.",
         ["3", "Ali", "40", "R103", "32", "3", "Sana", "22", "R101", "1",
          "3", "Omar", "35", "R102", "2", "5", "B1003", "7", "8"],
         lambda out: (
             (f"Reserved seats={last_number('Seats currently reserved', out)}, "
              f"Revenue={last_number('Confirmed revenue', out)}, "
              f"Fully booked routes={last_number('Fully booked routes', out)}; reconciliation line printed: "
              f"{'report totals agree' in out}."),
             (last_number("Seats currently reserved", out) == "33"
              and last_number("Confirmed revenue", out) == "Rs. 26,800"
              and last_number("Fully booked routes", out) == "1"
              and "report totals agree" in out)))


# ---------------------------------------------------------------------------
# RUN ALL TESTS AND WRITE test_cases.txt
# ---------------------------------------------------------------------------

def run_all_tests():
    results = []
    for test in tests:
        out = run_script(test["answers"])
        actual, ok = test["check"](out)
        # BR-13 is verified after every single test run.
        if not invariant_holds():
            ok = False
            actual += " [BR-13 violated!]"
        else:
            actual += " (BR-13 holds: 0 <= available <= total for every route.)"
        results.append((test, actual, ok))
    return results


def write_test_cases(results, path):
    passed = sum(1 for _, _, ok in results if ok)
    lines = []
    lines.append("SMART BUS TICKET BOOKING & RESERVATION SYSTEM - TEST CASES")
    lines.append("=" * 70)
    lines.append("These results were produced by actually running main.py with run_tests.py.")
    lines.append("Every test starts from a fresh run (5 starter routes, no bookings).")
    lines.append("'Actual result' is taken from the program's real output and its real data.")
    lines.append("Menu note: option 8 = Exit, option 9 = Route Schedule.")
    lines.append("Summary: " + str(passed) + " of " + str(len(results)) + " tests matched the expected result.")
    lines.append("=" * 70)
    for test, actual, ok in results:
        lines.append("")
        lines.append("Test ID        : " + test["id"])
        lines.append("Scenario       : " + test["scenario"])
        lines.append("Input / action : " + test["action"])
        lines.append("Expected result: " + test["expected"])
        lines.append("Actual result  : " + actual)
        lines.append("Matched?       : " + ("PASS" if ok else "FAIL"))
        lines.append("-" * 70)
    with open(path, "w", encoding="utf-8") as file:
        file.write("\n".join(lines) + "\n")
    return passed


# ---------------------------------------------------------------------------
# SAMPLE SESSIONS (real transcripts)
# ---------------------------------------------------------------------------

MENU_BLOCK = re.compile(r"\n-{25} MAIN MENU -{25}\n(?:\d\. [^\n]*\n)+")


def shorten_menus(text):
    """Keep the first menu in full, and replace later menus by a short note."""
    first = MENU_BLOCK.search(text)
    if not first:
        return text
    head = text[:first.end()]
    tail = MENU_BLOCK.sub("\n[... main menu shown again ...]\n", text[first.end():])
    return head + tail


SESSIONS = [
    ("Viewing routes", ["1", "n", "8"]),
    ("Searching (route ID, city with several matches, unknown city)",
     ["2", "R102", "2", "Hyderabad", "2", "Atlantis", "8"]),
    ("Successful booking", ["3", "Ahmed", "25", "R101", "2", "4", "8"]),
    ("Invalid bookings (blank name, bad age, unknown route, zero seats, too many seats)",
     ["3", "   ", "3", "Ahmed", "abc", "3", "Ahmed", "25", "R999",
      "3", "Ahmed", "25", "R101", "0", "3", "Ahmed", "25", "R101", "41", "4", "6", "n", "8"]),
    ("Cancellation (booking, cancel, history, availability)",
     ["3", "Ahmed", "25", "R101", "2", "5", "B1001", "4", "6", "n", "8"]),
    ("Repeated cancellation of the same booking",
     ["3", "Ahmed", "25", "R101", "2", "5", "B1001", "5", "B1001", "6", "n", "8"]),
    ("Seat availability (after bookings, with and without the filter)",
     ["3", "Ahmed", "25", "R101", "2", "3", "Sara", "30", "R103", "32", "6", "n", "6", "y", "8"]),
    ("Route schedule by departure city", ["9", "8"]),
    ("Report with no bookings", ["7", "8"]),
    ("Report after bookings and a cancellation",
     ["3", "Ahmed", "25", "R101", "2", "3", "Sara", "30", "R102", "3", "5", "B1001", "7", "8"]),
    ("Invalid menu choices", ["abc", "0", "10", "8"]),
]


def write_sample_sessions(path):
    lines = []
    lines.append("SMART BUS - SAMPLE TERMINAL SESSIONS")
    lines.append("=" * 70)
    lines.append("These are real transcripts produced by running main.py with scripted answers")
    lines.append("(what you type is shown after each prompt). Each session starts from a fresh run.")
    lines.append("To keep them short, the main menu is shown in full only the first time.")
    for title, answers in SESSIONS:
        out = run_script(answers)
        lines.append("")
        lines.append("#" * 70)
        lines.append("SESSION: " + title)
        lines.append("#" * 70)
        lines.append(shorten_menus(out).rstrip())
    with open(path, "w", encoding="utf-8") as file:
        file.write("\n".join(lines) + "\n")


if __name__ == "__main__":
    folder = os.path.dirname(os.path.abspath(__file__))
    all_results = run_all_tests()
    passed_count = write_test_cases(all_results, os.path.join(folder, "test_cases.txt"))
    write_sample_sessions(os.path.join(folder, "sample_sessions.txt"))
    print("Tests matched:", passed_count, "of", len(all_results))
    for test_info, actual_text, ok_flag in all_results:
        if not ok_flag:
            print("FAILED:", test_info["id"], "-", actual_text)
    print("Wrote test_cases.txt and sample_sessions.txt")
