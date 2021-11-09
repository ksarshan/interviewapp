from django.shortcuts import render

# Create your views here.
from rest_framework import status, generics
from rest_framework.permissions import AllowAny, IsAuthenticated, BasePermission
from rest_framework.response import Response
from rest_framework.views import APIView

from core.models import RegisterTimeSlots
from core.serializers import AvailabilitySerializer, AvailableScheduleSerializer


class IsSuperUser(BasePermission):
    """
    Allows access only to admin users.
    """

    def has_permission(self, request, view):
        return bool(request.user and request.user.is_staff and request.user.is_superuser)


class Availability(generics.ListCreateAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = AvailabilitySerializer
    queryset = RegisterTimeSlots.objects.all().order_by('-id')

    def get(self, request, *args, **kwargs):
        """ List Availability of Examiners or Candidates """
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        """
                Register time slot
                    :param request post :{
                                            "date": {
                                                "type": "date",
                                                "required": true,
                                                "read_only": false,
                                                "label": "Date"
                                            },
                                            "from_time": {
                                                "type": "time", 24 hr format
                                                "required": true,
                                                "read_only": false,
                                                "label": "From time"
                                            },
                                            "to_time": {
                                                "type": "time", 24 hr format
                                                "required": true,
                                                "read_only": false,
                                                "label": "To time"
                                            }
                                        }

                    :param kwargs: NA
                    :return: time slot details
        """

        data = request.data
        user = request.user
        serializer = self.serializer_class(data=data, context={'user': user})
        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST, data=serializer.errors)


class ScheduleTime(generics.GenericAPIView):
    permission_classes = (IsSuperUser,)
    serializer_class = AvailableScheduleSerializer
    queryset = RegisterTimeSlots.objects.all().order_by('-id')

    def get_object(self):
        queryset = self.queryset.filter(candidate_id=self.kwargs.get('pk'))
        return queryset

    def post(self, request, *args, **kwargs):
        """ Get the scheduled time
        "POST": {
            "interviewer": {
                "type": "integer", #interviewer id
                "required": true,
                "read_only": false,
                "label": "Interviewer",
                "max_length": 255
            },
            "candidate": {
                "type": "integer", candidate id
                "required": true,
                "read_only": false,
                "label": "Candidate",
                "max_length": 255
            },
            "time_slots": {
                "type": "field",
                "required": false,
                "read_only": true,
                "label": "Time slots"
            }

        """
        data = self.serializer_class(request.data)
        return Response(data.data)


# Todo: Schedule confirmation
# Todo: Schedule Cancellation
# Todo: Schedule Confirmation Mail
# Todo: authorization tokens of the user should be place in Redis




