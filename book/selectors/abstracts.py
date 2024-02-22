from abc import *
from django.shortcuts import get_object_or_404
from django.db.models.query import QuerySet
from book.models import Book,UserBook
from user.models import User
from typing import Dict, Optional, List

class AbstractBookSelector(metaclass=ABCMeta):
    @abstractmethod
    def get_books_by_user_id(user_id: int) -> "QuerySet[Book]":
        pass
    
    @abstractmethod
    def get_userbook(user_id:int, book_id:int) -> UserBook:
        pass

    @abstractmethod
    def get_booklist_by_user_id(user_id: int) -> "QuerySet[Book]":
        pass
    
    @abstractmethod
    def get_main_book(user_id:int) -> "Optional[UserBook]":
        pass

    @abstractmethod
    def update_main_book(user_id:int, book_id:int) -> "Optional[UserBook]":
        pass

class BookSelector(AbstractBookSelector):
    def get_books_by_user_id(user_id: int) -> "List[Queryset[Book]]":
        responsebody=[]
        user = get_object_or_404(User, id=user_id)
        for b_status in range(4):
            book_objects = UserBook.objects.filter(user=user,status=b_status).values_list("book",flat=True).order_by("book_id")
            books = Book.objects.filter(book_id__in = book_objects).order_by('book_id')
            responsebody.append(books)
        return responsebody

    def get_userbook(user_id:int, book_id:int) -> UserBook:
        user = get_object_or_404(User, id=user_id)
        book = get_object_or_404(Book, book_id=book_id)
        userbook = UserBook.objects.get(user=user,book=book)
        return userbook
        
    def get_booklist_by_user_id(user_id: int) -> "QuerySet[Book]":
        user = get_object_or_404(User, id=user_id)
        book_objects = UserBook.objects.filter(user=user).values_list("book",flat=True).order_by("book_id")
        books = Book.objects.filter(book_id__in = book_objects).order_by('book_id')
        return books

    def get_main_book(user_id:int) -> "Optional[UserBook]":
        user= get_object_or_404(User, id=user_id)
        try:
            userbook = UserBook.objects.select_related('book').get(user=user,status=0)
        except UserBook.DoesNotExist:
            userbook = None
        return userbook

    def update_main_book(user_id:int, book_id:int) -> "Optional[UserBook]":
        user = get_object_or_404(User, id=user_id)
        book = get_object_or_404(Book, book_id=book_id)
        if UserBook.objects.filter(user=user,status=0).exists():
            return None
        else:
            userbook=UserBook.objects.create(user=user,book=book,status=0)
            return userbook
