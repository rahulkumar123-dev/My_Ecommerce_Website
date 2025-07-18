# 📱 Mobi Flex – Flipkart‑Style E‑Commerce Django Website

A full‑stack Django project for a mobile repair & e‑commerce site, featuring user auth, cart with AJAX quantity controls, dynamic delivery estimates, checkout, order history, and an admin panel.

---

## 🏷️ Features

- **User Authentication**: Register, login, logout.
- **Product Catalog**: Browse mobile products with images, prices, delivery estimates.
- **AJAX Cart**: “Add to Cart” button turns into +/– controls without page reload.
- **Buy Now**: Instantly add one item and go to cart.
- **Cart Page**: Update quantities, remove items, view live subtotals & totals.
- **Checkout**: Address form with State → City AJAX dropdown.
- **Order History**: See past orders, statuses, delivery dates, request returns.
- **Admin Panel**: Manage products, orders, statuses, and overrides.

---

## ⚙️ Prerequisites

- **Python 3.10+**
- **pip** (Python package manager)
- **virtualenv** (recommended)
- **Git**

---

## 🚀 Quick Setup

1. **Clone the Repo**
   ```bash
   git clone https://github.com/YOUR-USERNAME/YOUR-REPO.git
   cd YOUR-REPO

2. **Create & Activate Virtualenv**
   ```bash
   python -m venv venv
   #Windows
   venv\Scripts\activate
   #macOS/Linux
   source venv/bin/activate

3. **Install Dependencies**
   ```bash
   pip install -r requirements.txt

4. **Run Migrations & Create Superuser**
    ```bash
    python manage.py migrate
    python manage.py createsuperuser

5. **Collect Static Files**
   ```bash
   python manage.py collectstatic

6. **Run the Development Server**
   ```bash
   python manage.py runserver

   #Home: http://127.0.0.1:8000/
   #Admin: http://127.0.0.1:8000/admin/

🔧 **Configuration Notes**
.gitignore excludes:
  venv/ (local virtual environment)
  __pycache__/, *.py[cod]
  db.sqlite3 (use manage.py migrate to rebuild)
  media/ is tracked here, so product images and logo stay in Git.
  static/ is tracked for CSS/JS/logo styling.
  Database: uses SQLite by default; fresh clones run migrate to generate db.sqlite3.


🛠 **Admin Panel**
Login via /admin/ with superuser credentials.
Manage Products (name, price, stock, delivery override).
View & update Orders, statuses, and returns.

📑 **Usage**
Register a new user.
Browse products, click Add to Cart (AJAX updates).
Adjust quantities in‑line on homepage or cart page.
Proceed to Checkout, fill address, place order.
View Order History, request returns within 7 days.

📚 **Troubleshooting**
Missing images? Ensure media/ folder exists and contains images.
Static not loading? Confirm collectstatic ran, and <link> in base.html points to /static/.
Custom filters error? Make sure store/templatetags/__init__.py and filter files are present.
Database errors? Delete db.sqlite3, then python manage.py migrate and createsuperuser.

🚢 **Deployment**
This project can be deployed on:
PythonAnywhere, Heroku, Render, DigitalOcean App Platform, etc.
Use environment variables for DEBUG, SECRET_KEY, and database settings.
Serve static/ and media/ via WhiteNoise or your hosting’s static‑file mechanism.

🤝 **Contributing**
Fork the repo
Create your branch: git checkout -b feature-name
Commit your changes: git commit -m "Add new feature"
Push to your branch: git push origin feature-name
Open a Pull Request

📝 **License & Author**
© 2025 Your Name
Released under the MIT License.

Enjoy building with Mobi Flex!

   


