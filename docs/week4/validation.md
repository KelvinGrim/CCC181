

# Part 10: Validation in three layers

| Rule | Layer | How I tested it | What happened |
| :--- | :--- | :--- | :--- |
| Email must be valid | Flask | `curl -i -X POST http://127.0.0.1:5000/join -d "name=Test" -d "email=not-an-email" -d "service_id=1"` | `400 BAD REQUEST`, ticket count unchanged |
| Name is required | Flask | `curl -i -X POST http://127.0.0.1:5000/join -d "name=" -d "email=ana@school.edu" -d "service_id=1"` | `400 BAD REQUEST`, ticket count unchanged |
| Service must exist | Flask | `curl -i -X POST http://127.0.0.1:5000/join -d "name=Test" -d "email=ana@school.edu" -d "service_id=999"` | `400 BAD REQUEST`, ticket count unchanged |
| Name must not be too long | Flask | `curl -i -X POST http://127.0.0.1:5000/join -d "name=$(python3 -c 'print("a"*200)')" -d "email=ana@school.edu" -d "service_id=1"` | `400 BAD REQUEST`, ticket count unchanged |
| Service must exist (FOREIGN KEY) | Database | `INSERT INTO tickets (user_id, service_id) VALUES ((SELECT min(id) FROM users), 999);` | `ERROR:  insert or update on table "tickets" violates foreign key constraint "tickets_service_id_fkey"` |
| Email must be unique (UNIQUE) | Database | `INSERT INTO users (name, email) SELECT 'Copy', email FROM users LIMIT 1;` | `ERROR:  duplicate key value violates unique constraint "users_email_key"` |
| Status must be allowed (CHECK) | Database | `UPDATE tickets SET status = 'lost', closed_at = now() WHERE id = (SELECT min(id) FROM tickets);` | `ERROR:  new row for relation "tickets" violates check constraint "ck_tickets_status"` |
| User is required (NOT NULL) | Database | `INSERT INTO tickets (user_id, service_id) VALUES (NULL, (SELECT min(id) FROM services));` | `ERROR:  null value in column "user_id" of relation "tickets" violates not-null constraint` |
| A service with tickets cannot be deleted (RESTRICT) | Database | `DELETE FROM services WHERE id = (SELECT service_id FROM tickets LIMIT 1);` | `ERROR:  update or delete on table "services" violates foreign key constraint "tickets_service_id_fkey" on table "tickets"` |