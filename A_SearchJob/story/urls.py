from django.urls import path
from .views import home, create_story, update_story, delete_story, \
    own_stories, delete_comment, like_story, liked_stories, story_content

app_name = 'story'

urlpatterns = [
    path('', home, name='home-story'),
    path('<int:id>/', story_content, name='story-content'),

    path('create/', create_story, name='story-create'),
    path('update/<int:id>/', update_story, name='story-update'),
    path('delete/<int:id>/', delete_story, name='story-delete'),

    path('liked_stories/', liked_stories, name='stories-liked'),
    path('own_stories/', own_stories, name='story-own'),

    path('delete_comment/<int:id>/', delete_comment, name='story-delete-comment'),
    path('like_story/<int:id>/', like_story, name='story-like')
]
