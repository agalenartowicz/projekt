"""Company_library URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from comp_lib.views import LibraryView, BookListView, BookSearchView, BookDetailView, BookAddView, BookDeleteView,\
    AddUserView, LoginView, LogoutView, LoanedBooksByUserListView, AvailableBooksListView, LoanedBooksListView,\
    BookHistoryListView, BookDetailHistoryListView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', LibraryView.as_view(), name="library"),
    path('books/', BookListView.as_view(), name="books"),
    path('search/', BookSearchView.as_view(), name="book-search"),
    path('book/<int:book_id>', BookDetailView.as_view(), name="book"),
    path('add/', BookAddView.as_view(), name="book-add"),
    path("book/<int:book_id>/delete/", BookDeleteView.as_view(), name="book-delete"),
    path("add_user/", AddUserView.as_view(), name="add-user"),
    path("login/", LoginView.as_view(), name="login"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("my_books/", LoanedBooksByUserListView.as_view(), name="loaned-list"),
    path("available/", AvailableBooksListView.as_view(), name="available-list"),
    path("loans/", LoanedBooksListView.as_view(), name="list-loaned"),
    path("history/", BookHistoryListView.as_view(), name="history"),
    path("book/<int:book_id>/history/", BookDetailHistoryListView.as_view(), name="book-history"),

]
