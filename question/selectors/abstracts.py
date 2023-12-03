# < 추상화 계층 >
from abc import *
from question.models import Question, UserQuestion
from django.shortcuts import get_object_or_404
from django.db.models.query import QuerySet
from book.models import Book, UserBook
from user.models import User

from typing import Optional

class AbstractQuestionSelector(metaclass=ABCMeta):
    @abstractmethod
    def get_user_question_received(user_id: int, book_id: int) -> "Optional[QuerySet[UserQuestion]]":
        pass
    
    @abstractmethod
    def get_user_question_mine(user_id: int, book_id: int) -> "Optional[QuerySet[UserQuestion]]":
        pass
    
    @abstractmethod
    def get_question_queryset_by_userquestion(book_id: int) -> "QuerySet[Question]":
        pass
    
    @abstractmethod
    def get_users_by_question_id(question_id: int) -> "QuerySet[User]":
        pass
    
    @abstractmethod
    def get_each_userquestion(user_id: int, question_id: int) -> UserQuestion:
        pass
    
    @abstractmethod
    def get_question_by_question_id(question_id:int) -> Question:
        pass
    
    @abstractmethod
    def get_shared_question_by_question_id(question_id:int) -> "QuerySet[UserQuestion]":
        pass
    
# selectors/posts.py
class QuestionSelector(AbstractQuestionSelector):
    def get_user_question_received(user_id: int, book_id: int) -> "Optional[QuerySet[UserQuestion]]":
        user = get_object_or_404(User, id=user_id)
        book = get_object_or_404(Book, book_id=book_id)
        return UserQuestion.objects.filter(user=user,book=book, q_owner=False)
        
    def get_user_question_mine(user_id: int, book_id: int) -> "Optional[QuerySet[UserQuestion]]":
        user = get_object_or_404(User, id=user_id)
        book = get_object_or_404(Book, book_id=book_id)
        return UserQuestion.objects.filter(user=user,book=book,q_owner=True)
    
    def get_question_queryset_by_userquestion(book_id: int) -> "QuerySet[Question]":
        book = get_object_or_404(Book, book_id=book_id)
        userquestions_objects = UserQuestion.objects.filter(book=book).values_list("question",flat=True).order_by("question_id")
        # disclosure = True 조건 추가 필요 !
        questions = Question.objects.filter(question_id__in = userquestions_objects).filter(disclosure=True).order_by('question_id')
        return questions
    
    def get_users_by_question_id(question_id: int) -> "QuerySet[User]":
        question = Question.objects.select_related('book').get(question_id=question_id)
        userbooks_objects = UserBook.objects.filter(book=question.book).values_list("user",flat=True)
        # 해당 책을 현재 읽고 있는 책으로 등록한 유저에 대해서만 질문을 보낼 수 있어야 함 !
        users = User.objects.filter(id__in = userbooks_objects).order_by('id')
        for user in users:
            if UserBook.objects.filter(user=user,book=question.book).filter(status__in = [2,3]).exists():
                users.remove(user)        
        return users
    
    def get_each_userquestion(user_id: int, question_id: int) -> UserQuestion:
        question = get_object_or_404(Question, question_id=question_id)
        user = get_object_or_404(User, id=user_id)
        userquestion = UserQuestion.objects.select_related('question').get(user=user, question=question)
        return userquestion
    
    def get_question_by_question_id(question_id:int) -> Question:
        question = Question.objects.select_related('book').get(question_id=question_id)
        return question
    
    def get_shared_question_by_question_id(question_id:int) -> "QuerySet[UserQuestion]":
       question = QuestionSelector.get_question_by_question_id(question_id=question_id)
       return UserQuestion.objects.select_related('user','question').filter(question=question,book=question.book,q_owner=False)
        