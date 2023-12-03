from abc import *
from django.shortcuts import get_object_or_404
from django.db.models.query import QuerySet
from book.models import Book,UserBook
from user.models import User

class AbstractBookSelector(metaclass=ABCMeta):
    @abstractmethod
    def get_books_by_user_id(user_id: int) -> "QuerySet[Book]":
        pass
    
    def get_userbook(user_id:int, book_id:int) -> UserBook:
        pass


class BookSelector(AbstractBookSelector):
    def get_books_by_user_id(user_id: int) -> "QuerySet[Book]":
        user = get_object_or_404(User, id=user_id)
        book_objects = UserBook.objects.filter(user=user).values_list("book",flat=True).order_by("book_id")
        books = Book.objects.filter(book_id__in = book_objects).order_by('book_id')
        return books
    def get_userbook(user_id:int, book_id:int) -> UserBook:
        user = get_object_or_404(User, id=user_id)
        book = get_object_or_404(Book, book_id=book_id)
        userbook = UserBook.objects.get(user=user,book=book)
        return userbook
        