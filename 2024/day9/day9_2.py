# Wrote part 2 in Python because I simply couldn't
# figure out how to optimize it enough in Haskell :/
import itertools as it
def compressed(disk_map):
    for i, block in zip(range(1, len(disk_map)), disk_map[1:]):
        if -1 in disk_map[i-1] and -1 not in block:
            return False
    return True
def is_free(block, min_length):
    return len(block) >= min_length and all([x == -1 for x in block])
def has_space(block, min_length):
    return block.count(-1) >= min_length
def concat_free_blocks(disk_map):
    for i in reversed(range(len(disk_map[1:]))):
        if is_free(disk_map[i-1], 1) and is_free(disk_map[i], 1):
            disk_map[i-1] += disk_map[i]
            del disk_map[i]
    return disk_map
with open('input.txt', 'r') as file:
    disk_map = list(map(int, file.read().strip()))
    disk_map = list(filter(lambda x: len(x) > 0, [[i // 2] * disk_map[i] if i % 2 == 0 else [-1] * disk_map[i] for i in range(len(disk_map))]))
    pretty = lambda dm: ''.join([str(x) if x != -1 else '.' for x in it.chain.from_iterable(dm)])
    file_i = len(disk_map)
    while not compressed(disk_map):
        # print(file_i)
        disk_map = concat_free_blocks(disk_map)
        file_i -= 1
        if file_i < 0: break
        block = disk_map[file_i]
        if is_free(block, 1): continue
        free_i = None
        for i, x in enumerate(disk_map[:file_i]):
            if has_space(disk_map[i], len(block)):
                free_i = i
                break
        if free_i == None: continue
        free_start = disk_map[free_i].index(-1)
        for j, item in enumerate(block):
            # print(disk_map[free_i][j-1])
            disk_map[free_i][free_start+j] = item
        # print(disk_map[i])
        disk_map[file_i] = [-1 for x in block]
    # print(f'final:    {pretty(disk_map)}')
    print(sum(map(lambda x: (x[0] * x[1]) if x[1] != -1 else 0, enumerate(it.chain.from_iterable(disk_map)))))