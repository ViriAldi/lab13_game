import random


class Node:
    def __init__(self, value):
        self.value = value
        self.children = []


class Board:
    def __init__(self, values=(0,)*9, last_step=None):
        self.values = values
        self.last = last_step
        self.next_pos = self.generate_position()

    @property
    def winner(self):
        for col in range(3):
            if len(set(self.values[col::3])) == 1 and self.values[col]:
                return self.values[col]

        for row in range(3):
            if len(set(self.values[row:row+3])) == 1 and self.values[row]:
                return self.values[row]

        if len(set(self.values[::4])) == 1 and self.values[0]:
            return self.values[0]

        if len(set(self.values[2::2])) == 1 and self.values[2]:
            return self.values[2]

    @property
    def available(self):
        return [ind for ind in range(9) if self.values[ind] == 0]

    def generate_position(self):
        if len(self.available) == 0:
            return

        if len(self.available) == 1:
            return self.available * 2

        return random.sample(self.available, 2)

    @property
    def decision_tree(self):
        def recurse(node: Node):
            board = node.value
            sign = -board.last
            if (not board.winner) and node.value.values.count(0) > 0:
                positions = node.value.next_pos

                new1 = board.values.copy()
                new1[positions[0]] = sign
                new1 = Node(Board(values=new1, last_step=sign))

                new2 = board.values.copy()
                new2[positions[1]] = sign
                new2 = Node(Board(values=new2, last_step=sign))

                recurse(new1)
                recurse(new2)

                node.children = [new1, new2]

        root = Node(self)
        recurse(root)
        return root

    @property
    def better(self):
        if self.winner:
            return

        def recurse(node):
            if not node.children:
                if node.value.winner == 1:
                    return 1
                else:
                    return 0

            node1, node2 = node.children

            return recurse(node1) + recurse(node2)

        score1 = recurse(self.decision_tree.children[0])
        score2 = recurse(self.decision_tree.children[1])

        if score1 >= score2:
            return 0
        else:
            return 1

    @property
    def better_step(self):
        return self.next_pos[self.better]

    def __str__(self):
        return "\n".join([" ".join(map(str, self.values[i:i+3])) for i in [0, 3, 6]])


print(Board([1, 1, 0, 0, 0, 0, 0, 0, 0], last_step=-1))
