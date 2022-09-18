from django.db import models


class Issue(models.Model):
    """Category for post"""
    title = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.title


class Help(models.Model):
    issue = models.ForeignKey(Issue, related_name='help', on_delete=models.CASCADE)
    description = models.TextField()


