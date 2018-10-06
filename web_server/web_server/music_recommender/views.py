from recommendation_service.rpc_client import RpcClient
from rest_framework.parsers import JSONParser
from django.http import JsonResponse
from rest_framework.decorators import api_view


@api_view(['GET', 'POST'])
def get_recommendation(request):

  if request.method == 'POST':
    recommender = RpcClient(host='queue', routing_key='rpc_recommendations')
    request_data = JSONParser().parse(request)
    user_id = request_data["user_id"]
    predicted_bands = recommender.call({'user_id': user_id})
    #predicted_bands = ['545', '3434', 'asdasd']
    return JsonResponse(predicted_bands, safe=False)
