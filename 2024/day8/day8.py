import itertools as it
from math import sqrt
with open('input.txt', 'r') as file:
    lines = list(map(lambda l: l.strip(), file.readlines()))
    antennas = list(filter(lambda a: a[0] != '.',
               it.chain.from_iterable([[(lines[i][j], (i, j))
                                        for j in range(len(lines[i]))]
                                       for i in range(len(lines))])))
    antennas = {a[0]: [b[1] for b in filter(lambda x: x[0] == a[0], antennas)]
                for a in antennas}
    antinodes = set()
    offset_of = lambda a, b: (a[0] - b[0], a[1] - b[1])
    neg_loc = lambda loc: (-loc[0], -loc[1])
    in_bounds = lambda loc: loc[0] >= 0 and loc[0] < len(lines) \
                            and loc[1] >= 0 and loc[1] < len(lines[0])
    get_antinodes = lambda loc, offset: it.chain.from_iterable(
                        [[(loc[0]+o[0], loc[1]+o[1])] for o in
                         [offset, neg_loc(offset)]])
    for freq, locs in antennas.items():
        for loc in locs:
            offsets = [offset_of(loc, other) for other in locs if other != loc]
            for offset in offsets:
                should_add = lambda x: in_bounds(x) and x not in locs
                new = filter(should_add, get_antinodes(loc, offset))
                for antinode in new:
                    antinodes.add(antinode)
    print(f'Part 1: {len(antinodes)}')
    for freq, locs in antennas.items():
        for loc in locs:
            offsets = [offset_of(loc, other) for other in locs if other != loc]
            for offset in offsets:
                new_offset = offset
                new = list(get_antinodes(loc, offset))
                while in_bounds(new[0]) or in_bounds(new[1]):
                    for antinode in filter(in_bounds, new):
                        antinodes.add(antinode)
                    new_offset = (new_offset[0] + offset[0], new_offset[1] + offset[1])
                    new = list(get_antinodes(loc, new_offset))
    print(f'Part 2: {len(antinodes)}')
    # for i in range(len(lines)):
    #     for pos in antinodes:
    #         if pos[0] == i and lines[i][pos[1]] == '.':
    #             lst = list(lines[i])
    #             lst[pos[1]] = '#'
    #             lines[i] = lst
    #     for c in lines[i]:
    #         print(c, end='')
    #     print()
