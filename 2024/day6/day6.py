import copy

dirs = ['<', '>', '^', 'v']

def find_guard(m):
    for line in m:
        for col in line:
            if col in dirs:
                return ((m.index(line), line.index(col)), col)

def rotate(guard):
    rotated = guard
    match guard:
        case '<': rotated = '^'
        case '^': rotated = '>'
        case '>': rotated = 'v'
        case 'v': rotated = '<'
    return rotated

visited = set()
def run_guard_ai(m, guard, track_visits=True):
    global visited
    pos, facing = guard
    if track_visits:
        visited.add(pos)

    if pos[0]+1 >= len(m) or pos[1]+1 >= len(m[0]) \
        or pos[0]-1 < 0 or pos[1]-1 < 0:
        return True

    should_turn = False
    match facing:
        case '<': should_turn = m[pos[0]][pos[1]-1] == '#'
        case '>': should_turn = m[pos[0]][pos[1]+1] == '#'
        case '^': should_turn = m[pos[0]-1][pos[1]] == '#'
        case 'v': should_turn = m[pos[0]+1][pos[1]] == '#'
    if should_turn:
        rotated = rotate(facing)
        match facing:
            case '<': m[pos[0]] = m[pos[0]].replace(facing, rotated)
            case '>': m[pos[0]] = m[pos[0]].replace(facing, rotated)
            case '^': m[pos[0]] = m[pos[0]].replace(facing, rotated)
            case 'v': m[pos[0]] = m[pos[0]].replace(facing, rotated)
        return (m, (pos, rotated))
    else:
        match facing:
            case '<':
                new = list(m[pos[0]])
                new[pos[1]] = '.'
                new[pos[1]-1] = facing
                m[pos[0]] = "".join(new)
                return (m, ((pos[0], pos[1]-1), facing))
            case '>':
                new = list(m[pos[0]])
                new[pos[1]] = '.'
                new[pos[1]+1] = facing
                m[pos[0]] = "".join(new)
                return (m, ((pos[0], pos[1]+1), facing))
            case '^':
                new = list(m[pos[0]-1])
                new[pos[1]] = facing
                m[pos[0]] = m[pos[0]].replace(facing, '.')
                m[pos[0]-1] = "".join(new)
                return (m, ((pos[0]-1, pos[1]), facing))
            case 'v':
                new = list(m[pos[0]+1])
                new[pos[1]] = facing
                m[pos[0]] = m[pos[0]].replace(facing, '.')
                m[pos[0]+1] = "".join(new)
                return (m, ((pos[0]+1, pos[1]), facing))

def find_possible_loops(m, guard):
    global visited
    positions = 0
    visited.remove(guard[0])
    for point in visited:
        # print(f'checking {point}')
        new = m.copy()
        tmp = list(new[point[0]])
        tmp[point[1]] = '#'
        new[point[0]] = "".join(tmp)
        _visited = set()
        looped = False
        new_guard = guard
        while not looped:
            new = run_guard_ai(new, new_guard, False)
            if new == True:
                break
            else:
                new, new_guard = new
            if new_guard in _visited:
                looped = True
            else:
                _visited.add(new_guard)
        if looped:
            positions += 1
    return positions

with open('input.txt', 'r') as file:
    m = [l.strip() for l in file.readlines()]
    _m = copy.deepcopy(m)
    guard = find_guard(m)
    _guard = copy.deepcopy(guard)
    print(guard)
    while True:
        m = run_guard_ai(m, guard)
        if m == True:
            break
        else:
            m, guard = m
    print(f'Part 1: {len(set(visited))}')
    loops = find_possible_loops(_m, _guard)
    print(f'Part 2: {loops}')
