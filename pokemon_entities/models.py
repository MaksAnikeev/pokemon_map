from django.db import models


class Pokemon(models.Model):
    title = models.CharField('имя рус.',
                             max_length=200)
    title_en = models.CharField('имя англ.',
                                max_length=200,
                                default="")
    title_jp = models.CharField('имя япон.',
                                max_length=200,
                                default="",
                                blank=True)
    description = models.TextField('описание',
                                   default="",
                                   blank=True)
    photo = models.ImageField('картинка аватар',
                              null=True)
    previous_evolution = models.ForeignKey('self',
                                           on_delete=models.SET_NULL,
                                           blank=True,
                                           null=True,
                                           related_name='next_evolutions',
                                           verbose_name='из кого эволюционировал')

    def __str__(self):
        return self.title


class PokemonEntity(models.Model):
    pokemon = models.ForeignKey(Pokemon,
                                on_delete=models.CASCADE,
                                related_name='pokemon_entities',
                                verbose_name='имя покемона')
    lat = models.FloatField('координата широта')
    lon = models.FloatField('координата длинна')
    appeared_at = models.DateTimeField('дата появления', null=True)
    disappeared_at = models.DateTimeField('дата исчезновения', null=True)
    level = models.IntegerField('уровень')
    health = models.IntegerField('здоровье',
                                 blank=True,
                                 null=True)
    attack = models.IntegerField('атака',
                                 blank=True,
                                 null=True)
    protection = models.IntegerField('защита',
                                     blank=True,
                                     null=True)
    endurance = models.IntegerField('обучение',
                                    blank=True,
                                    null=True)
