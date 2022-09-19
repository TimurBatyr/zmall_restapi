from django.shortcuts import render
from rest_framework import generics

from info.models import Issue, Help, AdminContact, AdminHat, ConfPolitics, Footer
from info.serializers import IssueSerializer, HelpSerializer, AdminContactSerializer, AdminHatSerializer, \
    ConfPoliticsSerializer, FooterSerializer


class IssueAPIView(generics.ListAPIView):
    '''List of issues'''
    queryset = Issue.objects.all()
    serializer_class = IssueSerializer


class HelpAPIView(generics.ListAPIView):
    '''List of names of help'''
    queryset = Help.objects.all()
    serializer_class = HelpSerializer


class HelpGetAPIView(generics.RetrieveAPIView):
    '''Detail help'''
    queryset = Help.objects.all()
    serializer_class = HelpSerializer


class AdminHatAPIView(generics.ListAPIView):
    '''List of categories'''
    queryset = AdminHat.objects.all()
    serializer_class = AdminHatSerializer


class AdminContactCreateAPIView(generics.CreateAPIView):
    '''Contact with admin'''
    queryset = AdminContact.objects.all()
    serializer_class = AdminContactSerializer


class AdminContactListAPIView(generics.ListAPIView):
    '''Contact with admin'''
    queryset = AdminContact.objects.all()
    serializer_class = AdminContactSerializer


class AdminContactGetAPIView(generics.RetrieveAPIView):
    '''Contact with admin'''
    queryset = AdminContact.objects.all()
    serializer_class = AdminContactSerializer


class ConfPoliticsAPIView(generics.ListAPIView):
    '''Confidentiality politics'''
    queryset = ConfPolitics.objects.all()
    serializer_class = ConfPoliticsSerializer


class FooterListAPIView(generics.ListAPIView):
    '''Footer'''
    queryset = Footer.objects.all()
    serializer_class = FooterSerializer



