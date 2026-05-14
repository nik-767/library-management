"""
Seed script to populate the database with fake data.
Run with: python seed_data.py
"""
import os
import sys
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'library_project.settings')
django.setup()

from django.contrib.auth.models import User
from library.models import Book, Student, IssuedBook
from datetime import date, timedelta
import random

# ──────────────────────────────────────────────────────────
# Create superuser admin
# ──────────────────────────────────────────────────────────
if not User.objects.filter(username='admin').exists():
    User.objects.create_superuser(
        username='admin',
        password='admin123',
        email='admin@library.com',
        first_name='Library',
        last_name='Admin',
        is_staff=True
    )
    print("✅ Admin user created: admin / admin123")
else:
    print("ℹ️  Admin user already exists.")

# ──────────────────────────────────────────────────────────
# Fake Books Data (60+ books)
# ──────────────────────────────────────────────────────────
books_data = [
    # Technology
    ("Python Crash Course", "Eric Matthes", "Technology"),
    ("Clean Code", "Robert C. Martin", "Technology"),
    ("The Pragmatic Programmer", "David Thomas", "Technology"),
    ("Introduction to Algorithms", "Thomas H. Cormen", "Technology"),
    ("Design Patterns", "Gang of Four", "Technology"),
    ("Django for Beginners", "William S. Vincent", "Technology"),
    ("JavaScript: The Good Parts", "Douglas Crockford", "Technology"),
    ("You Don't Know JS", "Kyle Simpson", "Technology"),
    ("Computer Networks", "Andrew S. Tanenbaum", "Technology"),
    ("Operating System Concepts", "Abraham Silberschatz", "Technology"),
    ("Database System Concepts", "Henry F. Korth", "Technology"),
    ("Artificial Intelligence", "Stuart Russell", "Technology"),
    ("Machine Learning Yearning", "Andrew Ng", "Technology"),
    ("Deep Learning", "Ian Goodfellow", "Technology"),
    ("Data Structures Using C", "Reema Thareja", "Technology"),

    # Science
    ("A Brief History of Time", "Stephen Hawking", "Science"),
    ("The Selfish Gene", "Richard Dawkins", "Science"),
    ("Cosmos", "Carl Sagan", "Science"),
    ("The Origin of Species", "Charles Darwin", "Science"),
    ("Sapiens", "Yuval Noah Harari", "Science"),
    ("The Grand Design", "Stephen Hawking", "Science"),
    ("Surely You're Joking, Mr. Feynman!", "Richard Feynman", "Science"),
    ("The Elegant Universe", "Brian Greene", "Science"),
    ("Seven Brief Lessons on Physics", "Carlo Rovelli", "Science"),

    # Mathematics
    ("Introduction to Linear Algebra", "Gilbert Strang", "Mathematics"),
    ("Calculus Made Easy", "Silvanus P. Thompson", "Mathematics"),
    ("The Man Who Knew Infinity", "Robert Kanigel", "Mathematics"),
    ("Mathematics: Its Content, Methods and Meaning", "A.D. Aleksandrov", "Mathematics"),
    ("Discrete Mathematics", "Kenneth H. Rosen", "Mathematics"),
    ("How to Solve It", "George Polya", "Mathematics"),
    ("Probability and Statistics", "Morris H. DeGroot", "Mathematics"),

    # Fiction
    ("To Kill a Mockingbird", "Harper Lee", "Fiction"),
    ("1984", "George Orwell", "Fiction"),
    ("The Great Gatsby", "F. Scott Fitzgerald", "Fiction"),
    ("Harry Potter and the Sorcerer's Stone", "J.K. Rowling", "Fiction"),
    ("The Alchemist", "Paulo Coelho", "Fiction"),
    ("The Hitchhiker's Guide to the Galaxy", "Douglas Adams", "Fiction"),
    ("Animal Farm", "George Orwell", "Fiction"),
    ("Brave New World", "Aldous Huxley", "Fiction"),
    ("The Catcher in the Rye", "J.D. Salinger", "Fiction"),
    ("Lord of the Flies", "William Golding", "Fiction"),
    ("The Da Vinci Code", "Dan Brown", "Fiction"),

    # History
    ("Guns, Germs, and Steel", "Jared Diamond", "History"),
    ("The Diary of a Young Girl", "Anne Frank", "History"),
    ("A People's History of the United States", "Howard Zinn", "History"),
    ("India After Gandhi", "Ramachandra Guha", "History"),
    ("Discovery of India", "Jawaharlal Nehru", "History"),
    ("Glimpses of World History", "Jawaharlal Nehru", "History"),

    # Philosophy
    ("The Republic", "Plato", "Philosophy"),
    ("Meditations", "Marcus Aurelius", "Philosophy"),
    ("Thus Spoke Zarathustra", "Friedrich Nietzsche", "Philosophy"),
    ("The Art of War", "Sun Tzu", "Philosophy"),
    ("Think and Grow Rich", "Napoleon Hill", "Philosophy"),

    # Self-Help
    ("Atomic Habits", "James Clear", "Self-Help"),
    ("The Power of Now", "Eckhart Tolle", "Self-Help"),
    ("Rich Dad Poor Dad", "Robert Kiyosaki", "Self-Help"),
    ("The 7 Habits of Highly Effective People", "Stephen R. Covey", "Self-Help"),
    ("How to Win Friends and Influence People", "Dale Carnegie", "Self-Help"),
    ("The Subtle Art of Not Giving a F*ck", "Mark Manson", "Self-Help"),
    ("Deep Work", "Cal Newport", "Self-Help"),

    # Biography
    ("Steve Jobs", "Walter Isaacson", "Biography"),
    ("Elon Musk", "Ashlee Vance", "Biography"),
    ("Long Walk to Freedom", "Nelson Mandela", "Biography"),
    ("Wings of Fire", "A.P.J. Abdul Kalam", "Biography"),
    ("My Experiments with Truth", "Mahatma Gandhi", "Biography"),

    # Literature
    ("Romeo and Juliet", "William Shakespeare", "Literature"),
    ("Hamlet", "William Shakespeare", "Literature"),
    ("Pride and Prejudice", "Jane Austen", "Literature"),
    ("Wuthering Heights", "Emily Bronte", "Literature"),
    ("Crime and Punishment", "Fyodor Dostoevsky", "Literature"),
]

# Clear existing books
Book.objects.all().delete()
print("🗑️  Cleared existing books.")

created_books = []
for name, author, category in books_data:
    qty = random.randint(1, 5)
    book = Book.objects.create(
        name=name,
        author=author,
        category=category,
        quantity=qty,
        available=qty
    )
    created_books.append(book)

print(f"✅ Created {len(created_books)} books.")

# ──────────────────────────────────────────────────────────
# Fake Students Data
# ──────────────────────────────────────────────────────────
students_data = [
    ("Aarav Sharma", "aarav.sharma@college.edu", "BCA", "9812345601"),
    ("Priya Patel", "priya.patel@college.edu", "BCA", "9812345602"),
    ("Rohit Verma", "rohit.verma@college.edu", "BBA", "9812345603"),
    ("Sneha Gupta", "sneha.gupta@college.edu", "B.Com", "9812345604"),
    ("Arjun Singh", "arjun.singh@college.edu", "BCA", "9812345605"),
    ("Kavya Nair", "kavya.nair@college.edu", "B.Sc", "9812345606"),
    ("Rahul Kumar", "rahul.kumar@college.edu", "BCA", "9812345607"),
    ("Ananya Joshi", "ananya.joshi@college.edu", "BBA", "9812345608"),
    ("Karan Mehta", "karan.mehta@college.edu", "B.Tech", "9812345609"),
    ("Deepika Rao", "deepika.rao@college.edu", "MCA", "9812345610"),
    ("Vikram Chaudhary", "vikram.chaudhary@college.edu", "BCA", "9812345611"),
    ("Pooja Mishra", "pooja.mishra@college.edu", "B.Com", "9812345612"),
    ("Aditya Pandey", "aditya.pandey@college.edu", "B.Tech", "9812345613"),
    ("Riya Kapoor", "riya.kapoor@college.edu", "BCA", "9812345614"),
    ("Saurabh Tiwari", "saurabh.tiwari@college.edu", "MBA", "9812345615"),
]

Student.objects.all().delete()
IssuedBook.objects.all().delete()
print("🗑️  Cleared existing students and issued books.")

created_students = []
for name, email, course, phone in students_data:
    student = Student.objects.create(name=name, email=email, course=course, phone=phone)
    created_students.append(student)

print(f"✅ Created {len(created_students)} students.")

# ──────────────────────────────────────────────────────────
# Create some sample issued books
# ──────────────────────────────────────────────────────────
sample_issues = [
    (0, 0, 7),   # (student_index, book_index, due_days)
    (1, 2, 14),
    (2, 5, 10),
    (3, 10, 14),
    (4, 15, 7),
    (5, 20, 14),
    (6, 25, 3),   # overdue
    (7, 30, -2),  # overdue
]

for student_idx, book_idx, due_days in sample_issues:
    if student_idx < len(created_students) and book_idx < len(created_books):
        student = created_students[student_idx]
        book = created_books[book_idx]
        if book.available > 0:
            IssuedBook.objects.create(
                book=book,
                student=student,
                due_date=date.today() + timedelta(days=due_days)
            )
            book.available -= 1
            book.save()

print(f"✅ Created sample issued books.")
print("\n" + "="*50)
print("🎉 Database seeded successfully!")
print("="*50)
print(f"   📚 Books: {Book.objects.count()}")
print(f"   👨‍🎓 Students: {Student.objects.count()}")
print(f"   📖 Issued: {IssuedBook.objects.filter(returned=False).count()}")
print(f"\n   🔑 Admin Login:")
print(f"      Username: admin")
print(f"      Password: admin123")
print("="*50)
