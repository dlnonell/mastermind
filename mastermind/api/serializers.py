from rest_framework import serializers

from api.models import Game, Guess


class GameSerializer(serializers.ModelSerializer):
    class Meta:
        model = Game
        fields = ('id', 'pattern_1', 'pattern_2', 'pattern_3', 'pattern_4', 'created_by', 'created_at')
        read_only_fields = ('id', 'pattern_1', 'pattern_2', 'pattern_3', 'pattern_4', 'created_at')


class GuessSerializer(serializers.ModelSerializer):
    class Meta:
        model = Guess
        fields = ('game', 'guess_1', 'guess_2', 'guess_3', 'guess_4', 'black', 'white', 'created_by', 'created_at')
        read_only_fields = ('black', 'white', 'created_at')
