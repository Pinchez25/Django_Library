import datetime

from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic.detail import DetailView
from django.views.generic.edit import *
from django.views.generic.list import ListView
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib import messages
from .forms import RenewBookModelForm
from .models import *
from django.http import HttpResponseRedirect


class Authors(ListView):
    model = Author
    context_object_name = 'authors'
    template_name = 'catalog/authors.html'
    paginate_by = 2


class AuthorDetails(DetailView):
    model = Author
    context_object_name = 'author'
    template_name = 'catalog/author-details.html'


class AuthorCreate(SuccessMessageMixin, CreateView):
    model = Author
    fields = ['first_name', 'last_name', 'date_of_birth', 'date_of_death']
    initial = {'date_of_death': '11/06/2020'}
    template_name = 'catalog/create-update-author.html'
    success_url = reverse_lazy('authors')
    success_message = f' was created successfully'


class AuthorUpdate(UpdateView):
    model = Author
    fields = '__all__'
    template_name = 'catalog/create-update-author.html'
    success_url = reverse_lazy('authors')

    def form_valid(self, form):
        messages.success(self.request, "Update successful")
        return super(AuthorUpdate, self).form_valid(form)


class AuthorDelete(DeleteView):
    model = Author
    success_url = reverse_lazy('authors')
    template_name = 'catalog/delete-author.html'


# Create your views here.
@login_required
@permission_required('catalog.can_mark_returned')
def index(request):
    num_books = Book.objects.all().count()
    num_instances = BookInstance.objects.all().count()
    num_instances_available = BookInstance.objects.filter(status__exact='a').count()
    num_authors = Author.objects.count()  # all() is implied by default

    return render(request, 'catalog/index.html', {
        'num_books': num_books,
        'num_instances': num_instances,
        'num_instances_available': num_instances_available,
        'num_authors': num_authors,
    })


class BookListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    model = Book
    # queryset = Book.objects.filter(title__icontains='Harry')[:5]
    template_name = 'catalog/list.html'
    context_object_name = 'book_list'
    paginate_by = 2
    login_url = 'login'
    permission_required = ('catalog.can_mark_returned',)

    # redirect_field_name = None

    # override the queryset method
    def get_queryset(self):
        return Book.objects.all()
        # return Book.objects.filter(title__icontains='kidnap')

    # Overriding the context_data
    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(BookListView, self).get_context_data(**kwargs)
        context['num_of_books'] = Book.objects.count()
        return context

    # def get_permission_denied_message(self):
    #     return redirect(to='/')


class BookDetailView(DetailView):
    model = Book
    context_object_name = 'book'
    template_name = 'catalog/book-details.html'


class ListOfBorrowedBooksByUser(LoginRequiredMixin, ListView):
    model = BookInstance
    template_name = 'catalog/borrowed_books.html'
    paginate_by = 2
    context_object_name = 'borrowed'

    def get_queryset(self):
        return BookInstance.objects.filter(borrower=self.request.user).filter(status__exact='o').order_by('due_back')


# @login_required
# @permission_required('catalog.can_mark_returned', raise_exception=True)
# def renew_book_librarian(request, pk):
#     book_instance = get_object_or_404(BookInstance, pk=pk)
#     form = RenewBookForm()
#     if request.method == "POST":
#         form = RenewBookForm(request.POST)
#
#         if form.is_valid():
#             book_instance.due_back = form.cleaned_data.get('renewal_date')
#             book_instance.save()
#
#             return HttpResponseRedirect(reverse('my-borrowed-books'))
#
#         else:
#             proposed_renewal_date = datetime.date.today() + datetime.timedelta(weeks=3)
#             form = RenewBookForm(initial={'renewal_date': proposed_renewal_date})
#
#     return render(request, 'catalog/book_renewal.html', {
#         'form': form,
#         'book_instance': book_instance
#     })


@login_required
@permission_required('catalog.can_mark_returned', raise_exception=True)
def renew_book_librarian2(request, pk):
    book_instance = get_object_or_404(BookInstance, pk=pk)
    proposed_renewal_date = datetime.date.today() + datetime.timedelta(weeks=3)
    form = RenewBookModelForm(initial={'due_back': proposed_renewal_date})
    if request.method == "POST":
        form = RenewBookModelForm(request.POST)

        if form.is_valid():
            book_instance.due_back = form.cleaned_data.get('due_back')
            book_instance.save()

            return HttpResponseRedirect(reverse('my-borrowed-books'))

        else:
            form = RenewBookModelForm(initial={'due_back': proposed_renewal_date})

    return render(request, 'catalog/book_renewal.html', {
        'form': form,
        'book_instance': book_instance
    })
