from django.core.management.base import BaseCommand
from app.models import *
from faker import Faker
import random

class Command(BaseCommand):
    fake = Faker()

    def add_arguments(self, parser):
        parser.add_argument("ratio", type=int)

    def handle(self, *args, **options):
        ratio = options['ratio']

        user_count = ratio
        question_count = ratio * 10
        answer_count = ratio * 100
        tag_count = ratio
        questionlike_count = ratio * 10
        answerlike_count = ratio * 10

        #self.create_users(user_count)
        # self.create_tags(tag_count)
        # self.create_questions(question_count)
        # self.create_answers(answer_count)
        #self.create_questionlikes(questionlike_count)
        #self.create_answerlikes(answerlike_count)
        #self.set_like_numbers()
        #self.tags_questions()
        #self.create_profiles(user_count)

    def create_users(self, count):
        print("Start: users")
        usernames = [self.fake.word() for _ in range(count)]
        users = [User(username=usernames[i] + str(i* 13), 
                      email = self.fake.email(), 
                      password = self.fake.password()) 
                      for i in range(count)]
        User.objects.bulk_create(users)
        print("Finish: users")

    def create_tags(self, count):
        print("Start: tags")
        tag_names = [self.fake.word() for _ in range(count)]
        tags = [Tag(name=tag_names[i]) for i in range(count)]
        Tag.objects.bulk_create(tags)
        print("Finish: tags")

    def create_questions(self, count):
        print("Start: questions")
        users = User.objects.all()
        questions = [Question(user=random.choice(users), 
                              title = self.fake.sentence(), 
                              text = self.fake.text()) 
                              for _ in range(count)]
        Question.objects.bulk_create(questions)
        print("Finish: questions")


    def create_answers(self, count):
        print("Start: answers")
        users = User.objects.all()
        questions = Question.objects.all()
        answers = [Answer(user=random.choice(users), 
                              question = random.choice(questions), 
                              text = self.fake.text()) 
                              for _ in range(count)]
        Answer.objects.bulk_create(answers)
        print("Finish: answers")

    def create_questionlikes(self, count):
        print("Start: question likes")
        users = User.objects.all()
        questions = Question.objects.all()
        questionlikes = []
        for i in range(count):
            question = questions[i]
            user = random.choice(users)
            if not (QuestionLike(question=question, user=user, value=random.choice([-1, 1])) in questionlikes or 
                    QuestionLike.objects.filter(user=user, question=question).exists()):
                questionlikes.append(QuestionLike(question=question,
                                      user=user,
                                      value=random.choice([-1, 1])))
            
        
        QuestionLike.objects.bulk_create(questionlikes)
        print("Finish: question likes")

    def create_answerlikes(self, count):
        print("Start: answer likes")
        users = User.objects.all()
        answers = Answer.objects.all()
        answerlikes = []
        for i in range(count):
            answer = answers[i]
            user = random.choice(users)
            if not (AnswerLike(answer=answer, user=user, value=random.choice([-1, 1])) in answerlikes or 
                    AnswerLike.objects.filter(user=user, answer=answer).exists()):
                answerlikes.append(AnswerLike(answer=answer,
                                      user=user,
                                      value=random.choice([-1, 1])))

            
        
        AnswerLike.objects.bulk_create(answerlikes)
        print("Finish: answer likes")

    def set_like_numbers(self):
        print("Start: set likes to questions")
        questions = Question.objects.all()
        for question in questions:
            likes_value = 0
            likes = QuestionLike.objects.filter(question=question)
            for like in likes:
                likes_value = likes_value + like.value

            question.like_number = likes_value
            question.save()
        print('Finish: set likes to questions')

        print("Start: set likes to answers")
        answers = Answer.objects.all()
        for answer in answers:
            likes_value = 0
            likes = AnswerLike.objects.filter(answer=answer)
            for like in likes:
                likes_value = likes_value + like.value

            answer.like_number = likes_value
            answer.save()
        print('Finish: set likes to answers')

    def tags_questions(self):
        tags = Tag.objects.all()
        print('Start: tags on questions')
        for question in Question.objects.all():
            tags_to_add = random.choices(tags, k=2)
            for tag in tags_to_add:
                question.tags.add(tag.id)
                question.save()

        print('Finish: tags on questions')

    def create_profiles(self, count):
        print("Start: profiles")
        users = User.objects.all()
        profiles = []
        for user in users:
            profiles.append(Profile(user=user))

        Profile.objects.bulk_create(profiles)
        print("Finish: profiles")



    

    

    



