from .test_factory import TestModelFactory


class PostModelTest(TestModelFactory):
    """Тест Постов"""

    def test_verbose_name(self):
        """verbose_name в полях совпадает с ожидаемым."""
        post = self.post
        field_verboses = {
            'text': 'Текст',
            'pub_date': 'Дата публикации поста',
            'author': 'Автор поста',
            'group': 'Группа поста',
        }
        for field, expected_value in field_verboses.items():
            with self.subTest(field=field):
                self.assertEqual(
                    post._meta.get_field(field).verbose_name, expected_value)

    def test_help_text(self):
        """help_text в полях совпадает с ожидаемым."""
        post = self.post
        field_help_texts = {
            'text': 'Напишите текст поста',
            'pub_date': 'Укажите дату публикации поста',
            'author': 'Укажите автора поста',
            'group': 'Укажите группу поста',
        }
        for field, expected_value in field_help_texts.items():
            with self.subTest(field=field):
                self.assertEqual(
                    post._meta.get_field(field).help_text, expected_value)

    def test_str_text(self):
        post = self.post
        self.assertEqual(str(post), post.text[:15])


class GroupModelTest(TestModelFactory):
    """Тест Групп"""

    def test_str_text(self):
        group = self.group
        self.assertEqual(str(group), group.title)
