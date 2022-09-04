from django.db import models  # noqa F401

class Pokemon(models.Model):
    title = models.CharField(max_length=200)
    title_en = models.CharField(max_length=200, null=True)
    title_jp = models.CharField(max_length=200, null=True)
    description = models.TextField(null=True)
    photo = models.ImageField(blank=True, null=True)
    previous_evolution = models.ForeignKey('self',
                                           on_delete=models.CASCADE,
                                           blank=True,
                                           null=True,
                                           related_name='next_evolution')

    def __str__(self):
        return '{}'.format(self.title)

# makemigrations
# migrate
# runserver

class PokemonEntity(models.Model):
    pokemon = models.ForeignKey(Pokemon, on_delete=models.CASCADE)
    lat = models.FloatField()
    lon = models.FloatField()
    appeared_at = models.DateTimeField(null=True)
    disappeared_at = models.DateTimeField(null=True)
    level = models.IntegerField()
    health = models.IntegerField()
    attack = models.IntegerField()
    protection = models.IntegerField()
    endurance = models.IntegerField()