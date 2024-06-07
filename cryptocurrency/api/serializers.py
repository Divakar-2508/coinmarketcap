from .models import Job, Task, Output, Contract, OfficialLink, Social
from rest_framework import serializers

class ContractSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contract
        fields = ['name', 'address']

class OfficialLinkSerializer(serializers.ModelSerializer):
    class Meta:
        model = OfficialLink
        fields = ['name', 'link']

class SocialSerializer(serializers.ModelSerializer):
    class Meta:
        model = Social
        fields = ['name', 'url']

class OutputSerializer(serializers.ModelSerializer):
    contracts = ContractSerializer(many=True)
    official_links = OfficialLinkSerializer(many=True)
    socials = SocialSerializer(many=True)

    class Meta:
        model = Output
        fields = [
            'price', 'price_change', 'market_cap', 'market_cap_rank',
            'volume', 'volume_rank', 'volume_change', 'circulating_supply', 
            'total_supply', 'diluted_market_cap', 'contracts', 'official_links', 'socials'
        ]

class TaskSerializer(serializers.ModelSerializer):
    output = OutputSerializer()

    class Meta:
        model = Task
        fields = ['coin', 'output']

class JobSerializer(serializers.ModelSerializer):
    tasks = TaskSerializer(many = True)

    class Meta:
        model = Job
        fields = ['job_id', 'tasks']