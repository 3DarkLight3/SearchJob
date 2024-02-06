from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from additional_functions.additional import paginator_array, get_current_year
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from .models import StoryModel, CommentModel
from django.db.models import Q
from django.conf import settings
from users.models import User
from story.forms import StoryForm
import json


def home(request):
    queryset = StoryModel.objects.all()

    query = request.GET.get('q_story')
    if query:
        queryset = queryset.filter(
            Q(headline__icontains=query) |
            Q(for_who__icontains=query)
        )

    stories_per_page = 8
    paginator = Paginator(queryset, stories_per_page)

    page_request_var = 'page'
    page = request.GET.get(page_request_var)

    try:
        queryset = paginator.get_page(page)
    except PageNotAnInteger:
        queryset = paginator.page(paginator.num_pages)
    except EmptyPage:
        queryset = paginator.page(paginator.num_pages)

    context = {
        'stories': queryset,
        'user_side': settings.USER_SIDE,
        'page_request_var': page_request_var,
        'paginator_range': paginator_array(paginator.num_pages, paginator.get_page(page).number),
        'count_of_pages': paginator.num_pages,
        'count_of_stories': len(queryset),
        'user': request.user,
        'current_year': get_current_year()
    }

    return render(request, 'story/home.html', context)


def story_content(request, id=None):

    story = get_object_or_404(StoryModel, id=id)

    user_visitor = get_object_or_404(User, id=request.user.id)
    user_author = get_object_or_404(User, username=story.user)

    if request.POST:

        comment_author = user_visitor
        comment_text = request.POST['text']

        story.commentmodel_set.create(user=comment_author, text=comment_text)

        return redirect(f'/story/{id}/')

    context = {
        'story': story,
        'id': id,
        'user_side': settings.USER_SIDE,
        'user_main': user_author,
        'comments': story.comments,
        'all_comments': story.commentmodel_set.order_by('-id'),
        'user_visitor': user_visitor,
        'current_year': get_current_year()
    }

    with open('additional_files/liked_stories.json', "r") as file:
        data = json.load(file)

    user_id = str(user_visitor.id)

    try:
        if story.id in data['users'][user_id]:
            context['existence_in_liked_stories'] = True
        else:
            context['existence_in_liked_stories'] = False
    except KeyError:
        context['existence_in_liked_stories'] = False

    return render(request, 'story/story.html', context)


def like_story(request, id):

    story = get_object_or_404(StoryModel, id=id)

    user = get_object_or_404(User, id=request.user.id)

    user_id = str(user.id)
    story_id = story.id

    with open('additional_files/liked_stories.json', "r") as file:
        data = json.load(file)

    if user_id in data['users']:
        if story_id in data['users'][user_id]:
            data['users'][user_id].remove(story_id)
        else:
            data['users'][user_id].append(story_id)
    else:
        data['users'][user_id] = [story_id]

    with open('additional_files/liked_stories.json', 'w') as file:
        json.dump(data, file)

    return redirect(f'/story/{story_id}/')


def own_stories(request):
    queryset = [story for story in StoryModel.objects.all() if story.user == request.user]

    context = {
        'own_stories': queryset,
        'count_of_stories': len(queryset),
        'user_side': settings.USER_SIDE,
        'current_year': get_current_year()
    }

    return render(request, 'story/own_stories.html', context)


def liked_stories(request):
    user = get_object_or_404(User, id=request.user.id)

    with open('additional_files/liked_stories.json', 'r') as file:
        data = json.load(file)

    user_id = str(user.id)

    try:
        liked_stories_lst = data['users'][user_id]
        queryset = StoryModel.objects.all().filter(id__in=liked_stories_lst)
    except KeyError:
        queryset = StoryModel.objects.all().filter(id__in=[0])

    query = request.GET.get('q_liked_s')
    if query:
        queryset = queryset.filter(
            Q(headline__icontains=query) |
            Q(for_who__icontains=query)
        )

    context = {
        'stories': queryset,
        'count_of_stories': len(queryset),
        'add_query': False,
        'user_side': settings.USER_SIDE,
        'current_year': get_current_year()
    }

    if query:
        context['add_query'] = True
    else:
        context['add_query'] = False

    return render(request, 'story/liked_stories.html', context)


def create_story(request):
    form = StoryForm(request.POST or None)

    if form.is_valid():
        story = form.save(commit=False)
        story.user = request.user
        story.save()

        extra_tags = 'html_safe'

        message = f'<p>The <a style="text-decoration: none; color: darkblue;" ' \
                  f'href="/story/{story.id}/">story</a> was successfully created!</p>' \
                  f'<p>To update your story, click <a style="text-decoration: none; color: darkblue;" ' \
                  f'href="/story/update/{story.id}/">here</a></p>'

        messages.info(request, message, extra_tags)

        return redirect('story:story-own')

    context = {
        'form': form,
        'headline': '',
        'title': '',
        'text': '',
        'comments': '',
        'text_for_btn': 'Create story',
        'user_side': settings.USER_SIDE,
        'current_year': get_current_year()
    }

    return render(request, 'story/story_creation.html', context)


def update_story(request, id=None):

    story = get_object_or_404(StoryModel, id=id)
    form = StoryForm(request.POST or None, instance=story)

    if form.is_valid():
        updated_story = form.save(commit=False)
        updated_story.save()

        extra_tags = 'html_safe'

        message = f'<p>The <a style="text-decoration: none; color: darkblue;" ' \
                  f'href="/story/{story.id}/">story</a> was successfully updated!</p>' \
                  f'<p>To update again your story, click <a style="text-decoration: none; color: darkblue;" ' \
                  f'href="/story/update/{story.id}/">here</a></p>'

        messages.info(request, message, extra_tags)

        return redirect('story:story-own')

    context = {
        'form': form,
        'headline': story.headline,
        'title': story.title,
        'text': story.text,
        'comments': story.comments,
        'text_for_btn': 'Update story',
        'user_side': settings.USER_SIDE,
        'current_year': get_current_year()
    }

    return render(request, 'story/story_creation.html', context)


def delete_story(request, id=None):
    story = get_object_or_404(StoryModel, id=id)
    story.delete()

    extra_tags = 'html_safe'

    message = f'<p>Story has just been successfully deleted!</p>'

    messages.info(request, message, extra_tags)

    return redirect('story:story-own')


def delete_comment(request, id=None):
    comment = get_object_or_404(CommentModel, id=id)
    story = get_object_or_404(StoryModel, headline=comment.story)

    comment.delete()

    return redirect(f'/story/{story.id}/')
