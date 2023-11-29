# <INSERT, UPDATE, DELETE 쿼리와 여러 비즈니스 로직들이 수행되는 Service 예시>
from .models import Question, UserQuestion
from book.models import Book
from user.models import User
from django.db import transaction
from typing import Optional
from .selectors.abstracts import QuestionSelector
from django.db.models.query import QuerySet

from django.shortcuts import get_object_or_404
#<selector 의존성 주입 예시>
class QuestionService:
    def __init__(self, selector: QuestionSelector):
        self.selector = selector
        
    @transaction.atomic 
    def create_question(self, user_id: int, book_id: int, content: str, disclosure: Optional[bool] = None) -> Question:
        book=get_object_or_404(Book,book_id=book_id)
        question=Question.objects.create(book=book,content=content,disclosure=disclosure)
        user=get_object_or_404(User,user_id=user_id)
        UserQuestion.objects.create(question=question,book=book,user=user,q_owner=True)
        transaction.on_commit()
        return question
        
    def get_question(self, user_id: int, book_id: int) -> "QuerySet[UserQuestion]":
        userquestions = self.selector.get_user_question(user_id=user_id,book_id=book_id)
        return userquestions
    
    @transaction.atomic 
    def update_question(self, question_id: int, content: str, disclosure: Optional[str] = None) -> Question:
        question = self.selector.get_question_by_id(question_id=question_id)
        question.content = content
        question.disclosure = disclosure
        question.save()
        transaction.on_commit()
        return question