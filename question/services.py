# <INSERT, UPDATE, DELETE 쿼리와 여러 비즈니스 로직들이 수행되는 Service 예시>
from .models import Question, UserQuestion
from book.models import Book
from user.models import User, Notification
from typing import Optional, List, Tuple
from .selectors.abstracts import QuestionSelector
from django.db.models.query import QuerySet
from .serializers import QuestionContentSerializer, UserQuestionReactionSerializer

from django.shortcuts import get_object_or_404

import random

#<selector 의존성 주입 예시>
class QuestionService:
    def __init__(self, selector: QuestionSelector):
        self.selector = selector
        
    def create_question(self, user_id: int, book_id: int, content: str, disclosure: Optional[bool] = None) -> Question:
        book=get_object_or_404(Book,book_id=book_id)
        question=Question.objects.create(book=book,content=content,disclosure=disclosure)
        user=get_object_or_404(User,id=user_id)
        UserQuestion.objects.create(question=question,book=book,user=user,q_owner=True)
        return question
        
    def get_my_question(self, user_id: int, book_id: int) -> Optional[List]:
        userquestions_mine = self.selector.get_user_question_mine(user_id=user_id,book_id=book_id)
        responsebody = []
        if userquestions_mine is not None:
            for userquestion in userquestions_mine:
                temp={}
                temp["content"]=userquestion.question.content
                temp["question_id"]=userquestion.question.question_id
                responsebody.append(temp)
            return responsebody
        else:
            return None
    
    def get_received_question(self, user_id: int, book_id: int) -> Optional[List]:
        userquestions_received = self.selector.get_user_question_received(user_id=user_id,book_id=book_id)
        if userquestions_received is not None:
            responsebody = []
            for userquestion in userquestions_received:
                temp={}
                temp["content"]=userquestion.question.content
                temp["question_id"]=userquestion.question.question_id
                temp["like"]=userquestion.like
                responsebody.append(temp)
            return responsebody
        else:
            return None
        
        
    def get_each_userquestion_info(self, user_id: int, question_id: int) -> UserQuestion:
        userquestion = self.selector.get_each_userquestion(user_id=user_id, question_id=question_id)
        return userquestion
    
    def update_question(self, user_id: int, question_id: int, update_opinion: Optional[str]="") -> None:
        userquestion = self.selector.get_each_userquestion(user_id=user_id, question_id=question_id)
        userquestion.opinion = update_opinion
        userquestion.save()
        return None
    
    def share_question(self, question_id:int) -> None:
        users = self.selector.get_users_by_question_id(question_id=question_id)
        question = get_object_or_404(Question, question_id=question_id)
        if question.disclosure == True:    
            noti_title = "<"+question.book.title+">를 같이 읽는 이웃으로부터 공유 질문이 들어왔어요 !"
            noti_content = question.content
            # 2명의 유저를 추출하여 질문 추천 알림 보내기
            user_sample = random.sample(list(users), 2)
            for user in user_sample:
                Notification.objects.create(user=user,title=noti_title, content=noti_content)
            return None
        else:
            raise ValueError("질문을 공개로 전환해야 공유가 가능합니다 !")
    
    def receive_question(self, book_id:int, user_id:int) -> List:
        questions = self.selector.get_question_queryset_by_userquestion(book_id=book_id,user_id=user_id)
        serializer = QuestionContentSerializer(questions, many=True)
        # 리스트에서 2개 랜덤 추출
        if len(questions) >= 2:
            samplelist = random.sample(list(serializer.data), 2)
            return samplelist
        else:
            raise ValueError("현재 등록된 질문 개수가 부족합니다 !")
            
    def save_question(self, user_id: int, question_id:int) -> None:
        question = self.selector.get_question_by_question_id(question_id=question_id)
        user = get_object_or_404(User,id=user_id)
        obj, created = UserQuestion.objects.get_or_create(book=question.book,user=user,question=question)
        if not created:
            raise ValueError("이미 등록된 질문입니다 !")
        else:
            return None
    
    def get_each_shared_question_reaction(self, question_id:int) -> Tuple[str,List]:
        question = get_object_or_404(Question, question_id=question_id)
        userquestions = self.selector.get_shared_question_by_question_id(question_id=question_id)
        serializer = UserQuestionReactionSerializer(userquestions, many=True)
        return (question.content, serializer.data)
    
    def update_like(self, userquestion_id:int) -> bool:
        userquestion = get_object_or_404(UserQuestion, id=userquestion_id)
        if userquestion.like == False:
            userquestion.like = True
        else:
            userquestion.like = False
        userquestion.save()
        return userquestion.like
            
