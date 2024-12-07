import itertools as it
def run(lines, part_2):
    sum = 0
    for line in lines:
        res, nums = line.strip().split(': ')
        nums = list(map(int, nums.split()))
        results = [nums[0]]
        for n in nums[1:]:
            f = lambda a: [a+n, a*n] + ([] if not part_2 else [int(str(a) + str(n))])
            results = list(it.chain.from_iterable(map(f, results)))
        if int(res) in results: sum += int(res)
    return sum
with open('test.txt', 'r') as file:
    lines = list(map(lambda l: l.strip(), file.readlines()))
    print(f'Part 1: {run(lines, False)}')
    print(f'Part 2: {run(lines, True)}')
