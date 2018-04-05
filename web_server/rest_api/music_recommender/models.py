from django.db import models


class VkProfile(models.Model):
  modified = models.DateTimeField(auto_now=True)
  vk_id = models.CharField(max_length=30)


class Band(models.Model)
  user = models.ForeignKey(VkProfile, related_name='bands')
  band_name = models.CharField(max_length=128)


class Song(models.Model):
  band = models.ForeignKey(Bands, related_name='songs')
  song_name = models.CharField(max_length=128)
