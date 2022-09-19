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
        return f'ID - {self.id} : Issue - {self.issue.title} : {self.title}'


class AdminHat(models.Model):
    """Admin hat"""
    title = models.CharField(max_length=100, unique=True)
    description = models.TextField()

    def __str__(self):
        return self.title


THEME = (
        ('abc', 'abc'),
        ('acb', 'acb'),
        ('cba', 'cba'),
        ('other', 'other')
    )


class AdminContact(models.Model):
    """Contact with admin"""
    adminhat = models.ForeignKey(AdminHat, related_name='categories', on_delete=models.CASCADE)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    theme = models.CharField(max_length=100, choices=THEME, default=('other', 'other'))
    message = models.TextField()
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'ID:{self.id} - {self.adminhat} - {self.theme} - {self.date_created}'


class ConfPolitics(models.Model):
    """Confidentiality politics"""
    title = models.CharField(max_length=100)
    description = models.TextField()

    def __str__(self):
        return self.title

class Footer(models.Model):
    """Footer"""
    title = models.CharField(max_length=100)
    image = models.ImageField()
    link = models.URLField()
    def __str__(self):
        return f'ID:{self.id} - {self.title} - {self.link}'
