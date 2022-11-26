import random
import itertools as it
from collections import defaultdict as dd, deque, OrderedDict
import sys
import os
import imageio.v2 as iio
import time
import shutil
from PIL import Image, ImageDraw

OKGREEN = '\033[92m'
FAIL = '\033[91m'
OPEN = "."
WALL = "#"


def make_image_from_state(board, final=False):
    global state_number, dim, output_dir
    canvas_size = dim * 4
    tile_size = canvas_size // dim
    im = Image.new(mode="RGB", size=(canvas_size, canvas_size))
    draw = ImageDraw.Draw(im)
    for y in range(dim):
        for x in range(dim):
            cur_x = x*tile_size
            cur_y = y*tile_size
            color = (0, 0, 0)
            match board[y][x]:
                case ".":
                    color = (0, 230, 0) if final else (255, 255, 255)
                case "?":
                    color = (128, 20, 128)
                case "P":
                    color = (128, 20, 128)
                case "G":
                    color = (255, 20, 20)
                case "@":
                    color = (0, 230, 0)
            draw.rectangle([cur_x, cur_y, cur_x+tile_size,
                           cur_y+tile_size], fill=color)
    ending = str(state_number).rjust(4, "0")
    im.save(f"{output_dir}/frame{ending}.png", "PNG")


def show_board(board, fix=False, newest_y=None, newest_x=None):
    global state_number
    # print(, flush=True)
    ret = []
    sep = "\n" * 15
    for line in board:
        to_show = "".join(line).replace("@" if fix else "((((", OPEN)
        ret.append(to_show + "\n")

    ret = "".join(ret)
    print(sep, flush=False)
    print(ret, flush=False)


def clean_board(board):
    for y in range(dim):
        board[y] = [WALL if x == WALL else OPEN for x in board[y]]

    # print("cleaned")
    # show_board(board)


# show_board(board)
# adj = list(it.pairwise([1, 0, -1, 0, 1]))
adj = [(-1, 0), (1, 0), (0, -1), (0, 1)]
dfs_seen = set()


def dfs(board, y, x):
    global state_number, show_printout
    if board[y][x] != OPEN:
        return
    if (y, x) in dfs_seen:
        return
    dfs_seen.add((y, x))
    new_adj = adj.copy()
    # random.shuffle(new_adj)
    for i in range(x % 4 + random.randint(0, 3)):
        new_adj.insert(0, new_adj.pop())
    board[y][x] = "@"
    total_placed = 0

    reviewed = set()
    for dy, dx in new_adj:
        new_y = dy + y
        new_x = dx + x
        reviewed.add((new_y, new_x))
        if new_y in range(dim) and new_x in range(dim) and board[new_y][new_x] == OPEN:
            temp = board[new_y][new_x]
            # board[new_y][new_x] = FAIL + "P" + '\033[0m'
            board[new_y][new_x] = "?"
            state_number += 1
            if state_number % 100 == 0:
                print(state_number)

            if show_printout:
                # os.system("cls")
                # time.sleep(.1)
                show_board(board, True, new_y)
            make_image_from_state(board)
            board[new_y][new_x] = temp

            total_placed += 1

            board[y][x] = "@"
            dfs(board, new_y, new_x)

    assert len(reviewed) == 4
    if total_placed == 0 and (x % 2 == 1 or y % 2 == 1):
        board[y][x] = WALL


def place_walls(board):
    board[0] = list(WALL * dim)
    board[-1] = list(WALL * dim)
    for y in range(dim):
        board[y][0] = WALL
        board[y][-1] = WALL
    board[start_y][start_x] = OPEN


def bfs(board):
    fringe = deque([((start_y, start_x), 0)])
    seen = OrderedDict()
    turn = 0
    while fringe:
        cur, steps = fringe.popleft()
        turn += 1
        if cur in seen:
            continue
        seen[cur] = turn
        y, x = cur
        # last = cur
        for dy, dx in adj:
            new_y = dy + y
            new_x = dx + x
            if new_y in range(dim) and new_x in range(dim) and board[new_y][new_x] == OPEN:
                fringe.append(((new_y, new_x), steps + 1))
    ret, _ = seen.popitem(True)
    return ret


# adj8 = [(y, x) for y in range(-1, 2) for x in range(-1, 2) if not (x == 0 and y == 0)]
def count_branches(board):
    return sum(board[y][x] == OPEN and sum(board[y + dy][x + dx] == OPEN for dy, dx in adj) >= 3 for y, x in it.product(range(1, dim - 1), range(1, dim - 1)))


def make_gif():
    global output_dir
    images = [iio.imread(f"{output_dir}/{x}")
              for x in sorted(os.listdir(output_dir)) if "frame" in x]
    images.extend(images[-1] for _ in range(20))
    final_gif = "combined.gif"
    iio.mimsave(final_gif, images, format="GIF", duration=.001)
    # pygifsicle.optimize(final_gif)


def initialize_board():
    global dim, show_printout
    # random.seed(5648)
    sys.setrecursionlimit(5000)
    random.seed(5)
    dim = 11
    dim = int(
        sys.argv[-1]) if len(sys.argv) > 1 and sys.argv[-1].isnumeric() else dim
    show_printout = len(sys.argv) > 1 and "show" in sys.argv[1]

    board = [list(OPEN*dim) for _ in range(dim)]
    for y in range(dim):
        for x in range(dim):
            if x % 2 == 0 and y % 2 == 0:
                board[y][x] = '#'
    return board

def reveal_start_and_end_positions(board):
    global start_x, start_y
    board[start_y][start_x] = "P"
    last_y, last_x = bfs(board)
    board[last_y][last_x] = "G"

def output_setup(output_directory="./images"):
    global output_dir
    output_dir = output_directory
    if os.path.exists(output_dir) and os.path.isdir(output_dir):
        shutil.rmtree(output_dir)
    os.mkdir(output_dir)

def main():
    global state_number, start_x, start_y
    start_x, start_y = (1, 0)
    state_number = 0
    board = initialize_board()
    output_setup()
    dfs(board, start_y, start_x)
    clean_board(board)
    reveal_start_and_end_positions(board)
    show_board(board, True)
    make_image_from_state(board, True)
    make_gif()


if __name__ == "__main__":
    main()
