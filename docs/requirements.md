# BankQ requirements

**Setting:** Bank branch, weekday afternoons
**People who wait:** Jill Royce, a 3rd-year student who joins from her phone (see [docs/week3/personas.md](week3/personas.md))
**People who serve:** Isabella Roberts, a teller at Counter 2 (see [docs/week3/personas.md](week3/personas.md))

**Problem statement:** A student with back-to-back classes needs a way to join the bank queue from her phone and know when it is her turn without waiting at the branch, because she can't tell how long the wait will be and is afraid of missing her number and having to start over. A teller needs a way to see exactly who is next and move the line quickly, because customers who don't come back when called slow everyone down.

## Functional requirements

| ID | Requirement | Priority | Stores data? | Status |
| --- | --- | --- | --- | --- |
| FR-01 | A customer can join the queue by choosing a service and entering their name and email. | Must | Yes | Built (Week 3) |
| FR-02 | A customer can see their ticket number, status and how many people are ahead of them. | Must | Yes | Built (Week 3) |
| FR-03 | A staff member can call the next waiting ticket, once the current called ticket has been marked served or no-show. | Must | Yes | Built (Week 3) |
| FR-04 | A staff member can mark a called ticket as served or no-show. | Must | Yes | Built (Week 3) |
| FR-05 | A customer can leave the queue before being called. | Must | Yes | Built (Week 3) |
| FR-06 | A staff member can add, rename and switch off a service. | Must | Yes | This week |
| FR-07 | A staff member can see how many people left before being served, per service, per day. | Should | Yes | Later |
| FR-08 ★ | A senior citizen, a pregnant person or a person with a disability can join a priority lane that is served first. | Should | Yes | Later |
| FR-09 | A customer can switch the page to a larger text size. | Could | No | Later |
| FR-10 | A customer is alerted on the page, with a banner, sound and vibration, when they are within 3 places of the front or when they are called. | Must | No | Built (Week 3) |
| FR-11 | A customer's page updates its status, position and queue list by itself, without a reload, within 5 seconds of a change. | Must | No | Built (Week 3) |
| FR-12 | A staff member can see the waiting and called tickets in order, and filter them by service. | Must | No | Built (Week 3) |
| FR-13 ★ | A customer is told which counter to go to when their ticket is called. | Should | Yes | Later |
| FR-14 ★ | A staff member sees only the waiting tickets for the services their counter handles. | Should | Yes | Later |
| FR-15 ★ | A customer is told which documents to bring (for example a valid ID for account opening) before they join. | Could | Yes | Later |
| FR-16 | Tickets and their status are kept when the server restarts. | Must | Yes | This week |
| FR-17 | A staff member can undo a ticket marked no-show by mistake. | Should | Yes | Later |
| FR-18 | A customer gets an alert while their phone screen is locked or the page is closed. | Won't (this semester) | Yes | Later |

★ = specific to a bank branch.



## Non-functional requirements

| ID | Requirement | Category | Priority |
| --- | --- | --- | --- |
| NFR-01 | No ticket is lost when the server or the database restarts. | Reliability | Must |
| NFR-02 | Two people can never get the same ticket number, even if they join at the same moment. | Data integrity | Must |
| NFR-03 | My place loads in under 2 seconds on mobile data. | Performance | Should |
| NFR-04 | Every screen scores 90 or higher in the Lighthouse accessibility check. | Accessibility | Must |
| NFR-05 | No password or secret key is stored in the repository. | Security | Must |
| NFR-06 | A customer's status, position and queue list on My place match the staff dashboard within 5 seconds of a change. | Consistency | Should |
| NFR-07 | The queue list shown to customers never includes other people's names or emails. | Privacy | Must |

## MVP

**MVP:** FR-01, FR-02, FR-03, FR-04, FR-05, FR-06, FR-10, FR-11, FR-12, FR-16, and NFR-01, NFR-02, NFR-04, NFR-05, NFR-07.

This is the smallest version that still solves the problem: a customer can join from her phone, see her place, and be alerted without waiting at the branch, and a teller can call, serve or no-show tickets in order. The data requirements (FR-16, NFR-01, NFR-02) are included because a queue that loses tickets on restart can't be trusted.

**Out of scope (this semester):**

- **Alerts when the screen is locked or the page is closed (FR-18):** This requires push notifications and a service worker, which is more than what we're including. The alert only functions when the page is open.
- **Sending email or text messages:** The app asks for an email. Sending messages requires an external service and more security work so it is not in the MVP
- **Multiple branches:** The app is for one branch, with its counters.

## Check with a real person

| Who (role only) | What they said | What I changed |
| --- | --- | --- |
| Bank Customer | "Kapoy jod ug hulat sa banko, dugay kaayo ko matawag samot kung daghan tao. Dili ko makabantay nga hapit na diay akong number dayon." | [e.g. Added FR-19 (Should)] |
| | | |