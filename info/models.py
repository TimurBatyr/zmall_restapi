from django.db import models


class Issue(models.Model):
    """Category for post"""
    title = models.CharField(max_length=100)

    def __str__(self):
        return f'ID {self.id} : {self.title}'


class Help(models.Model):
    issue = models.ForeignKey(Issue, related_name='help', on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    description = models.TextField()

    def __str__(self):
        return f'ID {self.id} : {self.title}'
