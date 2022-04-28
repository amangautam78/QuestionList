from django.db import models

# Create your models here.

class Question(models.Model):
    qid = models.IntegerField()
    title = models.CharField(max_length=200)
    type = models.CharField(max_length=50)
    url = models.URLField()

    def __str__(self):
        return self.qid + ' ' + self.title
