#! python

# usage: python pyet.py program

import sys
import logging
import operator
import optparse


# A list with a couple of helper functions
# and a pretend-it-never happened approach to errors
class PietStack(list):

    def push(self, x):
        x = int(x)
        self.append(x)
        pass

    def pop(self):
        if super().__len__() < 1:
            return None
        a = super().pop()
        return a

    def pop2(self):
        if super().__len__() < 2:
            return None, None
        a = self.pop()
        b = self.pop()
        return a, b

    def top(self):
        if super().__len__() < 1:
            return None
        return self[-1]

    def _bin_op(self, func):
        a, b = self.pop2()
        if a is not None and b is not None:
            self.push(func(b, a))

    def add(self):
        self._bin_op(operator.add)

    def subtract(self):
        self._bin_op(operator.sub)

    def multiply(self):
        self._bin_op(operator.mul)

    def divide(self):
        self._bin_op(operator.floordiv)

    def mod(self):
        self._bin_op(operator.mod)

    def logical_not(self):
        a = self.pop()
        if a is None:
            return
        if a:
            self.push(0)
        else:
            self.push(1)

    def greater(self):
        self._bin_op(operator.gt)

    def duplicate(self):
        a = self.top()
        if a is not None:
            self.push(a)

    def roll(self):
        n, depth = self.pop2()
        if n is not None and depth is not None:
            self._roll_helper(n, depth)

    def _roll_helper(self, n, depth):
        if depth <= 0 or depth > super().__len__():
            return
        n = n % depth
        if n == 0:
            return
        super().insert(super().__len__() - depth, super().pop())
        self._roll_helper(n - 1, depth)


class SourceMap():

    def print_map(self, show_corners=False):
        if show_corners:
            corners = set()
            for blob in self._annotations["corners"].keys():
                for corner in self._annotations["corners"][blob]:
                    corners.add(self._annotations["corners"][blob][corner])
        map_string = ""
        for j in range(len(self._source)):
            for i in range(len(self._source[0])):
                val = self._source_map[j][i]
                if show_corners and (i, j) in corners:
                    val = "*"
                map_string += str(val)
            map_string += "\n"
        print(map_string)

    def get_blob(self, loc):
        return self._source_map[loc[1]][loc[0]]

    def get_corner(self, loc, dp, cc):
        return self._annotations["corners"][self.get_blob(loc)][(dp, cc)]

    def get_blob_color(self, blob):
        return self._annotations["colors"][blob]

    def get_blob_size(self, blob):
        return self._annotations["size"][blob]

    def __init__(self, source):
        self._source = source
        source_map = [["-1" for col in row] for row in source]
        annotations = dict()
        annotations["size"] = dict()
        annotations["corners"] = dict()
        annotations["colors"] = dict()
        self._fill_and_annotate(self._source, source_map, annotations)
        self._source_map = source_map
        self._annotations = annotations

    def _fill_and_annotate(self, source, source_map, annotations):
        blobchar = 1
        for j in range(len(source)):
            for i in range(len(source[0])):
                if source_map[j][i] == "-1":
                    if source[j][i] == "S":
                        fill_value = " "
                    elif source[j][i] == "T":
                        fill_value = "0"
                    else:
                        fill_value = blobchar
                        annotations["colors"][fill_value] = source[j][i]
                        blobchar += 1
                    self._fill((i, j), source[j][i], fill_value,
                               source, source_map, annotations)

    def _fill(self, loc, target_value, fill_value,
              ingrid, outgrid, annotations):
        fill_queue = list()
        fill_queue.append(loc)
        while len(fill_queue):
            x, y = fill_queue[0]
            fill_queue = fill_queue[1:]
            if x < 0 or y < 0 or y >= len(ingrid) or x >= len(ingrid[0]):
                continue
            if outgrid[y][x] == fill_value:
                continue
            if ingrid[y][x] != target_value:
                continue
            outgrid[y][x] = fill_value
            if target_value != "S" and target_value != "T":
                annotations["size"][fill_value] = annotations["size"].get(
                    fill_value, 0) + 1
                self._update_corners((x, y), annotations, fill_value)
                fill_queue.append((x - 1, y))
                fill_queue.append((x + 1, y))
                fill_queue.append((x, y - 1))
                fill_queue.append((x, y + 1))

    def _update_corners(self, loc, annotations, fill_value):
        if fill_value not in annotations["corners"]:
            annotations["corners"][fill_value] = dict()
        # upper end of right edge
        oldloc = annotations["corners"][fill_value].get(
            ("right", "left"), (float('-inf'), float('+inf')))
        if loc[0] > oldloc[0] or (loc[0] == oldloc[0] and loc[1] < oldloc[1]):
            annotations["corners"][fill_value][("right", "left")] = loc
        # lower end of right edge
        oldloc = annotations["corners"][fill_value].get(
            ("right", "right"), (float('-inf'), float('-inf')))
        if loc[0] > oldloc[0] or (loc[0] == oldloc[0] and loc[1] > oldloc[1]):
            annotations["corners"][fill_value][("right", "right")] = loc
        # right end of lower edge
        oldloc = annotations["corners"][fill_value].get(
            ("down", "left"), (float('-inf'), float('-inf')))
        if loc[1] > oldloc[1] or (loc[1] == oldloc[1] and loc[0] > oldloc[0]):
            annotations["corners"][fill_value][("down", "left")] = loc
        # left end of lower edge
        oldloc = annotations["corners"][fill_value].get(
            ("down", "right"), (float('+inf'), float('-inf')))
        if loc[1] > oldloc[1] or (loc[1] == oldloc[1] and loc[0] < oldloc[0]):
            annotations["corners"][fill_value][("down", "right")] = loc
        # lower end of left edge
        oldloc = annotations["corners"][fill_value].get(
            ("left", "left"), (float('+inf'), float('-inf')))
        if loc[0] < oldloc[0] or (loc[0] == oldloc[0] and loc[1] > oldloc[1]):
            annotations["corners"][fill_value][("left", "left")] = loc
        # upper end of left edge
        oldloc = annotations["corners"][fill_value].get(
            ("left", "right"), (float('+inf'), float('+inf')))
        if loc[0] < oldloc[0] or (loc[0] == oldloc[0] and loc[1] < oldloc[1]):
            annotations["corners"][fill_value][("left", "right")] = loc
        # left end of upper edge
        oldloc = annotations["corners"][fill_value].get(
            ("up", "left"), (float('+inf'), float('+inf')))
        if loc[1] < oldloc[1] or (loc[1] == oldloc[1] and loc[0] < oldloc[0]):
            annotations["corners"][fill_value][("up", "left")] = loc
        # right end of upper edge
        oldloc = annotations["corners"][fill_value].get(
            ("up", "right"), (float('-inf'), float('+inf')))
        if loc[1] < oldloc[1] or (loc[1] == oldloc[1] and loc[0] > oldloc[0]):
            annotations["corners"][fill_value][("up", "right")] = loc

    def in_bounds(self, loc):
        x, y = loc
        if x < 0 or y < 0:
            return False
        if x >= len(self._source[0]) or y >= len(self._source):
            return False
        return True


# Holds the image data and tells the interpreter where to go
class Navigator:

    def __init__(self, source):
        self._source_map = SourceMap(source)

    def find_next_loc(self, loc, dp, cc, changes=0):
        if changes == 8:
            return ((-1, -1), dp, cc, False)
        if not self._source_map.in_bounds(loc):
            # the Interpreter is out of bounds
            return ((-1, -1), dp, cc, False)
        blob = self._source_map.get_blob(loc)
        if blob == "0":
            # the Interpreter is on a black square
            return ((-1, -1), dp, cc, False)
        if blob == " ":
            # the Interpreter is on a white square
            return self.slide(loc, dp, cc, set())
        corner = self._source_map.get_corner(loc, dp, cc)
        direction = Navigator._direction(dp)
        next_loc = (corner[0] + direction[0], corner[1] + direction[1])
        if not self._source_map.in_bounds(next_loc):
            changes += 1
            if changes % 2 == 0:
                dp = Interpreter.dp_rotate(dp)
            else:
                cc = Interpreter.cc_flip(cc)
            return self.find_next_loc(loc, dp, cc, changes)
        next_blob = self._source_map.get_blob(next_loc)
        if next_blob == "0":
            changes += 1
            if changes % 2 == 0:
                dp = Interpreter.dp_rotate(dp)
            else:
                cc = Interpreter.cc_flip(cc)
            return self.find_next_loc(loc, dp, cc, changes)
        if next_blob == " ":
            return self.slide(next_loc, dp, cc, set())
        return (next_loc, dp, cc, True)

    def slide(self, loc, dp, cc, history):
        if (loc, dp) in history:
            return ((-1, -1), dp, cc, False)
        history.add((loc, dp))
        direction = Navigator._direction(dp)
        next_loc = (loc[0] + direction[0], loc[1] + direction[1])
        if not self._source_map.in_bounds(next_loc):
            return self.slide(loc, Interpreter.dp_rotate(dp),
                              Interpreter.cc_flip(cc), history)
        next_blob = self._source_map.get_blob(next_loc)
        if next_blob == "0":
            return self.slide(loc, Interpreter.dp_rotate(dp),
                              Interpreter.cc_flip(cc), history)
        if next_blob == " ":
            return self.slide(next_loc, dp, cc, history)
        return (next_loc, dp, cc, False)

    @staticmethod
    def _direction(dp):
        if dp == "right":
            return (1, 0)
        if dp == "down":
            return (0, 1)
        if dp == "left":
            return (-1, 0)
        if dp == "up":
            return (0, -1)


# Operates on the stack and interprets
class Interpreter:

    def __init__(self, source):
        self._navigator = Navigator(source)
        self._stack = PietStack()
        self._loc = (0, 0)
        self._dp = "right"
        self._cc = "left"

    def run(self, step_max=None):
        steps = 0
        next_loc = self._navigator.find_next_loc(self._loc, self._dp, self._cc)
        while(next_loc[0] != (-1, -1)):
            previous_loc = self._loc
            previous_blob = self._navigator._source_map.get_blob(previous_loc)
            if previous_blob != " ":
                previous_color = self._navigator._source_map.get_blob_color(
                    previous_blob)
                previous_size = self._navigator._source_map.get_blob_size(
                    previous_blob)
            self._loc = next_loc[0]
            self._dp = next_loc[1]
            self._cc = next_loc[2]
            current_blob = self._navigator._source_map.get_blob(self._loc)
            current_color = self._navigator._source_map.get_blob_color(
                current_blob)
            if(previous_color != "S" and next_loc[3]):
                steps += 1
                if(step_max is not None and steps > step_max):
                    return
                self.execute(previous_color, current_color, previous_size)
            next_loc = self._navigator.find_next_loc(
                self._loc, self._dp, self._cc)

    def execute(self, old_color, new_color, size):
        lightness = dict()
        for color in range(ord('G') - ord('A')):
            lightness[chr(ord('A') + color)] = 0
        for color in range(ord('M') - ord('G')):
            lightness[chr(ord('G') + color)] = 1
        for color in range(ord('S') - ord('M')):
            lightness[chr(ord('M') + color)] = 2
        hue = dict()
        for color in range(ord('S') - ord('A')):
            hue[chr(ord('A') + color)] = color % 6
        hue_change = (hue[new_color] - hue[old_color]) % 6
        lightness_change = (lightness[new_color] - lightness[old_color]) % 3
        if hue_change == 0:
            if lightness_change == 0:
                pass
            elif lightness_change == 1:
                logging.debug("action: push, value %d" % size)
                self.push(size)
            elif lightness_change == 2:
                logging.debug("action: pop")
                self.pop()
        if hue_change == 1:
            if lightness_change == 0:
                logging.debug("action: add")
                self.add()
            elif lightness_change == 1:
                logging.debug("action: sub")
                self.subtract()
            elif lightness_change == 2:
                logging.debug("action: multiply")
                self.multiply()
        if hue_change == 2:
            if lightness_change == 0:
                logging.debug("action: divide")
                self.divide()
            elif lightness_change == 1:
                logging.debug("action: mod")
                self.mod()
            elif lightness_change == 2:
                logging.debug("action: not")
                self.logicalnot()
        if hue_change == 3:
            if lightness_change == 0:
                logging.debug("action: greater")
                self.greater()
            elif lightness_change == 1:
                logging.debug("action: pointer")
                self.pointer()
            elif lightness_change == 2:
                logging.debug("action: switch")
                self.switch()
        if hue_change == 4:
            if lightness_change == 0:
                logging.debug("action: duplicate")
                self.duplicate()
            elif lightness_change == 1:
                logging.debug("action: roll")
                self.roll()
            elif lightness_change == 2:
                logging.debug("action: in(number)")
                self.in_int()
        if hue_change == 5:
            if lightness_change == 0:
                logging.debug("action: in(char)")
                self.in_char()
            elif lightness_change == 1:
                logging.debug("action: out(number)")
                self.out_int()
            elif lightness_change == 2:
                logging.debug("action: out(char)")
                self.out_char()

    def push(self, value):
        self._stack.push(value)

    def pop(self):
        self._stack.pop()

    def add(self):
        self._stack.add()

    def subtract(self):
        self._stack.subtract()

    def multiply(self):
        self._stack.multiply()

    def divide(self):
        self._stack.divide()

    def mod(self):
        self._stack.mod()

    def logicalnot(self):
        self._stack.logical_not()

    def greater(self):
        self._stack.greater()

    @staticmethod
    def dp_rotate(dp):
        if dp == "right":
            dp = "down"
        elif dp == "down":
            dp = "left"
        elif dp == "left":
            dp = "up"
        elif dp == "up":
            dp = "right"
        return dp

    def pointer(self):
        if len(self._stack) < 1:
            return
        a = self._stack.pop() % 4
        for i in range(a):
            self._dp = Interpreter.dp_rotate(self._dp)

    @staticmethod
    def cc_flip(cc):
        if cc == "left":
            cc = "right"
        elif cc == "right":
            cc = "left"
        return cc

    def switch(self):
        if len(self._stack) < 1:
            return
        a = self._stack.pop() % 2
        if a == 1:
            self._cc = self.cc_flip(self._cc)

    def duplicate(self):
        self._stack.duplicate()

    def roll(self):
        self._stack.roll()

    def in_char(self):
        # print("Enter a character: ")
        c = sys.stdin.read(1)
        self._stack.push(ord(c[0]))  # TODO: Better input handling

    def in_int(self):
        print("Enter an integer: ")
        n = sys.stdin.read(1)
        self._stack.push(int(n))  # TODO:ignore non-int inputs

    def out_char(self):
        if len(self._stack) < 1:
            return
        c = chr(self._stack.pop())
        print(c, sep='', end='')

    def out_int(self):
        if len(self._stack) < 1:
            return
        n = self._stack.pop()
        print(n, sep='', end='')


def main():

    usage = "usage: python %prog [options] source_file"
    parser = optparse.OptionParser(usage=usage)
    parser.add_option("-d", "--debug", action="store_true", dest="debug",
                      help="print debugging information")
    parser.add_option("-e", action="store", dest="step_max", type="int",
                      help="execution step count limit")
    (options, args) = parser.parse_args()
    if len(args) < 1:
        parser.print_help()
        exit()
    if options.debug:
        logging.basicConfig(level="DEBUG", format='%(message)s')
    with open(args[0], "r") as sourcefile:
        source = [[char for char in row.strip()] for row in
                  sourcefile.readlines()]
    interpreter = Interpreter(source)
    # interpreter._navigator._source_map.print_map()
    interpreter.run(options.step_max)
if __name__ == "__main__":
    main()
