Environment Variables Setup Guide

Overview:
This project uses environment variables to store sensitive credentials. The .env file is excluded from Git for security.

Files:
- .env - Your local credentials (NOT tracked by Git)
- .env.example - Template for .env file (tracked by Git)
- .gitignore - Excludes .env from Git

Setup Instructions:

1. Copy .env.example to .env:
   cp .env.example .env

2. Edit .env with your credentials:
   DB_HOST=localhost
   DB_USER=root
   DB_PASSWORD=your_password_here
   DB_PORT=3306

3. The application will automatically load these variables

Environment Variables:

DB_HOST
- Description: MySQL database host
- Default: localhost
- Example: localhost, 127.0.0.1, db.example.com

DB_USER
- Description: MySQL database user
- Default: root
- Example: root, admin, user

DB_PASSWORD
- Description: MySQL database password
- Default: Mysql123
- Example: your_secure_password

DB_PORT
- Description: MySQL database port
- Default: 3306
- Example: 3306, 3307

STREAMLIT_THEME_BASE
- Description: Streamlit theme
- Default: light
- Options: light, dark

STREAMLIT_LOGGER_LEVEL
- Description: Logging level
- Default: info
- Options: debug, info, warning, error

How It Works:

1. Application starts
2. Loads .env file using python-dotenv
3. Reads environment variables
4. Uses values in configuration
5. Falls back to defaults if not set

Security Best Practices:

1. Never commit .env to Git
2. Keep .env file local only
3. Use strong passwords
4. Rotate credentials regularly
5. Don't share .env file
6. Use .env.example as template
7. Document required variables

For Team Development:

1. Share .env.example (not .env)
2. Each developer creates their own .env
3. Use same variable names
4. Document any new variables
5. Update .env.example when adding variables

For Production:

1. Set environment variables on server
2. Don't use .env file in production
3. Use secure credential management
4. Rotate credentials regularly
5. Monitor access logs
6. Use environment-specific configs

Troubleshooting:

Variables not loading?
- Check .env file exists
- Verify file is in project root
- Check variable names match
- Ensure no spaces around =
- Restart application

Wrong values being used?
- Check .env file content
- Verify environment variables
- Check default values in code
- Look for typos in variable names

Connection failing?
- Verify DB_HOST is correct
- Check DB_USER has permissions
- Confirm DB_PASSWORD is correct
- Ensure DB_PORT is accessible
- Test MySQL connection manually

Example .env File:

DB_HOST=localhost
DB_USER=root
DB_PASSWORD=MySecurePassword123
DB_PORT=3306
STREAMLIT_THEME_BASE=light
STREAMLIT_LOGGER_LEVEL=info

Installation with Environment Variables:

1. Activate virtual environment:
   .\env\Scripts\activate

2. Install dependencies:
   pip install -r requirements.txt

3. Create .env file:
   cp .env.example .env

4. Edit .env with your credentials

5. Run application:
   streamlit run streamlit_app.py

Git Workflow:

1. .env is in .gitignore (not tracked)
2. .env.example is tracked (template)
3. Developers create local .env
4. Each .env is independent
5. No credentials in Git

Checking Environment Variables:

Python:
import os
from dotenv import load_dotenv
load_dotenv()
print(os.getenv("DB_HOST"))

Streamlit:
import os
st.write(os.getenv("DB_HOST"))

Command Line:
echo %DB_HOST%  (Windows)
echo $DB_HOST   (Linux/Mac)

Common Issues:

Issue: "No module named 'dotenv'"
Solution: pip install python-dotenv

Issue: Variables not found
Solution: Ensure .env is in project root

Issue: Wrong values used
Solution: Check .env file and restart app

Issue: Connection failed
Solution: Verify credentials in .env

Support:

For issues:
1. Check ENV_SETUP.md
2. Verify .env file exists
3. Check variable names
4. Test MySQL connection
5. Review error messages
