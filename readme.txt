How to boot web server:

A. initiating method:
1. make SQL user and database
2. execute init.sql >>>
    mysql -u *username* -p *dbname* < database/init.sql
3. create and connect venv >>>
    source venv/bin/activate
4. execute backend/import_csv_i.py >>>
    python3 backend/import_csv_i.py

B. casual method:
1. execute backend/app.py >>>
    python3 backend/app.py