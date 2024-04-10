from django.shortcuts import render, get_object_or_404
from app.models import *
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Count

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

def question(request, question_id):
    answers = pagination(Answer.objects.filter(question=question_id).order_by('-created_at'), request, 5)
    item = get_object_or_404(Question, id=question_id)
    return render(request, "question.html", {"question": item, "answers" : answers})


def ask(request):
    return render(request, "ask.html")

def hot(request):
    questions = pagination(Question.objects.get_hot(), request, 5)
    return render(request, "hot.html", {"questions": questions})

def signup(request):
    return render(request, "signup.html")

def login(request):
    return render(request, "login.html")

def profile_edit(request):
    return render(request, "profile_edit.html")

def tag(request, tag_name):
    questions = pagination(Question.objects.get_tag(tag_name), request, 5)
    return render(request, "tag.html", {"questions": questions, "tag_name": tag_name})