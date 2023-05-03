from rest_framework import serializers
from .models import CustomUser, Event
# import the logging library
import logging
# Get an instance of a logger
logger = logging.getLogger('event_manager')

class CustomUserSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
        required=True
    )
    username = serializers.CharField()
    password = serializers.CharField(min_length=8, write_only=True)
    
    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'password', 'first_name', 'last_name')
        extra_kwargs    = {'password': {'write_only': True}}

    def create(self, validated_data):
        password = validated_data.pop('password', None)
        instance = self.Meta.model(**validated_data)  # as long as the fields are the same, we can just use this
        if password is not None:
            instance.set_password(password)
        instance.save()
        return instance
    
        user = CustomUser.objects.create_user(**validated_data)
        return user
    
class EventSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')
    description = serializers.CharField(required=False)
    location = serializers.CharField(required=False)
    
    class Meta:
        model = Event
        fields = ('id', 'name', 'description', 'start_date', 'end_date', 'max_capacity', 'location', 'attendees', 'owner')
        read_only_fields = ('attendees', 'owner')

    def validate(self, data):
        # Check that end_date is after start_date
        if data['end_date'] <= data['start_date']:
            raise serializers.ValidationError("End date must be after start date.")
        return data
    


class EditEventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = ('id', 'name', 'description', 'start_date', 'end_date', 'max_capacity', 'location')
        extra_kwargs = {
            'name': {'required': False},
            'description': {'required': False},
            'start_date': {'required': False},
            'end_date': {'required': False},
            'max_capacity': {'required': False},
            'location': {'required': False},
        }
    def validate(self, data):
        if all([data.get(field) is None for field in data]):
            raise serializers.ValidationError("At least one field is required")
        return data

class RegisterEventSerializer(serializers.ModelSerializer):
    attendees = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
    
    class Meta:
        model = Event
        fields = ('id', 'attendees')
        extra_kwargs = {
            'id': {'required': False},
            'attendees': {'required': False},
        }
        read_only_fields = ['id',]

    def update(self, instance, validated_data):
        # Update the attendees field with the current user
        user = self.context['request'].user
        instance.attendees.add(user)
        return instance
