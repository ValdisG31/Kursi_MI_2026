
def skaitit(teksts):
    skaiti = {}

    for i in range(len(teksts) - 1):
        a, b = teksts[i], teksts[i + 1]

        if a not in skaiti:
            skaiti[a] = {}

        skaiti[a][b] = skaiti[a].get(b, 0) + 1

    return skaiti


# Pārbaude ar vārdu "mamma"
teksts = "mamma"
rezultats = skaitit(teksts)

print("Burtu skaits un procenti:")

for burts, nakamie in rezultats.items():
    kopejais = sum(nakamie.values())

    print(f"\nAiz burta '{burts}':")

    for nakamais, skaits in nakamie.items():
        procenti = skaits / kopejais * 100
        print(f"  '{nakamais}' - {skaits} reizes ({procenti:.2f}%)")
