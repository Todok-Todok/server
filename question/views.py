from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .serializers import QuestionSerializer,UserQuestionSerializer
from .services import QuestionService
from .selectors.abstracts import QuestionSelector

# Business Layer인 서비스 로직만을 호출
class QuestionCreateView(APIView):
    def post(self, request, user_id, book_id):
        print(user_id)
        question=QuestionService(QuestionSelector).create_question(user_id,book_id,request.data["content"],request.data['disclosure'])
        return Response(status=status.HTTP_201_CREATED,data=QuestionSerializer(question).data)
    
    def get(self, request, user_id, book_id):
        questions = QuestionService(QuestionSelector).get_question(user_id,book_id)
        return Response(status=status.HTTP_200_OK, data=QuestionSerializer(questions, many=True).data)
        
# class QuestionShareView(APIView):
#     def post(self, request, *args, **kwargs):
        