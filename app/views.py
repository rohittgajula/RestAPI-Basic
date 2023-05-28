from rest_framework.response import Response
from rest_framework.decorators import api_view

from rest_framework.views import APIView

from rest_framework import viewsets                 # for model viewset.

from .models import *
from .serializers import *

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

    def get(self, request):
        obj = Person.objects.all()
        serializer = PersonSerializer(obj, many=True)
        return Response(serializer.data)
    
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
