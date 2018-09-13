import random
from django.db import models
from api.utils import Color


class Game(models.Model):
    # id = models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True)
    pattern_1 = models.CharField(max_length=10)
    pattern_2 = models.CharField(max_length=10)
    pattern_3 = models.CharField(max_length=10)
    pattern_4 = models.CharField(max_length=10)
    created_by = models.CharField(max_length=150)
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        # Creating a random pattern before saving
        self.pattern_1 = random.choice(list(Color)).name
        self.pattern_2 = random.choice(list(Color)).name
        self.pattern_3 = random.choice(list(Color)).name
        self.pattern_4 = random.choice(list(Color)).name
        super(Game, self).save()


class Guess(models.Model):
    # id = models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True)
    game = models.ForeignKey(Game, on_delete=models.CASCADE)
    guess_1 = models.CharField(max_length=10)
    guess_2 = models.CharField(max_length=10)
    guess_3 = models.CharField(max_length=10)
    guess_4 = models.CharField(max_length=10)
    black = models.SmallIntegerField(default=0)
    white = models.SmallIntegerField(default=0)
    created_by = models.CharField(max_length=150)
    created_at = models.DateTimeField(auto_now_add=True)

    def check_black_white(self):
        pattern = [self.game.pattern_1, self.game.pattern_2, self.game.pattern_3, self.game.pattern_4]
        guesses = [self.guess_1, self.guess_2, self.guess_3, self.guess_4]

        black = 0
        white = 0

        i = 0

        for guess in guesses:

            # Checking if color and position are correct
            if guess == pattern[i]:
                black = black + 1

            # Checking if color exists in pattern
            elif guess in pattern:
                white = white + 1

            i = i + 1

        return black, white

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        (self.black, self.white) = self.check_black_white()
        super(Guess, self).save()

    class Meta:
        ordering = ['-created_at']
