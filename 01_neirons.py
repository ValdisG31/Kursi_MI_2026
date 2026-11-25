"""
PD1 — Neirons: balsošana ar svariem un mācīšanās no kļūdām (UZDEVUMS, ~25 min)

Vajadzīgā matemātika: reizināšana, saskaitīšana, salīdzināšana (≥).

  A) Neirons pieņem lēmumu "iet uz pludmali?" pēc trim pazīmēm.
  B) Neirons PATS iemācās loģisko funkciju UN, labojot savas kļūdas.
  C) Tas pats noteikums nespēj iemācīties XOR ("vai nu viens, vai otrs").
  D) Divi slāņi ar TEVIS izvēlētiem svariem XOR atrisina (mīkla!).

Aizpildi vietas ar  # TODO.  Palaišana:  python pamatlimenis/uzdevumi/01_neirons.py
Gaidāmais rezultāts:  pludmale=[1, 0, 0] un=1.00 xor_viens=kļūdās xor_divi=1.00

Pirms koda — izrēķini A daļu uz papīra! Svari [3, 2, -4], slieksnis 4.
  "saulains un silts" = [1, 1, 0]:  1·3 + 1·2 + 0·(-4) = ?   Vai ≥ 4?

Jautājumi (atbildi faila beigās):
  1. Ko nozīmē, ka "vējains" svars ir negatīvs?
  2. Uzzīmē XOR 4 punktus koordinātu plaknē. Kāpēc viens neirons to nespēj?
  3. Kā īstos tīklos tiek atrasti miljardiem svaru?
"""


# ---------------------------------------------------------------- A daļa
def neirons(ieejas, svari, slieksnis):
    """Sareizini katru ieeju ar tās svaru un saskaiti visu.
    Ja summa ≥ slieksnis -> atgriez 1, citādi 0."""
    summa = 0
    # TODO: ar for ciklu (zip(ieejas, svari)) pieskaiti summai x * w
    # TODO: atgriez 1 vai 0
    raise NotImplementedError("TODO: neirons")


# ---------------------------------------------------------------- B daļa
def macit(piemeri, solu_skaits=20, solis=1):
    """Mācīšanās noteikums:
        kļūda = pareizā atbilde - neirona atbilde      (-1, 0 vai 1)
        jaunais svars = vecais svars + solis * kļūda * ieeja
        jaunais slieksnis = vecais slieksnis - solis * kļūda"""
    svari = [0, 0]
    slieksnis = 0
    for kartas_nr in range(1, solu_skaits + 1):
        kludu_skaits = 0
        for ieejas, pareizi in piemeri:
            atbilde = neirons(ieejas, svari, slieksnis)
            kluda = pareizi - atbilde
            if kluda != 0:
                kludu_skaits += 1
                # TODO: izmaini katru svaru pēc noteikuma (for i in range(len(svari)))
                # TODO: izmaini slieksni pēc noteikuma
                raise NotImplementedError("TODO: svaru labošana")
        print(f"  {kartas_nr:2}. kārta: kļūdas = {kludu_skaits}, svari = {svari}, slieksnis = {slieksnis}")
        if kludu_skaits == 0:
            print("  -> Kļūdu vairs nav, mācīšanās pabeigta!")
            break
    return svari, slieksnis, kludu_skaits


def precizitate(piemeri, funkcija):
    pareizi = sum(1 for ieejas, y in piemeri if funkcija(ieejas) == y)
    return pareizi / len(piemeri)


UN = [([0, 0], 0), ([0, 1], 0), ([1, 0], 0), ([1, 1], 1)]
XOR = [([0, 0], 0), ([0, 1], 1), ([1, 0], 1), ([1, 1], 0)]


# ---------------------------------------------------------------- D daļa
def xor_divi_slani(ieejas):
    """MĪKLA: atrodi svarus un sliekšņus!
       h1 = "VAI"    -> 1, ja vismaz viena ieeja ir 1
       h2 = "NE-UN"  -> 1, ja NAV abas ieejas reizē 1
       izeja = "UN" no h1 un h2
    Padoms: pārbaudi katru variantu uz papīra ar visām 4 ieejām."""
    h1 = neirons(ieejas, [0, 0], 0)      # TODO: nomaini svarus un slieksni
    h2 = neirons(ieejas, [0, 0], 0)      # TODO: (padoms: negatīvi skaitļi!)
    return neirons([h1, h2], [0, 0], 0)  # TODO


if __name__ == "__main__":
    print("A) Vai iet uz pludmali?  pazīmes: [saulains, silts, vējains]")
    svari, slieksnis = [3, 2, -4], 4
    situacijas = {"saulains un silts": [1, 1, 0],
                  "saulains, silts, vējains": [1, 1, 1],
                  "tikai silts": [0, 1, 0]}
    a_atbildes = []
    for nosaukums, x in situacijas.items():
        lemums = neirons(x, svari, slieksnis)
        a_atbildes.append(lemums)
        print(f"  {nosaukums:26} -> {'IET' if lemums else 'NEIET'}")

    print("\nB) Neirons mācās UN")
    w, s, _ = macit(UN)
    p_un = precizitate(UN, lambda x: neirons(x, w, s))
    print(f"  Precizitāte: {p_un:.0%}")

    print("\nC) Neirons mēģina iemācīties XOR")
    w, s, pedejas_kludas = macit(XOR, solu_skaits=10)
    p_xor1 = precizitate(XOR, lambda x: neirons(x, w, s))
    print(f"  Precizitāte: {p_xor1:.0%}")

    print("\nD) Divi slāņi atrisina XOR")
    for x, y in XOR:
        print(f"  {x} -> {xor_divi_slani(x)} (pareizi: {y})")
    p_xor2 = precizitate(XOR, xor_divi_slani)
    print(f"  Precizitāte: {p_xor2:.0%}")

    print(f"\nREZULTĀTS pludmale={a_atbildes} un={p_un:.2f} "
          f"xor_viens={'kļūdās' if pedejas_kludas > 0 else 'ok'} xor_divi={p_xor2:.2f}")

# Atbildes uz jautājumiem:
# 1.
# 2.
# 3.
