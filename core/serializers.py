import datetime
import logging

from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned
from django.http import Http404
from rest_framework import serializers

from .models import User, RegisterTimeSlots

logger = logging.getLogger(__name__)


class AvailabilitySerializer(serializers.ModelSerializer):
    class Meta:
        model = RegisterTimeSlots
        fields = ['user', 'date', 'from_time', 'to_time']
        extra_kwargs = {'user': {'read_only': True}
                        }

    def convert_time(self, key):
        time = self.initial_data[key]
        return datetime.datetime.strptime(time, '%H:%M').time()

    def validate_from_time(self, value):
        to_time = self.convert_time('to_time')
        if value.minute > 0:
            raise serializers.ValidationError("Time has wrong format. Minute must be 0")
        if value >= to_time:
            raise serializers.ValidationError("From time must be less than to time")

        return value

    def validate_to_time(self, value):
        from_time = self.convert_time('from_time')
        if value.minute > 0:
            raise serializers.ValidationError("Time has wrong format. Minute must be 0")
        if value <= from_time:
            raise serializers.ValidationError("To time must be greater than from time")
        return value

    def create(self, validated_data):

        validated_data['user'] = self.context['user']
        obj = RegisterTimeSlots(**validated_data)
        obj.save()
        return obj


class AvailableScheduleSerializer(serializers.Serializer):
    interviewer = serializers.CharField(max_length=255, required=True, write_only=True)
    candidate = serializers.CharField(max_length=255, required=True, write_only=True)
    time_slots = serializers.SerializerMethodField()

    class Meta:
        fields = ['interviewer', 'candidate', 'time_slots']

    @staticmethod
    def get_object(id):
        try:
            return RegisterTimeSlots.objects.get(user_id=id)
        except ObjectDoesNotExist:
            raise Http404
        except MultipleObjectsReturned:
            return RegisterTimeSlots.objects.filter(user_id=id).last()

    @staticmethod
    def available_time(start, end):
        today = datetime.datetime.now().date()
        start = datetime.datetime.combine(today, start)
        end = datetime.datetime.combine(today, end)
        delta = datetime.timedelta(hours=1)
        t = start
        value = []
        while t <= end:
            value.append(t.strftime('%H:%M'))
            t += delta
        return value

    def slots(self, interviewer, candidate):
        interview_time = self.available_time(interviewer.from_time, interviewer.to_time)
        candidate_time = self.available_time(candidate.from_time, candidate.to_time)
        available_slot = sorted(set(interview_time) & set(candidate_time))
        return list(zip(available_slot, available_slot[1:]))

    def get_time_slots(self, obj):

        interviewer = self.get_object(obj['interviewer'])
        candidate = self.get_object(obj['candidate'])
        if interviewer.date != candidate.date:
            raise serializers.ValidationError("No schedule available")

        return self.slots(interviewer, candidate)
