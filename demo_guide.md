# Smart Bus Project: Demonstration Guide (Roman Urdu)

Yeh guide Python beginner ke liye hai. Isse aap `main.py` ko step by step samajh kar viva ya demo me explain kar sakte ho.

---

## 1. Program ka basic flow

1. Program start hota hai aur `main()` function chalta hai.
2. Pehle welcome screen (`show_welcome()`) dikhti hai.
3. Phir `while True:` loop me menu (`show_menu()`) bar bar dikhta hai.
4. User number likhta hai (1 se 9). Program `if / elif / else` se sahi function chalata hai.
5. Har kaam ke baad menu dobara aata hai.
6. Jab user **8** likhta hai to `break` chalta hai, loop khatam hota hai aur program band ho jata hai.

**Galat input:** agar user `abc` likhe to `int()` error deta hai. Hum usko `try / except ValueError` se pakarte hain, "Invalid input" likhte hain aur `continue` se menu par wapas jate hain. Agar number 0 ya 10 ho to `else` wala hissa "Invalid choice" dikhata hai. Program crash nahi hota.

**Menu numbering:** PRD ke 1 se 8 options wese hi hain (8 = Exit). Schedule wali feature ko **9** par rakha taake koi purana number na badle.

---

## 2. Data structures (data kahan rakha hai)

| Cheez | Python type | Kyun |
|-------|-------------|------|
| `routes` | **list of dictionaries** | Har route ek dictionary hai (`route_id`, `departure_city`, `destination_city`, `departure_time`, `ticket_price`, `total_seats`, `available_seats`). List me 5 routes hain. |
| `bookings` | **list of dictionaries** | Har booking ek dictionary hai (`booking_id`, `passenger_name`, `passenger_age`, `route_id`, `seats`, `total_fare`, `status`). Cancelled bookings bhi isi list me rehti hain. |
| `SUPPORTED_CITIES` | **tuple** | Shehron ki list kabhi badalti nahi, isliye tuple. |
| `issued_booking_ids` | **set** | Set me duplicate nahi ho sakta. Naya ID banane se pehle check hota hai ke woh pehle use to nahi hua. |

Data sirf **memory** me hai. Program band hote hi sab bookings khatam. Yeh PRD ke mutabiq hai.

---

## 3. Important functions aur woh kya karte hain

**`format_money(amount)`**: 2400 ko `Rs. 2,400` bana deta hai.

**`describe_journey(route)`**: `Karachi -> Hyderabad` jese text banata hai.

**`parse_positive_int(text)`**: Text ko safely number banata hai. Agar text number nahi hai (`abc`, `2.5`, khali) ya number 0 / negative hai to `None` wapas karta hai. Age aur seats dono isi se check hote hain.

**`find_route_by_id(route_id)`**: Routes me loop chalata hai aur route dhoondta hai. Na mile to `None`.

**`get_route_status(route)`**:
- seats 0 hon to **Fully Booked**
- available = total ho to **Available**
- warna **Partially Booked**

**`generate_booking_id()`**: `B1001`, `B1002`... banata hai. ID ko set me add karne se pehle check karta hai ke woh set me pehle se to nahi (BR-06).

**`view_routes()`**: Pehle user se poochta hai "sirf available routes?" Agar haan to `continue` se fully booked routes skip hote hain. Phir `enumerate()` se 1, 2, 3... number laga kar table print hoti hai.

**`search_route()`**: Input ko `lower()` karta hai taake `Karachi`, `karachi`, `KARACHI` sab chalein.
- Pehle route ID check hota hai. Route ID unique hai, isliye match milte hi `break`.
- Agar loop bina `break` ke khatam ho (**for-else**), matlab yeh route ID nahi tha. Tab city search hoti hai jo **sab** matching routes dikhati hai (yahan `break` nahi, warna pehle match par ruk jata).
- Agar kuch na mile to "No route found" ka message.

**`book_ticket()`**: Neeche section 4 me detail hai.

**`view_bookings()`**: Agar list khali hai to "No bookings found." Warna `enumerate()` se saari bookings (cancelled bhi) dikhati hai.

**`cancel_booking()`**: Neeche section 5 me detail hai.

**`view_seat_availability()`**: Har route ke available aur total seats aur status dikhata hai. Filter me `continue` use hota hai.

**`generate_report()`**: Neeche section 6 me detail hai.

**`show_route_schedule()`**: **Nested loop**. Bahar wala loop har shehar par chalta hai, andar wala loop sab routes check karta hai. Agar kisi shehar se koi route na jaye (Mirpur Khas, Lahore) to "No scheduled departures."

---

## 4. Booking kese hoti hai (validation aur seats)

Order me ye checks hote hain:

1. **Name**: `strip()` ke baad khali ho to reject (BR-01).
2. **Age**: `parse_positive_int` se. Text, 0, negative reject (BR-02).
3. **Route ID**: `upper()` karke route dhoondte hain. Na mile to reject (BR-03).
4. **Seats**: positive integer hona chahiye (BR-04).
5. **Availability**: `seats > available_seats` ho to reject (BR-05).

Agar **koi bhi** check fail ho to function `return` kar deta hai. Is waqt tak na booking bani, na seats change hui. Yehi sab se zaroori rule hai.

Jab **saare checks pass** ho jayen, tab hi:
- `total_fare = ticket_price * seats` (BR-07)
- `generate_booking_id()` se ID
- booking dictionary banti hai, status `"Confirmed"`
- `bookings.append(booking)`
- `route["available_seats"] -= seats` ek hi dafa (BR-08)

**Misaal:** R101 ka fare Rs. 1200 hai. Ahmed 2 seats book kare to total fare = 1200 x 2 = **Rs. 2,400**. R101 ki available seats 40 se 38 ho jati hain.

---

## 5. Cancellation kese hoti hai

1. User booking ID likhta hai (`B1001`). Hum `upper()` karte hain.
2. `for` loop se bookings me wohi ID dhoondte hain.
3. **Agar mil gayi:**
   - Status `"Confirmed"` ho to: route dhoondo, `seats_to_restore = booking["seats"]` lo, route ki available seats me wohi seats wapas jodo, aur **usi jagah** status `"Cancelled"` kar do. Seats wapas karna aur status badalna ek saath hota hai (ek logical operation). Booking record delete nahi hota (BR-11).
   - Status pehle se `"Cancelled"` ho to: error dikhao, **seats mat badlo**. Isi wajah se seats do dafa wapas nahi aa sakti (BR-10).
   - Dono surat me `break`.
4. **Agar nahi mili:** loop bina `break` ke khatam hota hai, to **for-else** ka `else` chalta hai aur "no booking found" ka error aata hai. Kuch change nahi hota.

**Misaal:** R101 par 2 seats book (38 bachi). Cancel karne par 2 seats wapas, ab 40. Dobara cancel karo to refuse hota hai aur seats 40 hi rehti hain (42 nahi hoti).

---

## 6. Report kese calculate hoti hai

1. Ek loop bookings par: total, confirmed aur cancelled gine jate hain. Total me cancelled bhi shamil hain.
2. **Nested loop**: bahar wala loop routes par, andar wala loop bookings par. Andar `continue` se wo bookings skip hoti hain jo dusre route ki hon ya cancelled hon. Sirf **Confirmed** bookings ki seats aur fare jodte hain. Is wajah se cancelled fare revenue me nahi aata (BR-12).
3. Fully booked routes: wo routes jinki `available_seats == 0` (yeh current route data se aata hai, chahe bookings na hon).
4. Aakhir me **reconciliation check**: report ki "reserved seats" ko routes ki (total - available) se mila kar dekhte hain. Agar barabar hon to "OK".

**Misaal:** Ahmed ne R101 par 2 seats liye (Rs. 2,400), Sara ne R102 par 3 seats liye (Rs. 6,000), phir Ahmed ki booking cancel hui. Report: total 2, confirmed 1, cancelled 1, reserved seats 3, revenue **Rs. 6,000**.

---

## 7. Python concepts kahan use hue

| Concept | Kahan |
|---------|-------|
| `print()` / `input()` | Har function |
| list, dictionary, tuple, set | `routes`, `bookings`, `SUPPORTED_CITIES`, `issued_booking_ids` |
| `if / elif / else`, nested conditions | `main()`, `book_ticket()`, `cancel_booking()` |
| `for` aur nested `for` | `generate_report()`, `show_route_schedule()` |
| `while` | `main()` ka menu loop |
| `enumerate()` | `view_routes()`, `view_bookings()`, `view_seat_availability()` |
| for-else | `search_route()`, `cancel_booking()` |
| `break` | route ID search, cancel, menu exit |
| `continue` | available-only filter, report loop, galat menu input |
| `try / except` | `parse_positive_int()`, menu choice |

---

## 8. Demo kese dikhayen (5 minute)

1. `python main.py` chalao, menu dikhao.
2. **1**: sab 5 routes. **2**: `Hyderabad` search (3 routes), phir `Atlantis` (no match).
3. **3**: Ahmed, 25, R101, 2 seats. Rs. 2,400 aur ID B1001 dikhao.
4. **3** me galat cheezein try karo: khali naam, age `abc`, route `R999`, seats `0`, seats `41`. Har dafa "NOT created" aaye. Phir **6** se dikhao ke seats change nahi hui.
5. **6**: R101 par 38 seats, Partially Booked.
6. **5**: B1001 cancel. **5** dobara: refuse. **6**: seats wapas 40.
7. **9**: schedule (Mirpur Khas aur Lahore par "No scheduled departures.").
8. **7**: report. **8**: exit.

Viva me yeh point zaroor bolna: "Seats sirf tab ghatti hain jab saari validation pass ho jaye, aur cancel par sirf ek dafa wapas aati hain, kyunki status Confirmed se Cancelled hone ke baad dobara cancel nahi ho sakta."
