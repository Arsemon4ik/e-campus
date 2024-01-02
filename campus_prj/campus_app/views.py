from django.shortcuts import render, redirect
from django.contrib import messages
from django.core.exceptions import PermissionDenied, ObjectDoesNotExist
from django.contrib.auth.decorators import login_required
from django.forms import inlineformset_factory
from .forms import ArticleForm
from .models import Article
import json


#
#
def main_page(request):
    """ Dashboard function returns a template with subjects and tasks from DB based on user """
    articles = Article.objects.all().order_by('-id')
    return render(request, 'campus_app/main.html', context={'articles': articles})


#
#
@login_required()
def articles_by_user_page(request):
    """ Dashboard function returns a template with subjects and tasks from DB based on user """
    user_articles = Article.objects.filter(user=request.user)
    from django.db.models import Count, Case, When, IntegerField, Sum

    # count_types = user_articles.order_by('type').values('type').annotate(Count('type'))
    # print(count_types)
    # result_arr = [_['type__count'] for _ in count_types]
    # print(result_arr)
    all_types = [choice[0] for choice in Article.type.field.choices]
    print(all_types)


    # Запит до бази даних для підрахунку кількості робіт по кожному типу
    result = (
        user_articles
        .values('type')
        .annotate(total=Count('type'))
    )

    # Створення словника з результатів запиту, де відсутнім типам робіт буде призначено значення 0
    result_arr = []
    result_dict = {item['type']: item['total'] for item in result}
    for type in all_types:
        print(f"Тип: {type}, Кількість робіт: {result_dict.get(type, 0)}")
        result_arr.append(result_dict.get(type, 0))



    form = ArticleForm()
    if request.method == "POST":
        form = ArticleForm(request.POST, request.FILES)
        if form.is_valid():
            article = form.save(commit=False)
            article.user = request.user
            article.save()
            return redirect('articles_by_user')
        else:
            messages.error(request, f'Виникла помилка: {form.errors} під час створення, спробуйте ще раз')

    context = {'articles': user_articles, 'count_types': result_arr,
               'form': form}
    return render(request, 'campus_app/articles_by_user.html', context=context)


@login_required()
def edit_article_page(request, article_id):
    """ Subject function returns a template with subjects and tasks from DB based on user """
    article = Article.objects.filter(id=article_id, user=request.user).first()

    form = ArticleForm(instance=article)
    if request.method == 'POST':
        form = ArticleForm(request.POST, request.FILES, instance=article)
        if form.is_valid():
            form.save()
            return redirect('articles_by_user')
        else:
            messages.error(request, 'Виникла помилка під час редагування, спробуйте ще раз')
    return render(request, 'campus_app/edit_article.html', {'form': form, 'article': article})


@login_required()
def delete_article(request, article_id):
    """ Dashboard function returns a template with subjects and tasks from DB based on user """
    article = Article.objects.filter(id=article_id, user=request.user).first()
    if article:
        article.delete()
        return redirect('articles_by_user')
    else:
        return redirect('articles_by_user')

#     from django.db.models import Count, Case, When, IntegerField, Sum
#     tasks = subject.task_set.filter(user=request.user)
#
#
#     total = tasks.aggregate(total_score=Sum('score'), count_done=Count(Case(When(status="done", then=1),
#                                                                             output_field=IntegerField())))
#
#     context = {'subject': subject.theme, 'tasks': tasks,
#                'formset': formset, 'form': form, 'total_score': total['total_score'],
#                'total_done': total['count_done']}
#     return render(request, 'tracker_app/tasks_by_subject.html', context=context)
#
#
# @login_required()
# def tasks_page(request):
#     """ Dashboard function returns a template with subjects and tasks from DB based on user """
#     tasks = Task.objects.filter(user=request.user)
#     context = {'tasks': tasks}
#     return render(request, 'tracker_app/tasks.html', context=context)
#
#
# # @login_required()
# # def create_subject_page(request):
# #     """ Subject function returns a template with subjects and tasks from DB based on user """
# #     form = SubjectForm()
# #     if request.method == 'POST':
# #         form = SubjectForm(request.POST)
# #         if form.is_valid():
# #             subject = form.save(commit=False)
# #             subject.user = request.user
# #             subject.save()
# #             return redirect('dashboard')
# #         else:
# #             messages.error(request, 'Something wrong with creating, please try again')
# #     return render(request, 'authentication/register.html', {'form': form})
#
# @login_required()
# def edit_subject_page(request, subject_id):
#     """ Subject function returns a template with subjects and tasks from DB based on user """
#     subject = Subject.objects.filter(id=subject_id, user=request.user).first()
#     if not subject:
#         ...
#         # raise 404 page
#     form = SubjectForm(instance=subject)
#     if request.method == 'POST':
#         form = SubjectForm(request.POST, instance=subject)
#         if form.is_valid():
#             form.save()
#             return redirect('dashboard')
#         else:
#             messages.error(request, 'Виникла помилка під час редагування, спробуйте ще раз')
#     return render(request, 'tracker_app/edit_subject.html', {'form': form, 'subject_theme': subject.theme})
#
#
# @login_required()
# def edit_task_page(request, task_id):
#     """ Subject function returns a template with subjects and tasks from DB based on user """
#     task = Task.objects.filter(id=task_id, user=request.user).first()
#     if not task:
#         raise ObjectDoesNotExist()
#         # raise 404 page
#     form = TaskForm(instance=task)
#     if request.method == 'POST':
#         form = TaskForm(request.POST, instance=task)
#         if form.is_valid():
#             task = form.save(commit=False)
#             task.user = request.user
#             task.save()
#             return redirect('dashboard')
#         else:
#             # print(form.ge)
#             messages.error(request, f'Виникла помилка {form.errors} під час редагування, спробуйте ще раз')
#     return render(request, 'tracker_app/edit_task.html', {'task_name': task.name, 'form': form})
#
#
# @login_required()
# def delete_subject(request, subject_id):
#     """ Dashboard function returns a template with subjects and tasks from DB based on user """
#     subject = Subject.objects.filter(id=subject_id, user=request.user).first()
#     if subject:
#         subject.delete()
#         return redirect('dashboard')
#     return render(request, 'tracker_app/tasks_by_subject.html', {})
#
#
# @login_required()
# def delete_task(request, task_id):
#     """ Dashboard function returns a template with subjects and tasks from DB based on user """
#     task = Task.objects.filter(id=task_id, user=request.user).first()
#     if task:
#         task.delete()
#         return redirect('dashboard')
#     return render(request, 'tracker_app/tasks_by_subject.html', {})
#
#
# @login_required()
# def update_subject_page(request):
#     """ Dashboard function returns a template with subjects and tasks from DB based on user """
#     subjects = Subject.objects.filter(user=request.user)
#     context = {'subjects': subjects}
#     return render(request, 'tracker_app/dashboard.html', context=context)
#
#
# @login_required()
# def delete_subject_page(request):
#     """ Dashboard function returns a template with subjects and tasks from DB based on user """
#     subjects = Subject.objects.filter(user=request.user)
#     context = {'subjects': subjects}
#     return render(request, 'tracker_app/dashboard.html', context=context)
