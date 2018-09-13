from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated

from api.models import Game, Guess
from api.serializers import GameSerializer, GuessSerializer


class GameViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows Game objects to be viewed or edited.
    """
    authentication_classes = (SessionAuthentication, BasicAuthentication)
    permission_classes = (IsAuthenticated,)
    queryset = Game.objects.all()
    serializer_class = GameSerializer

    def create(self, request, *args, **kwargs):
        serializer = GameSerializer(data=request.data)
        serializer.initial_data['created_by'] = request.user.username

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['post'])
    def guess(self, request, pk=None):
        """
        Checks a Guess to solve the Game and returns the saved object with the black and white information.
        :param request: the request
        :param pk: the Game id
        :return: a Guess object
        """
        serializer = GuessSerializer(data=request.data)
        serializer.initial_data['game'] = pk
        serializer.initial_data['created_by'] = request.user.username

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['get'])
    def history(self, request, pk=None):
        """
        Gets a list of Guess objects representing the Game history.
        :param request: the request
        :param pk: the Game id
        :return: a list of Guess objects
        """
        queryset = Guess.objects.filter(game=pk)
        serializer = GuessSerializer(queryset, many=True)
        return Response(serializer.data)
