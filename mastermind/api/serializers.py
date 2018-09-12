from rest_framework import serializers

from api.models import Game, Guess


class GameSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Game
        fields = ('id', 'pattern_1', 'pattern_2', 'pattern_3', 'pattern_4', 'created_by', 'created_at')


class GuessSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Guess
        fields = ('game_id', 'guess_1', 'guess_2', 'guess_3', 'guess_4', 'black', 'white', 'created_by', 'created_at')
