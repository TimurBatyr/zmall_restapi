from django.http import JsonResponse
from django.shortcuts import render
from rest_framework import generics
from rest_framework.pagination import PageNumberPagination
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.views import APIView

from info.models import Issue, Help, AdminContact, AdminHat, ConfPolitics, Footer, AdminTheme
from info.serializers import IssueSerializer, HelpSerializer, AdminContactSerializer, AdminHatSerializer, \
    ConfPoliticsSerializer, FooterSerializer, AdminThemeSerializer


class Pagination(PageNumberPagination):
    '''Pagination for all'''
    def get_paginated_response(self, data):
        return super().get_paginated_response(data)


class IssueAPIView(generics.ListAPIView):
    '''List of issues'''
    queryset = Issue.objects.all()
    serializer_class = IssueSerializer


class HelpPagination(Pagination):
    page_size = 1000

class HelpAPIView(generics.ListAPIView):
    '''List of names of help'''
    queryset = Help.objects.all()
    serializer_class = HelpSerializer
    pagination_class = HelpPagination


class HelpGetAPIView(generics.RetrieveAPIView):
    '''Detail help'''
    queryset = Help.objects.all()
    serializer_class = HelpSerializer


class AdminHatAPIView(generics.ListAPIView):
    '''List of categories'''
    queryset = AdminHat.objects.all()
    serializer_class = AdminHatSerializer


class AdminThemeAPIView(generics.ListAPIView):
    queryset = AdminTheme.objects.all()
    serializer_class = AdminThemeSerializer


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



