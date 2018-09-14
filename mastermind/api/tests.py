from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from api.models import Game, Guess
from api.utils import Color


class GameAPITests(APITestCase):

    def setUp(self):
        self.username = 'test'
        self.password = 'password123'
        self.user = User.objects.create_user(self.username, email='test@test.com', password=self.password)

    # Login tests
    def test_login(self):
        """
        Ensure we can successfully log in
        """
        success = self.client.login(username=self.username, password=self.password)

        self.assertTrue(success)

    def test_login_error(self):
        """
        Ensure we cannot login with non-existing user
        """
        failure = self.client.login(username='wrong_user', password='wrong_password')

        self.assertFalse(failure)

    # Game tests
    def test_create_game(self):
        """
        Ensure we can create a new Game object.
        """
        self.client.login(username=self.username, password=self.password)

        url = reverse('game-list')
        data = {}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Game.objects.count(), 1)
        self.assertEqual(Game.objects.get(pk=1).created_by, self.user.username)

    def test_create_game_without_login(self):
        """
        Ensure we cannot create a Game without having been logged in
        """
        url = reverse('game-list')
        data = {}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    # Guess tests
    def test_make_guess(self):
        """
        Ensure we can create a new Guess.
        """
        self.client.login(username=self.username, password=self.password)
        game = Game.objects.create()

        url = reverse('game-list') + str(game.id) + '/guess/'
        data = {'guess_1': 'RED', 'guess_2': 'BLUE', 'guess_3': 'GREEN', 'guess_4': 'YELLOW'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Guess.objects.count(), 1)
        self.assertEqual(Guess.objects.get(pk=1).created_by, self.user.username)

    def test_make_guess_without_login(self):
        """
        Ensure we cannot create a new Guess without having been logged in.
        """
        game = Game.objects.create()

        url = reverse('game-list') + str(game.id) + '/guess/'
        data = {'guess_1': 'RED', 'guess_2': 'BLUE', 'guess_3': 'GREEN', 'guess_4': 'YELLOW'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_make_guess_no_game(self):
        """
        Ensure we cannot create a new Guess if Game does not exist
        """
        self.client.login(username=self.username, password=self.password)

        url = reverse('game-list') + str(10) + '/guess/'
        data = {'guess_1': 'RED', 'guess_2': 'BLUE', 'guess_3': 'GREEN', 'guess_4': 'YELLOW'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_make_guess_black_white(self):
        """
        Ensure new Guess black and white check works
        """
        self.client.login(username=self.username, password=self.password)
        game = Game.objects.create()

        # Should have 4 black and 0 white
        url = reverse('game-list') + str(game.id) + '/guess/'
        data = {
            'guess_1': game.pattern_1,
            'guess_2': game.pattern_2,
            'guess_3': game.pattern_3,
            'guess_4': game.pattern_4
        }
        response = self.client.post(url, data, format='json')
        guess = Guess.objects.first()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(guess.black, 4)
        self.assertEqual(guess.white, 0)

        # As the Game patterns are created randomly, the following tests do not work properly. Refactor is needed.
        '''
        # Should have 2 black and 2 white
        url = reverse('game-list') + str(game.id) + '/guess/'
        data = {
            'guess_1': game.pattern_1,
            'guess_2': game.pattern_3,
            'guess_3': game.pattern_3,
            'guess_4': game.pattern_2
        }
        response = self.client.post(url, data, format='json')
        guess = Guess.objects.first()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(guess.black, 2)
        self.assertEqual(guess.white, 2)

        # Should have 0 black and 4 white
        url = reverse('game-list') + str(game.id) + '/guess/'
        data = {
            'guess_1': game.pattern_4,
            'guess_2': game.pattern_3,
            'guess_3': game.pattern_2,
            'guess_4': game.pattern_1
        }
        response = self.client.post(url, data, format='json')
        guess = Guess.objects.first()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(guess.black, 0)
        self.assertEqual(guess.white, 4)
        '''

    # Game history tests
    def test_get_history(self):
        """
        Ensure we can get Game history.
        """
        self.client.login(username=self.username, password=self.password)
        game = Game.objects.create()

        # History without guesses
        url = reverse('game-list') + str(game.id) + '/history/'
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 0)

        # First guess
        Guess.objects.create(
            game=game,
            guess_1=Color.YELLOW.value,
            guess_2=Color.RED.value,
            guess_3=Color.RED.value,
            guess_4=Color.BLUE.value,
            created_by=self.username
        )

        url = reverse('game-list') + str(game.id) + '/history/'
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

        # Second guess
        Guess.objects.create(
            game=game,
            guess_1=Color.BLUE.value,
            guess_2=Color.RED.value,
            guess_3=Color.GREEN.value,
            guess_4=Color.BLUE.value,
            created_by=self.username
        )

        url = reverse('game-list') + str(game.id) + '/history/'
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

    def test_get_history_without_login(self):
        """
        Ensure we cannot get Game history without having logged in
        """
        game = Game.objects.create()

        # First guess
        Guess.objects.create(
            game=game,
            guess_1=Color.YELLOW.value,
            guess_2=Color.RED.value,
            guess_3=Color.RED.value,
            guess_4=Color.BLUE.value,
            created_by=self.username
        )

        url = reverse('game-list') + str(game.id) + '/history/'
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
