from recommendation_service.rpc_client import connection, channel, RpcClient
from rest_framework.parsers import JSONParser
from django.http import JsonResponse
from rest_framework.decorators import api_view
import time
import random


@api_view(['GET', 'POST'])
def get_recommendation(request):

  if request.method == 'POST':
    request_data = JSONParser().parse(request)
    user_id = request_data['user_id']

    rpc_client = RpcClient(connection=connection, channel=channel, routing_key='user_id')
    predicted_bands = rpc_client.call({'user_id': user_id})
    #time.sleep(5)
    #predicted_bands = ['545', '3434', str(random.randint(1, 100))]
    return JsonResponse(predicted_bands, safe=False)
