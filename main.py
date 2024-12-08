from random import randint


class Minesweeper:

    def __init__(self):

        self.bombs_n = 35
        self.size_x = 15
        self.size_y = 15

        self.bobms = []

        self.n_field = [[0 for __ in range(self.size_x)] for _ in range(self.size_y)]
        self.field = [["[ ]" for __ in range(self.size_x)] for _ in range(self.size_y)]

    def generate_bobms(self):
        self.n_field = [[0 for __ in range(self.size_x)] for _ in range(self.size_y)]
        self.bobms = []
        for i in range(self.bombs_n):
            while True:
                rand_pos = (randint(0, self.size_x-1), randint(0, self.size_y-1))

                if rand_pos not in self.bobms:
                    self.bobms.append(rand_pos)
                    break

            self.n_field[rand_pos[0]][rand_pos[1]] = -self.bombs_n-1

            arr = []
            for l in [-1, 0, 1]:
                for m in [-1, 0, 1]:
                    if l == 0 and m == 0:
                        continue
                    if (self.size_x != rand_pos[0] + l and rand_pos[0] + l >= 0) and (self.size_y != rand_pos[1] + m and rand_pos[1] + m >= 0) and (l, m) not in arr:
                        self.n_field[rand_pos[0]+l][rand_pos[1]+m] += 1
                        arr.append((l, m))

    def print_all(self):

        for i in range(self.size_y):
            for j in range(self.size_x):
                if (i, j) in self.bobms:
                    self.field[i][j] = f" X "
                else:
                    self.field[i][j] = f" {str(self.n_field[i][j])} "

                print(self.field[i][j], end="")
            print("")

    def get__field(self):
        for i in self.n_field:
            print(i)


def main():

    game = Minesweeper()
    game.generate_bobms()

    game.print_all()


if __name__ == "__main__":
    main()
