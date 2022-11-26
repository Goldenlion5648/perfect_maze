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
    global round_, dim
    # print(round_)
    # print("making image")
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
    ending = str(round_).rjust(4, "0")
    im.save(f"{output_dir}/frame{ending}.png", "PNG")

# make_image_from_state(board)
# exit()


def show_board(board, fix=False, newest_y=None, newest_x=None):
    global round_
    # print(, flush=True)
    ret = []
    sep = "\n" * 15
    for y, line in enumerate(board):
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
seen = set()


def dfs(y, x):
    global round_
    if board[y][x] != OPEN:
        return
    if (y, x) in seen:
        return
    seen.add((y, x))
    # print(y, x)
    new_adj = adj.copy()
    # random.shuffle(new_adj)
    for i in range(x % 4 + random.randint(0, 3)):
        new_adj.insert(0, new_adj.pop())
    board[y][x] = "@"
    # wall_mode = False
    total_placed = 0

    reviewed = set()
    for dy, dx in new_adj:
        # print(dy, dx)
        new_y = dy + y
        new_x = dx + x
        reviewed.add((new_y, new_x))
        if new_y in range(dim) and new_x in range(dim) and board[new_y][new_x] == OPEN:
            temp = board[new_y][new_x]
            # board[new_y][new_x] = FAIL + "P" + '\033[0m'
            board[new_y][new_x] = "?"
            round_ += 1
            if round_ % 100 == 0:
                print(round_)

            if show_printout:
                # os.system("cls")
                # time.sleep(.1)
                show_board(board, True, new_y)
            make_image_from_state(board)
            board[new_y][new_x] = temp

            total_placed += 1

            board[y][x] = "@"
            dfs(new_y, new_x)
    # temp = board[y][x]
    # board[y][x] = "?"
    # make_image_from_state(board)
    # board[y][x] = temp

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


def bfs():
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
    # random.seed(5648)
    sys.setrecursionlimit(5000)
    random.seed(5)
    dim = 11
    dim = int(
        sys.argv[-1]) if len(sys.argv) > 1 and sys.argv[-1].isnumeric() else dim
    show_printout = len(sys.argv) > 1 and "show" in sys.argv[1]
    # print(show_printout)
    output_dir = "./images"
    if os.path.exists(output_dir) and os.path.isdir(output_dir):
        shutil.rmtree(output_dir)
    os.mkdir(output_dir)

    board = [list(OPEN*dim) for _ in range(dim)]
    for y in range(dim):
        for x in range(dim):
            if x % 2 == 0 and y % 2 == 0:
                board[y][x] = '#'
    return board

def set_start_and_end_positions(board):
    global start_x, start_y
    board[start_y][start_x] = "P"
    last_y, last_x = bfs()
    board[last_y][last_x] = "G"


def main():
    global round_, start_x, start_y 
    round_ = 0
    board = initialize_board()
    dfs(start_y, start_x)
    clean_board(board)
    set_start_and_end_positions(board)
    show_board(board, True)
    make_image_from_state(board, True)
    make_gif()


if __name__ == "__main__":
    main()
