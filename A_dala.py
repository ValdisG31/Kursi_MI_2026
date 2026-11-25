
def skaitit(teksts):
    skaiti = {}
    for i in range(len(teksts) - 1):
        a, b = teksts[i], teksts[i + 1]

        if a not in skaiti:
            skaiti[a] = {}

        skaiti[a][b] = skaiti[a].get(b, 0) + 1

    return skaiti
