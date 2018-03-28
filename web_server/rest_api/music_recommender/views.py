from recommedation_client.rpc_client import RpcClient
from django.shortcuts import render


def index_page(request, user_id='', predicted_song=''):
    recommender = RpcClient(host='queue', routing_key='rpc_recommendations')

    if request.method == "POST":
        user_id = request.POST["text"]
        predicted_song = recommender.call({'user_id': user_id})

    return render(request, 'music_recommender/music_template.html', {'predicted_song': predicted_song,
                                                                     'user_id': user_id})
