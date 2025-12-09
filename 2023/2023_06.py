import numpy as np

if __name__ == '__main__':
    times = [7, 15, 30]
    dists = [9, 40, 200]
    times = [40,     81,     77,     72]
    dists = [219,   1012,   1365,   1089]
    times = [71530]
    dists = [940200]
    times = [40817772]
    dists = [219101213651089]

    alls = []
    for idx, t in enumerate(times):
        s = 0
        for ti in range(t):
            if (t - ti) * ti > dists[idx]:
                s += 1
        alls.append(s)
    print(np.prod(np.array(alls)))