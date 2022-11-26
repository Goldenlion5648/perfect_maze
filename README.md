# Perfect Maze Generator

This program generates a perfect maze (a maze each point has exactly one path to it).

# Preview
As an added bonus, a gif is generated showing the process that was taken to generate the maze.

This program was made for python 3.10 or later on windows. Seeing as the gif generated can be quite large, if you are on Linux and have `gifsicle` installed, you can use this command to optimize the gif:

`gifsicle -O3 --colors=32 --use-col=web --delay 5 --scale 8 combined.gif -o optimized_output.gif`

where 
* `-03` finds the best algorithm for compression, 
* `--colors=32` reduces the number of distinct colors to 32, 
* `--use-col=web` for web colors
* `--delay 5` to speed up the gif (.05 seconds between frames)
* `--scale 8` multiplies the XY size of the gif by 8 (exported version is very small)

