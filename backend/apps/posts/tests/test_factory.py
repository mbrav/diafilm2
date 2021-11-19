import random
from io import BytesIO

from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.test import Client, TestCase
from PIL import Image, ImageDraw, ImageFont
from apps.posts.models import Comment, Group, Post

User = get_user_model()


class TestModelFactory(TestCase):
    """Обобществлённый завод для создания моделей"""

    @classmethod
    def createFunTestImage(self, name, size=None, color=None):
        """Создаём весёлые разноцветные картинки для тестов"""

        contrast_color = (0, 0, 0)
        if color is None:
            color = (
                random.randint(0, 255),
                random.randint(0, 255),
                random.randint(0, 255))
            contrast_color = tuple((c + 125) % 255 for c in color)
        if size is None:
            size = (
                random.randint(150, 300),
                random.randint(150, 300))

        img_name = f'fun-test-image-{name}.jpg'
        fnt = ImageFont.load_default()

        im = Image.new(mode='RGB', size=size, color=color)
        d = ImageDraw.Draw(im)

        for i in range(100):
            rand_size = (random.randint(
                0, size[0]), random.randint(0, size[1]))
            rand_letter = img_name[i % len(img_name)]
            rand_color = (random.randint(0, 255), random.randint(
                0, 255), random.randint(0, 255))
            d.multiline_text(rand_size, rand_letter, font=fnt, fill=rand_color)

        d.multiline_text((10, size[1] - 20), img_name,
                         font=fnt, fill=contrast_color)

        im_io = BytesIO()
        im.save(im_io, 'JPEG')
        im_io.seek(0)

        image = InMemoryUploadedFile(
            im_io, None, img_name, 'image/jpeg', len(im_io.getvalue()), None)
        return image

    @classmethod
    def setUpClass(self):
        super().setUpClass()
        self.auth_user = User.objects.create_user(username='test_username')
        self.auth_user2 = User.objects.create_user(username='test_username2')
        self.authorized_client = Client()
        self.guest_client = Client()
        self.authorized_client.force_login(self.auth_user)
        self.group = Group.objects.create(
            title='Тестовая группа',
            slug='test_group_slug',
            description='Тестовое описание',
        )

        self.number_of_posts = random.randint(30, 100)
        posts = []
        for p in range(0, self.number_of_posts):
            test_image = self.createFunTestImage(f'post-{p}')
            new_p = Post(
                text=f'Тестовой пост №{p}',
                author=self.auth_user,
                group=self.group,
                image=test_image,
                id=p,
            )
            posts.append(new_p)

        Post.objects.bulk_create(objs=posts, batch_size=100)
        self.post = Post.objects.all().first()

        self.test_comment_text = 'Тестовый Коммент'
        self.test_comment = Comment(
            text=self.test_comment_text,
            post=self.post,
            author=self.auth_user,
        )
        self.test_comment.save()
