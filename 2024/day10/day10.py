import itertools as it
dirs = [(-1, 0), (0, -1), (1, 0), (0, 1)]
def move(pos, dir):
    return (pos[0]+dir[0], pos[1]+dir[1])
def get(pos, topo):
    if pos[0] >= 0 and pos[0] < len(topo) and \
        pos[1] >= 0 and pos[1] < len(topo[0]):
        return topo[pos[0]][pos[1]]
    else:
        return -1
def search_dir(pos, topo):
    if get(pos, topo) == 9:
        return 1
    valid_dirs = [dir for dir in dirs if (get(move(pos, dir), topo) == get(pos, topo) + 1) \
                                          and get(move(pos, dir), topo) != -1]
    print([(pos, get(move(pos, dir), topo)) for dir in valid_dirs])
    if len(valid_dirs) == 0:
        return 0
    return sum([search_dir(move(pos, dir), topo) for dir in valid_dirs])
def search(start, topo):
    return search_dir(start, topo)
with open('test.txt', 'r') as file:
    lines = list(map(lambda l: l.strip(), file.readlines()))
    topo = [list(map(int, line)) for line in lines]
    trail_starts = []
    for i in range(len(topo)):
        for j in range(len(topo[i])):
            if topo[i][j] == 0:
                trail_starts.append((i, j))
    sum_scores = 0
    for start in trail_starts:
        sum_scores += search(start, topo)
    print(sum_scores)
    # print(trail_starts)
    # print(len(trail_starts))