from django import forms
from django.core.cache import cache
from django.urls import reverse
from apps.posts.models import Follow

from .test_factory import TestModelFactory


class PostsViewsTests(TestModelFactory):
    """"Тест View"""

    # Проверяем, что словарь context страницы post/test-
    # содержит ожидаемые значения
    def test_task_detail_pages_show_correct_context(self):
        """Шаблон post_detail сформирован с правильным контекстом."""
        response = self.authorized_client.get(
            reverse('posts:post', kwargs={'post_id': self.post.id})
        )

        fields = {
            'author': self.auth_user,
            'text': self.post.text,
            'group': self.group,
            'id': self.post.id,
        }

        for value, expected in fields.items():
            with self.subTest(value=value):
                field = getattr(response.context.get('post'), value)
                self.assertEqual(field, expected)

    def test_post_create_show_correct_context(self):
        """Шаблон post_create сформирован с правильным контекстом."""
        response = self.authorized_client.get(reverse('posts:post_create'))

        form_fields = {
            'text': forms.fields.CharField,
            'group': forms.fields.ChoiceField,
        }

        for value, expected in form_fields.items():
            with self.subTest(value=value):
                form_field = response.context.get('form').fields.get(value)
                self.assertIsInstance(form_field, expected)

    def test_post_edit_show_correct_context(self):
        """Шаблон post_edit сформирован с правильным контекстом."""
        response = self.authorized_client.get(
            reverse('posts:post_edit', kwargs={'post_id': self.post.id}))

        form_fields = {
            'text': forms.fields.CharField,
            'group': forms.fields.ChoiceField,
        }

        for value, expected in form_fields.items():
            with self.subTest(value=value):
                form_field = response.context.get('form').fields.get(value)
                self.assertIsInstance(form_field, expected)


class GroupsViewsTests(TestModelFactory):
    """Проверяем, что словарь context страницы /index
    в первом элементе списка page содержит ожидаемые значения"""

    def test_index_page_show_correct_context(self):
        """Шаблон index сформирован с правильным контекстом."""
        cache.clear()
        response = self.authorized_client.get(reverse('posts:index'))
        first_object = response.context['page_obj'].object_list[0]

        self.assertEqual(first_object.id, self.post.id)
        self.assertEqual(first_object.text, self.post.text)
        self.assertEqual(first_object.author, self.auth_user)

    def test_group_detail_page_show_correct_context(self):
        """Шаблон group_detail сформирован с правильным контекстом."""
        cache.clear()
        response = self.authorized_client.get(
            reverse('posts:group_detail', kwargs={
                    'group_slug': self.group.slug})
        )
        first_object = response.context['page_obj'].object_list[0]
        self.assertEqual(first_object.id, self.post.id)
        self.assertEqual(first_object.text, self.post.text)
        self.assertEqual(first_object.author, self.auth_user)

    def test_profile_page_show_correct_context(self):
        """Шаблон profile сформирован с правильным контекстом."""
        cache.clear()
        response = self.authorized_client.get(
            reverse('posts:profile', kwargs={
                    'username': self.auth_user.username})
        )
        first_object = response.context['page_obj'].object_list[0]
        self.assertEqual(first_object.id, self.post.id)
        self.assertEqual(first_object.text, self.post.text)
        self.assertEqual(first_object.author, self.auth_user)


class PaginatorViewsTest(TestModelFactory):
    """Проверяем Паджинатор"""

    def test_paginator_contains_all_records(self):
        """Проверка: Есть ли все записи в паджинаторе"""
        cache.clear()
        response = self.guest_client.get(reverse('posts:index'))
        self.assertEqual(
            response.context['page_obj'].paginator.count, self.number_of_posts)

    def test_index_page_contains_ten_records(self):
        """Проверка: количество постов на первой странице равно 10."""
        cache.clear()
        response = self.guest_client.get(reverse('posts:index'))
        self.assertEqual(len(response.context['page_obj']), 10)

    def test_group_detail_contains_remainder_records(self):
        """Проверка: на последней странице group_detail должно быть
        % десяти от всего количества постов."""
        remainder = self.number_of_posts % 10
        response = self.client.get(
            reverse('posts:group_detail', kwargs={
                    'group_slug': self.group.slug}) + f'?page={remainder}'
        )
        last_page_posts_num = response.context['page_obj'].paginator.count % 10
        self.assertEqual(last_page_posts_num, remainder)

    def test_profile_contains_remainder_records(self):
        """Проверка: на последней странице profile должно быть
        % десяти от всего количества постов."""
        remainder = self.number_of_posts % 10
        response = self.client.get(
            reverse('posts:profile', kwargs={
                    'username': self.auth_user.username
                    }) + f'?page={remainder}'
        )
        last_page_posts_num = response.context['page_obj'].paginator.count % 10
        self.assertEqual(last_page_posts_num, remainder)


class CommentViewsTests(TestModelFactory):
    """Проверяем Комменты"""

    def test_comment_create_show_correct_context(self):
        """Проверить, что коммент создался."""
        response = self.guest_client.get(
            reverse('posts:post', kwargs={'post_id': self.post.id})
        )

        fields = {
            'text': self.test_comment_text,
            'post': self.post,
            'author': self.auth_user,
        }

        for value, expected in fields.items():
            with self.subTest(value=value):
                field = getattr(response.context.get('comments')[0], value)
                self.assertEqual(field, expected)

    def test_comment_create(self):
        """Проверить, что коммент создался."""
        response = self.guest_client.get(
            reverse('posts:post', kwargs={'post_id': self.post.id})
        )

        fields = {
            'text': self.test_comment_text,
            'post': self.post,
            'author': self.auth_user,
        }

        for value, expected in fields.items():
            with self.subTest(value=value):
                field = getattr(response.context.get('post')[0], value)
                self.assertEqual(field, expected)


class FollowViewsTest(TestModelFactory):
    """Проверяем Подписки"""

    def test_follow_user(self):
        """Проверить, что подписка создалась."""

        follow_count = Follow.objects.count()
        self.authorized_client.get(
            reverse('posts:follow_user', kwargs={
                    'username': self.auth_user2.username}))

        new_follow = Follow.objects.get(
            user=self.auth_user,
            author=self.auth_user2)

        self.assertEqual(Follow.objects.count(), follow_count + 1)
        self.assertEqual(new_follow.user, self.auth_user)
        self.assertEqual(new_follow.author, self.auth_user2)

    def test_unfollow_user(self):
        """Проверить, отписка успешно произошла."""

        self.authorized_client.get(
            reverse('posts:follow_user', kwargs={
                    'username': self.auth_user2.username}))

        follow_count = Follow.objects.count()

        self.authorized_client.get(
            reverse('posts:unfollow_user', kwargs={
                    'username': self.auth_user2.username}))

        follow_exists = Follow.objects.filter(
            user=self.auth_user,
            author=self.auth_user2).exists()

        self.assertEqual(Follow.objects.count(), follow_count - 1)
        self.assertEqual(follow_exists, False)
