from django.shortcuts import render, get_object_or_404
from app.models import *
from django.contrib import auth
from django.urls import reverse
from django.shortcuts import redirect
from django.contrib.auth import login, authenticate
from django.views.decorators.http import require_http_methods
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
    questions = pagination(Question.objects.get_new(), request, 5)
    return render(request, "index.html", {"questions": questions})

@require_http_methods(['GET', 'POST'])

def question(request, question_id):
    answers = pagination(Answer.objects.filter(question=question_id).order_by('-created_at'), request, 5)
    item = get_object_or_404(Question, id=question_id)
    if request.method == "GET":
        answer_form = AnswerForm()
    if request.method == "POST":
        answer_form = AnswerForm(request.POST)
        if answer_form.is_valid():
            text = answer_form.cleaned_data['answer']
            answer = Answer.objects.create(
                text = text,
                user = request.user,
                question = item
            )
            return redirect('question', question_id=question_id)
    return render(request, "question.html", {"question": item, "answers" : answers, "form": answer_form})


def ask(request):
    if request.method == "GET":
        question_form = QuestionForm()
    if request.method == 'POST':
        question_form = QuestionForm(request.POST)
        if question_form.is_valid():
            title = question_form.cleaned_data['title']
            text = question_form.cleaned_data['text']
            tags_input = question_form.cleaned_data['tags']
            tags = [tag.strip() for tag in tags_input.split(',')]
            question = Question.objects.create(
                title=title,
                text=text,
                user=request.user
            )
            for tag_name in tags:
                tag, created = Tag.objects.get_or_create(name=tag_name)
                question.tags.add(tag)

            question_id = question.id
            print(question_id)
            return redirect(reverse('question', kwargs={'question_id': question_id}))
    return render(request, "ask.html", {'form': question_form})

def hot(request):
    questions = pagination(Question.objects.get_hot(), request, 5)
    return render(request, "hot.html", {"questions": questions})

def signup(request):
    if request.method == "GET":
        user_form = RegisterForm()
    if request.method == "POST":
        user_form = RegisterForm(request.POST)
        if user_form.is_valid():
            username = user_form.cleaned_data['login']
            email = user_form.cleaned_data['email']
            password = user_form.cleaned_data['password']
            nickname = user_form.cleaned_data['nickname']
            password2 = user_form.cleaned_data['password2']
            avatar = user_form.cleaned_data['avatar']
            if password != password2:
                error_message = "Passwords do not match"
                return render(request, "signup.html", {'form': user_form, 'error_message': error_message})
            if User.objects.filter(username=username).exists():
                error_message = "This username is already taken. Please choose another one."
                return render(request, 'signup.html', {'form': user_form, 'error_message': error_message})
            user = User.objects.create_user(username=username, email=email, password=password)
            user = authenticate(request, username=username, password=password)
            if user:
                login(request, user)
            return redirect('index')
    return render(request, 'signup.html', {'form': user_form})


def log_in(request):
    if request.method == 'GET':
        login_form = LoginForm()
    if request.method == 'POST':
        login_form = LoginForm(data=request.POST)
        if login_form.is_valid():
            username = login_form.cleaned_data['login']
            password = login_form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)

            if user:
                login(request, user)
                return redirect(reverse('index'))
            else:
                error_message = "Invalid username or password"
                return render(request, 'log_in.html', {'form': login_form, 'error_message' : error_message})
    return render(request, "log_in.html", context={"form": login_form})

def logout(request):
    auth.logout(request)
    return redirect('index')

def profile_edit(request):
    if request.method == "GET":
        settings_form = SettingsForm(initial={'email': request.user.email, 'login': request.user.username})
    if request.method == "POST":
        settings_form = SettingsForm(request.POST, request.FILES)
        if settings_form.is_valid():
            email = settings_form.cleaned_data['email']
            login = settings_form.cleaned_data['login']
            nickname = settings_form.cleaned_data['nickname']
            avatar = settings_form.cleaned_data['avatar']

            user = request.user
            user.email = email
            user.username = login
            user.nickname = nickname
            user.save()

            return redirect('profile_edit')
    return render(request, "profile_edit.html", {'form': settings_form})

def tag(request, tag_name):
    questions = pagination(Question.objects.get_tag(tag_name), request, 5)
    return render(request, "tag.html", {"questions": questions, "tag_name": tag_name})