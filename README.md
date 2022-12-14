# Perfect Maze Generator

This program generates a perfect maze (a maze each point has exactly one path to it).

As an added bonus, a gif is generated showing the process that was taken to generate the maze. The red dot at the end of the gif is the goal point of the maze. It is the farthest point from the start.

<img src="example.gif" width="400" height="400">

For fun, here is a 61 by 61 maze

![](smaller_61x61.gif)

# Running the Program

This program was made for python 3.10 or later.

```
usage: maze_pretty.py [-h] [-d DIM] [-y Y_DIM] [-p] [-o OUTPUT] [-n]

Generates a perfect maze

options:
  -h, --help            show this help message and exit
  -d DIM, --dim DIM     The maze generated will be of size DIM by DIM (both should be odd)
  -y Y_DIM, --y_dim Y_DIM
                        Overrides the y dimension with this value
  -p, --print           Print every step of the generation to the console
  -o OUTPUT, --output OUTPUT
                        File name for the final gif
  -n, --noGif           Should the gif be left out? (The final result will only be printed to the console)
```

Seeing as the gif generated can be quite large, if you are on Linux and have `gifsicle` installed, you can use this command to optimize the gif:

`gifsicle -O3 --colors=32 --use-col=web --delay 5 --scale 8 combined.gif -o optimized_output.gif`

where 
* `-03` finds the best algorithm for compression, 
* `--colors=32` reduces the number of distinct colors to 32, 
* `--use-col=web` for web colors
* `--delay 5` to speed up the gif (.05 seconds between frames)
* `--scale 8` multiplies the XY size of the gif by 8 (exported version is very small)

