from django.db import models
from django.contrib.auth.models import User
from datetime import date

# Create your models here.


class Tag(models.Model):
    name = models.CharField(max_length=20)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
    

class QuestionManager(models.Manager):
    def get_hot(self):
        return self.order_by('-like_number')
    
    def get_new(self):
        return self.order_by('-created_at')
    
    def get_tag(self, tag_name):
        return self.filter(tags__name=tag_name)
    
    def get_answer_number(self):
        return Answer.objects.filter(question=self).count()


class Question(models.Model):
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    title = models.CharField(max_length=100)
    text = models.CharField(max_length=1000)
    tags = models.ManyToManyField(Tag)
    like_number = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = QuestionManager()

    def __str__(self):
        return self.title



class Answer(models.Model):
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    text = models.CharField(max_length=1000)
    like_number = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    def __str__(self):
        return self.text


class QuestionLike(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    value = models.IntegerField(default=1)
    class Meta:
        unique_together = ('user', 'question',)

    def __str__(self):
        return f"{self.user.username} {self.question.title}"


class AnswerLike(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    answer = models.ForeignKey(Answer, on_delete=models.CASCADE)
    value = models.IntegerField(default=1)

    class Meta:
        unique_together = ('user', 'answer',)

    def __str__(self):
        return f"{self.user.username} {self.answer.text}"


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    avatar = models.ImageField(null=True, blank=True)

    def __str__(self):
        return f"{self.user.username}"

