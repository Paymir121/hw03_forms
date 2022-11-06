from django.contrib.auth import get_user_model
from django.test import Client, TestCase
from django.urls import reverse

from ..models import Group, Post

User = get_user_model()


class PostModelTest(TestCase):
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
        # Создаем пользователя
        # Создаем второй клиент
        self.authorized_client = Client()
        # Авторизуем пользователя
        self.authorized_client.force_login(self.user)

    def test_index_page_show_correct_context(self):
        response = self.authorized_client.get(reverse('posts:index'))
        self.assertEqual(response.context['page_obj'][0], self.post)

    def test_pages_uses_correct_template(self):
        """View URL-адрес использует соответствующий шаблон."""
        # Собираем в словарь пары "имя_html_шаблона: reverse(name)"
        templates_pages_names = {
            'posts/index.html': reverse('posts:index'),

            'posts/group_list.html': (
                reverse('posts:group_list', kwargs={'slug': self.group.slug})
            ),

            'posts/profile.html': (
                reverse('posts:profile', kwargs={'username': self.user.username})
            ),

            'posts/post_create.html': reverse('posts:post_create'),

            'posts/post_detail.html': (
                reverse('posts:post_detail', kwargs={'post_id': self.post.id})
            ),

            'posts/post_create.html': (
                reverse('posts:post_edit', kwargs={'post_id': self.post.id})
            ),
        }
        # Проверяем, что при обращении к name вызывается соответствующий HTML-шаблон
        for template, reverse_name in templates_pages_names.items():
            with self.subTest(reverse_name=reverse_name):
                response = self.authorized_client.get(reverse_name)
                self.assertTemplateUsed(response, template) 


class PostPaginatorTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create_user(username='test_name')
        cls.group = Group.objects.create(
            title="Тестовая группа",
            slug='test_slug',
            description='Тестовое описание',
        )
        for count_post in range(18):
            cls.post = Post.objects.create(
                text='Тестовый текст',
                author=cls.user,
                group=cls.group
            )

    def setUp(self):
        self.guest_client = Client()
        self.authorized_client = Client()
        self.authorized_client.force_login(self.user)

    def test_first_page_contains_ten_posts(self):
        paginator_list = {
            'posts:index': reverse('posts:index'),
            'posts:group_list': reverse(
                'posts:group_list', kwargs={'slug': PostPaginatorTests.group.slug}),
            'posts:profile': reverse(
                'posts:profile', kwargs={'username': PostPaginatorTests.user.username}),
        }
        for template, reverse_name in paginator_list.items():
            response = self.guest_client.get(reverse_name)
            self.assertEqual(len(response.context['page_obj']), 10)

    def test_second_page_contains_ten_posts(self):
        paginator_list = {
            'posts:index': reverse('posts:index') + '?page=2',
            'posts:group_list': reverse(
                'posts:group_list', kwargs={'slug': PostPaginatorTests.group.slug}) + '?page=2',
            'posts:profile': reverse(
                'posts:profile', kwargs={'username': PostPaginatorTests.user.username}) + '?page=2',
        }
        for template, reverse_name in paginator_list.items():
            response = self.guest_client.get(reverse_name)
            self.assertEqual(len(response.context['page_obj']), 8)