from django.shortcuts import render


def index_page(request, user_id='', predicted_song=''):
    if request.method == "POST":
        user_id = request.POST["text"]
        predicted_song = 5 + int(user_id)
    return render(request, 'music_recommender/music_template.html', {'predicted_song': predicted_song,
                                                                     'user_id': user_id})