from django.contrib.auth import authenticate, login
from users.forms import UserForm
from django.shortcuts import render, redirect
from django.contrib import messages


def register(request):

    form = UserForm(request.POST or None)

    if form.is_valid():
        form.save()

        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password1')

        user = authenticate(username=username, password=password)
        login(request, user)

        extra_tags = 'html_safe'

        message = f'<p>Congratulations on your registration!</p>' \
                  f'<p><a style="text-decoration: none; color: darkblue;" ' \
                  f'href="/employee/create/">Create</a> your first resume.</p>'

        messages.info(request, message, extra_tags)

        return redirect('employee:home-employee')

    context = {
        'form': form
    }

    return render(request, 'registration/register.html', context)
