from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .serializers import QuestionSerializer, QuestionDetailSerializer
from .services import QuestionService
from .selectors.abstracts import QuestionSelector

# Business Layer인 서비스 로직만을 호출
class QuestionCreateView(APIView):
    def post(self, request, user_id, book_id):
        question=QuestionService(QuestionSelector).create_question(user_id,book_id,request.data["content"],request.data['disclosure'])
        return Response(status=status.HTTP_201_CREATED,data=QuestionSerializer(question).data)
    
    # q_owner=False 일 때만 like 여부 포함해서 response 보내주기
    # q_owner 여부에 따라 구분한 Dict 형태로 response 보내주기
    def get(self, request, user_id, book_id):
        my_questions = QuestionService(QuestionSelector).get_my_question(user_id,book_id)
        received_questions = QuestionService(QuestionSelector).get_received_question(user_id,book_id)
        return Response({"my_questions":my_questions,"received_questions":received_questions}, status=status.HTTP_200_OK)
        
class QuestionShareView(APIView):
    def post(self, request, question_id):
        QuestionService(QuestionSelector).share_question(question_id)
        return Response(status=status.HTTP_200_OK)
    
class QuestionReceiveView(APIView):
    def get(self, request, book_id):
        try:
            samplelist = QuestionService(QuestionSelector).receive_question(book_id)
            return Response(samplelist, status=status.HTTP_200_OK)
        except ValueError:
            return Response(status=status.HTTP_204_NO_CONTENT)
        
class QuestionSaveView(APIView):
    def post(self, request, question_id, user_id):
        try:
            QuestionService(QuestionSelector).save_question(user_id,question_id)
        except ValueError:
            return Response(status=status.HTTP_208_ALREADY_REPORTED)
        return Response(status=status.HTTP_200_OK)
    
class QuestionContentView(APIView):
    def post(self, request, user_id, question_id):
        QuestionService(QuestionSelector).update_question(user_id, question_id,request.data["opinion"])
        return Response(status=status.HTTP_200_OK)
    
    # 공유 받은 질문에 대한 내 생각
    def get(self, request, user_id, question_id):
        userquestion = QuestionService(QuestionSelector).get_each_userquestion_info(user_id,question_id)
        serializer = QuestionDetailSerializer(userquestion.question)
        responsebody = {'opinion': userquestion.opinion}
        responsebody.update(serializer.data)
        return Response(responsebody, status=status.HTTP_200_OK)

class SharedQuestionReactionView(APIView):
    def get(self, request, question_id):
        content_and_reactions = QuestionService(QuestionSelector).get_each_shared_question_reaction(question_id)
        return Response({"content":content_and_reactions[0],"reactions":content_and_reactions[1]}, status=status.HTTP_200_OK)
    
    def post(self, request, question_id):
        updated = QuestionService(QuestionSelector).update_like(request.data['userquestion_id'])
        return Response(updated, status=status.HTTP_200_OK)