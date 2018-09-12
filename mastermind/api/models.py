import uuid
from django.utils import timezone
from django.db import models


class Game(models.Model):
    id = models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True)
    pattern_1 = models.CharField(max_length=10)
    pattern_2 = models.CharField(max_length=10)
    pattern_3 = models.CharField(max_length=10)
    pattern_4 = models.CharField(max_length=10)
    created_by = models.CharField(max_length=150)
    created_at = models.DateTimeField(default=timezone.now())

    def __str__(self):
        return str(self.id)


class Guess(models.Model):
    id = models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True)
    game_id = models.ForeignKey('Game', on_delete=models.CASCADE)
    guess_1 = models.CharField(max_length=10)
    guess_2 = models.CharField(max_length=10)
    guess_3 = models.CharField(max_length=10)
    guess_4 = models.CharField(max_length=10)
    black = models.SmallIntegerField(default=0)
    white = models.SmallIntegerField(default=0)
    created_by = models.CharField(max_length=150)
    created_at = models.DateTimeField(default=timezone.now())

    def __str__(self):
        return '{} - [{},{},{},{}] - [{},{}]'\
            .format(self.game_id, self.guess_1, self.guess_2, self.guess_3, self.guess_4, self.black, self.white)

    class Meta:
        ordering = ['-created_at']
