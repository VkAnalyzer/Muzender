from recommedation_client import recommedation_client as rc
from django.shortcuts import render

def index_page(request, user_id='', predicted_song=''):
    recommender = rc.RpcClient()
    if request.method == "POST":
        user_id = request.POST["text"]
        predicted_song = recommender.call(user_id)

    return render(request, 'music_recommender/music_template.html', {'predicted_song': predicted_song,
                                                                     'user_id': user_id})