import random
import argparse
import time  

random.seed(0)


class Player:
    def __init__(self, name):
        self.name = name
        self.score = 0

    def add_score(self, points):
        self.score += points

class HumanPlayer(Player):
    def choose_action(self, turn_total):
        return input("Roll (r) or Hold (h)? ").lower()


class ComputerPlayer(Player):
    def choose_action(self, turn_total):
        hold_at = min(25, 100 - self.score)

        if turn_total >= hold_at:
            print(f"{self.name} chooses to hold.")
            return "h"
        else:
            print(f"{self.name} chooses to roll.")
            return "r"
class PlayerFactory:
    @staticmethod
    def create_player(player_type, name):
        if player_type == "human":
            return HumanPlayer(name)
        elif player_type == "computer":
            return ComputerPlayer(name)
        else:
            raise ValueError("Player type must be human or computer")
class Die:
    def roll(self):
        return random.randint(1, 6)


class PigGame:
    def __init__(self, player1="human", player2="human"):
        self.players = [
            PlayerFactory.create_player(player1, "Player 1"),
            PlayerFactory.create_player(player2, "Player 2")
        ]
        self.die = Die()
        self.current_player = 0

    def switch_player(self):
        self.current_player = 1 - self.current_player

    def play_turn(self, time_is_up=None):
        player = self.players[self.current_player]
        turn_total = 0
        last_roll = None

        print(f"\n{player.name}'s turn!")

        while True:
            if time_is_up is not None and time_is_up():
                return False
            print(f"\nLast roll: {last_roll if last_roll is not None else 'None yet'}")
            print(f"Current turn score: {turn_total}")
            print(f"Total game score: {player.score}")

            choice = player.choose_action(turn_total)   

            if choice == "r":
                last_roll = self.die.roll()
                print(f"You rolled a {last_roll}!")

                if last_roll == 1:
                    print("You rolled a 1! You lose your turn points.")
                    break

                turn_total += last_roll

            elif choice == "h":
                player.add_score(turn_total)
                print(f"{player.name} now has {player.score} points!")
                break

            else:
                print("Invalid choice. Please enter r or h.")

        return player.score >= 100

    def play(self):
        print("Welcome to the Pig Dice Game!")

        while True:
            game_over = self.play_turn(self.time_is_up) 

            if game_over:
                winner = self.players[self.current_player]
                print(f"\n{winner.name} wins with {winner.score} points!")
                break

            self.switch_player()

class TimedGameProxy:
    def __init__(self, player1="human", player2="human"):
        self.game = PigGame(player1, player2)
        self.start_time = None
        self.time_limit = 60 

    def time_is_up(self):
        return time.monotonic() - self.start_time >= self.time_limit

    def play(self):
        self.start_time = time.monotonic()
        print("Welcome to the Timed Pig Dice Game!")
        print("You have 60 seconds to play!")

        while True:
            if self.time_is_up():
                break

            game_over = self.game.play_turn(self.time_is_up) 

            if game_over:
                winner = self.game.players[self.game.current_player]
                print(f"\n{winner.name} wins with {winner.score} points!")
                return

            if self.time_is_up():
                break

            self.game.switch_player()

        print("\nTime is up!")
        highest_score = max(player.score for player in self.game.players)
        winners = [
            player for player in self.game.players
            if player.score == highest_score
        ]

        if len(winners) == 2:
            print(f"It's a tie! Both players have {highest_score} points.")
        else:
            print(f"{winners[0].name} wins with {highest_score} points!") 

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Pig Dice Game")

    parser.add_argument(
        "--player1",
        choices=["human", "computer"],
        default="human"
    )

    parser.add_argument(
        "--player2",
        choices=["human", "computer"],
        default="human"
    )

    parser.add_argument(
    "--timed",
    action="store_true",
    help="Play a 60-second timed game"
)

args = parser.parse_args()

if args.timed:
    game = TimedGameProxy(args.player1, args.player2)
else:
    game = PigGame(args.player1, args.player2)

game.play()
