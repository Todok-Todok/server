from book.models import Book,UserBook
from .serializers import BookViewSerializer,BookTitleSerializer
from .selectors.abstracts import BookSelector
from django.db.models.query import QuerySet
from typing import List, Tuple, Optional,Dict
        
class BookService:
    def __init__(self, selector:BookSelector):
        self.selector=selector
        
    def get_mybooks(self,user_id: int) -> Dict[str,List]:
        responsebody={}
        mybooks = self.selector.get_books_by_user_id(user_id=user_id)
        for book in range(len(mybooks)):
            serializer=BookViewSerializer(mybooks[book],many=True)
            responsebody[str(book)]=serializer.data
        return responsebody
    
    def remove_book(self, user_id:int, book_id:int) -> None:
        userbook=self.selector.get_userbook(user_id=user_id, book_id=book_id)
        userbook.delete()
        return None
    
    def update_status_main(self, user_id:int, book_id:int) -> None:
        userbook = self.selector.update_main_book(user_id=user_id, book_id=book_id)
        if userbook is None:
            raise ValueError
        else:
            return None
    
    # 리스트 안의 튜플 여러 개로 리턴됨.
    def get_titles(self, user_id: int) -> List:
        mybooks = self.selector.get_booklist_by_user_id(user_id=user_id)
        book_objects = BookTitleSerializer(mybooks,many=True)
        return book_objects.data
       
    
    def get_main_book_id(self, user_id: int) -> Optional[int]:
        userbook = self.selector.get_main_book(user_id=user_id)
        if userbook is not None:
            return userbook.book.book_id
        else:
            return None

    def delete_main_book(self, user_id: int) -> None:
        userbook = self.selector.get_main_book(user_id=user_id)
        userbook.delete()
        return None
    
    
