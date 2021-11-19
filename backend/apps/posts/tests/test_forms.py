from django.core.cache import cache
from django.urls import reverse

from apps.posts.models import Comment, Post

from .test_factory import TestModelFactory


class PostsFormTests(TestModelFactory):
    """Тест форм постов"""

    def test_post_create(self):
        """Валидная форма создает запись в Post."""
        post_count = Post.objects.count()
        new_text = 'Тестовый текст' + str(post_count + 1)

        test_image = self.createFunTestImage('post-create')

        form_data = {
            'text': new_text,
            'image': test_image,
            'group': self.group.id,
        }

        response = self.authorized_client.post(
            reverse('posts:post_create'),
            data=form_data,
            follow=True,
        )

        self.assertRedirects(response, reverse('posts:profile', kwargs={
            'username': self.auth_user.username}))
        self.assertEqual(Post.objects.count(), post_count + 1)
        self.assertTrue(Post.objects.filter(text=new_text).exists())

        # Проверяем картинки
        post = Post.objects.get(text=new_text)
        self.assertEqual(post.image.size, test_image.size)

    def test_post_create_cache(self):
        """Валидная форма создает запись в Post с кэшом."""

        post_count = Post.objects.count()

        form_data = {
            'text': 'Тестовый текст с кэшом',
            'group': self.group.id,
        }

        self.authorized_client.post(
            reverse('posts:post_create'),
            data=form_data,
            follow=True,
        )

        response = self.authorized_client.get(reverse('posts:index'))
        cached_post_count = response.context['page_obj'].paginator.count
        self.assertNotEqual(post_count, cached_post_count)

        cache.clear()
        post_count = Post.objects.count()
        response = self.authorized_client.get(reverse('posts:index'))
        cached_post_count = response.context['page_obj'].paginator.count
        self.assertEqual(post_count, cached_post_count)

    def test_edit_post(self):
        """Валидная форма редактирует запись в Post."""
        post_count = Post.objects.count()

        test_image = self.createFunTestImage('test_edit_post')

        post = Post.objects.get(text=self.post.text)
        new_text = self.post.text + 'Тестовая редакция'

        form_data = {
            'text': new_text,
            'image': test_image,
            'group': self.group.id,
        }

        response = self.authorized_client.post(
            reverse('posts:post_edit', kwargs={
                'post_id': self.post.id}),
            data=form_data,
            follow=True,
        )

        self.assertRedirects(response, reverse('posts:post', kwargs={
            'post_id': self.post.id}))
        self.assertEqual(Post.objects.count(), post_count)
        self.assertTrue(Post.objects.filter(text=new_text,).exists())

        # Проверяем картинки
        self.assertNotEqual(post.image.size, test_image.size)
        post = Post.objects.get(text=new_text)
        self.assertEqual(post.image.size, test_image.size)


class CommentFormTests(TestModelFactory):
    """Тест формы комментов"""

    @classmethod
    def setUp(self):
        self.comment_count = Comment.objects.count()
        self.new_comment_text = 'Тестовый коммент' + \
            str(self.comment_count + 1)

    def test_create_comment(self):
        """Валидная форма создает новый Comment под Post."""

        form_data = {
            'text': self.new_comment_text,
        }

        response = self.authorized_client.post(
            reverse('posts:add_comment', kwargs={'post_id': self.post.id}),
            data=form_data,
            follow=True,
        )

        self.assertRedirects(response, reverse(
            'posts:post', kwargs={'post_id': self.post.id}))
        self.assertEqual(Comment.objects.count(), self.comment_count + 1)
        self.assertTrue(Comment.objects.filter(
            text=self.new_comment_text).exists())

    def test_delete_comment(self):
        """Валидная форма удаляет Comment под Post."""

        form_data = {
            'text': self.new_comment_text,
        }

        self.authorized_client.post(
            reverse('posts:add_comment', kwargs={'post_id': self.post.id}),
            data=form_data,
            follow=True,
        )

        self.assertEqual(Comment.objects.count(), self.comment_count + 1)
        self.assertTrue(Comment.objects.filter(
            text=self.new_comment_text).exists())

        new_comment = Comment.objects.get(
            text=self.new_comment_text)

        self.authorized_client.post(
            reverse('posts:delete_comment', kwargs={
                    'post_id': self.post.id,
                    'comment_id': new_comment.id}),
            data=form_data,
            follow=True,
        )

        self.assertEqual(Comment.objects.count(), self.comment_count)
