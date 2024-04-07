from django.shortcuts import render
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

QUESTIONS = [
    {
        "id": i,
        "title": f"Question {i}",
        "text": f"This is question number {i}"
    } for i in range(40)
]

ANSWERS = [
    {
        "id": i,
        "title": f"Answer {i}",
        "text": f"This is answer number {i}"
    } for i in range(20)
]

# Create your views here.
def index(request):
    page_num = request.GET.get('page', 1)
    paginator = Paginator(QUESTIONS, 5)
    # page_obj = paginator.page(1)
    try:
        page_obj = paginator.page(page_num)
    except PageNotAnInteger:
        page_obj = paginator.page(1)
    except EmptyPage:
        page_obj = paginator.page(1)
    return render(request, "index.html", {"questions": page_obj})

def question(request, question_id):
    page_num = request.GET.get('page', 1)
    paginator = Paginator(ANSWERS, 5)
    try:
        page_obj = paginator.page(page_num)
    except PageNotAnInteger:
        page_obj = paginator.page(1)
    except EmptyPage:
        page_obj = paginator.page(1)
    item = QUESTIONS[question_id]
    return render(request, "question.html", {"question": item, "answers" : page_obj})


def ask(request):
    return render(request, "ask.html")

def hot(request):
    page_num = request.GET.get('page', 1)
    paginator = Paginator(QUESTIONS[20::2], 5)
    try:
        page_obj = paginator.page(page_num)
    except PageNotAnInteger:
        page_obj = paginator.page(1)
    except EmptyPage:
        page_obj = paginator.page(1)
    return render(request, "hot.html", {"questions": page_obj})

def signup(request):
    return render(request, "signup.html")

def login(request):
    return render(request, "login.html")

def profile_edit(request):
    return render(request, "profile_edit.html")

def tag(request, tag_name):
    page_num = request.GET.get('page', 1)
    paginator = Paginator(QUESTIONS, 5)
    try:
        page_obj = paginator.page(page_num)
    except PageNotAnInteger:
        # Если параметр 'page' не является целым числом, отобразить первую страницу
        page_obj = paginator.page(1)
    except EmptyPage:
        # Если параметр 'page' больше максимального числа страниц, отобразить последнюю страницу
        page_obj = paginator.page(paginator.num_pages)
    return render(request, "tag.html", {"questions": page_obj, "tag_name": tag_name})