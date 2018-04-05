from recommedation_client.rpc_client import RpcClient
from django.shortcuts import render
from rest_framework import viewsets
from .models import VkProfile, Band, Song
from .serializers import VkProfileSerializer, BandSerializer, SongSerializer


def index_page(request, user_id='', predicted_song=''):
    recommender = RpcClient(host='queue', routing_key='rpc_recommendations')

    if request.method == "POST":
        user_id = request.POST["text"]
        predicted_song = recommender.call({'user_id': user_id})

    return render(request, 'music_recommender/music_template.html', {'predicted_song': predicted_song,
                                                                     'user_id': user_id})


class VkProfileViewSet(viewsets.ModelViewSet):
  queryset = VkProfile.objects.all()
  serializer_class = VkProfileSerializer

  def perform_create(self, serializer):
    user_id = self.request.data['vk_id']
    if VkProfile.objects.filter(vk_id=user_id).exists():
      self.destroy(self.request)
    serializer.save()
