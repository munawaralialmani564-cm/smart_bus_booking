'''Professional Streamlit UI for the Smart Bus Ticket Booking System.

Business data and route definitions remain in main.py. This file provides the UI.
Demo note: bookings are stored in memory and reset when the app process restarts.
'''

import streamlit as st
import main as backend

st.set_page_config(
    page_title="Smart Bus | Ticket Booking",
    page_icon="🚌",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ------------------------------ Visual system ------------------------------
st.markdown(
    '''
    <style>
    :root {
      --navy:#10243a; --navy-2:#173b55; --teal:#0d9488; --teal-2:#0f766e;
      --mint:#dff7f2; --ink:#183044; --muted:#647789; --line:#dfe8ee;
      --paper:#ffffff; --canvas:#f4f7fa; --blue-soft:#eaf2f8;
    }
    .stApp { background:var(--canvas); color:var(--ink); }
    [data-testid="stMainBlockContainer"] { max-width:1500px; padding-top:1.6rem; padding-bottom:2.5rem; }
    [data-testid="stSidebar"] { background:linear-gradient(180deg,#10243a 0%,#173b55 100%); border-right:1px solid #29495e; }
    [data-testid="stSidebar"] * { color:#f5fbff; }
    [data-testid="stSidebar"] [data-testid="stMarkdownContainer"] p { color:#c6d8e3; }
    [data-testid="stSidebar"] hr { border-color:#315166; }
    [data-testid="stSidebar"] [data-testid="stRadio"] label { border-radius:10px; padding:.45rem .55rem; }
    [data-testid="stSidebar"] [data-testid="stRadio"] label:hover { background:rgba(255,255,255,.09); }
    [data-testid="stSidebar"] [data-testid="stRadio"] label p { font-weight:600; }
    h1,h2,h3 { color:var(--navy); letter-spacing:-.025em; }
    h1 { font-size:clamp(1.8rem,3vw,2.5rem)!important; font-weight:820!important; margin-bottom:.25rem!important; }
    h2 { font-size:1.5rem!important; font-weight:780!important; margin-top:1.15rem!important; }
    h3 { font-size:1.12rem!important; font-weight:730!important; }
    p, [data-testid="stCaptionContainer"] { color:var(--muted); }
    .brand-lockup { display:flex; gap:.7rem; align-items:center; margin:.3rem 0 1rem; }
    .brand-mark { width:43px; height:43px; border-radius:13px; background:linear-gradient(135deg,#23c6b7,#0d9488); display:flex; align-items:center; justify-content:center; font-size:1.45rem; box-shadow:0 7px 18px rgba(13,148,136,.25); }
    .brand-name { font-size:1.28rem; font-weight:850; color:white; letter-spacing:-.03em; }
    .brand-sub { font-size:.65rem; letter-spacing:.11em; color:#a9c4d3; font-weight:750; margin-top:.05rem; }
    .hero { position:relative; overflow:hidden; padding:2rem 2.1rem; border-radius:23px; background:linear-gradient(115deg,#10243a 0%,#174b60 58%,#0d9488 100%); color:white; margin-bottom:1.25rem; box-shadow:0 15px 35px rgba(16,36,58,.13); }
    .hero:after { content:""; position:absolute; width:250px; height:250px; right:-60px; top:-120px; border-radius:50%; border:35px solid rgba(255,255,255,.08); }
    .hero-eyebrow { color:#aaf1e8; font-size:.74rem; font-weight:850; letter-spacing:.15em; text-transform:uppercase; margin-bottom:.55rem; }
    .hero h1 { color:white!important; font-size:clamp(2rem,4vw,3rem)!important; margin:0 0 .55rem!important; }
    .hero p { color:#e2f2f5; font-size:1rem; max-width:700px; margin:0; }
    .page-intro { margin-bottom:1.15rem; }
    .eyebrow { color:var(--teal-2); font-size:.72rem; font-weight:850; letter-spacing:.13em; text-transform:uppercase; margin-bottom:.25rem; }
    .subhead { color:var(--muted); margin-top:0; }
    div[data-testid="stMetric"] { background:var(--paper); padding:1rem 1.1rem; border:1px solid var(--line); border-radius:16px; box-shadow:0 5px 18px rgba(16,36,58,.035); }
    [data-testid="stMetricLabel"] { color:var(--muted); font-weight:650; }
    [data-testid="stMetricValue"] { color:var(--navy); font-weight:850; }
    [data-testid="stDataFrame"] { border:1px solid var(--line); border-radius:14px; overflow:hidden; background:white; }
    [data-testid="stForm"] { background:white; border:1px solid var(--line); border-radius:18px; padding:1.25rem 1.35rem; box-shadow:0 7px 24px rgba(16,36,58,.04); }
    [data-testid="stTextInput"] input,[data-testid="stNumberInput"] input,[data-testid="stSelectbox"]>div,[data-testid="stDateInput"] input { border-radius:10px; }
    [data-testid="stTextInput"] input:focus,[data-testid="stNumberInput"] input:focus { border-color:var(--teal); box-shadow:0 0 0 1px var(--teal); }
    div.stButton>button,[data-testid="stFormSubmitButton"] button { border-radius:12px; font-weight:800; padding:.72rem 1rem; min-height:3.2rem; font-size:1rem; transition:all .15s ease; }
    /* Make the main dashboard actions and search CTA easy to notice and click. */
    div[data-testid="stHorizontalBlock"] div.stButton>button { min-height:4rem; font-size:1.08rem; box-shadow:0 5px 14px rgba(16,36,58,.08); }
    [data-testid="stFormSubmitButton"] button { min-height:3.65rem; font-size:1.08rem; letter-spacing:.01em; box-shadow:0 5px 14px rgba(13,148,136,.16); }
    div.stButton>button[kind="primary"],[data-testid="stFormSubmitButton"] button[kind="primary"] { background:linear-gradient(135deg,#0d9488,#0f766e); border:1px solid var(--teal); color:white; }
    div.stButton>button[kind="primary"]:hover,[data-testid="stFormSubmitButton"] button[kind="primary"]:hover { background:#0b6f68; border-color:#0b6f68; transform:translateY(-2px); box-shadow:0 8px 18px rgba(13,148,136,.22); }
    div.stButton>button[kind="secondary"] { background:#ffffff; border:1px solid #b8d0da; color:var(--navy); }
    div[data-testid="stHorizontalBlock"] div.stButton>button[kind="secondary"]:hover { background:#e6f7f4; border-color:var(--teal); color:#0f766e; transform:translateY(-2px); }
    .dashboard-section-title { display:flex; align-items:center; gap:.65rem; padding:.7rem .95rem; margin:.35rem 0 .75rem; border-radius:12px; background:linear-gradient(90deg,#e0f7f3,#f4fbfa); border:1px solid #bce8df; color:#12344a; font-size:1.12rem; font-weight:850; }
    .dashboard-section-title span { display:inline-flex; align-items:center; justify-content:center; width:2rem; height:2rem; border-radius:9px; background:#0d9488; color:white; font-size:1.05rem; }
    .dashboard-search-wrap { border:1px solid #bce8df; border-radius:16px; padding:.3rem; background:linear-gradient(135deg,#ffffff,#f0fbf8); box-shadow:0 7px 22px rgba(13,148,136,.07); }
    [data-testid="stAlert"] { border-radius:12px; }
    [data-testid="stExpander"] { background:white; border:1px solid var(--line); border-radius:13px; margin-bottom:.55rem; }
    [data-testid="stExpander"] summary { font-weight:700; color:var(--navy); }
    .info-card { background:white; border:1px solid var(--line); border-radius:17px; padding:1.1rem 1.15rem; height:100%; box-shadow:0 5px 18px rgba(16,36,58,.035); }
    .info-label { color:var(--muted); font-size:.73rem; text-transform:uppercase; letter-spacing:.09em; font-weight:800; }
    .info-value { color:var(--navy); font-size:1.18rem; font-weight:850; margin:.35rem 0; }
    .info-foot { color:var(--muted); font-size:.84rem; }
    .status { display:inline-block; padding:.28rem .62rem; border-radius:999px; font-size:.75rem; font-weight:800; white-space:nowrap; }
    .status-available { background:#dcfce7; color:#166534; }
    .status-partial { background:#fef3c7; color:#92400e; }
    .status-full { background:#fee2e2; color:#991b1b; }
    .status-confirmed { background:#d1fae5; color:#065f46; }
    .status-cancelled { background:#e2e8f0; color:#475569; }
    .route-card { background:white; border:1px solid var(--line); border-radius:16px; padding:1.05rem; margin:.25rem 0 .7rem; }
    .route-id { font-size:.72rem; letter-spacing:.1em; color:var(--teal-2); font-weight:850; }
    .route-journey { color:var(--navy); font-size:1.08rem; font-weight:850; margin:.25rem 0 .65rem; }
    .route-meta { color:var(--muted); font-size:.86rem; line-height:1.8; }
    .section-rule { border-top:1px solid var(--line); margin:1.3rem 0; }
    .app-footer { text-align:center; color:#8293a0; font-size:.78rem; padding:1.35rem .5rem .15rem; border-top:1px solid var(--line); margin-top:2.2rem; }
    @media(max-width:700px) { .hero{padding:1.45rem}.info-card{margin-bottom:.5rem}[data-testid="stMainBlockContainer"]{padding:1rem .8rem 2rem} }
    </style>
    ''',
    unsafe_allow_html=True,
)

routes = backend.routes
bookings = backend.bookings
PAGES = [
    "Dashboard", "View Routes", "Search Route", "Book a Ticket", "My Bookings",
    "Cancel Booking", "Seat Availability", "Booking Reports", "Route Schedule",
]

if "navigation" not in st.session_state:
    st.session_state.navigation = "Dashboard"
if "last_booking" not in st.session_state:
    st.session_state.last_booking = None

# ------------------------------ Shared helpers ------------------------------
def route_label(route):
    return (f'{route["route_id"]} | {route["departure_city"]} → '
            f'{route["destination_city"]} | {route["departure_time"]} | '
            f'{backend.format_money(route["ticket_price"])}')


def route_table(route_list):
    return [{
        "Route ID": r["route_id"], "From": r["departure_city"],
        "To": r["destination_city"], "Departure": r["departure_time"],
        "Fare / seat": backend.format_money(r["ticket_price"]),
        "Seats available": f'{r["available_seats"]} / {r["total_seats"]}',
        "Status": backend.get_route_status(r),
    } for r in route_list]


def booking_table(booking_list):
    rows = []
    for b in booking_list:
        route = backend.find_route_by_id(b["route_id"])
        journey = backend.describe_journey(route) if route else b["route_id"]
        rows.append({
            "Booking ID": b["booking_id"], "Passenger": b["passenger_name"],
            "Age": b["passenger_age"], "Journey": journey, "Route ID": b["route_id"],
            "Seats": b["seats"], "Total fare": backend.format_money(b["total_fare"]),
            "Status": b["status"],
        })
    return rows


def show_table(rows, empty_message="No records to display."):
    if rows:
        st.dataframe(rows, use_container_width=True, hide_index=True)
    else:
        st.info(empty_message)


def show_route_table(route_list):
    show_table(route_table(route_list), "No routes found. Try another city or route ID.")


def show_booking_table(booking_list):
    show_table(booking_table(booking_list), "No bookings found.")


def page_header(kicker, title, description):
    st.markdown(f'<div class="page-intro"><div class="eyebrow">{kicker}</div><h1>{title}</h1><p class="subhead">{description}</p></div>', unsafe_allow_html=True)


def status_badge(status):
    cls = {
        "Available": "status-available", "Partially Booked": "status-partial",
        "Fully Booked": "status-full", "Confirmed": "status-confirmed",
        "Cancelled": "status-cancelled",
    }.get(status, "status-cancelled")
    st.markdown(f'<span class="status {cls}">{status}</span>', unsafe_allow_html=True)


def go_to(page):
    # Update the radio value before the next run creates that widget.
    st.session_state.navigation_target = page
    st.rerun()

# ------------------------------ Page renderers ------------------------------
def show_dashboard():
    st.markdown('''<div class="hero"><div class="hero-eyebrow">Smart travel · Simple booking</div>
      <h1>Your journey, made simple.</h1><p>Discover routes, reserve your seats, and keep every trip organized from one easy dashboard.</p></div>''', unsafe_allow_html=True)

    confirmed = [b for b in bookings if b["status"] == "Confirmed"]
    cancelled = [b for b in bookings if b["status"] == "Cancelled"]
    seats = sum(r["available_seats"] for r in routes)
    revenue = sum(b["total_fare"] for b in confirmed)
    c = st.columns(4)
    c[0].metric("Bus routes", len(routes))
    c[1].metric("Confirmed bookings", len(confirmed))
    c[2].metric("Seats available", seats)
    c[3].metric("Confirmed revenue", backend.format_money(revenue))

    st.markdown('<div class="dashboard-section-title"><span>↗</span> Start your journey</div>', unsafe_allow_html=True)
    with st.container(border=True):
        actions = st.columns(3, gap="medium")
        if actions[0].button("🎟️  BOOK A TICKET", type="primary", use_container_width=True): go_to("Book a Ticket")
        if actions[1].button("🔎  FIND A ROUTE", use_container_width=True): go_to("Search Route")
        if actions[2].button("💺  CHECK SEATS", use_container_width=True): go_to("Seat Availability")

    st.markdown('<div class="dashboard-section-title"><span>⌕</span> Find your bus</div>', unsafe_allow_html=True)
    with st.container(border=True):
        with st.form("dashboard_search_form"):
            search_cols = st.columns([1, 1, 1, .7])
            with search_cols[0]: home_origin = st.selectbox("From", ["Any city"] + list(backend.SUPPORTED_CITIES), key="home_origin")
            with search_cols[1]: home_destination = st.selectbox("To", ["Any city"] + list(backend.SUPPORTED_CITIES), key="home_destination")
            with search_cols[2]: travel_date = st.date_input("Travel date (demo preview only)", key="home_travel_date")
            with search_cols[3]: requested_seats = st.number_input("Seats", min_value=1, max_value=10, value=1, step=1, key="home_seat_count")
            search_home = st.form_submit_button("🔎  SEARCH BUSES", type="primary", use_container_width=True)
        st.caption("The timetable is fixed sample data. The selected date is for preview only; it does not change departure schedules.")
    if search_home:
        if home_origin != "Any city" and home_destination != "Any city" and home_origin == home_destination:
            st.session_state.dashboard_search_results = []
            st.error("Choose two different cities for your journey.")
        else:
            matches = [r for r in routes
                       if (home_origin == "Any city" or r["departure_city"] == home_origin)
                       and (home_destination == "Any city" or r["destination_city"] == home_destination)
                       and r["available_seats"] >= int(requested_seats)]
            st.session_state.dashboard_search_results = [r["route_id"] for r in matches]
    if "dashboard_search_results" in st.session_state:
        result_routes = [r for r in routes if r["route_id"] in st.session_state.dashboard_search_results]
        st.markdown(f"#### Search results · {len(result_routes)} route(s)")
        if result_routes:
            for result_route in result_routes:
                with st.container(border=True):
                    left, middle, right = st.columns([2, 2, 1])
                    with left:
                        st.markdown(f'**{result_route["departure_city"]} → {result_route["destination_city"]}**')
                        st.caption(f'{result_route["route_id"]} · {result_route["departure_time"]}')
                    with middle:
                        st.markdown(f'**{backend.format_money(result_route["ticket_price"])} / seat**')
                        st.caption(f'{result_route["available_seats"]}/{result_route["total_seats"]} seats available')
                    with right:
                        if st.button("Book route", type="primary", key=f'home_book_{result_route["route_id"]}', use_container_width=True):
                            st.session_state.preselected_route = result_route["route_id"]
                            go_to("Book a Ticket")
        else:
            st.info("No routes found for these cities and seat requirements. Try different search options.")

    st.markdown("### Featured routes")
    cards = st.columns(2)
    for idx, route in enumerate(routes[:4]):
        with cards[idx % 2]:
            st.markdown(f'''<div class="route-card"><div class="route-id">{route["route_id"]} · INTERCITY ROUTE</div>
            <div class="route-journey">{route["departure_city"]} <span style="color:#0d9488">→</span> {route["destination_city"]}</div>
            <div class="route-meta">🕒 {route["departure_time"]}<br>💺 {route["available_seats"]} of {route["total_seats"]} seats available<br>💳 {backend.format_money(route["ticket_price"])} per seat</div></div>''', unsafe_allow_html=True)
            status_badge(backend.get_route_status(route))
    st.caption(f"Booking history: {len(bookings)} total · {len(cancelled)} cancelled. Demo data resets when the app process restarts.")


def show_routes():
    page_header("TRAVEL OPTIONS", "Bus routes", "Compare journeys, departure times, fares, and available seats.")
    left, right = st.columns([1, 1])
    with left: origin = st.selectbox("Filter by departure city", ["All cities"] + list(backend.SUPPORTED_CITIES), key="routes_origin")
    with right: destination = st.selectbox("Filter by destination", ["All cities"] + list(backend.SUPPORTED_CITIES), key="routes_destination")
    filtered = [r for r in routes if (origin == "All cities" or r["departure_city"] == origin) and (destination == "All cities" or r["destination_city"] == destination)]
    show_route_table(filtered)


def show_route_search():
    page_header("FIND YOUR JOURNEY", "Search routes", "Search by route ID or city. City and route matching is case-insensitive.")
    with st.container(border=True):
        a, b, c = st.columns([1, 1, 1])
        with a: origin = st.selectbox("From", ["Any city"] + list(backend.SUPPORTED_CITIES), key="search_origin")
        with b: destination = st.selectbox("To", ["Any city"] + list(backend.SUPPORTED_CITIES), key="search_destination")
        with c: route_id = st.text_input("Route ID (optional)", placeholder="e.g. r101", key="search_route_id").strip().upper()
    matches = [r for r in routes if (origin == "Any city" or r["departure_city"].casefold() == origin.casefold()) and (destination == "Any city" or r["destination_city"].casefold() == destination.casefold()) and (not route_id or r["route_id"].casefold() == route_id.casefold())]
    st.markdown(f"### {len(matches)} route(s) found")
    show_route_table(matches)
    if matches and st.button("Continue to booking", type="primary"):
        st.session_state.preselected_route = matches[0]["route_id"]
        go_to("Book a Ticket")


def show_confirmation(booking):
    route = backend.find_route_by_id(booking["route_id"])
    if not route: return
    st.success("Booking confirmed! Your reservation has been created.")
    st.markdown("### Booking confirmation")
    st.markdown(f'''<div class="route-card"><div class="route-id">BOOKING REFERENCE</div><div class="route-journey">{booking["booking_id"]}</div>
      <div class="route-meta">Passenger: <b>{booking["passenger_name"]}</b> · Age: {booking["passenger_age"]}<br>
      Journey: <b>{backend.describe_journey(route)}</b><br>Route: {route["route_id"]} · Departure: {route["departure_time"]}<br>
      Seats: {booking["seats"]} · Fare per seat: {backend.format_money(route["ticket_price"])}<br>
      Total fare: <b>{backend.format_money(booking["total_fare"])}</b></div></div>''', unsafe_allow_html=True)
    status_badge(booking["status"])
    st.warning("Keep your booking ID safe. It is needed if you want to cancel this reservation.")
    a, b = st.columns(2)
    if a.button("View my bookings", type="primary", use_container_width=True): go_to("My Bookings")
    if b.button("Back to routes", use_container_width=True): go_to("View Routes")


def show_book_ticket():
    page_header("RESERVE YOUR SEAT", "Book a ticket", "Add passenger details, select a route, and confirm your booking.")
    if not routes:
        st.warning("No routes are available for booking."); return

    preselected = st.session_state.pop("preselected_route", None)
    route_ids = [r["route_id"] for r in routes]
    default_index = route_ids.index(preselected) if preselected in route_ids else 0
    route_options = {route_label(r): r for r in routes}
    labels = list(route_options)
    default_label = next((lab for lab, r in route_options.items() if r["route_id"] == preselected), labels[default_index if default_index < len(labels) else 0])

    with st.form("booking_form", clear_on_submit=False):
        passenger_name = st.text_input("Passenger full name", placeholder="Enter passenger's full name")
        age = st.number_input("Passenger age", min_value=1, max_value=120, value=18, step=1)
        selected_label = st.selectbox("Choose bus route", labels, index=labels.index(default_label))
        selected_route = route_options[selected_label]
        seats_available = selected_route["available_seats"]
        price = selected_route["ticket_price"]
        st.info(f'**{backend.describe_journey(selected_route)}** · {selected_route["departure_time"]} · {seats_available}/{selected_route["total_seats"]} seats available · {backend.format_money(price)} per seat')
        seat_count = st.number_input("Number of seats", min_value=1, max_value=max(1, selected_route["total_seats"]), value=1, step=1)
        st.markdown(f"**Estimated total fare:** {backend.format_money(price * int(seat_count))}")
        if seats_available == 0:
            st.error("This route is fully booked. Choose another route.")
        submitted = st.form_submit_button("Confirm booking", type="primary", use_container_width=True, disabled=(seats_available == 0))

    if submitted:
        if not passenger_name.strip():
            st.error("Please enter the passenger's full name. No booking was created.")
        elif int(seat_count) > selected_route["available_seats"]:
            st.error(f'Only {selected_route["available_seats"]} seat(s) are available. No booking was created.')
        else:
            booking_id = backend.generate_booking_id()
            booking = {
                "booking_id": booking_id,
                "passenger_name": passenger_name.strip(),
                "passenger_age": int(age),
                "route_id": selected_route["route_id"],
                "seats": int(seat_count),
                "total_fare": price * int(seat_count),
                "status": "Confirmed",
            }
            bookings.append(booking)
            selected_route["available_seats"] -= int(seat_count)
            st.session_state.last_booking = booking.copy()
            st.rerun()

    last = st.session_state.last_booking
    if last and last.get("status") == "Confirmed":
        show_confirmation(last)


def show_my_bookings():
    page_header("YOUR RESERVATIONS", "My bookings", "Review booking history. Cancelled records remain visible for reference.")
    if not bookings:
        st.info("No bookings found. Your confirmed reservations will appear here.")
        if st.button("Book your first ticket", type="primary"): go_to("Book a Ticket")
        return
    status_filter = st.selectbox("Filter bookings by status", ["All bookings", "Confirmed", "Cancelled"])
    filtered = bookings if status_filter == "All bookings" else [b for b in bookings if b["status"] == status_filter]
    show_booking_table(filtered)
    if any(b["status"] == "Confirmed" for b in filtered):
        st.caption("Only confirmed bookings can be cancelled.")
        if st.button("Go to cancellation", type="primary"): go_to("Cancel Booking")


def show_cancel_booking():
    page_header("MANAGE RESERVATION", "Cancel a booking", "Cancellation restores the reserved seats and keeps the booking in your history.")
    confirmed = [b for b in bookings if b["status"] == "Confirmed"]
    if not confirmed:
        st.info("There are no confirmed bookings to cancel.")
        if bookings: st.caption("Previously cancelled bookings remain in My Bookings and cannot be cancelled again.")
        return
    options = {f'{b["booking_id"]} — {b["passenger_name"]} — {b["route_id"]} — {b["seats"]} seat(s)': b for b in confirmed}
    with st.form("cancel_form"):
        selected_label = st.selectbox("Select a confirmed booking", list(options))
        booking = options[selected_label]
        route = backend.find_route_by_id(booking["route_id"])
        st.info(f'**{booking["booking_id"]}** · {booking["passenger_name"]} · {backend.describe_journey(route) if route else booking["route_id"]} · {booking["seats"]} seat(s) · {backend.format_money(booking["total_fare"])}')
        confirm = st.checkbox("I understand this will cancel the selected booking.")
        submitted = st.form_submit_button("Confirm cancellation", type="primary", use_container_width=True)
    if submitted:
        if not confirm:
            st.error("Please tick the confirmation box before cancelling.")
        elif booking["status"] != "Confirmed":
            st.error("This booking has already been cancelled. No seats were restored again.")
        elif route is None:
            st.error("The route could not be found. No changes were made.")
        else:
            route["available_seats"] = min(route["total_seats"], route["available_seats"] + booking["seats"])
            booking["status"] = "Cancelled"
            if st.session_state.last_booking and st.session_state.last_booking.get("booking_id") == booking["booking_id"]:
                st.session_state.last_booking = booking.copy()
            st.success(f'{booking["booking_id"]} has been cancelled. {booking["seats"]} seat(s) restored to {route["route_id"]}.')
            status_badge("Cancelled")


def show_seat_availability():
    page_header("LIVE IN THIS DEMO", "Seat availability", "See the remaining capacity for every route. Availability updates after booking or cancellation.")
    only_available = st.toggle("Show only routes with available seats", value=False)
    visible = [r for r in routes if not only_available or r["available_seats"] > 0]
    if not visible:
        st.warning("No routes currently have seats available."); return
    for route in visible:
        with st.container(border=True):
            left, middle, right = st.columns([2, 2, 1])
            with left:
                st.markdown(f'**{route["route_id"]} · {route["departure_city"]} → {route["destination_city"]}**')
                st.caption(f'{route["departure_time"]} · {backend.format_money(route["ticket_price"])} per seat')
            with middle:
                st.markdown(f'**{route["available_seats"]} / {route["total_seats"]} seats available**')
                st.progress(route["available_seats"] / route["total_seats"] if route["total_seats"] else 0)
            with right:
                status_badge(backend.get_route_status(route))


def show_booking_reports():
    page_header("OPERATIONS OVERVIEW", "Booking reports", "A summary calculated from actual bookings and current route capacity.")
    confirmed = [b for b in bookings if b["status"] == "Confirmed"]
    cancelled = [b for b in bookings if b["status"] == "Cancelled"]
    revenue = sum(b["total_fare"] for b in confirmed)
    seats_reserved = sum(b["seats"] for b in confirmed)
    fully_booked = sum(r["available_seats"] == 0 for r in routes)
    c = st.columns(3)
    c[0].metric("Total bookings", len(bookings))
    c[1].metric("Confirmed bookings", len(confirmed))
    c[2].metric("Cancelled bookings", len(cancelled))
    d = st.columns(3)
    d[0].metric("Seats currently reserved", seats_reserved)
    d[1].metric("Confirmed revenue", backend.format_money(revenue))
    d[2].metric("Fully booked routes", fully_booked)
    st.caption("Confirmed revenue and reserved seats exclude cancelled bookings. Totals update with each booking action.")
    if not bookings:
        st.info("No bookings have been created yet. Booking totals, reserved seats, and confirmed revenue are zero.")
    rows = []
    for route in routes:
        route_bookings = [b for b in confirmed if b["route_id"] == route["route_id"]]
        rows.append({
            "Route ID": route["route_id"], "Journey": backend.describe_journey(route),
            "Confirmed bookings": len(route_bookings), "Seats reserved": sum(b["seats"] for b in route_bookings),
            "Confirmed revenue": backend.format_money(sum(b["total_fare"] for b in route_bookings)),
            "Seats available": f'{route["available_seats"]}/{route["total_seats"]}',
        })
    st.markdown("### Route-wise breakdown")
    show_table(rows)


def show_route_schedule():
    page_header("DEPARTURE PLANNER", "Route schedule", "Browse the fixed sample timetable by departure city.")
    for city in backend.SUPPORTED_CITIES:
        city_routes = [r for r in routes if r["departure_city"] == city]
        with st.expander(f"📍 Departures from {city} · {len(city_routes)} route(s)", expanded=True):
            if city_routes:
                show_table([{"Route ID": r["route_id"], "Destination": r["destination_city"], "Departure": r["departure_time"], "Fare / seat": backend.format_money(r["ticket_price"]), "Seats available": f'{r["available_seats"]}/{r["total_seats"]}', "Status": backend.get_route_status(r)} for r in city_routes])
            else:
                st.info("No scheduled departures.")

# ------------------------------ Navigation ------------------------------
# Apply page changes before the keyed navigation widget is created.
if "navigation_target" in st.session_state:
    st.session_state.navigation = st.session_state.pop("navigation_target")

st.sidebar.markdown('''<div class="brand-lockup"><div class="brand-mark">🚌</div><div><div class="brand-name">Smart Bus</div><div class="brand-sub">TICKET BOOKING SYSTEM</div></div></div>''', unsafe_allow_html=True)
st.sidebar.markdown("Navigate your travel workspace")
st.sidebar.divider()
st.sidebar.markdown('<div style="font-size:.69rem;font-weight:850;letter-spacing:.14em;color:#91b5c5;margin:0 0 .35rem">WORKSPACE</div>', unsafe_allow_html=True)
st.sidebar.radio("Navigation", PAGES, key="navigation", label_visibility="collapsed")
st.sidebar.divider()
st.sidebar.markdown('''<div style="padding:.8rem;background:rgba(255,255,255,.07);border:1px solid rgba(255,255,255,.12);border-radius:12px;font-size:.78rem;line-height:1.6"><b style="color:#aaf1e8">DEMO MODE</b><br/>Bookings are kept in memory. Data resets when the app process restarts.</div>''', unsafe_allow_html=True)
st.sidebar.caption("Built with Python + Streamlit")

renderers = {
    "Dashboard": show_dashboard, "View Routes": show_routes, "Search Route": show_route_search,
    "Book a Ticket": show_book_ticket, "My Bookings": show_my_bookings,
    "Cancel Booking": show_cancel_booking, "Seat Availability": show_seat_availability,
    "Booking Reports": show_booking_reports, "Route Schedule": show_route_schedule,
}
renderers[st.session_state.navigation]()
st.markdown('<div class="app-footer">SMART BUS · TICKET BOOKING & RESERVATION SYSTEM<br>Designed for clear, reliable demo workflows</div>', unsafe_allow_html=True)
