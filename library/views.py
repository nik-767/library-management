from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from datetime import date, timedelta
from .models import Book, Student, IssuedBook


# ─────────────────────────────────────────────
# Authentication
# ─────────────────────────────────────────────

def login_view(request):
    """Admin login page."""
    if request.user.is_authenticated:
        return redirect('dashboard')

    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        password = request.POST.get('password', '').strip()
        user = authenticate(request, username=username, password=password)
        if user is not None and user.is_staff:
            login(request, user)
            messages.success(request, f'Welcome back, {user.first_name or user.username}!')
            return redirect('dashboard')
        else:
            messages.error(request, 'Invalid credentials or insufficient permissions.')

    return render(request, 'library/login.html')


def logout_view(request):
    """Admin logout."""
    logout(request)
    messages.info(request, 'You have been logged out.')
    return redirect('login')


# ─────────────────────────────────────────────
# Dashboard
# ─────────────────────────────────────────────

@login_required
def dashboard(request):
    """Main dashboard with summary stats."""
    total_books = Book.objects.count()
    total_students = Student.objects.count()
    issued_books = IssuedBook.objects.filter(returned=False).count()
    overdue_books = sum(1 for ib in IssuedBook.objects.filter(returned=False) if ib.is_overdue)
    recent_issues = IssuedBook.objects.filter(returned=False).select_related('book', 'student')[:5]

    context = {
        'total_books': total_books,
        'total_students': total_students,
        'issued_books': issued_books,
        'overdue_books': overdue_books,
        'recent_issues': recent_issues,
    }
    return render(request, 'library/dashboard.html', context)


# ─────────────────────────────────────────────
# Book Management
# ─────────────────────────────────────────────

@login_required
def book_list(request):
    """List and search books."""
    query = request.GET.get('q', '').strip()
    books = Book.objects.all()
    if query:
        books = books.filter(
            Q(name__icontains=query) |
            Q(author__icontains=query) |
            Q(category__icontains=query)
        )
    return render(request, 'library/books.html', {'books': books, 'query': query})


@login_required
def add_book(request):
    """Add a new book."""
    if request.method == 'POST':
        name = request.POST.get('name', '').strip()
        author = request.POST.get('author', '').strip()
        category = request.POST.get('category', 'Fiction').strip()
        quantity = int(request.POST.get('quantity', 1))

        if not name or not author:
            messages.error(request, 'Book name and author are required.')
            return redirect('add_book')

        Book.objects.create(
            name=name,
            author=author,
            category=category,
            quantity=quantity,
            available=quantity
        )
        messages.success(request, f'Book "{name}" added successfully!')
        return redirect('book_list')

    return render(request, 'library/add_book.html', {'categories': Book.CATEGORY_CHOICES})


@login_required
def edit_book(request, pk):
    """Edit an existing book."""
    book = get_object_or_404(Book, pk=pk)

    if request.method == 'POST':
        book.name = request.POST.get('name', '').strip()
        book.author = request.POST.get('author', '').strip()
        book.category = request.POST.get('category', book.category).strip()
        quantity = int(request.POST.get('quantity', book.quantity))
        diff = quantity - book.quantity
        book.quantity = quantity
        book.available = max(0, book.available + diff)
        book.save()
        messages.success(request, f'Book "{book.name}" updated successfully!')
        return redirect('book_list')

    return render(request, 'library/edit_book.html', {
        'book': book,
        'categories': Book.CATEGORY_CHOICES
    })


@login_required
def delete_book(request, pk):
    """Delete a book."""
    book = get_object_or_404(Book, pk=pk)
    if request.method == 'POST':
        name = book.name
        book.delete()
        messages.success(request, f'Book "{name}" deleted successfully!')
    return redirect('book_list')


# ─────────────────────────────────────────────
# Student Management
# ─────────────────────────────────────────────

@login_required
def student_list(request):
    """List and search students."""
    query = request.GET.get('q', '').strip()
    students = Student.objects.all()
    if query:
        students = students.filter(
            Q(name__icontains=query) |
            Q(email__icontains=query) |
            Q(course__icontains=query)
        )
    return render(request, 'library/students.html', {'students': students, 'query': query})


@login_required
def add_student(request):
    """Add a new student."""
    if request.method == 'POST':
        name = request.POST.get('name', '').strip()
        email = request.POST.get('email', '').strip()
        course = request.POST.get('course', 'BCA').strip()
        phone = request.POST.get('phone', '').strip()

        if not name or not email:
            messages.error(request, 'Name and email are required.')
            return redirect('add_student')

        if Student.objects.filter(email=email).exists():
            messages.error(request, 'A student with this email already exists.')
            return redirect('add_student')

        Student.objects.create(name=name, email=email, course=course, phone=phone)
        messages.success(request, f'Student "{name}" added successfully!')
        return redirect('student_list')

    return render(request, 'library/add_student.html', {'courses': Student.COURSE_CHOICES})


@login_required
def edit_student(request, pk):
    """Edit an existing student."""
    student = get_object_or_404(Student, pk=pk)

    if request.method == 'POST':
        student.name = request.POST.get('name', '').strip()
        student.email = request.POST.get('email', '').strip()
        student.course = request.POST.get('course', student.course).strip()
        student.phone = request.POST.get('phone', '').strip()
        student.save()
        messages.success(request, f'Student "{student.name}" updated successfully!')
        return redirect('student_list')

    return render(request, 'library/edit_student.html', {
        'student': student,
        'courses': Student.COURSE_CHOICES
    })


@login_required
def delete_student(request, pk):
    """Delete a student."""
    student = get_object_or_404(Student, pk=pk)
    if request.method == 'POST':
        name = student.name
        student.delete()
        messages.success(request, f'Student "{name}" deleted successfully!')
    return redirect('student_list')


# ─────────────────────────────────────────────
# Issue & Return System
# ─────────────────────────────────────────────

@login_required
def issued_books(request):
    """List all issued books."""
    issues = IssuedBook.objects.filter(returned=False).select_related('book', 'student')
    return render(request, 'library/issued_books.html', {'issues': issues})


@login_required
def issue_book(request):
    """Issue a book to a student."""
    books = Book.objects.filter(available__gt=0)
    students = Student.objects.all()

    if request.method == 'POST':
        book_id = request.POST.get('book')
        student_id = request.POST.get('student')
        due_days = int(request.POST.get('due_days', 14))

        book = get_object_or_404(Book, pk=book_id)
        student = get_object_or_404(Student, pk=student_id)

        if book.available <= 0:
            messages.error(request, 'This book is not available.')
            return redirect('issue_book')

        # Check if student already has this book
        if IssuedBook.objects.filter(book=book, student=student, returned=False).exists():
            messages.error(request, f'{student.name} already has "{book.name}" issued.')
            return redirect('issue_book')

        IssuedBook.objects.create(
            book=book,
            student=student,
            due_date=date.today() + timedelta(days=due_days)
        )
        book.available -= 1
        book.save()
        messages.success(request, f'"{book.name}" issued to {student.name} successfully!')
        return redirect('issued_books')

    return render(request, 'library/issue_book.html', {'books': books, 'students': students})


@login_required
def return_book(request, pk):
    """Return an issued book."""
    issued = get_object_or_404(IssuedBook, pk=pk, returned=False)
    if request.method == 'POST':
        issued.returned = True
        issued.return_date = date.today()
        issued.save()
        issued.book.available += 1
        issued.book.save()
        messages.success(request, f'"{issued.book.name}" returned successfully!')
    return redirect('issued_books')


@login_required
def return_history(request):
    """Show all returned books."""
    history = IssuedBook.objects.filter(returned=True).select_related('book', 'student')
    return render(request, 'library/return_history.html', {'history': history})
