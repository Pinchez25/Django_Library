from django.urls import path
from .views import *

urlpatterns = [
    path('', index, name='index'),
    path('books/', BookListView.as_view(), name='books'),
    path('authors/', Authors.as_view(), name='authors'),
    path('author-details/<str:pk>', AuthorDetails.as_view(), name='author-details'),
    path('book/<str:pk>/', BookDetailView.as_view(), name='book-detail'),
    path('mybooks/', ListOfBorrowedBooksByUser.as_view(), name='my-borrowed-books'),
    path('book/<uuid:pk>/renew/', renew_book_librarian2, name='renew-book'),

    path('author/create/', AuthorCreate.as_view(), name='create-author'),
    path('author/<int:pk>/update/', AuthorUpdate.as_view(), name='update-author'),
    path('author/<str:pk>/delete/', AuthorDelete.as_view(), name='delete-author'),
]
