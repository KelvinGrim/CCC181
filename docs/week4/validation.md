# Part 10: Validation in Three Layers

| Rule | Layer | How I tested it | What happened |
| :--- | :--- | :--- | :--- |
| Email must be valid | Flask | `curl -i -X POST http://127.0.0.1:5000/join -d "name=Test" -d "email=not-an-email" -d "service_id=2"` | `400 BAD REQUEST`, nothing saved |
| Name is required | Flask | `curl -i -X POST http://127.0.0.1:5000/join -d "name=" -d "email=ana@school.edu" -d "service_id=2"` | `400 BAD REQUEST`, nothing saved |
| Service must be active | Flask | `curl -i -X POST http://127.0.0.1:5000/join -d "name=Test" -d "email=ana@school.edu" -d "service_id=999"` | `400 BAD REQUEST`, nothing saved |
| Service must exist (FOREIGN KEY) | Database | `INSERT INTO tickets (user_id, service_id) VALUES (1, 999);` in psql | `ERROR: insert or update on table "tickets" violates foreign key constraint "tickets_service_id_fkey"` |
| Status must be allowed (CHECK) | Database | `UPDATE tickets SET status = 'lost' WHERE id = 1;` in psql | `ERROR: new row for relation "tickets" violates check constraint "ck_tickets_status"` |
| Email must be unique (UNIQUE) | Database | `INSERT INTO users (name, email) VALUES ('Copy', 'ana@school.edu');` in psql | `ERROR: duplicate key value violates unique constraint "users_email_key"` |
| Avg minutes positive (CHECK) | Database | `INSERT INTO services (name, avg_minutes) VALUES ('Test', 0);` in psql | `ERROR: new row for relation "services" violates check constraint "ck_services_avg_minutes_positive"` |
| User required (NOT NULL) | Database | `INSERT INTO tickets (user_id, service_id) VALUES (NULL, 2);` in psql | `ERROR: null value in column "user_id" of relation "tickets" violates not-null constraint` |
| Restrict service deletion (RESTRICT) | Database | `DELETE FROM services WHERE id = 2;` in psql | `ERROR: update or delete on table "services" violates foreign key constraint "tickets_service_id_fkey"` |