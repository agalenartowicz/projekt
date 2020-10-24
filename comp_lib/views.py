from django.shortcuts import render, get_object_or_404, redirect, reverse
from django.contrib.auth import get_user_model, authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin, UserPassesTestMixin
from django.views import View
from .models import Book, HistoricalRecords
from django.contrib.auth.models import User, Permission
from .forms import BookSearchForm, BookAddForm, AddUserForm, LoginForm
from django.views.generic import DetailView, DeleteView, ListView
from datetime import date


class LibraryView(View):

    def get(self, request):
        num_books = Book.objects.all().count()
        num_books_available = Book.objects.filter(is_available=True).count()
        return render(request, "index.html", {
            "num_books": num_books,
            "num_books_available": num_books_available}
                      )


class BookListView(View):
    def get(self, request):
        books = Book.objects.all()
        return render(request, "books.html", {"books": books})


class BookSearchView(View):

    def get(self, request):
        form = BookSearchForm()
        ctx = {
            "form": form,
        }
        return render(request, "book_search.html", ctx)

    def post(self, request):
        form = BookSearchForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data["name"]
            results = Book.objects.filter(name__icontains=name)
            ctx = {
                "form": form,
                "results": results,
            }
            return render(request, "book_search.html", ctx)


class BookDetailView(View):

    def get(self, request, book_id):
        book = get_object_or_404(Book, id=book_id)
        ctx = {
            "book": book,
        }
        return render(request, "book.html", ctx)

    def post(self, request, book_id):
        if request.POST.get('loan'):
            book = get_object_or_404(Book, id=book_id)
            current_user = request.user
            book.is_available = False
            book.borrower = current_user
            book.borrowed_on = date.today()
            book.save()
            return redirect("book", book_id=book.id)
        elif request.POST.get('return'):
            book = get_object_or_404(Book, id=book_id)
            book.is_available = True
            book.borrower = None
            book.borrowed_on = None
            book.save()
            return redirect("book", book_id=book.id)


class BookAddView(View, UserPassesTestMixin):

    def test_func(self):
        return self.request.user.is_superuser

    def get(self, request):
        if request.user.is_superuser:
            form = BookAddForm()
            return render(request, "book_add.html", {"form": form})
        else:
            return redirect("books")

    def post(self, request):
        form = BookAddForm(request.POST)
        if form.is_valid():
            book = Book.objects.create(
                number=form.cleaned_data["number"],
                name=form.cleaned_data["name"]
            )
            return redirect("book", book_id=book.id)
        return render(request, "book_add.html", {"form": form})


class BookDeleteView(DeleteView, UserPassesTestMixin):
    model = Book
    template_name = "book_delete.html"
    pk_url_kwarg = "book_id"

    def test_func(self):
        return self.request.user.is_superuser

    def get_context_data(self, **kwargs):
            book_id = self.kwargs["book_id"]
            context = super().get_context_data(**kwargs)
            context["book"] = get_object_or_404(Book, pk=book_id)
            return context

    def get_success_url(self):
        return reverse("books")


class AddUserView(View):

    def get(self, request):
        form = AddUserForm()
        return render(request, "add_user.html", {"form": form})

    def post(self, request):
        form = AddUserForm(request.POST)
        if form.is_valid():
            form.cleaned_data.pop("password2")
            user = get_user_model().objects.create_user(**form.cleaned_data)
            return redirect("/")
        return render(request, "add_user.html", {"form": form})


class LoginView(View):

    def get(self, request):
        form = LoginForm()
        return render(request, "login.html", {"form": form})

    def post(self, request):
        form = LoginForm(request.POST)
        if form.is_valid():
            user = authenticate(**form.cleaned_data)
            if user is not None:
                login(request, user)
                return redirect("/")
        return render(request, "login.html", {"form": form})


class LogoutView(View):
    def get(self, request):
        if request.user.is_authenticated:
            logout(request)
        return redirect("/")


class LoanedBooksByUserListView(LoginRequiredMixin, ListView):

    model = Book
    template_name = 'list_loaned_user.html'

    def get_queryset(self):
        return Book.objects.filter(borrower=self.request.user)


class AvailableBooksListView(ListView):

    model = Book
    template_name = 'list_available.html'

    def get_queryset(self):
        return Book.objects.filter(is_available=True)


class LoanedBooksListView(ListView):

    model = Book
    template_name = 'list_loaned.html'

    def get_queryset(self):
        return Book.objects.filter(is_available=False)


class BookHistoryListView(ListView):
    template_name = "history.html"

    def get_queryset(self):
        history = Book.history.all()
        return history


class BookDetailHistoryListView(ListView):
    template_name = "book_history.html"
    context_object_name = 'book_history'

    def get_queryset(self):
        book_history = Book.history.filter(id=self.kwargs['book_id'])
        return book_history












