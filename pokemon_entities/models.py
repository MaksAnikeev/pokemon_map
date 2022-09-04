from django.db import models  # noqa F401

class Pokemon(models.Model):
    title = models.CharField('имя рус.',
                             max_length=200)
    title_en = models.CharField('имя англ.',
                                max_length=200,
                                null=True)
    title_jp = models.CharField('имя япон.',
                                max_length=200,
                                null=True,
                                blank=True)
    description = models.TextField('описание',
                                   null=True,
                                   blank=True)
    photo = models.ImageField('картинка аватар',
                              null=True)
    previous_evolution = models.ForeignKey('self',
                                           on_delete=models.CASCADE,
                                           blank=True,
                                           null=True,
                                           related_name='next_evolution',
                                           verbose_name='из кого эволюционировал')

    def __str__(self):
        return '{}'.format(self.title)

# makemigrations
# migrate
# runserver

class PokemonEntity(models.Model):
    pokemon = models.ForeignKey(Pokemon,
                                on_delete=models.CASCADE,
                                verbose_name='имя покемона')
    lat = models.FloatField('координата широта')
    lon = models.FloatField('координата длинна')
    appeared_at = models.DateTimeField('дата появления', null=True)
    disappeared_at = models.DateTimeField('дата исчезновения', null=True)
    level = models.IntegerField('уровень')
    health = models.IntegerField('здоровье',
                                 blank=True)
    attack = models.IntegerField('атака',
                                 blank=True)
    protection = models.IntegerField('защита',
                                     blank=True)
    endurance = models.IntegerField('обучение',
                                    blank=True)