from django.db import models
from django.contrib.auth.models import User

class Question(models.Model):
    user = models.ForeignKey(User)
    title = models.CharField(max_length=255)
    description = models.TextField(max_length=2000)
    tags = models.CharField(max_length=255, null=True, blank=True)
    create_date = models.DateTimeField(auto_now_add=True)
    update_date = models.DateTimeField(auto_now_add=True)
    favorites = models.IntegerField(default=0)
    
    class Meta:
        verbose_name = 'Question'
        verbose_name_plural = 'Questions'
        ordering = ('-update_date',)

    def __unicode__(self):
        return self.title

    def get_answers(self):
        return Answer.objects.filter(question=self)

    def get_accepted_answer(self):
        return Answer.objects.get(question=self, is_accepted=True)

class Answer(models.Model):
    user = models.ForeignKey(User)
    question = models.ForeignKey(Question)
    description = models.TextField(max_length=2000)
    create_date = models.DateTimeField(auto_now_add=True)
    update_date = models.DateTimeField(null=True, blank=True)
    votes = models.IntegerField(default=0)
    is_accepted = models.BooleanField(default=False)
    
    class Meta:
        verbose_name = 'Answer'
        verbose_name_plural = 'Answers'
        ordering = ('-create_date',)

    def __unicode__(self):
        return self.description

    def accept(self):
        answers = Answer.objects.filter(question=self.question)
        for answer in answers:
            answer.is_accepted = False
            answer.save()
        self.is_accepted = True
        self.save()