import time
import turtle

def draw_square(x, y, size, color):
    turtle.up()
    turtle.goto(x, y)
    turtle.color(color)
    turtle.begin_fill()
    for _ in range(4):
        turtle.forward(size)
        turtle.right(90)
    turtle.end_fill()


def draw_maze(maze):
    turtle.hideturtle()
    turtle.tracer(False)
    rows = len(maze)
    cols = len(maze[0])
    square_size = 20
    offset_x = - cols * square_size // 2
    offset_y = rows * square_size // 2
    for i in range(rows):
        for j in range(cols):
            x = offset_x + j * square_size
            y = offset_y - i * square_size
            if maze[i][j] == '%':
                draw_square(x, y, square_size, 'black')
            elif maze[i][j] == 'S':
                draw_square(x, y, square_size, 'red')
            elif maze[i][j] == 'G':
                draw_square(x, y, square_size, 'green')
            else:
                draw_square(x, y, square_size, 'white')


def draw_path(maze, path, start_pos):
    turtle.hideturtle()
    turtle.tracer(True)
    rows = len(maze)
    cols = len(maze[0])
    square_size = 20
    offset_x = - cols * square_size // 2
    offset_y = rows * square_size // 2
    y, x = start_pos
    for step in path[:-1]:
        if step == 'U':
            y -= 1
        elif step == 'D':
            y += 1
        elif step == 'L':
            x -= 1
        elif step == 'R':
            x += 1
        draw_square(offset_x + x * square_size, offset_y - y * square_size, square_size, 'cyan')


def read_maze_file(file_path: str):
    with open(file_path, 'r') as f:
        # read the dimensions of the maze from the first line
        dimensions = f.readline().strip().split(',')
        num_rows, num_cols = int(dimensions[0]), int(dimensions[1])
        maze = [list(line.strip()) for line in f]
    return maze, num_rows, num_cols


# function to find start position
def find_start(maze: list, rows: int, cols: int):
    for row in range(rows):
        for col in range(cols):
            if maze[row][col] == 'S':
                start = (row, col)
                return start


# function to check if a position is valid
def is_valid_position(maze, row, col, num_rows, num_cols):
    return 0 <= row < num_rows and 0 <= col < num_cols and maze[row][col] != '%'


# function to get the neighbors of a position
def get_neighbors(maze, row, col, num_rows, num_cols):
    neighbors = []
    for drow, dcol, move in [(-1, 0, 'U'), (1, 0, 'D'), (0, -1, 'L'), (0, 1, 'R')]:
        new_row, new_col = row + drow, col + dcol
        if is_valid_position(maze, new_row, new_col, num_rows, num_cols):
            neighbors.append(((new_row, new_col), move))
    return neighbors


def solve_maze_dfs(maze: list, start_pos: tuple, num_rows, num_cols):
    # initialize the stack with the start position
    stack = [(start_pos, [])]

    # initialize a set to keep track of visited positions
    visited = set()

    # loop until the stack is empty
    while stack:
        # pop the last element from the stack and get its position and path
        pos, path = stack.pop()

        # if the position is the goal, return the path
        if maze[pos[0]][pos[1]] == 'G':
            return path

        # if the position has not been visited, mark it as visited and add its neighbors to the stack
        if pos not in visited:
            visited.add(pos)
            for neighbor_pos, move in get_neighbors(maze, pos[0], pos[1], num_rows, num_cols):
                stack.append((neighbor_pos, path + [move]))

    # if the stack is empty and the goal has not been found, return None
    return None


# main function
if __name__ == '__main__':
    file_path = input('Please enter the maze file path: ')
    maze, rows, cols = read_maze_file(file_path)
    start_pos = find_start(maze, rows, cols)

    start_time = time.perf_counter()
    path = solve_maze_dfs(maze, start_pos, rows, cols)
    end_time = time.perf_counter()
    run_time = (end_time - start_time) * 1e9
    type_time = 'ns'
    if run_time / 1000000 > 1:
        run_time = run_time / 1000000
        type_time = 'ms'
        if run_time / 1000 > 1:
            run_time = run_time / 1000
            type_time = 's'

    if path is None:
        print('Not found')
    else:
        print('Find:', ','.join(path))
        print(f'Run time: {run_time:.3f} {type_time}')
        command = input('Do you like to print the maze with turtle [y/n]? ')
        if command.lower() == 'y':
            draw_maze(maze)
            draw_path(maze, path, start_pos)
            turtle.done()

