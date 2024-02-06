from django.db import models
from django.conf import settings


def types_of_profession():
    types = [
        ('employers', 'Employers'),
        ('employees', 'Employees'),
        ('everyone', 'Everyone')
    ]

    return types


# Create your models here.
class StoryModel(models.Model):
    headline = models.CharField(verbose_name='Headline of story', max_length=200)
    title = models.TextField(verbose_name='Title of story')
    text = models.TextField(verbose_name='Text of story')
    for_who = models.CharField(verbose_name='Useful for whom', max_length=20, choices=types_of_profession(), default=types_of_profession()[2][0])

    comments = models.BooleanField(default=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    update = models.DateTimeField(auto_now=True)

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        default=1,
        on_delete=models.PROTECT
    )

    def __str__(self):
        return self.headline

    def get_url_to_story(self):
        return f'/story/{self.id}/'

    def get_url_to_update_story(self):
        return f'/story/update/{self.id}/'

    class Meta:
        ordering = ['-timestamp']
        verbose_name = 'Story'
        verbose_name_plural = 'Stories'


class CommentModel(models.Model):
    story = models.ForeignKey('StoryModel', on_delete=models.CASCADE)
    text = models.CharField(max_length=300, verbose_name='Text of comment')
    timestamp = models.DateTimeField(auto_now_add=True)

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        default=1,
        on_delete=models.PROTECT
    )

    def __str__(self):
        return f'{self.story} - {self.id}'

    class Meta:
        verbose_name = 'Comment'
        verbose_name_plural = 'Comments'
        ordering = ('-timestamp', )
