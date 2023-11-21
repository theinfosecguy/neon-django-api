from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import permissions
from .models import Note
from .serializers import NoteSerializer

class NoteListApiView(APIView):
    # add permission to check if user is authenticated
    permission_classes = [permissions.IsAuthenticated]

    # 1. List all
    def get(self, request, *args, **kwargs):
        '''
        List all the note items for given requested user
        '''
        notes = Note.objects.filter(user = request.user.id)
        serializer = NoteSerializer(notes, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    # 2. Create
    def post(self, request, *args, **kwargs):
        '''
        Create the Note with given note data
        '''
        data = {
            'task': request.data.get('task'), 
            'completed': request.data.get('completed'), 
            'user': request.user.id
        }
        serializer = NoteSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class NoteDetailApiView(APIView):
    # add permission to check if user is authenticated
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self, note_id, user_id):
        '''
        Helper method to get the object with given note_id, and user_id
        '''
        try:
            return Note.objects.get(id=note_id, user = user_id)
        except Note.DoesNotExist:
            return None

    # 3. Retrieve
    def get(self, request, note_id, *args, **kwargs):
        '''
        Retrieves the Note with given note_id
        '''
        note_instance = self.get_object(note_id, request.user.id)
        if not note_instance:
            return Response(
                {"res": "Object with note id does not exists"},
                status=status.HTTP_400_BAD_REQUEST
            )

        serializer = NoteSerializer(note_instance)
        return Response(serializer.data, status=status.HTTP_200_OK)

    # 4. Update
    def put(self, request, note_id, *args, **kwargs):
        '''
        Updates the note item with given note_id if exists
        '''
        note_instance = self.get_object(note_id, request.user.id)
        if not note_instance:
            return Response(
                {"res": "Object with note id does not exists"}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        data = {
            'task': request.data.get('task'), 
            'completed': request.data.get('completed'), 
            'user': request.user.id
        }
        serializer = NoteSerializer(instance = note_instance, data=data, partial = True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # 5. Delete
    def delete(self, request, note_id, *args, **kwargs):
        '''
        Deletes the note item with given note_id if exists
        '''
        note_instance = self.get_object(note_id, request.user.id)
        if not note_instance:
            return Response(
                {"res": "Object with note id does not exists"}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        note_instance.delete()
        return Response(
            {"res": "Object deleted!"},
            status=status.HTTP_200_OK
        )
