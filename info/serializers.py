from rest_framework import serializers

from info.models import Issue, Help


class IssueSerializer(serializers.ModelSerializer):
    '''List of issues'''
    class Meta:
        model = Issue
        fields = '__all__'


class HelpSerializer(serializers.ModelSerializer):
    '''List of names of help'''
    class Meta:
        model = Help
        fields = '__all__'