from django.shortcuts import render
from rest_framework import generics

from info.models import Issue, Help
from info.serializers import IssueSerializer, HelpSerializer


class IssueAPIView(generics.ListAPIView):
    '''List of issues'''
    queryset = Issue.objects.all()
    serializer_class = IssueSerializer


class HelpAPIView(generics.ListAPIView):
    '''List of names of help'''
    queryset = Help.objects.all()
    serializer_class = HelpSerializer


class DetailHelpAPIView(generics.RetrieveAPIView):
    '''Detail help'''
    queryset = Help.objects.all()
    serializer_class = HelpSerializer
