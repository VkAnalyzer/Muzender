from recommendation_client.rpc_client import RpcClient
from rest_framework.parsers import JSONParser
from django.http import JsonResponse
from rest_framework.decorators import api_view
import time
import random


@api_view(['GET', 'POST'])
def get_recommendation(request):
    if request.method == 'POST':
        request_data = JSONParser().parse(request)

        rpc_client = RpcClient(routing_key='user_id', host='queue')
        response = rpc_client.call(request_data)
        recommendations = response['recommendations']
        return JsonResponse(recommendations, safe=False)
