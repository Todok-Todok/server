import secret
import requests
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from .serializers import BookSerializer,UserBookSerializer
from .models import Book, UserBook
from user.models import User
from django.shortcuts import get_object_or_404
from .services import BookService
from .selectors.abstracts import BookSelector

KAKAO_REST_API_KEY = secret.KAKAO_REST_API_KEY

# Create your views here.
class SearchAPIView(APIView):
    def get(self, request):
        book_name = request.data['book_name']
        headers = {"Authorization": "KakaoAK "+KAKAO_REST_API_KEY}
        doc = requests.get(
            f"https://dapi.kakao.com/v3/search/book?query={book_name}", headers=headers)
        doc = doc.json()
        #title #doc['documents'][0]['title']
        #author #', '.join(doc['documents'][0]['authors'])
        #book_image #doc['documents'][0]['thumbnail']
        #publisher #doc['documents'][0]['publisher']
        return Response(doc, status=status.HTTP_200_OK)
    

class AddUserBookAPIView(APIView):
    def post(self, request, b_status, user_id):
        user = get_object_or_404(User, id=user_id)
        serializer = BookSerializer(data=request.data)
        if serializer.is_valid(): # 유효성 검사
            book = serializer.save() # 저장
            userbook = UserBookSerializer({"user":user,"book":book,"status":b_status})
            userbook.save()
        else:
            book = get_object_or_404(Book,title=request.data["title"])
            userbook = UserBook.objects.create(user=user,book=book,status=b_status)
        return Response(status=status.HTTP_201_CREATED)
        

class BookAllAPIView(APIView):  
    def get(self,request, user_id, book_id):
        books = BookService(BookSelector).get_mybooks(user_id=user_id)
        serializer = BookSerializer(books, many=True)
        return Response(serializer.data,status=status.HTTP_200_OK)
    
    def delete(self, request, user_id, book_id):
        BookService(BookSelector).remove_book(user_id=user_id,book_id=book_id)
        return Response(status=status.HTTP_200_OK)
    
    # 현재 읽고 있는 메인 책 등록 !
    def post(self, request, user_id, book_id):
        BookService(BookSelector).update_status_main(user_id=user_id,book_id=book_id)
        return Response(status=status.HTTP_200_OK)
    
    
class BookTitleAPIView(APIView):
    def get(self, request, user_id):
        id_and_titles = BookService(BookSelector).get_titles(user_id=user_id)
        return Response(id_and_titles, status=status.HTTP_200_OK)