from django.db import models


class Book(models.Model):
    """Model representing a book in the library."""
    CATEGORY_CHOICES = [
        ('Fiction', 'Fiction'),
        ('Non-Fiction', 'Non-Fiction'),
        ('Science', 'Science'),
        ('Technology', 'Technology'),
        ('History', 'History'),
        ('Mathematics', 'Mathematics'),
        ('Literature', 'Literature'),
        ('Philosophy', 'Philosophy'),
        ('Biography', 'Biography'),
        ('Self-Help', 'Self-Help'),
    ]

    name = models.CharField(max_length=255)
    author = models.CharField(max_length=255)
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES, default='Fiction')
    quantity = models.PositiveIntegerField(default=1)
    available = models.PositiveIntegerField(default=1)
    added_date = models.DateField(auto_now_add=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return f"{self.name} by {self.author}"

    @property
    def is_available(self):
        return self.available > 0


class Student(models.Model):
    """Model representing a student."""
    COURSE_CHOICES = [
        ('BCA', 'BCA'),
        ('BBA', 'BBA'),
        ('B.Com', 'B.Com'),
        ('B.Sc', 'B.Sc'),
        ('B.Tech', 'B.Tech'),
        ('MBA', 'MBA'),
        ('MCA', 'MCA'),
        ('M.Sc', 'M.Sc'),
    ]

    name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    course = models.CharField(max_length=50, choices=COURSE_CHOICES, default='BCA')
    phone = models.CharField(max_length=15, blank=True, null=True)
    enrollment_date = models.DateField(auto_now_add=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return f"{self.name} ({self.course})"

    @property
    def issued_books_count(self):
        return self.issuedbook_set.filter(returned=False).count()


class IssuedBook(models.Model):
    """Model representing a book issued to a student."""
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    issue_date = models.DateField(auto_now_add=True)
    due_date = models.DateField()
    return_date = models.DateField(null=True, blank=True)
    returned = models.BooleanField(default=False)

    class Meta:
        ordering = ['-issue_date']

    def __str__(self):
        return f"{self.book.name} -> {self.student.name}"

    @property
    def is_overdue(self):
        from datetime import date
        if not self.returned:
            return date.today() > self.due_date
        return False
