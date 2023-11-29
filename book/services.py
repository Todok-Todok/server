from book.models import Book,UserBook
from .selectors.abstracts import BookSelector
from django.db.models.query import QuerySet

        
class BookService:
    def __init__(self, selector:BookSelector):
        self.selector=selector
        
    def get_mybooks(self,user_id: int) -> "QuerySet[Book]":
        mybooks = self.selector.get_userbook_by_user_id(user_id=user_id)
        return mybooks
    
    