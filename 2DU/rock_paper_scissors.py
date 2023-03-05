import random


class Player:
    # constructor
    def __init__(self, probabilities:dict) -> None:
        self.probabilities = probabilities
        self.validity = self.validity_check()

    # validity_check
    def validity_check(self) ->bool:
        if not self.probabilities["rock"] + \
               self.probabilities["paper"]+ \
               self.probabilities["scissors"] == 1:
            return False
        if self.probabilities["rock"] < 0 or \
                self.probabilities["paper"] < 0 or \
                self.probabilities["scissors"] < 0:
            return False
        if self.probabilities["rock"] > 1 or \
                self.probabilities["paper"] > 1 or \
                self.probabilities["scissors"] > 1:
            return False
        return True

    def __repr__(self) -> str:
        return(f"rock:{self.probabilities['rock']},",
               f"papper:{self.probabilities['paper']},",
               f"scissors:{self.probabilities['scissors']}")

class Game:

    def __init__(self, player1:Player, player2:Player, NOR:int) -> None:
        self.player1 = player1
        self.player2 = player2
        self.NOR = NOR

    def validity_check(self) -> bool:
        if not any([self.player1.validity == True, self.player2.validity == True]):
            return False
        if self.NOR <= 0:
            return False
        return True

    # run_game
    def run_game(self):
        if self.validity_check() == True:
            player1_score = 0
            player2_score = 0
            ties = 0
            for i in range(self.NOR):
                player1_choise = self.player_s_choise(self.player1)
                player2_choise = self.player_s_choise(self.player2)

                if self.rock_paper_or_scissors(player1_choise, player2_choise) == 0:
                    ties = ties + 1
                if self.rock_paper_or_scissors(player1_choise, player2_choise) == 1:
                    player1_score = player1_score + 1
                if self.rock_paper_or_scissors(player1_choise, player2_choise) == 2:
                    player2_score = player2_score + 1
            self.game_results = {"player_a": player1_score,
                                "player_b": player2_score,
                                'tie': ties}
        else:
            self.game_results = False

    def player_s_choise(self, player):
        random_number = random.uniform(0, 1)
        if random_number>= 0 and random_number< player.probabilities["rock"]:
            return 'rock'
        if random_number >= player.probabilities["rock"] and random_number < player.probabilities["paper"]+player.probabilities["rock"]:
            return 'papper'
        if random_number >= player.probabilities["paper"]+player.probabilities["rock"] and random_number < 1:
            return 'scissors'

    def rock_paper_or_scissors(self, item1:str, item2:str) -> int:
        if item1 == "rock":
            if item2 == "rock":
                return 0
            if item2 == "paper":
                return 2
            if item2 == "scissors":
                return 1

        if item1 == "paper":
            if item2 == "rock":
                return 1
            if item2 == "paper":
                return 0
            if item2 == "scissors":
                return 2

        if item1 == "scissors":
            if item2 == "rock":
                return 2
            if item2 == "paper":
                return 1
            if item2 == "scissors":
                return 0


    # __repr__

    pass


def rock_paper_scissors(number_of_rounds, player_a, player_b):

    # create player_a
    player_a = Player(player_a)
    # create player_b
    player_b = Player(player_b)
    # create game
    game = Game(player_a, player_b, number_of_rounds)
    # run game
    game.run_game()
    # get result
    result = game.game_results

    return result


if __name__ == '__main__':

    N = 1000
    PLAYER_A = {
        "paper": 0.8,
        "scissors": 0.1,
        "rock": 0.1,
    }
    PLAYER_B = {
        "paper": 0.1,
        "scissors": 0.8,
        "rock": 0.1,
    }
    rock_paper_scissors(N, PLAYER_A, PLAYER_B)
    # Approximate output {'player_a' 170, 'player_b' 640, 'tie' 190} (could vary slightly because of the randomness)

    # Test case 2
    N = 100
    PLAYER_A = {
        "paper": 0,
        "scissors": 1,
        "rock": 0,
    }
    PLAYER_B = {
        "paper": 0,
        "scissors": 0,
        "rock": 1,
    }
    assert rock_paper_scissors(N, PLAYER_A, PLAYER_B) == {'player_a': 0, 'player_b': 100, 'tie': 0}

    # Test case 3
    N = 0
    PLAYER_A = {
        "paper": 0,
        "scissors": 1,
        "rock": 0,
    }
    PLAYER_B = {
        "paper": 0,
        "scissors": 0,
        "rock": 1,
    }
    assert rock_paper_scissors(N, PLAYER_A, PLAYER_B) is False