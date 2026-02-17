import streamlit as st
import pandas as pd
import mysql.connector
from mysql.connector import Error
from faker import Faker
import random
import io
from datetime import datetime, timedelta
import os
from dotenv import load_dotenv

load_dotenv()

fake = Faker()

DB_CONFIG = {
    "host": os.getenv("DB_HOST", "localhost"),
    "user": os.getenv("DB_USER", "root"),
    "password": os.getenv("DB_PASSWORD", "Mysql123"),
    "port": int(os.getenv("DB_PORT", 3306))
}

DOMAINS = ['ecommerce', 'fintech', 'healthcare', 'education', 'logistics', 'hr']

class DatabaseManager:
    def __init__(self, config):
        self.config = config
        self.conn = None
        self.cursor = None
    
    def connect(self):
        try:
            self.conn = mysql.connector.connect(**self.config)
            self.cursor = self.conn.cursor()
            return True
        except Error as e:
            st.error(f"Database connection error: {e}")
            return False
    
    def disconnect(self):
        if self.conn and self.conn.is_connected():
            self.cursor.close()
            self.conn.close()
    
    def create_database(self, db_name):
        try:
            self.cursor.execute(f"CREATE DATABASE IF NOT EXISTS {db_name}")
            self.cursor.execute(f"USE {db_name}")
            self.conn.commit()
            return True
        except Error as e:
            st.error(f"Error creating database: {e}")
            return False
    
    def execute_query(self, query):
        try:
            self.cursor.execute(query)
            self.conn.commit()
            return True
        except Error as e:
            st.error(f"Query execution error: {e}")
            return False
    
    def fetch_data(self, query):
        try:
            self.cursor.execute(query)
            columns = [desc[0] for desc in self.cursor.description]
            data = self.cursor.fetchall()
            return pd.DataFrame(data, columns=columns)
        except Error as e:
            st.error(f"Fetch error: {e}")
            return None

class SchemaManager:
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
            ]
        }
        return schemas.get(domain, [])

class DataGenerator:
    def __init__(self, db_manager, row_limit):
        self.db = db_manager
        self.row_limit = row_limit
        self.batch_size = 500
    
    def _truncate(self, value, length):
        if isinstance(value, str) and len(value) > length:
            return value[:length]
        return value
    
    def _batch_insert(self, query, data):
        if not data:
            return
        for i in range(0, len(data), self.batch_size):
            try:
                self.db.cursor.executemany(query, data[i:i + self.batch_size])
                self.db.conn.commit()
            except Error as e:
                st.error(f"Batch insert error: {e}")
    
    def _get_ids(self, table, col):
        try:
            self.db.cursor.execute(f"SELECT {col} FROM {table}")
            result = [x[0] for x in self.db.cursor.fetchall()]
            return result
        except Error as e:
            st.error(f"Error fetching IDs: {e}")
            return []
    
    def generate_ecommerce(self):
        st.info("Generating ecommerce data...")
        
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
        
        if not cat_ids:
            st.error("Failed to generate categories")
            return
        
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
        
        if not cust_ids:
            st.error("Failed to generate customers")
            return
        
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
        
        order_ids = self._get_ids('orders', 'order_id')
        if not order_ids or not prod_ids:
            st.error("Failed to generate orders")
            return
        
        items = []
        for oid in order_ids:
            for _ in range(random.randint(1, 4)):
                pid = random.choice(prod_ids)
                qty = random.randint(1, 3)
                u_price = round(random.uniform(10, 100), 2)
                items.append((oid, pid, qty, u_price, qty * u_price, 0, 'None'))
        self._batch_insert("INSERT INTO order_items (order_id, product_id, quantity, unit_price, total_price, discount_applied, return_status) VALUES (%s, %s, %s, %s, %s, %s, %s)", items)
        
        st.success("Ecommerce data generated successfully!")

def main():
    st.set_page_config(page_title="Data Generation Platform", layout="wide")
    st.title("Data Generation & Analytics Platform")
    
    st.sidebar.header("Database Configuration")
    
    host = st.sidebar.text_input("Database Host", value=os.getenv("DB_HOST", "localhost"))
    user = st.sidebar.text_input("Database User", value=os.getenv("DB_USER", "root"))
    password = st.sidebar.text_input("Database Password", value=os.getenv("DB_PASSWORD", "Mysql123"), type="password")
    
    domain = st.sidebar.selectbox(
        "Select Domain",
        DOMAINS,
        format_func=lambda x: x.capitalize()
    )
    
    row_count = st.sidebar.number_input(
        "Number of Records",
        min_value=10,
        max_value=10000,
        value=100,
        step=10
    )
    
    col1, col2 = st.sidebar.columns(2)
    
    with col1:
        test_conn = st.sidebar.button("Test Connection")
    
    with col2:
        generate_button = st.sidebar.button("Generate Data")
    
    if test_conn:
        db_config = {"host": host, "user": user, "password": password}
        db = DatabaseManager(db_config)
        if db.connect():
            st.sidebar.success("Database connection successful!")
            db.disconnect()
        else:
            st.sidebar.error("Failed to connect to database")
    
    if generate_button:
        db_config = {"host": host, "user": user, "password": password}
        db = DatabaseManager(db_config)
        
        if db.connect():
            db_name = f"analytics_{domain}"
            
            if db.create_database(db_name):
                schema = SchemaManager.get_schema(domain)
                
                progress_bar = st.progress(0)
                status_text = st.empty()
                
                for idx, sql in enumerate(schema):
                    status_text.text(f"Creating tables... {idx + 1}/{len(schema)}")
                    if not db.execute_query(sql):
                        st.error(f"Failed to create table")
                        db.disconnect()
                        return
                    progress_bar.progress((idx + 1) / len(schema))
                
                status_text.text("Generating data...")
                gen = DataGenerator(db, row_count)
                
                if domain == 'ecommerce':
                    gen.generate_ecommerce()
                
                st.success(f"Data generation completed for {domain}!")
                
                st.header(f"Data Preview - {domain.capitalize()}")
                
                if domain == 'ecommerce':
                    df_products = db.fetch_data("SELECT * FROM products LIMIT 10")
                    if df_products is not None:
                        st.subheader("Products")
                        st.dataframe(df_products)
                    
                    df_customers = db.fetch_data("SELECT * FROM customers LIMIT 10")
                    if df_customers is not None:
                        st.subheader("Customers")
                        st.dataframe(df_customers)
                    
                    df_orders = db.fetch_data("SELECT * FROM orders LIMIT 10")
                    if df_orders is not None:
                        st.subheader("Orders")
                        st.dataframe(df_orders)
                
                st.header("Export Data")
                
                if domain == 'ecommerce':
                    df_export = db.fetch_data("SELECT * FROM products")
                    if df_export is not None:
                        csv_buffer = io.StringIO()
                        df_export.to_csv(csv_buffer, index=False)
                        csv_data = csv_buffer.getvalue()
                        
                        st.download_button(
                            label="Download Products CSV",
                            data=csv_data,
                            file_name=f"products_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                            mime="text/csv"
                        )
                
                db.disconnect()
        else:
            st.error("Failed to connect to database")

if __name__ == "__main__":
    main()
