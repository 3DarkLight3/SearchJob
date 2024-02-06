from django.shortcuts import render, get_object_or_404, redirect
from additional_functions.additional import paginator_array, split_lines, set_width_height_for_image, get_current_year
from employee.models import EmployeeModel
from employer.models import EmployerModel
from users.models import User
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db.models import Q
from employee.forms import EmployeeForm
from django.conf import settings
from django.contrib import messages

from django.core.mail import EmailMessage
from django.template.loader import render_to_string

import json


def home(request):

    if not str(request.get_full_path()).replace('/', ''):
        return redirect('employee:home-employee')

    settings.USER_SIDE = 'employee'

    queryset = EmployerModel.objects.all()

    query = request.GET.get('q')
    if query:
        queryset = queryset.filter(
            Q(name_of_job__icontains=query) |
            Q(location__icontains=query) |
            Q(name_of_company__icontains=query) |
            Q(type_of_job__icontains=query) |
            Q(main_programming_language__icontains=query)
        )

    vacancies_per_page = 4
    paginator = Paginator(queryset, vacancies_per_page)

    page_request_var = 'page'
    page = request.GET.get(page_request_var)

    try:
        queryset = paginator.get_page(page)
    except PageNotAnInteger:
        queryset = paginator.page(paginator.num_pages)
    except EmptyPage:
        queryset = paginator.page(paginator.num_pages)

    context = {
        'vacancies': queryset,
        'page_request_var': page_request_var,
        'paginator_range': paginator_array(paginator.num_pages, paginator.get_page(page).number),
        'count_of_pages': paginator.num_pages,
        'count_of_vacancies': len(queryset),
        'current_year': get_current_year()
    }

    return render(request, 'employee/home.html', context)


def create_resume(request):
    form = EmployeeForm(request.POST or None, request.FILES or None)

    if form.is_valid():
        resume_ins = form.save(commit=False)
        resume_ins.user = request.user
        resume_ins.save()

        extra_tags = 'html_safe'

        message = f'<p>The <a style="text-decoration: none; color: darkblue;" ' \
                  f'href="/employee/resume/{resume_ins.id}/">resume</a> was successfully created!</p>' \
                  f'<p>To update your resume, click <a style="text-decoration: none; color: darkblue;" ' \
                  f'href="/employee/update/{resume_ins.id}/">here</a></p>'

        messages.info(request, message, extra_tags)

        return redirect('employee:resumes')

    context = {
        'form': form,
        'text_for_btn': 'Create resume',
        'current_year': get_current_year()
    }

    return render(request, 'employee/resume_creation.html', context)


def update_resume(request, id=None):

    resume_ins = get_object_or_404(EmployeeModel, id=id)
    form = EmployeeForm(request.POST or None, request.FILES or None, instance=resume_ins)

    if form.is_valid():
        resume_ins = form.save(commit=False)
        resume_ins.save()

        extra_tags = 'html_safe'
        message = f'<p>The <a style="text-decoration: none; color: darkblue;" ' \
                  f'href="/employee/resume/{resume_ins.id}/">resume</a> was successfully updated!</p>' \
                  f'<p>To update again your resume, click <a style="text-decoration: none; color: darkblue;" ' \
                  f'href="/employee/update/{resume_ins.id}/">here</a></p>'

        messages.info(request, message, extra_tags)

        return redirect('employee:resumes')

    context = {
        'form': form,
        'text_for_btn': 'Update resume',
        'current_year': get_current_year()
    }

    return render(request, 'employee/resume_creation.html', context)


def delete_resume(request, id=None):
    resume_instance = get_object_or_404(EmployeeModel, id=id)
    resume_instance.delete()

    extra_tags = 'html_safe'
    message = f'<p>Resume has just been successfully deleted!</p>'

    messages.info(request, message, extra_tags)

    return redirect('employee:resumes')


def liked_vacancies(request):
    user = get_object_or_404(User, id=request.user.id)

    with open('additional_files/liked_vacancies.json', "r") as file:
        data = json.load(file)

    user_id = str(user.id)

    try:
        liked_vacancies_user = data['users'][user_id]
        queryset = EmployerModel.objects.all().filter(id__in=liked_vacancies_user)
    except KeyError:
        queryset = EmployerModel.objects.all().filter(id__in=[0])

    query = request.GET.get('q_liked_v')
    if query:
        queryset = queryset.filter(
            Q(name_of_job__icontains=query) |
            Q(location__icontains=query) |
            Q(name_of_company__icontains=query) |
            Q(type_of_job__icontains=query) |
            Q(main_programming_language__icontains=query)
        )

    context = {
        'vacancies': queryset,
        'count_of_vacancies': len(queryset),
        'add_query': False,
        'current_year': get_current_year()
    }

    if query:
        context['add_query'] = True
    else:
        context['add_query'] = False

    return render(request, 'employee/liked_vacancies.html', context)


def own_resumes(request):
    queryset = [resume for resume in EmployeeModel.objects.all() if resume.user == request.user]
    context = {
        'resumes': queryset,
        'count_of_resumes': len(queryset),
        'current_year': get_current_year()
    }

    return render(request, 'employee/own_resumes.html', context)


def like_vacancy(request, id=None):

    vacancy_obj = get_object_or_404(EmployerModel, id=id)

    if request.user.is_authenticated:
        user = get_object_or_404(User, id=request.user.id)

        user_id = str(user.id)
        vacancy_id = vacancy_obj.id

        with open('additional_files/liked_vacancies.json', "r") as file:
            data = json.load(file)

        if user_id in data['users']:
            if vacancy_id in data['users'][user_id]:
                data['users'][user_id].remove(vacancy_id)
            else:
                data['users'][user_id].append(vacancy_id)
        else:
            data['users'][user_id] = [vacancy_id]

        with open('additional_files/liked_vacancies.json', 'w') as file:
            json.dump(data, file)

    return redirect(f'/employee/vacancy/{vacancy_obj.id}/')


def vacancy(request, id=None):

    vacancy_obj = get_object_or_404(EmployerModel, id=id)

    context = {
        'vacancy': vacancy_obj,
        'requirements': split_lines(vacancy_obj.requirements_of_job),
        'benefits': split_lines(vacancy_obj.benefits_of_job),
        'responsibilities': split_lines(vacancy_obj.responsibilities_of_job),
        'current_year': get_current_year()
    }

    if request.user.is_authenticated:
        user = get_object_or_404(User, id=request.user.id)
        context['user_main'] = user

        with open('additional_files/liked_vacancies.json', "r") as file:
            data = json.load(file)

        user_id = str(user.id)

        try:
            if vacancy_obj.id in data['users'][user_id]:
                context['existence_in_liked_vacancies'] = True
            else:
                context['existence_in_liked_vacancies'] = False
        except KeyError:
            context['existence_in_liked_vacancies'] = False

    return render(request, 'employee/vacancy.html', context)


def resume(request, id=None):

    resume_obj = get_object_or_404(EmployeeModel, id=id)
    size_of_image = set_width_height_for_image(resume_obj.width_field, resume_obj.height_field)

    context = {
        'resume': resume_obj,
        'image_width': size_of_image[0],
        'image_height': size_of_image[1],
        'soft_skills': split_lines(resume_obj.soft_skills),
        'hard_skills': split_lines(resume_obj.hard_skills),
        'user': request.user,
        'current_year': get_current_year()
    }

    if resume_obj.image:
        context['image_existence'] = True
    else:
        context['image_existence'] = False

    return render(request, 'employee/resume.html', context)


def respond_to_vacancy(request, id=None):

    if not request.user.is_authenticated:
        return redirect('users:login')

    vacancy_obj = get_object_or_404(EmployerModel, id=id)
    user_obj = get_object_or_404(User, id=request.user.id)

    queryset_of_appropriate_resumes = EmployeeModel.objects.all().filter(user=user_obj)
    number_of_resumes = len(queryset_of_appropriate_resumes)

    subject = 'Response to the vacancy'
    from_email = settings.EMAIL_HOST_USER
    to = vacancy_obj.email

    # for local site
    prefix_for_url = 'http://127.0.0.1:8000'

    context_for_email = {
        'subject': subject,
        'vacancy': vacancy_obj,
        'resumes': queryset_of_appropriate_resumes,
        'number_of_resumes': number_of_resumes,
        'prefix': prefix_for_url
    }

    if queryset_of_appropriate_resumes:
        id_for_resume = [obj_id.id for obj_id in queryset_of_appropriate_resumes]
        emails = list(set([obj.email for obj in queryset_of_appropriate_resumes]))
        phone_numbers = list(set([obj.phone_number for obj in queryset_of_appropriate_resumes]))

        if number_of_resumes == 1:
            context_for_email['id_for_resume'] = id_for_resume[0]
            context_for_email['email'] = emails[0]
            context_for_email['phone_number'] = phone_numbers[0]
        else:
            context_for_email['id_for_resume'] = id_for_resume
            context_for_email['email'] = emails
            context_for_email['phone_number'] = phone_numbers

    html_content = render_to_string('employee/email_content.html', context_for_email)

    msg = EmailMessage(subject, html_content, from_email, [to])
    msg.content_subtype = "html"
    msg.send()

    extra_tags = 'html_safe'

    message = "An email with your information has been sent to the company's email address. " \
              "Wait for answer from employer. " \
              "Have a successful interview!"

    messages.info(request, message, extra_tags)

    return redirect('employee:home-employee')
