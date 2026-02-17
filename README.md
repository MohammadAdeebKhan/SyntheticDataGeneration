Data Generation & Analytics Platform

A Streamlit-based web application for generating realistic test data across multiple domains and storing it in a MySQL database.

Features

- Multiple domain support (ecommerce, fintech, healthcare, education, logistics, hr)
- Real-time database connection testing
- Configurable data generation with custom row counts
- Direct MySQL database integration
- CSV export functionality
- Data preview and analytics
- Progress tracking during data generation

Prerequisites

- Python 3.8 or higher
- MySQL Server running locally
- Virtual environment (recommended)

Installation

1. Activate virtual environment:
   .\env\Scripts\activate

2. Install required packages:
   python -m pip install streamlit pandas faker mysql-connector-python

3. Update database credentials in streamlit_app.py if needed:
   - Default: host=localhost, user=root, password=Mysql123

Running the Application

1. Activate virtual environment:
   .\env\Scripts\activate

2. Run Streamlit app:
   streamlit run streamlit_app.py

3. Open browser to http://localhost:8501

Usage

1. Configure Database Connection:
   - Enter host, user, and password in sidebar
   - Click "Test Connection" to verify connectivity

2. Select Domain and Row Count:
   - Choose domain from dropdown
   - Set number of records to generate (10-10000)

3. Generate Data:
   - Click "Generate Data" button
   - Monitor progress bar
   - View generated data in preview tables

4. Export Data:
   - Click "Download CSV" button
   - CSV file will be downloaded with timestamp

Database Schema

Ecommerce Domain Tables:
- categories: Product categories
- products: Product information
- customers: Customer details
- orders: Order records
- order_items: Individual items in orders

Data Generation Details

- Uses Faker library for realistic data
- Maintains referential integrity with foreign keys
- Batch inserts for performance (500 records per batch)
- Automatic database and table creation
- Unique constraints on email and SKU fields

Troubleshooting

Connection Issues:
- Verify MySQL server is running
- Check credentials in sidebar
- Ensure database user has CREATE DATABASE privilege

Data Generation Errors:
- Check available disk space
- Verify row count is within limits
- Review MySQL error logs

Performance Tips

- For large datasets (5000+ records), generation may take time
- Use batch processing for optimal performance
- Monitor database disk space

File Structure

streamlit_app.py - Main Streamlit application
data_generation.py - Original data generation script
README.md - This file

Future Enhancements

- Support for all 6 domains (currently ecommerce only)
- Advanced analytics dashboard
- Data validation and quality checks
- Scheduled data generation
- Multi-database support
