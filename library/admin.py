from django.contrib import admin
from .models import Book, Student, IssuedBook


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ['name', 'author', 'category', 'quantity', 'available', 'added_date']
    search_fields = ['name', 'author']
    list_filter = ['category']


@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'course', 'enrollment_date']
    search_fields = ['name', 'email']
    list_filter = ['course']


@admin.register(IssuedBook)
class IssuedBookAdmin(admin.ModelAdmin):
    list_display = ['book', 'student', 'issue_date', 'due_date', 'returned']
    list_filter = ['returned']
    search_fields = ['book__name', 'student__name']
