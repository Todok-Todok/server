# < 추상화 계층 >
from abc import *
from question.models import Question, UserQuestion
from django.shortcuts import get_object_or_404
from django.db.models.query import QuerySet
from book.models import Book
from user.models import User

class AbstractQuestionSelector(metaclass=ABCMeta):
    @abstractmethod
    def get_question_by_id(self, question_id: int) -> Question:
        pass

    @abstractmethod
    def get_question_queryset_by_book_id(self, book_id: int) -> "QuerySet[Question]":
        pass

# selectors/posts.py
class QuestionSelector(AbstractQuestionSelector):
    def get_question_by_id(self, question_id: int) -> Question:
        return Question.objects.filter(id=question_id, deleted_at__isnull=True).get()

    def get_user_question(self, user_id: int, book_id: int) -> "QuerySet[UserQuestion]":
        user = get_object_or_404(User, id=user_id)
        book = get_object_or_404(Book, id=book_id)
        return UserQuestion.objects.filter(user=user,book=book)
        
    def get_user_question_mine(self, user_id: int, book_id: int) -> "QuerySet[UserQuestion]":
        user = get_object_or_404(User, id=user_id)
        book = get_object_or_404(Book, id=book_id)
        return UserQuestion.objects.filter(user=user,book=book,q_owner=True)
    
    def get_question_queryset_by_book_id(self, book_id: int) -> "QuerySet[Question]":
        book = get_object_or_404(Book, id=book_id)
        return Question.objects.filter(book=book, deleted_at__isnull=True)