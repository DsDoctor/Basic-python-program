# Made by Sheng Du


class MazeError(Exception):
    def __init__(self, message):
        self.message = message


class Point(object):
    def __init__(self, y, x):
        self.co = (y, x)

        self.left = None
        self.right = None
        self.up = None
        self.down = None

        self.west = True
        self.east = True
        self.north = True
        self.south = True

        self.draw_up = False
        self.draw_down = False
        self.draw_left = False
        self.draw_right = False

        self.pillar = False
        self.wall = None
        self.cds = False
        self.entry = False
        self.ee = False
        self.drown = False
        self.travel_wall = False
        self.travel_path = False
        self.travel_cds = False
        self.travel_ee = False


class Maze:
    def __init__(self, file_name):
        self.file_name = file_name
        self.matrix = {}
        self.text = self.read_file()
        self.error_detect()
        self.make_matrix()
        self.cds_starts = []
        self.ee_end = []
        self.stack = []

        self.n_gate = 0
        self.con_walls = 0
        self.in_points = 0
        self.acc_area = 0
        self.c_d_s = 0
        self.ee_path = 0
        # REPLACE PASS ABOVE WITH YOUR CODE

    def error_detect(self):
        if (self.text.__len__() not in range(2, 32)) or (self.text[0].__len__() not in range(2, 42)):
            raise MazeError('Incorrect input.')
        for i in range(self.text.__len__()):
            if self.text[i].__len__() != self.text[0].__len__():
                raise MazeError('Incorrect input.')
            for j in range(self.text[i].__len__()):
                if self.text[i][j] not in ['0', '1', '2', '3']:
                    raise MazeError('Incorrect input.')
        for i in range(self.text.__len__()):
            if self.text[i][self.text[i].__len__() - 1] not in ['0', '2']:
                raise MazeError('Input does not represent a maze.')
        for j in range(self.text[0].__len__() - 1):
            if self.text[self.text.__len__() - 1][j] not in ['0', '1']:
                raise MazeError('Input does not represent a maze.')

    def analyse(self):
        self.get_n_gates()
        self.get_set_walls()
        self.get_acc_areas()
        self.get_in_point()
        self.get_cds()
        self.get_ee_paths()
        self.analyze_print()
        pass
        # REPLACE PASS ABOVE WITH YOUR CODE

    def display(self):
        # w_file = str(self.file_name.split('.')[0]) + '_test.tex'
        w_file = str(self.file_name.split('.')[0]) + '.tex'
        with open(w_file, 'w') as f:
            f.write("\\documentclass[10pt]{article}\n\\usepackage{tikz}\n"
                    "\\usetikzlibrary{shapes.misc}\n\\usepackage[margin=0cm]{geometry}\n"
                    "\\pagestyle{empty}\n\\tikzstyle{every node}=[cross out, draw, red]\n\n"
                    "\\begin{document}\n\n"
                    "\\vspace*{\\fill}\n\\begin{center}\n\\begin{tikzpicture}[x=0.5cm, y=-0.5cm, ultra thick, blue]\n")
            f.write(self.dis_walls())
            f.write(self.dis_pillars())
            f.write(self.dis_cds())
            f.write(self.dis_ee())
            f.write("\\end{tikzpicture}\n""\\end{center}\n""\\vspace*{\\fill}\n\n"
                    "\\end{document}\n")
        # REPLACE PASS ABOVE WITH YOUR CODE

    def read_file(self):
        text = {}
        num = 0
        with open(self.file_name) as f:
            for line in f.readlines():
                line = ' '.join(line)
                line = line.split()
                if line.__len__() > 0:
                    text[num] = line
                    num += 1
        return text

    def make_matrix(self):
        self.matrix = {}
        for i in range(self.text.__len__()):
            self.matrix[i] = []
            for j in range(self.text[i].__len__()):
                self.make_point(i, j)

    def make_point(self, i, j):
        self.matrix[i].append(Point(i, j))
        self.matrix[i][j].wall = int(self.text[i][j])
        if j != 0:
            self.matrix[i][j].left = self.matrix[i][j - 1]
            self.matrix[i][j - 1].right = self.matrix[i][j]
        if i != 0:
            self.matrix[i][j].up = self.matrix[i - 1][j]
            self.matrix[i - 1][j].down = self.matrix[i][j]
        if self.matrix[i][j].wall == 1 or self.matrix[i][j].wall == 3:
            self.matrix[i][j].north = False
            if self.matrix[i][j].up is not None:
                self.matrix[i][j].up.south = False
        if self.matrix[i][j].wall == 2 or self.matrix[i][j].wall == 3:
            self.matrix[i][j].west = False
            if self.matrix[i][j].left is not None:
                self.matrix[i][j].left.east = False
        if self.matrix[i][j].wall == 0:
            if i == 0:
                try:
                    if not (self.matrix[i][j].left.wall == 1 or self.matrix[i][j].left.wall == 3):
                        self.matrix[i][j].pillar = True
                except AttributeError:
                    self.matrix[i][j].pillar = True
            if j == 0:
                try:
                    if not (self.matrix[i][j].up.wall == 2 or self.matrix[i][j].up.wall == 3):
                        self.matrix[i][j].pillar = True
                except AttributeError:
                    self.matrix[i][j].pillar = True
            elif i != 0 and j != 0:
                if not ((self.matrix[i][j].up.wall == 2 or self.matrix[i][j].up.wall == 3)
                        or (self.matrix[i][j].left.wall == 1 or self.matrix[i][j].left.wall == 3)):
                    self.matrix[i][j].pillar = True

    def get_n_gates(self):
        for i in range(self.matrix.__len__() - 1):
            if self.matrix[i][0].wall == 0 or self.matrix[i][0].wall == 1:
                self.n_gate += 1
            if self.matrix[i][self.matrix[i].__len__() - 1].wall == 0:
                self.n_gate += 1
        for j in range(self.matrix[0].__len__() - 1):
            if self.matrix[0][j].wall == 0 or self.matrix[0][j].wall == 2:
                self.n_gate += 1
            if self.matrix[self.matrix.__len__() - 1][j].wall == 0:
                self.n_gate += 1

    def get_set_walls(self):
        for i in range(self.matrix.__len__()):
            for j in range(self.matrix[i].__len__()):
                if self.matrix[i][j].wall and not self.matrix[i][j].travel_wall:
                    self.con_walls += 1
                    self.stack.append(self.matrix[i][j])
                    while self.stack.__len__():
                        self.travel_points()

    def get_acc_areas(self):
        for i in range(self.matrix.__len__() - 1):
            if self.matrix[i][0].west and not self.matrix[i][0].travel_path:
                self.acc_area += 1
                self.stack.append(self.matrix[i][0])
                while self.stack.__len__():
                    self.travel_paths()
            if self.matrix[i][self.matrix[0].__len__() - 2].east \
                    and not self.matrix[i][self.matrix[0].__len__() - 2].travel_path:
                self.acc_area += 1
                self.stack.append(self.matrix[i][self.matrix[0].__len__() - 2])
                while self.stack.__len__():
                    self.travel_paths()
        for j in range(self.matrix[0].__len__() - 1):
            if self.matrix[0][j].north and not self.matrix[0][j].travel_path:
                self.acc_area += 1
                self.stack.append(self.matrix[0][j])
                while self.stack.__len__():
                    self.travel_paths()
            if self.matrix[self.matrix.__len__() - 2][j].south \
                    and not self.matrix[self.matrix.__len__() - 2][j].travel_path:
                self.acc_area += 1
                self.stack.append(self.matrix[self.matrix.__len__() - 2][j])
                while self.stack.__len__():
                    self.travel_paths()

    def get_in_point(self):
        for i in range(self.matrix.__len__() - 1):
            for j in range(self.matrix[i].__len__() - 1):
                if not self.matrix[i][j].travel_path:
                    self.in_points += 1

    def get_cds(self):
        self.find_cds_starts()
        for start in self.cds_starts:
            if not start.travel_cds:
                self.c_d_s += 1
                self.stack.append(start)
                while self.stack.__len__():
                    self.travel_cds()

    def get_ee_paths(self):
        for i in range(self.matrix.__len__() - 1):
            if self.matrix[i][0].west and not self.matrix[i][0].travel_ee:
                self.matrix[i][0].entry = True
                self.stack.append(self.matrix[i][0])
                while self.stack.__len__():
                    self.travel_ee()
            if self.matrix[i][self.matrix[i].__len__() - 2].east \
                    and not self.matrix[i][self.matrix[i].__len__() - 2].travel_ee:
                self.matrix[i][self.matrix[i].__len__() - 2].entry = True
                self.stack.append((self.matrix[i][self.matrix[i].__len__() - 2]))
                while self.stack.__len__():
                    self.travel_ee()
        for j in range(self.matrix[0].__len__() - 1):
            if self.matrix[0][j].north and not self.matrix[0][j].travel_ee:
                self.matrix[0][j].entry = True
                self.stack.append(self.matrix[0][j])
                while self.stack.__len__():
                    self.travel_ee()
            if self.matrix[self.matrix.__len__() - 2][j].south \
                    and not self.matrix[self.matrix.__len__() - 2][j].travel_ee:
                self.matrix[self.matrix.__len__() - 2][j].entry = True
                self.stack.append((self.matrix[self.matrix.__len__() - 2][j]))
                while self.stack.__len__():
                    self.travel_ee()
        for path in self.ee_end:
            self.stack.append(path)
            while self.stack.__len__():
                path = self.stack.pop()
                if path.north:
                    path.draw_up = True
                    path.drown = True
                    if path.up is not None:
                        if not path.up.drown:
                            self.stack.append(path.up)
                if path.south:
                    path.draw_down = True
                    path.drown = True
                    if path.down.down is not None:
                        if not path.down.drown:
                            self.stack.append(path.down)
                if path.west:
                    path.draw_left = True
                    path.drown = True
                    if path.left is not None:
                        if not path.left.drown:
                            self.stack.append(path.left)
                if path.east:
                    path.draw_right = True
                    path.drown = True
                    if path.right.right is not None:
                        if not path.right.drown:
                            self.stack.append(path.right)

    def travel_points(self):
        point = self.stack.pop()
        point.travel_wall = True
        if point.wall == 1 or point.wall == 3:
            if not point.right.travel_wall:
                self.stack.append(point.right)
        if point.wall == 2 or point.wall == 3:
            if not point.down.travel_wall:
                self.stack.append(point.down)
        if point.left:
            if (point.left.wall == 1 or point.left.wall == 3) and (not point.left.travel_wall):
                self.stack.append(point.left)
        if point.up:
            if (point.up.wall == 2 or point.up.wall == 3) and (not point.up.travel_wall):
                self.stack.append(point.up)

    def travel_paths(self):
        path = self.stack.pop()
        path.travel_path = True
        if path.east and (path.right is not None):
            if (not path.right.travel_path) and (path.right.co[-1] < self.matrix[0].__len__() - 1):
                self.stack.append(path.right)
        if path.south and (path.down is not None) and (path.down.co[0] < self.matrix.__len__() - 1):
            if not path.down.travel_path:
                self.stack.append(path.down)
        if path.west and (path.left is not None):
            if not path.left.travel_path:
                self.stack.append(path.left)
        if path.north and (path.up is not None):
            if not path.up.travel_path:
                self.stack.append(path.up)

    def travel_cds(self):
        point = self.stack.pop()
        if point.travel_cds:
            if sum([point.south, point.north, point.west, point.east]) < 2:
                self.c_d_s -= 1
        point.travel_cds = True
        edge_count = sum([point.north, point.south, point.east, point.west])
        if edge_count == 1:
            point.cds = True
            if point.north:
                point.north = False
                if point.co[0] > 0:
                    point.up.south = False
                    self.stack.append(point.up)
            if point.south:
                point.south = False
                if point.down.co[0] < self.matrix.__len__() - 1:
                    point.down.north = False
                    self.stack.append(point.down)
            if point.west:
                point.west = False
                if point.co[-1] > 0:
                    point.left.east = False
                    self.stack.append(point.left)
            if point.east:
                point.east = False
                if point.right.co[-1] < self.matrix[0].__len__() - 1:
                    point.right.west = False
                    self.stack.append(point.right)

    def travel_ee(self):
        path = self.stack.pop()
        path.travel_ee = True
        if sum([path.north, path.south, path.west, path.east]) > 2:
            return False
        if sum([path.north, path.south, path.west, path.east]) == 2:
            if path.co == (0, 0):
                if path.north and path.west:
                    self.end_path(path)
            elif path.co == (0, self.matrix[0].__len__() - 2):
                if path.north and path.east:
                    self.end_path(path)
            elif path.co == (self.matrix.__len__() - 2, 0):
                if path.west and path.south:
                    self.end_path(path)
            elif path.co == (self.matrix.__len__() - 2, self.matrix[0].__len__() - 2):
                if path.east and path.south:
                    self.end_path(path)
        if self.is_exit(path) and not path.entry:
            self.end_path(path)
            return True
        if path.west and path.left is not None:
            if not path.left.travel_ee:
                self.stack.append(path.left)
        if path.east and path.right.right is not None:
            if not path.right.travel_ee:
                self.stack.append(path.right)
        if path.north and path.up is not None:
            if not path.up.travel_ee:
                self.stack.append(path.up)
        if path.south and path.down.down is not None:
            if not path.down.travel_ee:
                self.stack.append(path.down)

    def analyze_print(self):
        if self.n_gate > 1:
            print(f'The maze has {self.n_gate} gates.')
        elif self.n_gate == 1:
            print(f'The maze has a single gate.')
        else:
            print(f'The maze has no gate.')
        if self.con_walls > 1:
            print(f'The maze has {self.con_walls} sets of walls that are all connected.')
        elif self.con_walls == 1:
            print(f'The maze has walls that are all connected.')
        else:
            print(f'The maze has no wall.')
        if self.in_points > 1:
            print(f'The maze has {self.in_points} inaccessible inner points.')
        elif self.in_points == 1:
            print(f'The maze has a unique inaccessible inner point.')
        else:
            print(f'The maze has no inaccessible inner point.')
        if self.acc_area > 1:
            print(f'The maze has {self.acc_area} accessible areas.')
        elif self.acc_area == 1:
            print(f'The maze has a unique accessible area.')
        else:
            print(f'The maze has no accessible area.')
        if self.c_d_s > 1:
            print(f'The maze has {self.c_d_s} sets of accessible cul-de-sacs that are all connected.')
        elif self.c_d_s == 1:
            print(f'The maze has accessible cul-de-sacs that are all connected.')
        else:
            print(f'The maze has no accessible cul-de-sac.')
        if self.ee_path > 1:
            print(f'The maze has {self.ee_path} entry-exit paths with no intersections not to cul-de-sacs.')
        elif self.ee_path == 1:
            print(f'The maze has a unique entry-exit path with no intersection not to cul-de-sacs.')
        else:
            print(f'The maze has no entry-exit path with no intersection not to cul-de-sacs.')

    def dis_walls(self):
        walls = "% Walls\n"
        for i in range(self.matrix.__len__()):
            j = 0
            while j < self.matrix[i].__len__():
                start = self.wall_start_h(i, j)
                if start is not None:
                    end = start.right
                    while end.wall == 1 or end.wall == 3:
                        end = end.right
                    walls += f'\t\\draw ({start.co[-1]},{start.co[0]}) -- ({end.co[-1]},{end.co[0]});\n'
                    j = end.co[-1] + 1
                else:
                    break
        for j in range(self.matrix[0].__len__()):
            i = 0
            while i < self.matrix.__len__():
                start = self.wall_start_v(i, j)
                if start is not None:
                    end = start.down
                    while end.wall == 2 or end.wall == 3:
                        end = end.down
                    walls += f'\t\\draw ({start.co[-1]},{start.co[0]}) -- ({end.co[-1]},{end.co[0]});\n'
                    i = end.co[0] + 1
                else:
                    break
        return walls

    def dis_pillars(self):
        pillar = "% Pillars\n"
        for i in range(self.matrix.__len__()):
            for j in range(self.matrix[i].__len__()):
                if self.matrix[i][j].pillar:
                    pillar += f'\t\\fill[green] ({self.matrix[i][j].co[-1]},{self.matrix[i][j].co[0]}) circle(0.2);\n'
        return pillar

    def dis_cds(self):
        cds = "% Inner points in accessible cul-de-sacs\n"
        for i in range(self.matrix.__len__()):
            for j in range(self.matrix[i].__len__()):
                if self.matrix[i][j].cds:
                    cds += f"\t\\node at ({self.matrix[i][j].co[-1] + 0.5},{self.matrix[i][j].co[0] + 0.5}) {{}};\n"
        return cds

    def dis_ee(self):
        ee = "% Entry-exit paths without intersections\n"
        for i in range(self.matrix.__len__()):
            j = 0
            while j < self.matrix[i].__len__():
                start = self.path_start_h(i, j)
                if start is not None:
                    end = start
                    if end.right.draw_left:
                        end = start.right
                    while end.draw_right:
                        end = end.right
                    x_start = start.co[-1] + 0.5
                    x_end = end.co[-1] + 0.5
                    if start.draw_left:
                        x_start -= 1
                    if end.draw_right:
                        x_end -= 1
                    ee += f'\t\\draw[dashed, yellow] ({x_start},{i + 0.5}) -- ({x_end},{i + 0.5});\n'
                    j = end.co[-1] + 1
                else:
                    break
        for j in range(self.matrix[0].__len__()):
            i = 0
            while i < self.matrix.__len__():
                start = self.path_start_v(i, j)
                if start is not None:
                    end = start
                    if end.down.draw_up:
                        end = start.down
                    while end.draw_down:
                        end = end.down
                    y_start = start.co[0] + 0.5
                    y_end = end.co[0] + 0.5
                    if start.draw_up:
                        y_start -= 1
                    if end.draw_down:
                        y_end += 1
                    ee += f'\t\\draw[dashed, yellow] ({j + 0.5},{y_start}) -- ({j + 0.5},{y_end});\n'
                    i = end.co[0] + 1
                else:
                    break
        return ee

    def wall_start_h(self, i, j):
        start = self.matrix[i][j]
        while start.right:
            if start.wall == 1 or start.wall == 3:
                return start
            start = start.right
        return None

    def wall_start_v(self, i, j):
        start = self.matrix[i][j]
        while start.down:
            if start.wall == 2 or start.wall == 3:
                return start
            start = start.down
        return None

    def find_cds_starts(self):
        for i in range(self.matrix.__len__() - 1):
            for j in range(self.matrix[i].__len__() - 1):
                edge_count = [self.matrix[i][j].north, self.matrix[i][j].south,
                              self.matrix[i][j].west, self.matrix[i][j].east]
                if sum(edge_count) == 1 and self.matrix[i][j].travel_path:
                    self.matrix[i][j].cds = True
                    self.cds_starts.append(self.matrix[i][j])

    def is_exit(self, path):
        if path.co[0] == 0 and path.north:
            return True
        if path.co[0] == self.matrix.__len__() - 2 and path.south:
            return True
        if path.co[-1] == 0 and path.west:
            return True
        if path.co[-1] == self.matrix[0].__len__() - 2 and path.east:
            return True
        return False

    def end_path(self, path):
        self.ee_path += 1
        path.ee = True
        self.ee_end.append(path)

    def path_start_h(self, i, j):
        start = self.matrix[i][j]
        while start.right:
            if start.draw_left or start.draw_right:
                return start
            start = start.right
        return None

    def path_start_v(self, i, j):
        start = self.matrix[i][j]
        while start.down:
            if start.draw_up or start.draw_down:
                return start
            start = start.down
        return None


if __name__ == "__main__":
    maze = Maze('data/maze_1.txt')
    maze.analyse()
    maze.display()
