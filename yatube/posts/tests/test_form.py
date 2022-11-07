from http import HTTPStatus

from django.contrib.auth import get_user_model
from django.test import Client, TestCase
from django.urls import reverse
from django.db import models

from ..forms import PostForm
from ..models import Group, Post

User = get_user_model()


class PostFormTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create_user(username='auth')
        cls.group = Group.objects.create(
            title='Тестовая группа',
            slug='slug_slug',
            description='Тестовое описание',
        )
        cls.post = Post.objects.create(
            author=cls.user,
            text='Тестовый пост',
        )

    def setUp(self):
        # Создаем неавторизованный клиент
        self.guest_client = Client()
        self.authorized_client = Client()
        # Авторизуем пользователя
        self.authorized_client.force_login(self.user)

    def test_post_create_form(self):
        """Posts.Forms. Создание нового Post."""
        posts_count = Post.objects.count()
        form_data = {
            'text': 'Тестовый пост',
            'author': self.user
        }

        response = self.authorized_client.post(
            reverse('posts:post_create'),
            data=form_data,
            follow=True
        )

        self.assertRedirects(
            response,
            reverse('posts:profile', kwargs={'username': self.user.username}),
        )
        self.assertEqual(Post.objects.count(), posts_count + 1)

    def test_edit_post_create_form(self):
        """Posts.Forms. Можно редатикровать посты."""
        response = self.authorized_client.get(
            reverse(
                'posts:post_edit',
                kwargs={"post_id": self.post.id})
        )
        form_data = {
            'text': 'Тестовый пост от редактированный',
            'author': self.user
        }

        response = self.authorized_client.post(reverse(
            'posts:post_edit',
            kwargs={"post_id": self.post.id}),
            data=form_data,
            follow=True)
        self.assertRedirects(
            response,
            reverse(
                'posts:post_detail',
                kwargs={"post_id": self.post.id}))
        self.assertTrue(
            Post.objects.filter(
                text='Тестовый пост от редактированный',
                author=self.user
            ).exists()
        ) 
