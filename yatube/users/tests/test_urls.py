# from django.contrib.auth import get_user_model
# from django.test import TestCase, Client
# from http import HTTPStatus


# User = get_user_model()


# class TaskURLTests(TestCase):
#     @classmethod
#     def setUpClass(cls):
#         super().setUpClass()
#         cls.user = User.objects.create_user(username='auth')
        
        

#     def setUp(self):
#         # Создаем неавторизованный клиент
#         self.guest_client = Client()
#         # Создаем пользователя
#         # Создаем второй клиент
#         self.authorized_client = Client()
#         # Авторизуем пользователя
#         self.authorized_client.force_login(self.user)



#     def test_urls_guest_client(self):
#         """URL-адрес доступен  и  использует соответствующий шаблон для всех."""
#         templates_url_names = {
#             '/logout/': 'users/logged_out.html',
#             '/signup/': 'users/signup.html',
#             '/login/': 'users/login.html',
            
#         }
#         for  address, template, in templates_url_names.items():
#             with self.subTest(address=address):
#                 response = self.guest_client.get(address)
#                 self.assertEqual(response.status_code, HTTPStatus.OK)
#                 self.assertTemplateUsed(response, template)



