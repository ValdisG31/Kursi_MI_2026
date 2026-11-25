"""
PD2 — Nākamā burta minētājs: mazākais iespējamais valodas modelis (UZDEVUMS, ~30 min)

Vajadzīgā matemātika: skaitīšana, procenti, daļskaitļi, kvadrāts un kvadrātsakne.

Ideja: modelis skatās tikai uz VIENU iepriekšējo burtu un atceras, cik bieži
aiz tā nāca katrs cits burts.

  A) Saskaitīt, kas seko katram burtam.
  B) Pārvērst skaitus procentos.
  C) Cik bieži modelis uzmin nākamo burtu? Salīdzināt ar nejaušu minēšanu.
  D) Ģenerēt jaunu tekstu trīs režīmos.

Palaišana:  python pamatlimenis/uzdevumi/02_nakama_burta_minetajs.py
Gaidāmais:  simboli=37 summa=100 nejauss=2.7 modelis=25.2

Papīra iesildīšanās: vārdā "mamma" aiz burta "m" nāk: a, m, a. Cik % gadījumu
aiz "m" nāk "a"?  (2 no 3 = ?%)

Jautājumi (atbildi faila beigās):
  1. Kāpēc ģenerētais teksts izklausās pēc latviešu valodas, bet nav jēgpilns?
  2. Cik kombināciju būtu tabulā, ja modelis atcerētos 5 burtus (37 simboli)?
  3. Ja nākamajiem burtiem svari ir 4 un 1, kādas ir iespējas (%) katrā režīmā?
"""
from pathlib import Path
import random

random.seed(1)
teksts = (Path(__file__).resolve().parent.parent / "dati" / "teksts.txt").read_text(encoding="utf-8").lower()
burti = sorted(set(teksts))


# ---------------------------------------------------------------- A daļa
def skaitit(teksts):
    """Atgriez vārdnīcu: skaiti[a][b] = cik reizes aiz burta a nāca burts b.
    Piemērs tekstam "aba": {"a": {"b": 1}, "b": {"a": 1}}"""
    skaiti = {}
    for i in range(len(teksts) - 1):
        a, b = teksts[i], teksts[i + 1]
        # TODO: ja a vēl nav skaiti, izveido skaiti[a] = {}
        # TODO: palielini skaiti[a][b] par 1  (padoms: .get(b, 0) + 1)
        raise NotImplementedError("TODO: skaitit")
    return skaiti


# ---------------------------------------------------------------- B daļa
def procenti(skaiti, burts):
    """Atgriez {nākamais_burts: procents}, procents = skaits / kopā · 100,
    noapaļots līdz 1 zīmei aiz komata (round(x, 1))."""
    rinda = skaiti[burts]
    # TODO
    raise NotImplementedError("TODO: procenti")


# ---------------------------------------------------------------- C daļa
def minet(skaiti, burts):
    """Atgriez biežāko burtu, kas seko `burts`. Padoms: max(rinda, key=rinda.get)"""
    # TODO
    raise NotImplementedError("TODO: minet")


def cik_bieži_uzmin(skaiti, teksts):
    """Katrai vietai i: vai minet(skaiti, teksts[i]) == teksts[i+1]?
    Atgriez pareizo minējumu procentu."""
    # TODO
    raise NotImplementedError("TODO: cik_bieži_uzmin")


# ---------------------------------------------------------------- D daļa
def generet(skaiti, sakums, garums=80, rezims="parasts"):
    """uzmanīgs: svari kvadrātā;  parasts: svari;  drosmīgs: kvadrātsakne no svariem."""
    rezultats = sakums
    burts = sakums
    for _ in range(garums):
        rinda = skaiti[burts]
        varianti = list(rinda.keys())
        svari = list(rinda.values())
        # TODO: pārveido svarus atkarībā no režīma (s ** 2 vai s ** 0.5)
        burts = random.choices(varianti, weights=svari)[0]
        rezultats += burts
    return rezultats


if __name__ == "__main__":
    print(f"Tekstā ir {len(teksts)} rakstzīmes un {len(burti)} dažādi simboli.")
    skaiti = skaitit(teksts)
    rinda = sorted(skaiti["ā"].items(), key=lambda kv: -kv[1])[:5]
    print("\nA) Kas seko burtam 'ā':", ", ".join(f"{b!r}: {s}" for b, s in rinda))

    p = procenti(skaiti, "ā")
    print("B) Procentos:", ", ".join(f"{b!r}: {p[b]}%" for b, _ in rinda))

    nejauss = 100 / len(burti)
    modelis = cik_bieži_uzmin(skaiti, teksts)
    print(f"\nC) Nejauši: {nejauss:.1f}%, modelis: {modelis:.1f}%")

    print("\nD) Ģenerēšana:")
    for r in ("uzmanīgs", "parasts", "drosmīgs"):
        print(f"   {r:9}: {generet(skaiti, 'm', 70, r)!r}")

    print(f"\nREZULTĀTS simboli={len(burti)} summa={round(sum(p.values()))} "
          f"nejauss={nejauss:.1f} modelis={modelis:.1f}")

# Atbildes uz jautājumiem:
# 1.
# 2.
# 3.
