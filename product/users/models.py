from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.validators import (MinValueValidator)

from courses.models import Course, Group


class CustomUser(AbstractUser):
    """Кастомная модель пользователя - студента."""

    email = models.EmailField(
        verbose_name='Адрес электронной почты',
        max_length=250,
        unique=True
    )
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = (
        'username',
        'first_name',
        'last_name',
        'password'
    )

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
        ordering = ('-id',)

    def __str__(self):
        return self.get_full_name()


class Balance(models.Model):
    """Модель баланса пользователя."""

    student = models.ForeignKey(
        CustomUser,
        verbose_name='Студент',
        on_delete=models.CASCADE
    )
    bonus = models.DecimalField(
        decimal_places=1,
        verbose_name='Бонус',
        max_digits=10,
        default=1000,
        validators=[MinValueValidator(0.5),]
    )

    class Meta:
        verbose_name = 'Баланс'
        verbose_name_plural = 'Балансы'
        ordering = ('-id',)


class Subscription(models.Model):
    """Модель подписки пользователя на курс."""

    student = models.ForeignKey(
        CustomUser,
        verbose_name='Студент',
        on_delete=models.CASCADE,
        related_name='subscriptions'
    )
    course = models.ForeignKey(
        Course,
        verbose_name='Курс',
        on_delete=models.CASCADE,
        related_name='subscriptions'
    )
    group = models.ForeignKey(
        Group,
        verbose_name='Группа',
        on_delete=models.CASCADE,
        related_name='subscriptions'
    )

    class Meta:
        verbose_name = 'Подписка'
        verbose_name_plural = 'Подписки'
        ordering = ('-id',)
        unique_together = ('student', 'course', 'group')
