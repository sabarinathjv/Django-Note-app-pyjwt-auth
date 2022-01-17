from .models import *
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import *
from rest_framework import status,permissions
from datetime import datetime , timedelta
import jwt, datetime
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import AuthenticationFailed
from django.utils import timezone





class Login(APIView):

    permission_classes=(permissions.AllowAny,)  
    def get(self,request):
        try:      
            return Response(data={"data":"True"},status=status.HTTP_202_ACCEPTED,template_name="register.html")
        except:
            return Response(data={"data":"False","message":"Oops something went wrong !"},status=status.HTTP_202_ACCEPTED)






class Createuser(APIView):
    permission_classes=(permissions.AllowAny,)  
    def post(self, request):


        try:
            data = User.objects.filter(username=request.data.get('username')).exists()
            if data:
                return Response(data={"data":"False","message":" User already exists"},status=status.HTTP_202_ACCEPTED)
            serializer = UserSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(data={"data":"True","message":"User successfully registered please login"},status=status.HTTP_201_CREATED)
            return Response(data={"data":"False","message":"Oops something went wrong !"},status=status.HTTP_202_ACCEPTED)    
        except Exception as e:
            return Response(data={"data":"False","message":"Oops something went wrong !"},status=status.HTTP_202_ACCEPTED)





class LoginView(APIView):
    def post(self, request):
        username = request.data['username']
        password = request.data['password']
        user = User.objects.filter(username=username).first()
        if user is None:
            raise AuthenticationFailed('User not found!')
        data = User.objects.filter(username=username,password=password).exists()
        if data==None:
            raise AuthenticationFailed('Incorrect password!')   
        payload = {
            'id': user.id,
            'exp': datetime.datetime.utcnow() + datetime.timedelta(days=2),
            'iat': datetime.datetime.utcnow() #created time 
        }
        token = jwt.encode(payload, 'secret', algorithm='HS256')

        response = Response()
        response.set_cookie(key='jwt', value=token, httponly=True)
        response.data = {
            'jwt': token
        }
        return response



class Notes(APIView):

  
    def get(self, request, format=None):
        token = request.COOKIES.get('jwt')
        if not token:
            return Response(data={"data":"True"},status=status.HTTP_202_ACCEPTED,template_name="register.html")

        try:
            payload = jwt.decode(token, "secret", algorithms=["HS256"])

        except jwt.ExpiredSignatureError:
            return Response(data={"data":"True"},status=status.HTTP_202_ACCEPTED,template_name="register.html")


        user = User.objects.filter(id=payload['id']).first()

        notes = Note.objects.filter(user_id=payload['id']).all()
        notes_data = Notesserializer(notes, many=True)

        return Response(data={"results":notes_data.data,"user":user},template_name="index.html")        









class Logout(APIView):
    def post(self,request):

        try:
            response = Response()
            response.delete_cookie('jwt')
            response.data = {
                'message': 'success'
            }

            return response
            
        except:
            return Response(data={"data":"False","message":"Oops something went wrong !"},status=status.HTTP_202_ACCEPTED)
 

from rest_framework.parsers import MultiPartParser, FormParser


class CreatePost(APIView):

    parser_classes = [MultiPartParser, FormParser]


    def post(self, request, format=None):
        try:
           
            serializer = PostSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(data={"data":"True","message":"Subscribed sucessfully"},status=status.HTTP_200_OK)

            else:
                return Response(data={"data":"False","message":serializer.errors},status=status.HTTP_400_BAD_REQUEST)

        except:
               return Response(data={"data":"False","message":"Opps somethng went wrong "},status=status.HTTP_500_INTERNAL_SERVER_ERROR)



class Edit(APIView):
    def get(self, request, *args, **kwargs):
        token = request.COOKIES.get('jwt')
        if not token:
            return Response(data={"data":"True"},status=status.HTTP_202_ACCEPTED,template_name="register.html")
        try:
            payload = jwt.decode(token, "secret", algorithms=["HS256"])

        except jwt.ExpiredSignatureError:
            return Response(data={"data":"True"},status=status.HTTP_202_ACCEPTED,template_name="register.html")
        user = User.objects.filter(id=payload['id']).first()

        check = Note.objects.filter(id=kwargs.get("pk"),user=user).last() 
        if  check==None:
            notes = Note.objects.filter(user_id=payload['id']).all()
            notes_data = Notesserializer(notes, many=True)
            return Response(data={"results":notes_data.data,"user":user},template_name="index.html")  


   

        notes = Note.objects.get(id=kwargs.get("pk"))
        notes_data = Notesserializer(notes)

        return Response(data={"results":notes_data.data,"user":user,"id":notes.id},template_name="list.html")  





    def put(self, request, *args, **kwargs):
        try:
            token = request.COOKIES.get('jwt')
            if not token:
                raise AuthenticationFailed('You are not logged in! Or Token Expired Log in again.')
            try:
                payload = jwt.decode(token, "secret", algorithms=["HS256"])

            except jwt.ExpiredSignatureError:
                raise AuthenticationFailed('En error!')
            user = User.objects.filter(id=payload['id']).first()
            note = Note.objects.filter(id=kwargs.get("pk"),user=user).last()
            if note ==None:
                return Response(data={"data":"False","message":"you dont have the permission to perform this action"},status=status.HTTP_200_OK)



            serializer = PostSerializer(note, data=request.data)
            if serializer.is_valid():
                serializer.save(updated_on=timezone.now())
            
        
                return Response(data={"data":"True","message":"Subscribed sucessfully"},status=status.HTTP_200_OK)

            else:
                return Response(data={"data":"False","message":serializer.errors},status=status.HTTP_400_BAD_REQUEST)

        except:
               return Response(data={"data":"False","message":"Opps somethng went wrong "},status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    


    def delete(self, request, *args, **kwargs):
        try:
            token = request.COOKIES.get('jwt')
            if not token:
                raise AuthenticationFailed('You are not logged in! Or Token Expired Log in again.')
            try:
                payload = jwt.decode(token, "secret", algorithms=["HS256"])

            except jwt.ExpiredSignatureError:
                raise AuthenticationFailed('En error!')
            user = User.objects.filter(id=payload['id']).first()
            note = Note.objects.filter(id=kwargs.get("pk"),user=user).last()
            if note ==None:
                return Response(data={"data":"False","message":"you dont have the permission to perform this action"},status=status.HTTP_200_OK)

            note = Note.objects.get(id=kwargs.get("pk"))
            note.delete()     
            return Response(data={"data":"True","message":"Deleted sucessfully"},status=status.HTTP_200_OK)

            
        except:
               return Response(data={"data":"False","message":"Opps somethng went wrong "},status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    



