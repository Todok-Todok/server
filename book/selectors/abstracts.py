from abc import *
from django.shortcuts import get_object_or_404
from django.db.models.query import QuerySet
from book.models import Book,UserBook
from user.models import User

class AbstractBookSelector(metaclass=ABCMeta):
    @abstractmethod
    def get_userbook_by_user_id(user_id: int) -> "QuerySet[Book]":
        pass


class BookSelector(AbstractBookSelector):
    def get_userbook_by_user_id(user_id: int) -> "QuerySet[Book]":
        user = get_object_or_404(User, id=user_id)
        book_objects = UserBook.objects.filter(user=user).values_list("book",flat=True).order_by("book_id")
        books = Book.objects.filter(book_id__in = book_objects).order_by('book_id')
        return books