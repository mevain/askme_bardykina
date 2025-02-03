from django.shortcuts import render, get_object_or_404
from app.models import *
from django.contrib import auth
from django.urls import reverse
from django.shortcuts import redirect
from django.contrib.auth import login, authenticate
from django.views.decorators.http import require_http_methods
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Count
from app.forms import LoginForm, RegisterForm, QuestionForm, SettingsForm, AnswerForm

def pagination(objects, request, per_page):
    page_num = request.GET.get('page', 1)
    paginator = Paginator(objects, per_page)
    try:
        page_obj = paginator.page(page_num)
    except PageNotAnInteger:
        page_obj = paginator.page(1)
    except EmptyPage:
        page_obj = paginator.page(1)

    return page_obj
    

# Create your views here.
def index(request):
    popular_tags = Tag.objects.get_popular()
    questions = pagination(Question.objects.get_new(), request, 5)
    return render(request, "index.html", {"questions": questions, 'popular_tags': popular_tags})

@require_http_methods(['GET', 'POST'])

def question(request, question_id):
    popular_tags = Tag.objects.get_popular()
    item = get_object_or_404(Question, id=question_id)
    answers = Answer.objects.filter(question=item).order_by('-created_at')
    paginated_answers = pagination(answers, request, 5)
    
    if request.method == "GET":
        answer_form = AnswerForm()
    if request.method == "POST":
        answer_form = AnswerForm(request.POST)
        if answer_form.is_valid():
            text = answer_form.cleaned_data['text']
            new_answer = Answer.objects.create(
                text=text,
                user=request.user,
                question=item
            )
            answer_position = list(answers).index(new_answer) + 1
            page_number = (answer_position - 1) // 5 + 1

            return redirect(f'{request.path}?page={page_number}#{new_answer.id}')
    return render(request, "question.html", {"question": item, "answers" : answers, "form": answer_form, 'popular_tags': popular_tags})

def ask(request):
    popular_tags = Tag.objects.get_popular()
    if request.method == "GET":
        question_form = QuestionForm()
    if request.method == 'POST':
        question_form = QuestionForm(request.POST)
        if question_form.is_valid():
            title = question_form.cleaned_data['title']
            text = question_form.cleaned_data['text']
            tags_input = question_form.cleaned_data['tags']
            tags = [tag.strip() for tag in tags_input.split(' ')]
            if len(tags) > 3:
                error_message = "You cannot use more than 3 tags"
                return render(request, "signup.html", {'form': question_form, 'error_message': error_message})
            question = Question.objects.create(
                title=title,
                text=text,
                user=request.user
            )
            for tag_name in tags:
                print(tag_name)
                tag, created = Tag.objects.get_or_create(name=tag_name)
                question.tags.add(tag)

            question_id = question.id
            print(question_id)
            return redirect(reverse('question', kwargs={'question_id': question_id}))
    return render(request, "ask.html", {'form': question_form, 'popular_tags': popular_tags})

def hot(request):
    popular_tags = Tag.objects.get_popular()
    questions = pagination(Question.objects.get_hot(), request, 5)
    return render(request, "hot.html", {"questions": questions, 'popular_tags': popular_tags})

def signup(request):
    popular_tags = Tag.objects.get_popular()
    if request.method == 'GET':
        user_form = RegisterForm()
    if request.method == 'POST':
        user_form = RegisterForm(request.POST)
        if user_form.is_valid():
            user = user_form.save()
            auth.login(request, user)
            profile = Profile.objects.create(user=user, avatar=user_form.cleaned_data['avatar'])
            if user:
                return redirect(reverse('index'))
            else:
                user_form.add_error(field=None, error="User saving error!")
    return render(request, "signup.html", {'form': user_form, 'popular_tags': popular_tags})


def log_in(request):
    popular_tags = Tag.objects.get_popular()
    redirect_to = request.GET.get('next', '')
    if request.method == 'POST':
        redirect_to = request.POST.get('next', '')
        login_form = LoginForm(data=request.POST)
        if login_form.is_valid():
            username = login_form.cleaned_data['login']
            password = login_form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user:
                login(request, user)
                if redirect_to:
                    return HttpResponseRedirect(redirect_to)
                return redirect('index')
            else:
                error_message = "Invalid username or password"
                return render(request, 'log_in.html', {'form': login_form, 'error_message': error_message, 'redirect_to': redirect_to})
    else:
        login_form = LoginForm()

    return render(request, "log_in.html", context={"form": login_form, 'popular_tags': popular_tags, 'redirect_to': redirect_to})

def logout(request):
    auth.logout(request)
    return redirect('index')

def profile_edit(request):
    popular_tags = Tag.objects.get_popular()
    if request.method == "GET":
        settings_form = SettingsForm(initial={'username': request.user.username})
    if request.method == "POST":
        settings_form = SettingsForm(request.POST, request.FILES)
        if settings_form.is_valid():
            user = settings_form.save()
            return redirect('profile_edit')
    return render(request, "profile_edit.html", {'form': settings_form, 'popular_tags': popular_tags})

def tag(request, tag_name):
    popular_tags = Tag.objects.get_popular()
    questions = pagination(Question.objects.get_tag(tag_name), request, 5)
    return render(request, "tag.html", {"questions": questions, "tag_name": tag_name, 'popular_tags': popular_tags})