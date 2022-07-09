from django.db.models import *
import uuid
from datetime import date
# Create your models here.
from django.urls import reverse
from django.contrib.auth.models import User


class Genre(Model):
    name = CharField(max_length=200, help_text="Enter a book genre (e.g. SciFi)")

    def __str__(self):
        return self.name


class Book(Model):
    title = CharField(max_length=200)
    author = ForeignKey('Author', on_delete=SET_NULL, null=True)
    summary = TextField(max_length=1000, help_text='Enter a brief description of the book')
    isbn = CharField('ISBN', max_length=13, unique=True, help_text='13 Character <a '
                                                                   'href="https://www.isbn-international.org/content'
                                                                   '/what-isbn">ISBN number</a>')
    genre = ManyToManyField(Genre, help_text='Select a genre for this book')

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        """ Returns url to access a detail record for this book """
        return reverse('book-detail', args=[str(self.id)])

    def display_genre(self):
        return ', '.join(genre.name for genre in self.genre.all()[:3])

    display_genre.short_description = 'Genre'

    class Meta:
        ordering = ['title']


class BookInstance(Model):
    LOAN_STATUS = (
        ('m', 'Maintenance'),
        ('o', 'On Loan'),
        ('a', 'Available'),
        ('r', 'Reserved'),
    )
    id = UUIDField(primary_key=True, default=uuid.uuid4, help_text='Unique id for this book across entire library')
    book = ForeignKey('Book', on_delete=RESTRICT, null=True)
    imprint = CharField(max_length=200)
    borrower = ForeignKey(User, on_delete=SET_NULL, null=True, blank=True)
    due_back = DateField(null=True, blank=True)
    status = CharField(max_length=1, choices=LOAN_STATUS, blank=True, default='m', help_text='Book availability')

    class Meta:
        ordering = ['due_back']
        # NB: The current user's permissions are stored in a template variable called {{ perms }}
        """
          Check whether the current user has a particular permission using the
          specific variable name associated with the django "app"
          e.g. {{ perms.catalog.can_mark_returned }}
          
          
          Permissions can be tested in a view (FBV) using the permission required decorator
          or in a CBV using PermissionRequiredMixin. See views.py
        """
        permissions = (('can_mark_returned', "Set book as returned"),)

    def __str__(self):
        return f'{self.id} ({self.book.title})'

    @property
    def is_overdue(self):
        if self.due_back and date.today() > self.due_back:
            return True
        return False


class Author(Model):
    first_name = CharField(max_length=100)
    last_name = CharField(max_length=100)
    date_of_birth = DateField(null=True, blank=True)
    date_of_death = DateField('Died', null=True, blank=True)


    class Meta:
        ordering = ['last_name', 'first_name']

    def get_absolute_url(self):
        return reverse('author-detail', args=[str(self.id)])

    def __str__(self):
        return f'{self.first_name} {self.last_name}'
