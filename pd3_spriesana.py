# =====================================================================
#  PRAKTISKAIS DARBS 3 — UZDEVUMS  (≈ 35 min)
#  Spriešana: domāšanas soļi un balsošana (paš-saskaņotība)
# =====================================================================
#  Spriešanas modeļi pirms atbildes "domā" — uzraksta starpsoļus.
#  Vēl viens triks: uzdot to pašu jautājumu vairākas reizes un izvēlēties
#  biežāko atbildi (balsošana). Pārbaudīsim, vai tas tiešām palīdz!
#
#  Aizpildi vietas ar  # TODO  un palaid failu. ✅ = pareizi.
# =====================================================================
import random

random.seed(7)

# ---------------------------------------------------------------------
# 3.1 Atrisini uzdevumu PA SOĻIEM (tā, kā to dara spriešanas modelis)
# ---------------------------------------------------------------------
# Uzdevums: Ābols maksā 0,40 €, banāns 0,25 €. Anna nopērk 3 ābolus
# un 4 banānus un maksā ar 5 € banknoti. Cik naudas viņa saņems atpakaļ?
#
# Rēķini CENTOS (veselos skaitļos)! Pamēģini termināli:  0.1 + 0.2
# Katru soli pievieno sarakstam "soli" kā tekstu, piemēram:
#   soli.append(f"1. solis: 3 āboli × {abols} c = {aboli_kopa} c")
def risinat_pa_soliem():
    soli = []
    abols, banans, banknote = 40, 25, 500   # centi
    aboli_kopa = 3 * abols
    soli.append(f"1. solis: 3 āboli × {abols} c = {aboli_kopa} c")
    banani_kopa = 4 * banans
    soli.append(f"2. solis: 4 banāni × {banans} c = {banani_kopa} c")
    pirkums = aboli_kopa + banani_kopa
    soli.append(f"3. solis: pirkums kopā maksā {aboli_kopa} + {banani_kopa} = {pirkums} c")
    atlikums = banknote - pirkums
    soli.append(f"4. solis: atlikums ir {banknote} - {pirkums} = {atlikums} c")
    return soli, atlikums


# ---------------------------------------------------------------------
# Simulēts MI modelis (gatavs — tas imitē īstu modeli, NEMAINI)
# ---------------------------------------------------------------------
PAREIZI = 280
NEPAREIZAS = [220, 300, 180, 380, 270, 120]


def modelis_atbild(rezims):
    """'ātri'  – atbild uzreiz, bez soļiem (pareizi ~55% gadījumu)
       'soļi'  – domā 4 soļos, katrs solis pareizs ar 93% varbūtību"""
    if rezims == "ātri":
        if random.random() < 0.55:
            return PAREIZI
        return random.choice(NEPAREIZAS)
    if rezims == "soļi":
        for _ in range(4):
            if random.random() > 0.93:      # kļūda kādā solī
                return random.choice(NEPAREIZAS)
        return PAREIZI
    raise ValueError("Nezināms režīms")


# ---------------------------------------------------------------------
# 3.2 Balsošana: biežākā atbilde uzvar
# ---------------------------------------------------------------------
# Piemērs: balsot([280, 300, 280]) -> 280
# Padoms: saskaiti atbildes vārdnīcā (kā 1. darbā), tad max(skaiti, key=skaiti.get)
def balsot(atbildes):
    skaiti = {}
    for atbilde in atbildes:
        skaiti[atbilde] = skaiti.get(atbilde, 0) + 1
    return max(skaiti, key=skaiti.get, default=None)


# ---------------------------------------------------------------------
# 3.3 Eksperiments: cik bieži modelis atbild pareizi?
# ---------------------------------------------------------------------
# n reizes:
#   1) savāc "balsis" atbildes:  [modelis_atbild(rezims) for _ in range(balsis)]
#   2) ja balsot(atbildes) == PAREIZI  -> pareizi += 1
# Atgriez pareizi / n  (skaitlis no 0 līdz 1)
def precizitate(rezims, balsis=1, n=1000):
    pareizi = 0
    for _ in range(n):
        atbildes = [modelis_atbild(rezims) for _ in range(balsis)]
        if balsot(atbildes) == PAREIZI:
            pareizi += 1
    return pareizi / n


# ---------------------------------------------------------------------
# 3.4 Cena: vairāk domāšanas = vairāk tokenu = vairāk laika un naudas
# ---------------------------------------------------------------------
TOKENI = {"ātri": 20, "soļi": 150}   # cik tokenu tērē VIENA atbilde


def izmaksas(rezims, balsis):
    return TOKENI[rezims] * balsis


# =====================================================================
#  PĀRBAUDES (nemaini šo daļu)
# =====================================================================
def parbaude(nosaukums, funkcija):
    try:
        ok = funkcija()
    except Exception as e:
        print(f"  ❌ {nosaukums}: kļūda — {e}")
        return
    print(f"  {'✅' if ok else '❌'} {nosaukums}")


if __name__ == "__main__":
    print("PĀRBAUDES:")
    parbaude("3.1 atlikums = 280 centi", lambda: risinat_pa_soliem()[1] == 280)
    parbaude("3.1 ir vismaz 3 soļi", lambda: len(risinat_pa_soliem()[0]) >= 3)
    parbaude("3.2 balsot([3,5,3]) == 3", lambda: balsot([3, 5, 3]) == 3)
    parbaude("3.2 balsot([7]) == 7", lambda: balsot([7]) == 7)
    parbaude("3.3 'soļi' precīzāki par 'ātri'", lambda: precizitate("soļi") > precizitate("ātri"))
    parbaude("3.3 balsošana uzlabo 'soļi'", lambda: precizitate("soļi", 5) > precizitate("soļi", 1))
    parbaude("3.4 izmaksas('soļi', 5) == 750", lambda: izmaksas("soļi", 5) == 750)

    print("\nDOMĀŠANAS SOĻI:")
    for s in risinat_pa_soliem()[0]:
        print("  " + s)

    print("\nEKSPERIMENTS (1000 mēģinājumi katram):")
    print(f"  {'Režīms':<22}{'Precizitāte':>12}{'Tokeni':>9}")
    for rezims, balsis in [("ātri", 1), ("ātri", 5), ("soļi", 1), ("soļi", 5)]:
        nosaukums = f"{rezims}" + (f" + {balsis} balsis" if balsis > 1 else "")
        print(f"  {nosaukums:<22}{precizitate(rezims, balsis)*100:>11.1f}%{izmaksas(rezims, balsis):>9}")

# ---------------------------------------------------------------------
# JAUTĀJUMI PĀRDOMĀM:
#  a) Cik reizes dārgāks ir režīms "soļi + 5 balsis" nekā "ātri"?
#     Vai tas ir tā vērts jautājumam "Kāda ir Latvijas galvaspilsēta?"
#  b) Kāpēc 4 soļi ar 93% precizitāti katrs dod tikai ~75%?
#     (Padoms: 0.93 × 0.93 × 0.93 × 0.93 = ?)
#  c) Kādos uzdevumos tu izmantotu spriešanas modeli, kādos — ātro?
# ---------------------------------------------------------------------
