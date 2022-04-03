from django.contrib.auth import get_user_model
from django.test import Client, TestCase
from django.urls import reverse
from django import forms

from posts.models import Group, Post, User

User = get_user_model()


class TestView(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user_1 = User.objects.create_user(username='inesa')
        cls.group = Group.objects.create(
            title='Заголовок',
            slug='test-slug',
            description='Тестовое описание'
        )
        cls.post_1 = Post.objects.create(
            text='Текст текстогвого сообщения',
            author=cls.user_1,
            group=cls.group,
        )
        # for i in range(1, 13):
        #     cls.post_1[i] = Post.objects.create(
        #         text=f'Тестовый пост {i}',
        #         author=cls.author_1,
        #         group=cls.group
        #     )

    def setUp(self):
        self.user = User.objects.create_user(username='inesa')
        self.authorized_client = Client()
        self.authorized_client.force_login(self.user)

    def test_uses_correct_template(self):
        """URL-адрес использует соответствующий шаблон."""
        reversed_names_template = {
            reverse('posts:index'): 'posts/index.html',
            reverse('posts:group_list', kwargs={'slug':'test-slug'}): 'posts/group_list.html',
            reverse('posts:profile', kwargs={'username':'auth_1'}): 'posts/profile.html',
            reverse('posts:post_detail', kwargs={'post_id': TestView.post_1.pk}): 'posts/post_detail.html',
            reverse('posts:post_edit', kwargs={'post_id': TestView.post_1.pk}): 'posts/create_post.html',
            reverse('posts:post_create'): 'posts/create_post.html',   
        }
        for reversed_name, template in reversed_names_template.items():
            with self.subTest(template=template):
                response = self.authorized_client.get(reversed_name)
                self.assertTemplateUsed(response, template)
