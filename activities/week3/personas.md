## Jill Royce, the waiting person
> "“Two hours just to open an account. I could have finished my whole day’s work.”"

| | |
| --- | --- |
| **Photo or sketch** | ![Jill Royce](Jill-Royce.jpg) |
| **Age, role and background** | 21 years old, a 3rd-year business student, has back-to-back classes, has organizational duties.|
| **Goals** | She wants to join the queue while she is studying for her classes, she wants to work her duties as an organization member instead of being stuck on the bank waiting for her number to be called. |
| **Frustrations** | She doesn't know how long the wait will be, so she can't plan her other responsibilities around it. She also worries that if she steps away to go to class, she will miss her number and will get another number again. |
| **Devices and context** | She uses a smart phone, and her laptop for school. She uses her phone more and often on mobile data or campus WI-FI. She joins the queue on the way to the bank or from campus, she might also be studying while waiting for her queue. She checks her phone between tasks.  |
| **Tech comfort** | High, she uses online banking, e-wallets, and almost all social medias. She expects pages to load fast, work on mobile, and update by themselves. She knows her way around when using applications. |
| **Accessibility needs** | She needs light pages that load on mobile data, she also needs to be alerted by notification either by sound or haptic in-case she is studying, or doing other duties.|

### Scenario

Thursday afternoon. Jill is in between her 2hr long econometrics class and a meeting for an organization. She needs to go to the bank to open a new savings account (a personal appearance is required with a valid ID, so she can get her org allowance), but she can’t afford to be waiting in the bank during the 2hr gap. She leaves class.Opening the BankQ on her phone she selects Account opening, gives her name & email. Gets assigned ticket #14. She needs to know how long will she need to wait. She checks her position. 3rd in line. There are two others waiting for a new account. She goes to a cafe close to the branch. Meanwhile she continues to work on her org's budget report. Occasionally she glances at her phone between paragraphs and the page refreshes by itself. She sees "You're almost up". She then packs her laptop and goes back. Her number is called. The page instructs her to go to counter 2. She completes the application process. Makes it just in time for the meeting.

### Top tasks in the app

| Task | Screen | Requirement ID |
| --- | --- | --- |
| Join the queue by choosing a bank service (e.g. Account opening) | Join | FR-01 |
| Check my position and how many people are ahead | My place | FR-02 |
| See which counter to go to once I’m called | My place| FR-02|
|Get alerted when I’m near the front (position 3 or less)|My place| FR-02|
| See the waiting tickets my counter can serve| Staff dashboard|FR-02|
|Call the next customer to my counter| Staff dashboard| FR-04
### What this means for my interface

1. Because Jill wants to study and do org work instead of sitting in the branch, my interface must let her join in a few taps on her phone and show her position in large, glanceable text.
2. Because Jill steps away and glances at her phone between tasks, my interface must update on its own and show a clear “You’re almost up” alert when she is almost at the front of the queue.
3.Because Jill often works on mobile data and may be studying or doing org work with her phone out of sight, my interface must load as a light, text-first page and alert her with a sound or vibration when she is near the front or called.


## Isabella Roberts, the bank teller
> "I call a number and half the time nobody comes, and the whole line just sits there waiting on me."

| | |
| --- | --- |
| **Photo or sketch** | ![Isabella Roberts](Isabella-Roberts.jpg) |
| **Age, role and background** | 36 years old, a teller at Counter 2 with several years of experience at the branch. She handles deposits and account opening and serves customers one after another all day. |
| **Goals** | She wants to know exactly who is next for the services her counter handles, so she can call them quickly and keep her line moving. She wants to spend her time serving customers, not answering "how much longer?" or hunting for the next ticket. |
| **Frustrations** | Customers who step away and don't return when called waste her time and slow the whole line. She often doesn't know who is next when tickets for different services are mixed together. Customers also crowd her counter and ask about their turn while she is in the middle of a transaction. |
| **Devices and context** | A desktop computer with a mouse and a standard monitor at Counter 2. She sits there most of the day with a customer in front of her, glancing at the dashboard for a few seconds between transactions. She can't read long screens or fill in forms mid-rush. |
| **Tech comfort** | Medium to high. She uses the bank's internal systems daily and picks up new tools quickly, but she has no patience for anything that takes more than one or two clicks during a busy period. |
| **Accessibility needs** | She needs a glanceable layout, with ticket number, service, and status readable in a second from normal sitting distance. She needs large, obvious buttons that are easy to hit quickly with a mouse. Statuses must use words ("Waiting," "Called," "Served," "No-show"), not only color, and she should have to type almost nothing. |

### Scenario

It's mid-afternoon at the branch, and Isabella has just finished with a customer at Counter 2. She needs to know who is next without searching through papers or asking around. She glances at the BankQ staff dashboard and sees the waiting tickets her counter can serve, in order: #11 for Deposit / Withdrawal, then #12 for Account opening. She clicks the call next button, and ticket #11 changes to "called" at Counter 2 while the customer's phone tells them to proceed to her counter. The customer arrives, she serves them, and she marks the ticket served. When a called customer doesn't show up, she marks the ticket no-show and calls the next person, so her line keeps moving.

### Top tasks in the app

| Task | Screen | Requirement ID |
| --- | --- | --- |
| See the waiting tickets my counter can serve, in order | Staff dashboard | FR-04 |
| Call the next customer to my counter | Staff dashboard | FR-05 |
| Mark a called customer as served (planned) | Staff dashboard | FR-07 |
| Mark a called customer as no-show (planned) | Staff dashboard | FR-08 |

### What this means for my interface

1. Because Isabella has only a few seconds between customers and often has someone in front of her, my interface must show her counter's waiting tickets in order, with ticket number, service, and status readable at a glance, and one large "Call next" button.
2. Because Isabella works at a desktop with a mouse and can't afford long screens or typing mid-rush, my interface must let her call, serve, or no-show a ticket in one click each, with no forms, and show statuses as words, not only color.
3. Because Isabella loses time when called customers don't show up and the line keeps growing, my interface must show which ticket is currently called at her counter and put the "No-show" button next to it, so she can move on to the next person right away.
