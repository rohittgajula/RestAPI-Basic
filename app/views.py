from rest_framework.response import Response
from rest_framework.decorators import api_view

from rest_framework.views import APIView

from rest_framework import viewsets                 # for model viewset.

from rest_framework import status                   # to import status code.

from .models import *
from .serializers import *

from django.contrib.auth.models import User         # helps in registering & login the user

from django.contrib.auth import authenticate        # for LoginAPI to authenticate
from rest_framework.authtoken.models import Token   # for LoginAPI to import token

from rest_framework.permissions import IsAuthenticated  # used for token authentication
from rest_framework.authentication import TokenAuthentication    # for token

from django.core.paginator import Paginator         # paginator used to send huge data in small forms.

from rest_framework.decorators import action        # action is used to perform all the opertaions in one class

# fetching data using api_view decorator.

@api_view(['GET', 'POST', 'PUT', 'PATCH', 'DELETE'])
def people(request):
    if request.method == 'GET':
        obj = Person.objects.all()
        # obj = Person.objects.filter(color__isnull = False) --  color with null will not be shown.
        serializer = PersonSerializer(obj, many = True)
        return Response(serializer.data)

    elif request.method == 'POST':
        data = request.data
        serializer = PersonSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors)
    
    elif request.method == 'PUT':
        data = request.data
        obj = Person.objects.get(id = data['id'])
        serializer = PersonSerializer(obj, data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors)
    
    elif request.method == 'PATCH':
        data = request.data
        obj = Person.objects.get(id = data['id'])
        serializer = PersonSerializer(obj, data=data, partial = True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors)
    
    elif request.method == 'DELETE':
        data = request.data
        obj = Person.objects.get(id = data['id'])
        obj.delete()
        return Response({'Data deleated...'})
    
# login serializer code.

@api_view(['POST'])
def login(request):
    data = request.data
    serializer = loginSerializer(data=data)
    if serializer.is_valid():
        data = serializer.data
        print(data)
        return Response({'message': 'Sucess..'})
    return Response(serializer.errors)

# fetching data using APIview class.

class PersonAPI(APIView):
    permission_classes = [IsAuthenticated]          # to use tokens.
    authentication_classes = [TokenAuthentication]  # to use tokens to allow acess to selected users.

    def get(self, request):
        try:
            print(request.user)
            obj = Person.objects.all()
            page = request.GET.get('page',1)
            page_size = 2
            paginator = Paginator(obj, page_size)
            serializer = PersonSerializer(paginator.page(page), many=True)
            return Response(serializer.data)
        except Exception as e:
            return Response({
                'status':False,
                'message':'invalid page'
            })
    
    def post(self, request):
        data = request.data
        serializer = PersonSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors)
    
    def put(self, request):
        data = request.data
        obj = Person.objects.get(id = data['id'])
        serializer = PersonSerializer(obj, data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors)
    
    def patch(self, request):
        data = request.data
        obj = Person.objects.get(id = data['id'])
        serializer = PersonSerializer(obj, data=data, partial = True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors)
    
    def delete(self, request):
        data = request.data
        obj = Person.objects.get(id = data['id'])
        obj.delete()
        return Response({'message':'Deleted sucessfully.'})
    
# fetching data using API class. 

class loginAPI(APIView):

    def post(self, request):
        data = request.data
        serializer = loginSerializer(data=data)
        if serializer.is_valid():
            data = serializer.data
            print(data)
            return Response({'message':'sucess..'})
        return Response(serializer.errors)
    
# -------------------------

# model-viewset is used to make CRUD operations in two lines of code. 

class PeopleViewSet(viewsets.ModelViewSet):
    serializer_class = PersonSerializer
    queryset =Person.objects.all()
    http_method_names = ['get', 'post']             # this helps in acessing those mentioned methods only

    # to filter the data [api/person/?search=____]

    def list(self, request):
        search = request.GET.get('search')
        queryset = self.queryset
        if search:
            queryset = queryset.filter(name__startswith = search)

        serializer = PersonSerializer(queryset, many=True)
        return Response({'status':200, 'data':serializer.data}, status=status.HTTP_200_OK)
                                # status is used to show the status of api.

    @action(detail=True, methods=['GET'])
    def send_mail_to_person(self, request, pk):             # add function name after url to call this action
        obj = Person.objects.get(pk=pk)
        serializer = PersonSerializer(obj)

        return Response({
            'status':True,
            'message':'email sent sucessfuly.',
            'data': serializer.data
        })
    
#   To registering Users
class RegisterAPI(APIView):

    def post(self, request):
        data = request.data
        serializer = RegisterSerilizer(data=data)

        if not serializer.is_valid():
            return Response({
                'status' : False,
                'message' : serializer.errors,
            }, status.HTTP_400_BAD_REQUEST )
        
        serializer.save()          # .save() method is not of use because we are using save function in serializers.py
        
        return Response({'status':True, 
                         'message':'user created..',
                    }, status.HTTP_201_CREATED)
    
#  Login API

class LoginAPI(APIView):

    def post(self, request):
        data = request.data
        serializer = loginSerializer(data=data)
        if not serializer.is_valid():
            return Response({
                'status':False,
                'message':serializer.errors,
            }, status.HTTP_400_BAD_REQUEST)
        
        user = authenticate(username = serializer.data['username'], password = serializer.data['password'])

        if not user:
            return Response({
                'status':False,
                'message':'invalid creadentials',
            }, status.HTTP_400_BAD_REQUEST)

        token, _ = Token.objects.get_or_create(user=user)

        return Response({
            'status': True,
            'message': 'user created',
            'token':str(token)
        }, status.HTTP_201_CREATED)
    
