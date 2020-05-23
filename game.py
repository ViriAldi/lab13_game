import random
from board import Board


class Game:
    def __init__(self, to_print=False):
        self.values = [0] * 9
        self.sign = random.choice([-1, 1])
        self.winner = 0
        self.to_print = to_print

    @property
    def board(self):
        return Board(self.values, -self.sign)

    def step(self):
        if self.sign == 1:
            pos = self.board.better_step
            self.values[pos] = 1

        else:
            pos = random.choice(self.board.available)
            self.values[pos] = -1

        self.sign = -self.sign

    def run(self):
        while 1:
            if self.board.winner:
                if self.to_print:
                    print(f"Winner: {self.board.winner}")
                self.winner = self.board.winner
                break

            elif self.board.values.count(0) == 0:
                if self.to_print:
                    print("No winner")
                break

            else:
                self.step()
                if self.to_print:
                    print(self.board, "\n")


if __name__ == "__main__":
    num_cases = 10**3
    won = 0
    draw = 0
    lost = 0

    for case in range(num_cases):
        game = Game()
        game.run()

        if game.winner == 1:
            won += 1
        elif game.winner == 0:
            draw += 1
        else:
            lost += 1

    print(f"Efficiency:\nwon: {won / num_cases}\ndraw: {draw / num_cases}\nlost: {lost / num_cases}")
