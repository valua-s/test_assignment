from django.contrib.auth import get_user_model
from djoser.serializers import UserSerializer
from rest_framework import serializers

from users.models import Subscription, Group, Balance
from courses.models import Course

User = get_user_model()


class CustomUserSerializer(UserSerializer):
    """Сериализатор пользователей."""
    class Meta:
        model = User
        fields = '__all__'

    def update(self, instance, validated_data):
        if not self.context['request'].user.is_staff:
            validated_data.pop('editable_field', None)
        return super().update(instance, validated_data)


class SubscriptionSerializer(serializers.ModelSerializer):
    """Сериализатор подписки."""

    class Meta:
        model = Subscription
        fields = (
            'student',
            'course',
            'group'
        )
        only_read_fields = ('group')

    def create(self, validated_data):
        balance = Balance.objects.get(
            student=validated_data['student'])
        course_cost = Course.objects.get(validated_data['course'])
        if balance.bonus >= course_cost:
            balance.bonus -= course_cost
            balance.save()
            group = Group.objects.all().order_by('count').first()
            group.count += 1
            group.save()
            return Subscription.objects.create(
                student=validated_data['student'],
                course=validated_data['course'],
                group=group.id
            )
        raise serializers.ValidationError(
            'На балансе недостаточно средств'
        )
