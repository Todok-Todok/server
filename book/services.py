from book.models import Book,UserBook
from .selectors.abstracts import BookSelector
from django.db.models.query import QuerySet
from typing import List, Tuple, Optional
        
class BookService:
    def __init__(self, selector:BookSelector):
        self.selector=selector
        
    def get_mybooks(self,user_id: int) -> "QuerySet[Book]":
        mybooks = self.selector.get_books_by_user_id(user_id=user_id)
        return mybooks
    
    def remove_book(self, user_id:int, book_id:int) -> None:
        userbook=self.selector.get_userbook(user_id=user_id, book_id=book_id)
        userbook.delete()
        return None
    
    def update_status_main(self, user_id:int, book_id:int) -> None:
        userbook=self.selector.get_userbook(user_id=user_id, book_id=book_id)
        userbook.status=0
        userbook.save()
        return None
    
    # 리스트 안의 튜플 여러 개로 리턴됨.
    def get_titles(self, user_id: int) -> List[Optional[Tuple[int,str]]]:
        mybooks = self.selector.get_books_by_user_id(user_id=user_id)
        book_objects = mybooks.values_list("book_id","title")
        return book_objects
        
    
    
    