from django.shortcuts import render

# Create your views here.
from rest_framework import generics, status
from rest_framework.permissions import AllowAny, IsAuthenticated, BasePermission
from rest_framework.response import Response

from users.serializers import UserSerializer
from .models import User

SAFE_METHODS = ['POST']


class IsAuthenticatedOrCreateOnly(BasePermission):
    """
    The request is authenticated as a user, or is a create-only request.
    post method is allowed
    """

    def has_permission(self, request, view):
        return bool(
            request.method in SAFE_METHODS or
            request.user and
            request.user.is_authenticated
        )


class CreateUser(generics.ListCreateAPIView):
    permission_classes = (IsAuthenticatedOrCreateOnly,)
    serializer_class = UserSerializer
    queryset = User.objects.all().order_by('-id')

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        """
            create user details
            :param request:{
                            "email": "",
                            "first_name": "",
                            "password": "",
                            "is_staff": false #Determines the candidate
                                        True #Determines the Interviewer
                        }
            :param kwargs: NA
            :return: user details
        """
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data, status=status.HTTP_201_CREATED)
        return Response(status=status.HTTP_400_BAD_REQUEST, data=serializer.errors)


