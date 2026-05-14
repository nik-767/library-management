# 📚 Library Management System
### BCA College Project — Django + SQLite

---

## 1. 📖 Project Brief
The **Library Management System** is a web-based application designed to digitize and simplify the manual record-keeping processes of a college or school library. Built primarily for educational institutions, it provides a centralized dashboard for librarians (administrators) to efficiently manage book inventories, student records, and the day-to-day transactions of issuing and returning books.

## 2. 🎯 Project Explanation
Traditionally, libraries rely on physical ledgers or Excel sheets to track which student has borrowed which book and when it is due. This manual process is prone to errors, data loss, and makes it incredibly difficult to track overdue books. 

This system completely automates that workflow. By logging into the secure admin portal, a librarian can instantly see the total number of books, registered students, and active book issues. The system automatically calculates due dates, flags overdue books in red, and provides instant, as-you-type search functionality to locate specific books or students in seconds without reloading the page.

## 3. ⚙️ How It Works (Working Mechanism)
1. **Authentication:** The librarian opens the application and is greeted by a secure login screen. Only authorized admin personnel can access the system.
2. **Dashboard Overview:** Upon login, the system calculates real-time statistics (Total Books, Total Students, Issued Books, Overdue Books) and displays a quick-glance table of recently issued books.
3. **Inventory Management:** The librarian can navigate to the "Books" section to add new arrivals, edit quantities, or remove lost/damaged books.
4. **Student Registration:** Before a student can borrow a book, the librarian registers them in the "Students" section with their course and contact details.
5. **Issue & Return Flow:** 
   - **Issue:** The librarian selects a book, selects a student, specifies the due duration, and clicks "Issue". The system automatically deducts `1` from the book's available quantity.
   - **Return:** When the student brings the book back, the librarian clicks "Return". The system logs the return date, moves the record to the Return History, and increments the book's available quantity back by `1`.

## 4. 🧩 Core Modules
The project is divided into 5 logically separated modules:
* **Authentication Module:** Handles secure login and logout using Django's built-in session-based authentication.
* **Dashboard Module:** Acts as the analytical hub, aggregating data from all tables to display actionable metrics and quick links.
* **Book Management Module:** Handles full CRUD (Create, Read, Update, Delete) operations for the library's catalog. Tracks total vs. available quantities.
* **Student Management Module:** Handles CRUD operations for library members, tracking their enrolled courses and active book counts.
* **Transaction Module (Issue/Return):** The core operational module that links Books and Students together via Foreign Keys, tracks issue/due dates, and maintains a historical log of returned books.

## 5. ✨ Key Features
* **Secure Admin Access:** Protected routes that redirect unauthenticated users.
* **Real-time Availability Tracking:** Prevents issuing out-of-stock books.
* **Dynamic JavaScript Search:** Instantly filters tables by name, author, or category as you type.
* **Overdue Highlights:** Automatically compares due dates with the current date and highlights overdue rows in red.
* **Flash Messages (Toasts):** Provides immediate visual feedback (success/error) for actions like adding or deleting records.
* **Delete Confirmation Modals:** Prevents accidental data deletion with a secure popup warning.
* **Responsive UI:** Clean, modern, and sidebar-driven interface that works across laptops and tablets.
* **Pre-seeded Fake Data:** Comes with a Python script to instantly generate 65+ realistic books and 15 students for immediate demonstration.

## 6. 💻 Technology Stack
* **Frontend (Client-Side):**
  * **HTML5:** Semantic structure.
  * **CSS3:** Custom Vanilla CSS (No Bootstrap) utilizing CSS Variables, Flexbox, and CSS Grid for a modern, glass-like UI.
  * **JavaScript (Vanilla):** DOM manipulation for live search, modals, and password toggles.
  * **FontAwesome 6:** Scalable vector icons.
  * **Google Fonts:** "Inter" typeface for modern typography.
* **Backend (Server-Side):**
  * **Python 3.9+:** Core programming language.
  * **Django 4.2:** High-level web framework following the MVT (Model-View-Template) architectural pattern.
* **Database:**
  * **SQLite3:** Lightweight, file-based relational database included by default with Django.
* **Utilities:**
  * **Faker (Python Package):** Used in the seed script to generate realistic dummy data.

## 7. 🗂️ Project Structure
```text
library management/
├── manage.py                    ← Django command-line utility
├── requirements.txt             ← Project dependencies (Django, Faker)
├── seed_data.py                 ← Python script to auto-fill the database
├── setup.bat                    ← 1-click Windows automated setup script
├── README.md                    ← Project documentation
│
├── library_project/             ← Core Django Configuration
│   ├── settings.py              ← Global settings, installed apps, DB config
│   ├── urls.py                  ← Root URL routing
│   └── wsgi.py                  ← Web Server Gateway Interface
│
├── library/                     ← Main Application Logic
│   ├── models.py                ← Database tables (Book, Student, IssuedBook)
│   ├── views.py                 ← Business logic and HTTP response handling
│   ├── urls.py                  ← Application-specific route definitions
│   └── admin.py                 ← Django Admin panel configuration
│
├── templates/library/           ← Frontend HTML Views
│   ├── base.html                ← Master layout (sidebar, topbar, messages)
│   ├── dashboard.html           ← Main metrics screen
│   ├── books.html / students.html ← Listing tables
│   ├── issue_book.html          ← Transaction form
│   └── ...                      
│
└── static/                      ← Static Assets
    ├── css/style.css            ← Main stylesheet
    ├── css/sidebar.css          ← Sidebar specific styling
    └── js/main.js               ← Client-side interactivity
```

## 8. 🚀 Setup & Installation

### Prerequisites
* Python 3.9 or higher
* pip (Python package manager)

### Installation Steps (Windows)
**Option A — 1-Click Setup:**
Simply double click the `setup.bat` file. It will install dependencies, run migrations, and seed the database automatically.

**Option B — Manual Setup via Terminal:**
```bash
# 1. Install required packages
pip install -r requirements.txt

# 2. Create the database tables
python manage.py makemigrations library
python manage.py migrate

# 3. Populate database with dummy data
python seed_data.py

# 4. Start the development server
python manage.py runserver
```

### Accessing the Application
* **URL:** `http://127.0.0.1:8000`
* **Username:** `admin`
* **Password:** `admin123`

## 9. 🗄️ Database Schema (Models)
The system utilizes a relational database with three primary tables:

### 1. Book Table
| Field Name | Data Type | Description |
|------------|-----------|-------------|
| `name` | CharField | Title of the book |
| `author` | CharField | Writer's name |
| `category` | CharField | Dropdown choice (Fiction, Tech, etc.) |
| `quantity` | Integer | Total physical copies owned |
| `available` | Integer | Copies currently on the shelf |
| `added_date` | DateField | Auto-timestamp of creation |

### 2. Student Table
| Field Name | Data Type | Description |
|------------|-----------|-------------|
| `name` | CharField | Full name of the student |
| `email` | EmailField | Unique contact email |
| `course` | CharField | Academic program (BCA, MCA, etc.) |
| `phone` | CharField | Contact number |
| `enrollment_date` | DateField | Auto-timestamp of registration |

### 3. IssuedBook Table (Transaction / Mapping Table)
| Field Name | Data Type | Description |
|------------|-----------|-------------|
| `book` | ForeignKey | Links to the Book table |
| `student` | ForeignKey | Links to the Student table |
| `issue_date` | DateField | Day the book was borrowed |
| `due_date` | DateField | Deadline for returning |
| `return_date` | DateField | Actual day returned (Nullable) |
| `returned` | BooleanField | True if returned, False if active |

## 10. 🎓 Presentation & Viva Guide

### How to Present the Project (Demo Flow)
1. **Start at Login:** Show the login page. Explain that the system is protected and only authorized librarians can enter.
2. **Dashboard Impact:** Once logged in, immediately point out the 4 colorful stat cards. Mention how the system calculates "Overdue Books" dynamically.
3. **Demonstrate Search:** Go to the Books tab. Type a letter in the search bar to show how the table filters instantly using JavaScript, highlighting the user experience (UX).
4. **Issue a Book (The Core Logic):** 
   - Go to "Issue Book". 
   - Explain how the dropdown *only* shows books that have an `available > 0`.
   - Issue a book to a student.
5. **Show the Result:** 
   - Go back to the Books tab and show that the "Available" count dropped by 1.
   - Go to "Issued Books" to show the new active transaction.
6. **Return the Book:** Click "Return" on that transaction. Show how the book moves to the "Return History" tab and the inventory count goes back up.

### Common Viva Questions & Answers
**Q1: What architecture does Django follow?**
*Answer:* Django follows the MVT (Model-View-Template) architecture. The **Model** handles the database, the **View** handles the Python logic/URL routing, and the **Template** handles the HTML UI.

**Q2: Which database are you using and why?**
*Answer:* I am using SQLite3. It is a lightweight, file-based relational database that comes pre-packaged with Django. It is perfect for a college project because it requires no extra server configuration.

**Q3: How are the tables connected?**
*Answer:* The `IssuedBook` model uses **Foreign Keys** to connect to both the `Book` model and the `Student` model. This creates a Many-to-Many relationship between students and books, tracked by the transaction table.

**Q4: How does the system know a book is overdue?**
*Answer:* In the `models.py`, there is a Python property (`@property`) inside the `IssuedBook` class. It takes today's date (`date.today()`) and compares it against the `due_date` saved in the database. If today is greater than the due date and `returned` is False, it flags it as overdue.

**Q5: How did you implement the instant search without reloading the page?**
*Answer:* I used Vanilla JavaScript. An event listener watches the search input field. Every time a key is typed, it converts the text to lowercase and hides any HTML table rows (`<tr>`) that do not contain the matching text string.

---
*Developed as a BCA College Academic Project.*
