"""
Smart Bus Ticket Booking & Reservation System
=============================================
A beginner-friendly Python 3 console application.

* Uses only built-in Python features (no external packages).
* All data (routes, bookings, issued booking IDs) lives in memory only.
  When the program exits, every booking is lost. This is expected.

Menu options 1-8 are exactly the ones required by the PRD (8 = Exit).
Option 9 (Route Schedule by Departure City) was added so that the
schedule feature is reachable without changing any original number.
"""

# ---------------------------------------------------------------------------
# DATA (all stored in memory)
# ---------------------------------------------------------------------------

APP_NAME = "SMART BUS TICKET BOOKING & RESERVATION SYSTEM"

# Tuple: the list of supported cities never changes while the program runs.
SUPPORTED_CITIES = ("Karachi", "Hyderabad", "Sukkur", "Mirpur Khas", "Lahore")

# List of dictionaries: one dictionary per route.
routes = [
    {
        "route_id": "R101",
        "departure_city": "Karachi",
        "destination_city": "Hyderabad",
        "departure_time": "08:00 AM",
        "ticket_price": 1200,
        "total_seats": 40,
        "available_seats": 40,
    },
    {
        "route_id": "R102",
        "departure_city": "Karachi",
        "destination_city": "Sukkur",
        "departure_time": "09:30 AM",
        "ticket_price": 2000,
        "total_seats": 36,
        "available_seats": 36,
    },
    {
        "route_id": "R103",
        "departure_city": "Hyderabad",
        "destination_city": "Mirpur Khas",
        "departure_time": "11:00 AM",
        "ticket_price": 800,
        "total_seats": 32,
        "available_seats": 32,
    },
    {
        "route_id": "R104",
        "departure_city": "Karachi",
        "destination_city": "Lahore",
        "departure_time": "07:00 PM",
        "ticket_price": 5000,
        "total_seats": 45,
        "available_seats": 45,
    },
    {
        "route_id": "R105",
        "departure_city": "Sukkur",
        "destination_city": "Hyderabad",
        "departure_time": "02:00 PM",
        "ticket_price": 1500,
        "total_seats": 30,
        "available_seats": 30,
    },
]

# List of dictionaries: every booking ever made (Confirmed AND Cancelled).
bookings = []

# Set: every booking ID issued during this run (a set cannot hold duplicates).
issued_booking_ids = set()


# ---------------------------------------------------------------------------
# SMALL HELPER FUNCTIONS
# ---------------------------------------------------------------------------

def format_money(amount):
    """Return an integer fare as text, for example 2400 -> 'Rs. 2,400'."""
    return "Rs. " + format(amount, ",")


def describe_journey(route):
    """Return the journey text, for example 'Karachi -> Hyderabad'."""
    return route["departure_city"] + " -> " + route["destination_city"]


def parse_positive_int(text):
    """
    Safely convert text to a positive whole number.
    Returns the number, or None if the text is not a whole number
    or if the number is zero or negative.
    """
    try:
        number = int(text.strip())
    except ValueError:
        return None  # text such as "abc" or "2.5" or "" cannot be converted
    if number <= 0:
        return None  # zero and negative numbers are rejected
    return number


def ask_yes_no(question):
    """Ask a y/n question. Only 'y' or 'yes' means True; anything else is False."""
    answer = input(question).strip().lower()
    return answer in ("y", "yes")


def find_route_by_id(route_id):
    """Return the route dictionary with this route ID, or None if it does not exist."""
    for route in routes:
        if route["route_id"] == route_id:
            return route
    return None


def get_route_status(route):
    """Classify a route as Available, Partially Booked or Fully Booked."""
    if route["available_seats"] == 0:
        return "Fully Booked"
    if route["available_seats"] == route["total_seats"]:
        return "Available"  # nothing has been booked yet
    return "Partially Booked"  # some seats booked, some still free


def generate_booking_id():
    """
    Create a booking ID such as B1001 that has not been used in this run.
    The ID is checked against the set of issued IDs before it is used.
    """
    number = 1001 + len(issued_booking_ids)
    new_id = "B" + str(number)
    while new_id in issued_booking_ids:  # extra safety: keep going until unused
        number += 1
        new_id = "B" + str(number)
    issued_booking_ids.add(new_id)
    return new_id


def print_route_details(route):
    """Print every detail of one route."""
    print("  Route ID       :", route["route_id"])
    print("  Journey        :", describe_journey(route))
    print("  Departure time :", route["departure_time"])
    print("  Ticket price   :", format_money(route["ticket_price"]), "per seat")
    print("  Seats          :", route["available_seats"], "available of", route["total_seats"])
    print("  Status         :", get_route_status(route))


# ---------------------------------------------------------------------------
# MENU SCREENS
# ---------------------------------------------------------------------------

def show_welcome():
    """Show the application name once, at startup."""
    print("=" * 62)
    print(APP_NAME.center(62))
    print("=" * 62)
    print("(All data is kept in memory only and is lost when you exit.)")


def show_menu():
    """Show the numbered main menu."""
    print("\n------------------------- MAIN MENU -------------------------")
    print("1. View Available Routes")
    print("2. Search for a Route")
    print("3. Book a Ticket")
    print("4. View My Bookings")
    print("5. Cancel a Booking")
    print("6. View Seat Availability")
    print("7. Generate Booking Report")
    print("8. Exit")
    print("9. View Route Schedule by Departure City")


# ---------------------------------------------------------------------------
# 1) VIEW ROUTES
# ---------------------------------------------------------------------------

def view_routes():
    """Show routes in a numbered table, optionally hiding fully booked ones."""
    print("\n--- ROUTES ---")
    only_available = ask_yes_no("Show only routes with seats available? (y/n): ")

    # Step 1: build the list of routes to show.
    visible_routes = []
    for route in routes:
        if only_available and route["available_seats"] == 0:
            continue  # skip fully booked routes when the filter is on
        visible_routes.append(route)

    if len(visible_routes) == 0:
        print("No routes with available seats right now.")
        return

    # Step 2: print the table. enumerate() gives each row its sequence number.
    print()
    print(f"{'No.':<5}{'Route':<8}{'Journey':<26}{'Departs':<10}{'Fare':<11}{'Seats Left':<12}Status")
    print("-" * 80)
    for number, route in enumerate(visible_routes, start=1):
        if route["available_seats"] == 0:
            status = "Fully Booked"
        else:
            status = "Available"
        print(f"{number:<5}{route['route_id']:<8}{describe_journey(route):<26}"
              f"{route['departure_time']:<10}{format_money(route['ticket_price']):<11}"
              f"{route['available_seats']:<12}{status}")


# ---------------------------------------------------------------------------
# 2) SEARCH FOR A ROUTE
# ---------------------------------------------------------------------------

def search_route():
    """Search by route ID, departure city or destination city (case-insensitive)."""
    print("\n--- SEARCH FOR A ROUTE ---")
    query = input("Enter a route ID or a city name: ").strip().lower()

    if query == "":
        print("Nothing was entered. Please type a route ID (e.g. R101) or a city (e.g. Karachi).")
        return

    # First try a route ID. A route ID is unique, so we stop (break) at the first match.
    for route in routes:
        if route["route_id"].lower() == query:
            print("\nRoute found:")
            print_route_details(route)
            break
    else:
        # for-else: this part runs only when the loop finished WITHOUT break,
        # meaning the text was not a route ID. So now we try it as a city name.
        matches_found = 0
        for route in routes:
            departs_from_city = route["departure_city"].lower() == query
            arrives_in_city = route["destination_city"].lower() == query
            if departs_from_city or arrives_in_city:
                matches_found += 1
                print("\nMatch " + str(matches_found) + ":")
                print_route_details(route)  # no break: show ALL matching routes
        if matches_found == 0:
            print("No route found for '" + query + "'.")
            print("Try a route ID like R101, or one of these cities: " + ", ".join(SUPPORTED_CITIES) + ".")
        else:
            print("\n" + str(matches_found) + " matching route(s) found.")


# ---------------------------------------------------------------------------
# 3) BOOK A TICKET
# ---------------------------------------------------------------------------

def book_ticket():
    """
    Collect and validate passenger details, then create a booking.
    Every field is validated BEFORE anything is changed. If any check fails,
    we print the reason and return: no booking is created and no seats change.
    """
    print("\n--- BOOK A TICKET ---")

    # Passenger name (BR-01): must not be empty or only spaces.
    passenger_name = input("Passenger name: ").strip()
    if passenger_name == "":
        print("Error: passenger name cannot be empty. Booking was NOT created. No seats were changed.")
        return

    # Passenger age (BR-02): must be a positive whole number.
    age = parse_positive_int(input("Passenger age: "))
    if age is None:
        print("Error: age must be a positive whole number (for example 25). "
              "Booking was NOT created. No seats were changed.")
        return

    # Route ID (BR-03): the route must exist.
    route_id = input("Route ID (for example R101): ").strip().upper()
    route = find_route_by_id(route_id)
    if route is None:
        print("Error: route '" + route_id + "' does not exist. Booking was NOT created. No seats were changed.")
        return

    # Number of seats (BR-04): must be a positive whole number.
    seats = parse_positive_int(input("Number of seats: "))
    if seats is None:
        print("Error: number of seats must be a positive whole number (1 or more). "
              "Booking was NOT created. No seats were changed.")
        return

    # Availability (BR-05): cannot ask for more seats than are free.
    if seats > route["available_seats"]:
        if route["available_seats"] == 0:
            print("Error: route " + route_id + " is Fully Booked.", end=" ")
        else:
            print("Error: only " + str(route["available_seats"]) + " seat(s) are available on route "
                  + route_id + ", but you asked for " + str(seats) + ".", end=" ")
        print("Booking was NOT created. No seats were changed.")
        return

    # ---- Every validation passed. Only now do we change any data. ----
    fare_per_seat = route["ticket_price"]
    total_fare = fare_per_seat * seats  # BR-07
    booking_id = generate_booking_id()  # BR-06 (checked against the set)

    booking = {
        "booking_id": booking_id,
        "passenger_name": passenger_name,
        "passenger_age": age,
        "route_id": route_id,
        "seats": seats,
        "total_fare": total_fare,
        "status": "Confirmed",
    }
    bookings.append(booking)
    route["available_seats"] -= seats  # BR-08: subtract exactly once

    print("\n*** BOOKING CONFIRMED ***")
    print("  Booking ID    :", booking_id)
    print("  Passenger     :", passenger_name, "(age " + str(age) + ")")
    print("  Route         :", route_id, "-", describe_journey(route))
    print("  Departure     :", route["departure_time"])
    print("  Seats booked  :", seats)
    print("  Fare per seat :", format_money(fare_per_seat))
    print("  Total fare    :", format_money(total_fare))
    print("  Status        :", booking["status"])


# ---------------------------------------------------------------------------
# 4) VIEW BOOKINGS
# ---------------------------------------------------------------------------

def view_bookings():
    """Show every booking, including cancelled ones."""
    print("\n--- BOOKING HISTORY ---")
    if len(bookings) == 0:
        print("No bookings found.")
        return

    print(f"{'No.':<5}{'Booking':<9}{'Passenger':<16}{'Route':<30}{'Seats':<7}{'Total Fare':<13}Status")
    print("-" * 88)
    for number, booking in enumerate(bookings, start=1):
        route = find_route_by_id(booking["route_id"])
        route_text = booking["route_id"] + " " + describe_journey(route)
        print(f"{number:<5}{booking['booking_id']:<9}{booking['passenger_name']:<16}{route_text:<30}"
              f"{booking['seats']:<7}{format_money(booking['total_fare']):<13}{booking['status']}")


# ---------------------------------------------------------------------------
# 5) CANCEL A BOOKING
# ---------------------------------------------------------------------------

def cancel_booking():
    """Cancel a Confirmed booking and give its seats back to its route (only once)."""
    print("\n--- CANCEL A BOOKING ---")
    booking_id = input("Enter the booking ID to cancel (for example B1001): ").strip().upper()

    for booking in bookings:
        if booking["booking_id"] == booking_id:
            # We found the booking. Now check its status (nested condition).
            if booking["status"] == "Confirmed":
                route = find_route_by_id(booking["route_id"])
                # One logical operation: give the seats back AND mark as Cancelled together.
                seats_to_restore = booking["seats"]
                new_available = route["available_seats"] + seats_to_restore
                if new_available > route["total_seats"]:
                    new_available = route["total_seats"]  # safety: never above capacity (BR-13)
                route["available_seats"] = new_available
                booking["status"] = "Cancelled"  # the record stays in the history (BR-11)

                print("\n*** BOOKING CANCELLED ***")
                print("  Booking ID     :", booking_id)
                print("  Passenger      :", booking["passenger_name"])
                print("  Route          :", route["route_id"], "-", describe_journey(route))
                print("  Seats restored :", seats_to_restore)
                print("  Seats now free :", route["available_seats"], "of", route["total_seats"])
                print("  Status         :", booking["status"])
            else:
                # Already cancelled: do nothing, so seats can never be restored twice (BR-10).
                print("Error: booking " + booking_id + " is already " + booking["status"]
                      + ". Nothing was changed and no seats were restored.")
            break  # booking IDs are unique, so stop searching
    else:
        # for-else: the loop ended without break, so no booking had this ID.
        print("Error: no booking found with ID '" + booking_id + "'. Nothing was changed.")


# ---------------------------------------------------------------------------
# 6) SEAT AVAILABILITY
# ---------------------------------------------------------------------------

def view_seat_availability():
    """Show available seats and capacity for each route, with its status."""
    print("\n--- SEAT AVAILABILITY ---")
    only_available = ask_yes_no("Show only routes with seats available? (y/n): ")

    visible_routes = []
    for route in routes:
        if only_available and route["available_seats"] == 0:
            continue
        visible_routes.append(route)

    if len(visible_routes) == 0:
        print("No routes with available seats right now.")
        return

    print()
    print(f"{'No.':<5}{'Route':<8}{'Journey':<26}{'Available':<11}{'Capacity':<10}Status")
    print("-" * 72)
    for number, route in enumerate(visible_routes, start=1):
        print(f"{number:<5}{route['route_id']:<8}{describe_journey(route):<26}"
              f"{route['available_seats']:<11}{route['total_seats']:<10}{get_route_status(route)}")


# ---------------------------------------------------------------------------
# 7) BOOKING REPORT
# ---------------------------------------------------------------------------

def generate_report():
    """Calculate and show the booking report from the real records."""
    print("\n--- BOOKING REPORT ---")

    # Count all records by status.
    total_bookings = 0
    confirmed_bookings = 0
    cancelled_bookings = 0
    for booking in bookings:
        total_bookings += 1
        if booking["status"] == "Confirmed":
            confirmed_bookings += 1
        elif booking["status"] == "Cancelled":
            cancelled_bookings += 1

    # Nested loops: the OUTER loop goes over routes, the INNER loop goes over bookings.
    # Only Confirmed bookings are added, so cancelled fares are never counted (BR-12).
    seats_reserved = 0
    confirmed_revenue = 0
    print("Confirmed bookings grouped by route:")
    for route in routes:
        route_count = 0
        route_seats = 0
        route_revenue = 0
        for booking in bookings:
            if booking["route_id"] != route["route_id"]:
                continue  # booking belongs to another route
            if booking["status"] != "Confirmed":
                continue  # cancelled bookings are excluded
            route_count += 1
            route_seats += booking["seats"]
            route_revenue += booking["total_fare"]
        seats_reserved += route_seats
        confirmed_revenue += route_revenue
        print(f"  {route['route_id']} {describe_journey(route):<26} "
              f"bookings: {route_count:<3} seats: {route_seats:<4} revenue: {format_money(route_revenue)}")

    # Fully booked routes come from the CURRENT route availability.
    fully_booked_routes = 0
    seats_missing_from_routes = 0  # seats that routes show as taken (capacity - available)
    for route in routes:
        if route["available_seats"] == 0:
            fully_booked_routes += 1
        seats_missing_from_routes += route["total_seats"] - route["available_seats"]

    print()
    print("Total bookings created      :", total_bookings, "(includes cancelled)")
    print("Confirmed bookings          :", confirmed_bookings)
    print("Cancelled bookings          :", cancelled_bookings)
    print("Seats currently reserved    :", seats_reserved)
    print("Confirmed revenue           :", format_money(confirmed_revenue), "(cancelled fares excluded)")
    print("Fully booked routes         :", fully_booked_routes)

    # Reconciliation: the report must agree with the route availability.
    if seats_reserved == seats_missing_from_routes and total_bookings == confirmed_bookings + cancelled_bookings:
        print("Check: report totals agree with the booking records and route seat counts. OK")
    else:
        print("WARNING: report totals do not agree with route seat counts!")


# ---------------------------------------------------------------------------
# 9) ROUTE SCHEDULE BY DEPARTURE CITY
# ---------------------------------------------------------------------------

def show_route_schedule():
    """List departures city by city using an outer loop (cities) and inner loop (routes)."""
    print("\n--- ROUTE SCHEDULE BY DEPARTURE CITY ---")
    for city in SUPPORTED_CITIES:  # outer loop: every supported city
        print("\nDepartures from " + city + ":")
        has_departures = False
        for route in routes:  # inner loop: check every route
            if route["departure_city"] == city:
                has_departures = True
                print("  " + route["departure_time"] + "  " + route["route_id"] + "  "
                      + describe_journey(route) + "  " + format_money(route["ticket_price"]))
        if not has_departures:
            print("  No scheduled departures.")


# ---------------------------------------------------------------------------
# MAIN PROGRAM LOOP
# ---------------------------------------------------------------------------

def main():
    """Show the menu again and again until the user chooses Exit (option 8)."""
    show_welcome()

    while True:
        show_menu()
        try:
            choice_text = input("\nEnter your choice (1-9): ").strip()
        except EOFError:
            print("\nNo more input available. Exiting.")
            break

        # Safely convert the choice to a number.
        try:
            choice = int(choice_text)
        except ValueError:
            print("Invalid input: please type a number from the menu (1-9), not text.")
            continue

        if choice == 1:
            view_routes()
        elif choice == 2:
            search_route()
        elif choice == 3:
            book_ticket()
        elif choice == 4:
            view_bookings()
        elif choice == 5:
            cancel_booking()
        elif choice == 6:
            view_seat_availability()
        elif choice == 7:
            generate_report()
        elif choice == 8:
            print("\nThank you for using the Smart Bus system. Goodbye!")
            break  # the exit condition of the menu loop
        elif choice == 9:
            show_route_schedule()
        else:
            print("Invalid choice: " + str(choice) + " is not on the menu. Please choose 1 to 9.")


if __name__ == "__main__":
    main()
