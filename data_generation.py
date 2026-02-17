import argparse
import mysql.connector
from mysql.connector import Error
from faker import Faker
import random
import sys
from datetime import datetime, timedelta

# Database Configuration
# In a real production environment, use environment variables for credentials
DB_CONFIG = {
    "host": "localhost",
    "user": "root",
    "password": "Mysql123"  # CHANGE THIS
}

fake = Faker()

class SchemaManager:
    @staticmethod
    def get_available_domains():
        return ['ecommerce', 'fintech', 'healthcare', 'education', 'logistics', 'hr']

    @staticmethod
    def get_schema(domain):
        schemas = {
            'ecommerce': [
                """CREATE TABLE IF NOT EXISTS categories (
                    category_id INT AUTO_INCREMENT PRIMARY KEY, 
                    name VARCHAR(100), 
                    description TEXT,
                    slug VARCHAR(150),
                    is_active BOOLEAN DEFAULT TRUE,
                    created_at DATETIME,
                    updated_at DATETIME
                )""",
                """CREATE TABLE IF NOT EXISTS products (
                    product_id INT AUTO_INCREMENT PRIMARY KEY, 
                    category_id INT, 
                    sku VARCHAR(50) UNIQUE,
                    name VARCHAR(255), 
                    description TEXT,
                    price DECIMAL(10,2), 
                    cost_price DECIMAL(10,2), 
                    currency VARCHAR(10) DEFAULT 'USD',
                    stock_level INT, 
                    weight_kg DECIMAL(5,2),
                    dimensions_cm VARCHAR(100),
                    vendor_name VARCHAR(150),
                    is_digital BOOLEAN DEFAULT FALSE,
                    created_at DATETIME,
                    FOREIGN KEY (category_id) REFERENCES categories(category_id)
                )""",
                """CREATE TABLE IF NOT EXISTS customers (
                    customer_id INT AUTO_INCREMENT PRIMARY KEY, 
                    first_name VARCHAR(100), 
                    last_name VARCHAR(100), 
                    email VARCHAR(255) UNIQUE, 
                    phone_number VARCHAR(50),
                    gender VARCHAR(20),
                    birth_date DATE,
                    address_line1 VARCHAR(255),
                    city VARCHAR(100),
                    state VARCHAR(100),
                    postal_code VARCHAR(50),
                    country VARCHAR(100),
                    join_date DATETIME, 
                    last_login DATETIME,
                    loyalty_tier VARCHAR(50),
                    marketing_opt_in BOOLEAN
                )""",
                """CREATE TABLE IF NOT EXISTS orders (
                    order_id INT AUTO_INCREMENT PRIMARY KEY, 
                    customer_id INT, 
                    order_date DATETIME, 
                    status VARCHAR(50), 
                    payment_method VARCHAR(100),
                    payment_status VARCHAR(50),
                    subtotal DECIMAL(12,2),
                    tax_amount DECIMAL(12,2),
                    shipping_cost DECIMAL(12,2),
                    discount_amount DECIMAL(12,2),
                    total_amount DECIMAL(12,2),
                    shipping_address TEXT, 
                    billing_address TEXT,
                    ip_address VARCHAR(50),
                    user_agent TEXT,
                    FOREIGN KEY (customer_id) REFERENCES customers(customer_id)
                )""",
                """CREATE TABLE IF NOT EXISTS order_items (
                    item_id INT AUTO_INCREMENT PRIMARY KEY, 
                    order_id INT, 
                    product_id INT, 
                    quantity INT, 
                    unit_price DECIMAL(10,2), 
                    total_price DECIMAL(12,2), 
                    discount_applied DECIMAL(10,2),
                    return_status VARCHAR(50) DEFAULT 'None',
                    FOREIGN KEY (order_id) REFERENCES orders(order_id), 
                    FOREIGN KEY (product_id) REFERENCES products(product_id)
                )"""
            ],
            'fintech': [
                """CREATE TABLE IF NOT EXISTS branches (
                    branch_id INT AUTO_INCREMENT PRIMARY KEY, 
                    branch_code VARCHAR(50) UNIQUE,
                    name VARCHAR(150), 
                    address VARCHAR(255),
                    city VARCHAR(100),
                    state VARCHAR(100),
                    zip_code VARCHAR(50),
                    phone VARCHAR(50),
                    manager_name VARCHAR(150),
                    opened_date DATE,
                    vault_capacity DECIMAL(15,2)
                )""",
                """CREATE TABLE IF NOT EXISTS customers (
                    customer_id INT AUTO_INCREMENT PRIMARY KEY, 
                    branch_id INT, 
                    first_name VARCHAR(100), 
                    last_name VARCHAR(100), 
                    email VARCHAR(255),
                    phone VARCHAR(50),
                    national_id VARCHAR(100) UNIQUE,
                    dob DATE, 
                    address VARCHAR(255),
                    employment_status VARCHAR(100),
                    annual_income DECIMAL(15,2),
                    kyc_status VARCHAR(50), 
                    risk_score INT, 
                    credit_score INT,
                    created_at DATETIME,
                    FOREIGN KEY (branch_id) REFERENCES branches(branch_id)
                )""",
                """CREATE TABLE IF NOT EXISTS accounts (
                    account_id INT AUTO_INCREMENT PRIMARY KEY, 
                    customer_id INT, 
                    account_number VARCHAR(50) UNIQUE,
                    account_type VARCHAR(100), 
                    currency VARCHAR(10),
                    balance DECIMAL(15,2), 
                    overdraft_limit DECIMAL(15,2),
                    interest_rate DECIMAL(5,2),
                    open_date DATE, 
                    status VARCHAR(50), 
                    last_activity DATETIME,
                    FOREIGN KEY (customer_id) REFERENCES customers(customer_id)
                )""",
                """CREATE TABLE IF NOT EXISTS transactions (
                    txn_id INT AUTO_INCREMENT PRIMARY KEY, 
                    account_id INT, 
                    txn_reference VARCHAR(100) UNIQUE,
                    txn_type VARCHAR(50), 
                    category VARCHAR(100),
                    amount DECIMAL(15,2), 
                    fee_amount DECIMAL(10,2),
                    currency VARCHAR(10),
                    txn_date DATETIME, 
                    merchant_name VARCHAR(150), 
                    merchant_city VARCHAR(100),
                    merchant_country VARCHAR(100),
                    channel VARCHAR(50),
                    status VARCHAR(50),
                    ip_address VARCHAR(50),
                    device_id VARCHAR(150),
                    FOREIGN KEY (account_id) REFERENCES accounts(account_id)
                )"""
            ],
            'healthcare': [
                """CREATE TABLE IF NOT EXISTS departments (
                    dept_id INT AUTO_INCREMENT PRIMARY KEY, 
                    name VARCHAR(150), 
                    floor_number INT,
                    wing VARCHAR(100),
                    phone_extension VARCHAR(50),
                    head_doctor VARCHAR(150),
                    bed_capacity INT,
                    is_emergency_unit BOOLEAN
                )""",
                """CREATE TABLE IF NOT EXISTS doctors (
                    doctor_id INT AUTO_INCREMENT PRIMARY KEY, 
                    dept_id INT, 
                    first_name VARCHAR(100), 
                    last_name VARCHAR(100), 
                    email VARCHAR(255),
                    phone VARCHAR(50),
                    license_number VARCHAR(100),
                    specialty VARCHAR(150), 
                    qualification VARCHAR(150),
                    years_experience INT,
                    consultation_fee DECIMAL(10,2),
                    join_date DATE, 
                    is_active BOOLEAN,
                    FOREIGN KEY (dept_id) REFERENCES departments(dept_id)
                )""",
                """CREATE TABLE IF NOT EXISTS patients (
                    patient_id INT AUTO_INCREMENT PRIMARY KEY, 
                    first_name VARCHAR(100), 
                    last_name VARCHAR(100), 
                    dob DATE, 
                    gender VARCHAR(20),
                    blood_group VARCHAR(10), 
                    height_cm DECIMAL(5,2),
                    weight_kg DECIMAL(5,2),
                    allergies TEXT,
                    chronic_conditions TEXT,
                    emergency_contact_name VARCHAR(150),
                    emergency_contact_phone VARCHAR(50),
                    insurance_provider VARCHAR(150),
                    insurance_policy_no VARCHAR(100),
                    address TEXT
                )""",
                """CREATE TABLE IF NOT EXISTS appointments (
                    appt_id INT AUTO_INCREMENT PRIMARY KEY, 
                    patient_id INT, 
                    doctor_id INT, 
                    appt_date DATETIME, 
                    duration_minutes INT,
                    type VARCHAR(50), 
                    status VARCHAR(50), 
                    reason_for_visit TEXT, 
                    diagnosis_notes TEXT,
                    symptoms TEXT,
                    FOREIGN KEY (patient_id) REFERENCES patients(patient_id), 
                    FOREIGN KEY (doctor_id) REFERENCES doctors(doctor_id)
                )"""
            ],
            'education': [
                """CREATE TABLE IF NOT EXISTS departments (
                    dept_id INT AUTO_INCREMENT PRIMARY KEY, 
                    name VARCHAR(150), 
                    code VARCHAR(50),
                    building_name VARCHAR(150),
                    office_number VARCHAR(50),
                    budget DECIMAL(15,2),
                    start_date DATE,
                    dean_name VARCHAR(150)
                )""",
                """CREATE TABLE IF NOT EXISTS professors (
                    prof_id INT AUTO_INCREMENT PRIMARY KEY, 
                    dept_id INT, 
                    first_name VARCHAR(100),
                    last_name VARCHAR(100),
                    email VARCHAR(255),
                    phone VARCHAR(50),
                    title VARCHAR(100), 
                    specialization VARCHAR(150),
                    salary DECIMAL(10,2),
                    tenure_status BOOLEAN,
                    hire_date DATE, 
                    office_hours TEXT,
                    FOREIGN KEY (dept_id) REFERENCES departments(dept_id)
                )""",
                """CREATE TABLE IF NOT EXISTS students (
                    student_id INT AUTO_INCREMENT PRIMARY KEY, 
                    first_name VARCHAR(100), 
                    last_name VARCHAR(100), 
                    email VARCHAR(255),
                    phone VARCHAR(50),
                    dob DATE,
                    gender VARCHAR(20),
                    enrollment_year INT,
                    major VARCHAR(150),
                    minor VARCHAR(150),
                    gpa DECIMAL(3,2),
                    credits_earned INT,
                    status VARCHAR(50),
                    address TEXT
                )""",
                """CREATE TABLE IF NOT EXISTS courses (
                    course_id INT AUTO_INCREMENT PRIMARY KEY, 
                    dept_id INT, 
                    prof_id INT, 
                    code VARCHAR(50),
                    name VARCHAR(150), 
                    description TEXT,
                    credits INT, 
                    capacity INT,
                    semester VARCHAR(50),
                    schedule_days VARCHAR(100),
                    room_number VARCHAR(50),
                    FOREIGN KEY (dept_id) REFERENCES departments(dept_id), 
                    FOREIGN KEY (prof_id) REFERENCES professors(prof_id)
                )"""
            ],
            'logistics': [
                """CREATE TABLE IF NOT EXISTS warehouses (
                    warehouse_id INT AUTO_INCREMENT PRIMARY KEY, 
                    code VARCHAR(50),
                    name VARCHAR(150),
                    address VARCHAR(255),
                    city VARCHAR(100),
                    country VARCHAR(100),
                    latitude DECIMAL(10,8),
                    longitude DECIMAL(11,8),
                    capacity_sqft INT, 
                    temperature_controlled BOOLEAN,
                    manager_name VARCHAR(150),
                    operating_hours VARCHAR(150)
                )""",
                """CREATE TABLE IF NOT EXISTS drivers (
                    driver_id INT AUTO_INCREMENT PRIMARY KEY, 
                    first_name VARCHAR(100),
                    last_name VARCHAR(100),
                    license_number VARCHAR(100) UNIQUE,
                    license_expiry DATE,
                    phone VARCHAR(50),
                    email VARCHAR(255),
                    rating DECIMAL(3,2),
                    total_trips INT,
                    employment_type VARCHAR(50), 
                    status VARCHAR(50)
                )""",
                """CREATE TABLE IF NOT EXISTS vehicles (
                    vehicle_id INT AUTO_INCREMENT PRIMARY KEY, 
                    warehouse_id INT, 
                    vin VARCHAR(100) UNIQUE,
                    make VARCHAR(100),
                    model VARCHAR(100),
                    year INT,
                    vehicle_type VARCHAR(100), 
                    license_plate VARCHAR(50), 
                    fuel_type VARCHAR(50),
                    max_load_kg DECIMAL(10,2),
                    mileage_km DECIMAL(10,2),
                    last_service_date DATE,
                    status VARCHAR(50), 
                    FOREIGN KEY (warehouse_id) REFERENCES warehouses(warehouse_id)
                )""",
                """CREATE TABLE IF NOT EXISTS shipments (
                    shipment_id INT AUTO_INCREMENT PRIMARY KEY, 
                    warehouse_id INT, 
                    tracking_number VARCHAR(100) UNIQUE,
                    sender_name VARCHAR(150),
                    sender_address TEXT,
                    recipient_name VARCHAR(150),
                    recipient_address TEXT,
                    recipient_phone VARCHAR(50),
                    weight_kg DECIMAL(10,2), 
                    volume_m3 DECIMAL(10,2),
                    cargo_type VARCHAR(100),
                    priority VARCHAR(50),
                    status VARCHAR(50), 
                    create_date DATETIME, 
                    estimated_delivery DATETIME,
                    actual_delivery DATETIME,
                    FOREIGN KEY (warehouse_id) REFERENCES warehouses(warehouse_id)
                )"""
            ],
            'hr': [
                """CREATE TABLE IF NOT EXISTS departments (
                    dept_id INT AUTO_INCREMENT PRIMARY KEY, 
                    name VARCHAR(150), 
                    description TEXT,
                    location VARCHAR(150),
                    cost_center_code VARCHAR(50),
                    budget_yearly DECIMAL(15,2),
                    head_count_limit INT,
                    created_at DATE
                )""",
                """CREATE TABLE IF NOT EXISTS jobs (
                    job_id INT AUTO_INCREMENT PRIMARY KEY, 
                    title VARCHAR(150), 
                    job_code VARCHAR(50),
                    min_salary DECIMAL(10,2), 
                    max_salary DECIMAL(10,2),
                    level VARCHAR(50), 
                    requirements TEXT,
                    is_remote_allowed BOOLEAN
                )""",
                """CREATE TABLE IF NOT EXISTS employees (
                    emp_id INT AUTO_INCREMENT PRIMARY KEY, 
                    first_name VARCHAR(100), 
                    last_name VARCHAR(100), 
                    email VARCHAR(255) UNIQUE, 
                    phone VARCHAR(50),
                    ssn VARCHAR(50),
                    dob DATE,
                    gender VARCHAR(20),
                    marital_status VARCHAR(50),
                    hire_date DATE, 
                    dept_id INT, 
                    job_id INT, 
                    manager_id INT, 
                    employment_status VARCHAR(50), 
                    salary DECIMAL(10,2), 
                    currency VARCHAR(10),
                    address TEXT,
                    FOREIGN KEY (dept_id) REFERENCES departments(dept_id), 
                    FOREIGN KEY (job_id) REFERENCES jobs(job_id)
                )""",
                """CREATE TABLE IF NOT EXISTS attendance (
                    att_id INT AUTO_INCREMENT PRIMARY KEY, 
                    emp_id INT, 
                    date DATE, 
                    check_in TIME, 
                    check_out TIME, 
                    hours_worked DECIMAL(4,2),
                    status VARCHAR(50), 
                    location_ip VARCHAR(50),
                    FOREIGN KEY (emp_id) REFERENCES employees(emp_id)
                )"""
            ]
        }
        return schemas.get(domain, [])

class DataGenerator:
    def __init__(self, connection, row_limit):
        self.conn = connection
        self.cursor = connection.cursor()
        self.row_limit = row_limit
        self.batch_size = 500

    def _truncate(self, value, length):
        """Helper to truncate strings to fit database columns"""
        if isinstance(value, str) and len(value) > length:
            return value[:length]
        return value

    def _batch_insert(self, query, data):
        if not data: return
        for i in range(0, len(data), self.batch_size):
            try:
                self.cursor.executemany(query, data[i:i + self.batch_size])
                self.conn.commit()
            except Error as e:
                print(f"Error inserting batch: {e}")
                # Important: If batch insert fails, we must continue or exit based on logic
                # Here we continue, but logging would be appropriate in production.

    def _get_ids(self, table, col):
        self.cursor.execute(f"SELECT {col} FROM {table}")
        result = [x[0] for x in self.cursor.fetchall()]
        if not result:
            print(f"Warning: No IDs found in {table}. Subsequent tables might fail.")
        return result

    def generate(self, domain):
        method_name = f"generate_{domain}"
        if hasattr(self, method_name):
            getattr(self, method_name)()
        else:
            print(f"Generator for {domain} not implemented.")

    def generate_ecommerce(self):
        print("Populating Ecommerce tables...")
        # 1. Categories
        cats = []
        for _ in range(20):
            cats.append((
                self._truncate(fake.word().title(), 100), 
                fake.sentence(), 
                self._truncate(fake.slug(), 150), 
                True, fake.date_time_this_decade(), fake.date_time_this_year()
            ))
        self._batch_insert("INSERT INTO categories (name, description, slug, is_active, created_at, updated_at) VALUES (%s, %s, %s, %s, %s, %s)", cats)
        cat_ids = self._get_ids('categories', 'category_id')

        # 2. Products
        if not cat_ids: return
        prods = []
        for _ in range(self.row_limit):
            price = round(random.uniform(10, 2000), 2)
            prods.append((
                random.choice(cat_ids), self._truncate(fake.uuid4()[:8].upper(), 50), 
                self._truncate(fake.catch_phrase(), 255), fake.text(), 
                price, price * 0.7, 'USD', random.randint(0, 500), random.uniform(0.1, 50.0), 
                self._truncate(f"{random.randint(10,100)}x{random.randint(10,100)}x{random.randint(10,100)}", 100), 
                self._truncate(fake.company(), 150),
                random.choice([True, False]), fake.date_time_this_decade()
            ))
        self._batch_insert("INSERT INTO products (category_id, sku, name, description, price, cost_price, currency, stock_level, weight_kg, dimensions_cm, vendor_name, is_digital, created_at) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)", prods)
        prod_ids = self._get_ids('products', 'product_id')

        # 3. Customers
        custs = []
        for _ in range(self.row_limit):
            custs.append((
                self._truncate(fake.first_name(), 100), self._truncate(fake.last_name(), 100), 
                self._truncate(fake.unique.email(), 255), self._truncate(fake.phone_number(), 50), 
                random.choice(['Male', 'Female', 'Other']), fake.date_of_birth(minimum_age=18, maximum_age=90), 
                self._truncate(fake.street_address(), 255), self._truncate(fake.city(), 100), 
                self._truncate(fake.state(), 100), self._truncate(fake.postcode(), 50), 
                self._truncate(fake.country(), 100),
                fake.date_time_this_decade(), fake.date_time_this_year(), 
                random.choice(['Bronze', 'Silver', 'Gold', 'Platinum']), random.choice([True, False])
            ))
        self._batch_insert("""INSERT INTO customers 
            (first_name, last_name, email, phone_number, gender, birth_date, address_line1, city, state, postal_code, country, join_date, last_login, loyalty_tier, marketing_opt_in) 
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)""", custs)
        cust_ids = self._get_ids('customers', 'customer_id')

        # 4. Orders
        if not cust_ids: return
        orders = []
        for _ in range(self.row_limit):
            subtotal = round(random.uniform(50, 1000), 2)
            orders.append((
                random.choice(cust_ids), fake.date_time_this_year(), 
                random.choice(['Pending', 'Processing', 'Shipped', 'Delivered', 'Cancelled']),
                random.choice(['Credit Card', 'PayPal', 'Apple Pay', 'Bank Transfer']), 
                random.choice(['Paid', 'Pending', 'Failed']),
                subtotal, round(subtotal * 0.08, 2), round(random.uniform(5, 50), 2), 
                round(random.uniform(0, 20), 2), subtotal + 50, fake.address(), fake.address(), 
                fake.ipv4(), fake.user_agent()
            ))
        self._batch_insert("""INSERT INTO orders 
            (customer_id, order_date, status, payment_method, payment_status, subtotal, tax_amount, shipping_cost, discount_amount, total_amount, shipping_address, billing_address, ip_address, user_agent) 
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)""", orders)

        # 5. Order Items
        order_ids = self._get_ids('orders', 'order_id')
        if not order_ids or not prod_ids: return
        items = []
        for oid in order_ids:
            for _ in range(random.randint(1, 4)):
                pid = random.choice(prod_ids)
                qty = random.randint(1, 3)
                u_price = round(random.uniform(10, 100), 2)
                items.append((oid, pid, qty, u_price, qty * u_price, 0, 'None'))
        self._batch_insert("INSERT INTO order_items (order_id, product_id, quantity, unit_price, total_price, discount_applied, return_status) VALUES (%s, %s, %s, %s, %s, %s, %s)", items)

    def generate_fintech(self):
        print("Populating Fintech tables...")
        # 1. Branches
        branches = []
        for _ in range(20):
            branches.append((
                self._truncate(fake.bothify('BR-####'), 50), self._truncate(fake.company() + " Branch", 150), 
                self._truncate(fake.street_address(), 255), self._truncate(fake.city(), 100), 
                self._truncate(fake.state_abbr(), 100), self._truncate(fake.postcode(), 50), 
                self._truncate(fake.phone_number(), 50), self._truncate(fake.name(), 150), 
                fake.date_this_century(), random.uniform(1000000, 50000000)
            ))
        self._batch_insert("INSERT INTO branches (branch_code, name, address, city, state, zip_code, phone, manager_name, opened_date, vault_capacity) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)", branches)
        branch_ids = self._get_ids('branches', 'branch_id')

        # 2. Customers
        if not branch_ids: return
        custs = []
        for _ in range(self.row_limit):
            custs.append((
                random.choice(branch_ids), self._truncate(fake.first_name(), 100), self._truncate(fake.last_name(), 100), 
                self._truncate(fake.unique.email(), 255), self._truncate(fake.phone_number(), 50),
                self._truncate(fake.unique.ssn(), 100), fake.date_of_birth(minimum_age=18), self._truncate(fake.address(), 255), 
                random.choice(['Employed', 'Self-Employed', 'Unemployed', 'Retired']), random.uniform(30000, 200000),
                random.choice(['Verified', 'Pending', 'Rejected']), random.randint(1, 100), random.randint(300, 850), fake.date_time_this_decade()
            ))
        self._batch_insert("""INSERT INTO customers 
            (branch_id, first_name, last_name, email, phone, national_id, dob, address, employment_status, annual_income, kyc_status, risk_score, credit_score, created_at)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)""", custs)
        cust_ids = self._get_ids('customers', 'customer_id')

        # 3. Accounts
        if not cust_ids: return
        accs = []
        for cid in custs: 
            accs.append((
                random.choice(cust_ids), self._truncate(fake.iban(), 50), 
                random.choice(['Savings', 'Checking', 'Business', 'Investment']), 'USD',
                round(random.uniform(0, 100000), 2), round(random.uniform(0, 5000), 2), round(random.uniform(0.1, 5.0), 2),
                fake.date_this_decade(), 'Active', fake.date_time_this_year()
            ))
        self._batch_insert("""INSERT INTO accounts 
            (customer_id, account_number, account_type, currency, balance, overdraft_limit, interest_rate, open_date, status, last_activity)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)""", accs)
        acc_ids = self._get_ids('accounts', 'account_id')

        # 4. Transactions
        if not acc_ids: return
        txns = []
        for _ in range(self.row_limit * 2):
            amt = round(random.uniform(10, 5000), 2)
            txns.append((
                random.choice(acc_ids), self._truncate(fake.uuid4(), 100), 
                random.choice(['Debit', 'Credit']), random.choice(['Groceries', 'Utilities', 'Travel', 'Dining']),
                amt, round(amt * 0.01, 2), 'USD', fake.date_time_this_year(), 
                self._truncate(fake.company(), 150), self._truncate(fake.city(), 100), 
                self._truncate(fake.country(), 100),
                random.choice(['Mobile', 'Web', 'ATM', 'POS']), random.choice(['Success', 'Pending', 'Failed']), 
                fake.ipv4(), fake.mac_address()
            ))
        self._batch_insert("""INSERT INTO transactions 
            (account_id, txn_reference, txn_type, category, amount, fee_amount, currency, txn_date, merchant_name, merchant_city, merchant_country, channel, status, ip_address, device_id)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)""", txns)

    def generate_healthcare(self):
        print("Populating Healthcare tables...")
        # 1. Depts
        depts = []
        for name in ['Cardiology', 'Neurology', 'Oncology', 'Pediatrics', 'Orthopedics', 'Emergency', 'Radiology']:
            depts.append((
                name, random.randint(1, 10), random.choice(['North', 'South', 'East']), 
                fake.numerify('###'), fake.name(), random.randint(10, 50), True
            ))
        self._batch_insert("INSERT INTO departments (name, floor_number, wing, phone_extension, head_doctor, bed_capacity, is_emergency_unit) VALUES (%s, %s, %s, %s, %s, %s, %s)", depts)
        dept_ids = self._get_ids('departments', 'dept_id')

        # 2. Doctors
        if not dept_ids: return
        docs = []
        for _ in range(50):
            docs.append((
                random.choice(dept_ids), self._truncate(fake.first_name(), 100), self._truncate(fake.last_name(), 100), 
                self._truncate(fake.email(), 255), self._truncate(fake.phone_number(), 50),
                self._truncate(fake.license_plate(), 100), self._truncate(fake.job(), 150), "MD", 
                random.randint(1, 30), round(random.uniform(100, 500), 2),
                fake.date_this_century(), True
            ))
        self._batch_insert("""INSERT INTO doctors 
            (dept_id, first_name, last_name, email, phone, license_number, specialty, qualification, years_experience, consultation_fee, join_date, is_active)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)""", docs)
        doc_ids = self._get_ids('doctors', 'doctor_id')

        # 3. Patients
        pats = []
        for _ in range(self.row_limit):
            pats.append((
                self._truncate(fake.first_name(), 100), self._truncate(fake.last_name(), 100), 
                fake.date_of_birth(), random.choice(['Male', 'Female']),
                random.choice(['A+', 'A-', 'B+', 'O+', 'O-']), random.uniform(150, 200), random.uniform(50, 120),
                "None", "None", self._truncate(fake.name(), 150), self._truncate(fake.phone_number(), 50), 
                self._truncate(fake.company(), 150), self._truncate(fake.bothify('POL-####'), 100), fake.address()
            ))
        self._batch_insert("""INSERT INTO patients 
            (first_name, last_name, dob, gender, blood_group, height_cm, weight_kg, allergies, chronic_conditions, emergency_contact_name, emergency_contact_phone, insurance_provider, insurance_policy_no, address)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)""", pats)
        pat_ids = self._get_ids('patients', 'patient_id')

        # 4. Appointments
        if not pat_ids or not doc_ids: return
        appts = []
        for _ in range(self.row_limit):
            appts.append((
                random.choice(pat_ids), random.choice(doc_ids), fake.date_time_this_year(), random.choice([15, 30, 45, 60]),
                random.choice(['In-person', 'Video']), random.choice(['Scheduled', 'Completed', 'Cancelled', 'No-show']),
                fake.sentence(), fake.sentence(), fake.sentence()
            ))
        self._batch_insert("""INSERT INTO appointments 
            (patient_id, doctor_id, appt_date, duration_minutes, type, status, reason_for_visit, diagnosis_notes, symptoms)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)""", appts)

    def generate_education(self):
        print("Populating Education tables...")
        # 1. Depts
        depts = []
        for name in ['Computer Science', 'Mathematics', 'Physics', 'Biology', 'Literature', 'History', 'Engineering']:
            depts.append((
                name, name[:3].upper(), fake.building_number() + " Hall", fake.room_number(), 
                random.uniform(500000, 5000000), fake.date_this_century(), fake.name()
            ))
        self._batch_insert("INSERT INTO departments (name, code, building_name, office_number, budget, start_date, dean_name) VALUES (%s, %s, %s, %s, %s, %s, %s)", depts)
        dept_ids = self._get_ids('departments', 'dept_id')

        # 2. Professors
        if not dept_ids: return
        profs = []
        for _ in range(50):
            profs.append((
                random.choice(dept_ids), self._truncate(fake.first_name(), 100), self._truncate(fake.last_name(), 100), 
                self._truncate(fake.email(), 255), self._truncate(fake.phone_number(), 50),
                random.choice(['Assistant Prof', 'Associate Prof', 'Professor']), fake.bs(), random.uniform(60000, 150000),
                random.choice([True, False]), fake.date_this_century(), "Mon-Wed 2-4PM"
            ))
        self._batch_insert("""INSERT INTO professors 
            (dept_id, first_name, last_name, email, phone, title, specialization, salary, tenure_status, hire_date, office_hours)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)""", profs)
        prof_ids = self._get_ids('professors', 'prof_id')

        # 3. Students
        studs = []
        for _ in range(self.row_limit):
            studs.append((
                self._truncate(fake.first_name(), 100), self._truncate(fake.last_name(), 100), 
                self._truncate(fake.unique.email(), 255), self._truncate(fake.phone_number(), 50),
                fake.date_of_birth(minimum_age=18, maximum_age=30), random.choice(['Male', 'Female']), random.randint(2020, 2024),
                self._truncate(fake.job(), 150), "None", random.uniform(2.0, 4.0), random.randint(0, 120), 'Active', fake.address()
            ))
        self._batch_insert("""INSERT INTO students 
            (first_name, last_name, email, phone, dob, gender, enrollment_year, major, minor, gpa, credits_earned, status, address)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)""", studs)

        # 4. Courses
        if not prof_ids: return
        courses = []
        for _ in range(50):
            courses.append((
                random.choice(dept_ids), random.choice(prof_ids), self._truncate(fake.bothify('??-###'), 50), 
                self._truncate(fake.catch_phrase(), 150),
                fake.sentence(), random.randint(1, 4), random.randint(20, 100), random.choice(['Fall', 'Spring', 'Summer']),
                "MWF", fake.room_number()
            ))
        self._batch_insert("""INSERT INTO courses 
            (dept_id, prof_id, code, name, description, credits, capacity, semester, schedule_days, room_number)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)""", courses)

    def generate_logistics(self):
        print("Populating Logistics tables...")
        # 1. Warehouses
        whs = []
        for _ in range(10):
            whs.append((
                fake.bothify('WH-##'), self._truncate(fake.city() + " Hub", 150), self._truncate(fake.street_address(), 255), 
                self._truncate(fake.city(), 100), self._truncate(fake.country(), 100),
                fake.latitude(), fake.longitude(), random.randint(10000, 100000), True, self._truncate(fake.name(), 150), "24/7"
            ))
        self._batch_insert("""INSERT INTO warehouses 
            (code, name, address, city, country, latitude, longitude, capacity_sqft, temperature_controlled, manager_name, operating_hours)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)""", whs)
        wh_ids = self._get_ids('warehouses', 'warehouse_id')

        # 2. Drivers
        drivers = []
        for _ in range(50):
            drivers.append((
                self._truncate(fake.first_name(), 100), self._truncate(fake.last_name(), 100), 
                self._truncate(fake.bothify('LIC-#####'), 100), fake.date_this_decade(),
                self._truncate(fake.phone_number(), 50), self._truncate(fake.email(), 255), 
                random.uniform(3.5, 5.0), random.randint(100, 5000),
                random.choice(['Full-time', 'Contract']), 'Active'
            ))
        self._batch_insert("""INSERT INTO drivers 
            (first_name, last_name, license_number, license_expiry, phone, email, rating, total_trips, employment_type, status)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)""", drivers)

        # 3. Vehicles
        if not wh_ids: return
        vehs = []
        for _ in range(50):
            vehs.append((
                random.choice(wh_ids), self._truncate(fake.vin(), 100), random.choice(['Ford', 'Mercedes', 'Volvo']), fake.bothify('Model-?'),
                random.randint(2015, 2024), random.choice(['Truck', 'Van', 'Semi']), self._truncate(fake.license_plate(), 50),
                random.choice(['Diesel', 'Electric']), random.uniform(1000, 10000), random.uniform(10000, 200000),
                fake.date_this_year(), 'Available'
            ))
        self._batch_insert("""INSERT INTO vehicles 
            (warehouse_id, vin, make, model, year, vehicle_type, license_plate, fuel_type, max_load_kg, mileage_km, last_service_date, status)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)""", vehs)

        # 4. Shipments
        ships = []
        for _ in range(self.row_limit):
            ships.append((
                random.choice(wh_ids), self._truncate(fake.bothify('TRK-#########'), 100), 
                self._truncate(fake.name(), 150), fake.address(),
                self._truncate(fake.name(), 150), fake.address(), self._truncate(fake.phone_number(), 50), 
                random.uniform(1, 500), random.uniform(0.1, 5.0),
                random.choice(['Fragile', 'General', 'Hazardous']), random.choice(['Standard', 'Express']),
                random.choice(['Pending', 'In-Transit', 'Delivered']), fake.date_time_this_year(),
                fake.date_time_this_year(), fake.date_time_this_year()
            ))
        self._batch_insert("""INSERT INTO shipments 
            (warehouse_id, tracking_number, sender_name, sender_address, recipient_name, recipient_address, recipient_phone, weight_kg, volume_m3, cargo_type, priority, status, create_date, estimated_delivery, actual_delivery)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)""", ships)

    def generate_hr(self):
        print("Populating HR tables...")
        # 1. Departments
        depts = []
        for _ in range(10):
            depts.append((
                self._truncate(fake.job(), 150), fake.bs(), self._truncate(fake.city(), 150), 
                self._truncate(fake.bothify('CC-###'), 50), 
                random.uniform(500000, 2000000), random.randint(10, 100), fake.date_this_decade()
            ))
        self._batch_insert("INSERT INTO departments (name, description, location, cost_center_code, budget_yearly, head_count_limit, created_at) VALUES (%s, %s, %s, %s, %s, %s, %s)", depts)
        dept_ids = self._get_ids('departments', 'dept_id')

        # 2. Jobs
        jobs = []
        for _ in range(20):
            jobs.append((
                self._truncate(fake.job(), 150), self._truncate(fake.bothify('JOB-##'), 50), 
                random.uniform(40000, 60000), random.uniform(80000, 120000),
                random.choice(['Entry', 'Mid', 'Senior']), fake.text(), random.choice([True, False])
            ))
        self._batch_insert("INSERT INTO jobs (title, job_code, min_salary, max_salary, level, requirements, is_remote_allowed) VALUES (%s, %s, %s, %s, %s, %s, %s)", jobs)
        job_ids = self._get_ids('jobs', 'job_id')

        # 3. Employees
        # Check if parent tables are populated
        if not dept_ids or not job_ids:
            print("Error: Departments or Jobs failed to generate. Aborting Employee generation.")
            return

        emps = []
        for _ in range(self.row_limit):
            emps.append((
                self._truncate(fake.first_name(), 100), self._truncate(fake.last_name(), 100), 
                self._truncate(fake.unique.email(), 255), self._truncate(fake.phone_number(), 50), 
                self._truncate(fake.ssn(), 50),
                fake.date_of_birth(minimum_age=20), random.choice(['M', 'F', 'X']), random.choice(['Single', 'Married']),
                fake.date_this_decade(), random.choice(dept_ids), random.choice(job_ids), 0,
                random.choice(['FullTime', 'PartTime']), random.uniform(50000, 100000), 'USD', fake.address()
            ))
        self._batch_insert("""INSERT INTO employees 
            (first_name, last_name, email, phone, ssn, dob, gender, marital_status, hire_date, dept_id, job_id, manager_id, employment_status, salary, currency, address)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)""", emps)
        
        emp_ids = self._get_ids('employees', 'emp_id')

        # 4. Attendance
        if not emp_ids:
            print("Error: No employees generated. Skipping attendance.")
            return

        atts = []
        for _ in range(self.row_limit):
            atts.append((
                random.choice(emp_ids), fake.date_this_year(), "09:00:00", "17:00:00", 8.0, 
                'Present', fake.ipv4()
            ))
        self._batch_insert("INSERT INTO attendance (emp_id, date, check_in, check_out, hours_worked, status, location_ip) VALUES (%s, %s, %s, %s, %s, %s, %s)", atts)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--domain", type=str)
    parser.add_argument("--rows", type=int)
    args = parser.parse_args()

    domains = SchemaManager.get_available_domains()
    
    selected_domain = args.domain
    if not selected_domain:
        print(f"Available domains: {', '.join(domains)}")
        selected_domain = input("Enter domain: ").strip().lower()

    if selected_domain not in domains:
        print("Invalid domain. Exiting.")
        sys.exit(1)

    row_count = args.rows
    if not row_count:
        try:
            row_count = int(input("Enter row count (Max 10000): "))
        except ValueError:
            print("Invalid number.")
            sys.exit(1)

    if row_count > 10000:
        row_count = 10000

    conn = None
    try:
        conn = mysql.connector.connect(
            host=DB_CONFIG["host"], 
            user=DB_CONFIG["user"], 
            password=DB_CONFIG["password"]
        )
        cursor = conn.cursor()
        
        db_name = f"analytics_{selected_domain}"
        cursor.execute(f"CREATE DATABASE IF NOT EXISTS {db_name}")
        cursor.execute(f"USE {db_name}")
        
        schema = SchemaManager.get_schema(selected_domain)
        for sql in schema:
            cursor.execute(sql)
            
        gen = DataGenerator(conn, row_count)
        gen.generate(selected_domain)
        
        print(f"Successfully generated complex analytics data for {selected_domain} in database {db_name}")
        
    except Error as e:
        print(f"Critical Database Error: {e}")
    finally:
        if conn and conn.is_connected():
            cursor.close()
            conn.close()

if __name__ == "__main__":
    main()