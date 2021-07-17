"""script thrown together which computes dice odds for boardbame Dragonwood"""
import math
die = [1, 2, 2, 3, 3, 4]


def go(num_dice):
    a = [[x] for x in die]
    b = []
    #print("early a = %s" % a)
    for _ in range(num_dice-1):
        for i, x in enumerate(a):
            b.extend([x + [d] for d in die])
        a = b
        b = []
    total = len(a)
    #print("total=%d" % total)
    expected = 6**num_dice
    if total != expected:
        raise RuntimeError("total %d != expected %d" % (total, expected))

    counts = {}
    for x in a:
        s = sum(x)
        if s in counts:
            counts[s] += 1
        else:
            counts[s] = 1

    answer = list([(k, counts[k]) for k in sorted(counts.keys(), reverse=True)])
    adjusted = []
    running = 0
    for k, v in answer:
        running += v
        adjusted.append((k, v, running))
    #print("adjusted=%s" % adjusted)
    #return

    print("-" * 40)
    print("Number of dice: %d\n" % num_dice)
    for k, v, running in reversed(adjusted):
        running_p = 100*running/total
        running_p_str = "%03.5f%%" % running_p
        running_f_str = "%6d/%d" % (running, total)
        p = 100*v/total
        p_str = "%03.5f%%" % p
        f_str = "%6d/%d" % (v, total)
        #print("%3d  =  %2d%%    %12s  (%10s)" % (k, int(p), f_str, p_str))
        print("%3d  =  %3s%%  %12s  (%10s)" % (k, int(running_p), running_f_str, running_p_str))

    return adjusted


big_table = {}
for n in range(1, 7):
    big_table[n] = go(n)


need_table = {k: [0 for _ in range(0, 7)] for k in range(3, 16)}
#print("need_table=%s" % need_table)
for n, entry in big_table.items():
    total = 6**n
    for k, v, running in entry:
        if 3 <= k <= 15:
            #print("k,n = %d, %d" % (k, n))
            need_table[k][n] = math.floor(100*running/total)

for k, v in need_table.items():
    prev = 0
    row = []
    for item in v:
        if prev >= 100:
            item = 100
        row.append(item)
        prev = item
    need_table[k] = row

print("\n\nNeed    1      2      3      4      5      6")
print("=" * 45)
for k in sorted(need_table.keys()):
    values = need_table[k]
    row = "  ".join(["%5s" % ("%d%%" % v) for v in values[1:7]])
    print("%2s   %s" % (k, row))

