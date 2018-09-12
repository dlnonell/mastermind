from rest_framework import viewsets

from api.models import Game, Guess
from api.serializers import GameSerializer, GuessSerializer


class GameViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows Game objects to be viewed or edited.
    """
    queryset = Game.objects.all()
    serializer_class = GameSerializer


class GuessViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows Guess objects to be viewed or edited.
    """
    queryset = Guess.objects.all()
    serializer_class = GuessSerializer
