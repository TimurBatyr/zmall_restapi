from rest_framework import serializers

from info.models import Issue, Help, AdminContact, AdminHat, ConfPolitics, Footer


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


class AdminHatSerializer(serializers.ModelSerializer):
    """Admin hat"""
    class Meta:
        model = AdminHat
        fields = '__all__'


class AdminContactSerializer(serializers.ModelSerializer):
    """Contact with admin"""
    class Meta:
        model = AdminContact
        fields = ['adminhat', 'first_name', 'last_name', 'theme', 'message', 'date_created']


class ConfPoliticsSerializer(serializers.ModelSerializer):
    """Confidentiality politics"""
    class Meta:
        model = ConfPolitics
        fields = '__all__'


class FooterSerializer(serializers.ModelSerializer):
    """Footer"""
    class Meta:
        model = Footer
        fields = '__all__'

    def to_representation(self, instance):
        repr = super().to_representation(instance)
        repr["text"] = "@ 2022 все права защищены"
        return repr

