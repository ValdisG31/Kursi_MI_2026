# =====================================================================
#  PRAKTISKAIS DARBS 6 — UZDEVUMS  (≈ 30 min)
#  Datu drošība pirms MI lietošanas un ES MI akta riska līmeņi
# =====================================================================
#  A daļa: pirms ielīmē tekstu čatbotā, aizstāj personas datus ar
#          marķieriem, piemēram [E-PASTS]. Uzrakstīsim "datu filtru".
#  B daļa: novērtē, kurā ES MI akta riska līmenī ir katrs MI lietojums.
#
#  Aizpildi vietas ar  # TODO  un palaid failu. ✅ = pareizi.
# =====================================================================
import re
import base64
import json

# ---------------------------------------------------------------------
# A DAĻA. PERSONAS DATU MASKĒŠANA
# ---------------------------------------------------------------------
# Regulārās izteiksmes (regex) īsumā:
#   \d      – jebkurš cipars              {6}   – tieši 6 reizes
#   \w      – burts, cipars vai _         +     – viens vai vairāk
#   \s?     – atstarpe vai nekas          [26]  – cipars 2 vai 6
#   (?<!\d) – "priekšā NAV cipara"        (?!\d) – "aiz NAV cipara"
#   re.sub(paraugs, aizstājējs, teksts)   – aizstāj visas atrastās vietas


# 6.1 PIEMĒRS (gatavs) — e-pasta adreses
def masket_epastus(teksts):
    return re.sub(r"[\w.\-]+@[\w\-]+\.[\w.]+", "[E-PASTS]", teksts)


# 6.2 Latvijas personas kods: 6 cipari, domuzīme, 5 cipari (piem., 010203-12345)
#     Aizstāj ar "[PERSONAS KODS]".
#     Padoms: paraugs ir  r"(?<!\d)\d{6}-\d{5}(?!\d)"
def masket_personas_kodus(teksts):
    return re.sub(r"(?<!\d)\d{6}-\d{5}(?!\d)", "[PERSONAS KODS]", teksts)


# 6.3 Latvijas tālrunis: 8 cipari, sākas ar 2 vai 6, priekšā var būt "+371 "
#     Aizstāj ar "[TĀLRUNIS]".
#     Padoms: (?:\+371\s?)?  nozīmē "+371 vai +371 ar atstarpi, vai nekas"
#             tad (?<!\d)[26]\d{7}(?!\d)
def masket_talrunus(teksts):
    return re.sub(r"(?<!\d)(?:\+371\s?)?[26]\d{7}(?!\d)", "[TĀLRUNIS]", teksts)


def masket_visu(teksts):  # gatavs
    teksts = masket_epastus(teksts)
    teksts = masket_personas_kodus(teksts)   # pirms tālruņiem!
    teksts = masket_talrunus(teksts)
    return teksts


# 6.4 Atrodi, kādi datu veidi ir tekstā.
#     Atgriez sarakstu, piem. ["e-pasts", "tālrunis"] (šādā secībā:
#     "e-pasts", "personas kods", "tālrunis").
#     Padoms: ja masket_epastus(teksts) != teksts  -> tekstā ir e-pasts
def atrast_sensitivus(teksts):
    atrasti = []
    for veids, masket in (
        ("e-pasts", masket_epastus),
        ("personas kods", masket_personas_kodus),
        ("tālrunis", masket_talrunus),
    ):
        maskets = masket(teksts)
        if maskets != teksts:
            atrasti.append(veids)
        teksts = maskets
    return atrasti


def drosa_uzvedne(teksts):  # gatavs
    atrasti = atrast_sensitivus(teksts)
    if atrasti:
        print(f"  ⚠️ Atrasti personas dati: {', '.join(atrasti)}. Tie tiks aizstāti.")
    return masket_visu(teksts)


# ---------------------------------------------------------------------
# B DAĻA. ES MI AKTA RISKA LĪMEŅI
# ---------------------------------------------------------------------
# 6.5 Aizstāj katru "?" ar vienu no līmeņiem:
#     "nepieņemams"  – aizliegts ES
#     "augsts"       – atļauts, bet ar stingrām prasībām
#     "ierobežots"   – jāinformē cilvēks (caurskatāmība)
#     "minimāls"     – nav īpašu prasību
MANAS_ATBILDES = {
    "Surogātpasta (spama) filtrs e-pastā": "minimāls",
    "Čatbots e-veikala klientu atbalstam": "ierobežots",
    "MI, kas atlasa CV darbā pieņemšanai": "augsts",
    "Valsts iedzīvotāju 'sociālā vērtēšana' ar punktiem": "nepieņemams",
    "MI, kas vērtē studentu eksāmenu darbus": "augsts",
    "Pretinieks datorspēlē": "minimāls",
    "MI ģenerēts video ar reālas personas seju (dziļviltojums)": "ierobežots",
    "Darbinieku emociju atpazīšana darbavietā": "nepieņemams",
    "Bankas MI, kas izlemj par kredīta piešķiršanu": "augsts",
}

# Pareizās atbildes ir "noslēptas" (base64). Nemēģini atšifrēt — padomā pats! 😉
_PAREIZAS = json.loads(base64.b64decode(
    "eyJTdXJvZ8SBdHBhc3RhIChzcGFtYSkgZmlsdHJzIGUtcGFzdMSBIjogIm1pbmltxIFscyIsICLEjGF0Ym90cyBlLXZlaWthbGEga2xpZW50dSBhdGJhbHN0YW0iOiAiaWVyb2Jlxb5vdHMiLCAiTUksIGthcyBhdGxhc2EgQ1YgZGFyYsSBIHBpZcWGZW3FoWFuYWkiOiAiYXVnc3RzIiwgIlZhbHN0cyBpZWR6xKt2b3TEgWp1ICdzb2NpxIFsxIEgdsSTcnTEk8WhYW5hJyBhciBwdW5rdGllbSI6ICJuZXBpZcWGZW1hbXMiLCAiTUksIGthcyB2xJNydMSTIHN0dWRlbnR1IGVrc8SBbWVudSBkYXJidXMiOiAiYXVnc3RzIiwgIlByZXRpbmlla3MgZGF0b3JzcMSTbMSTIjogIm1pbmltxIFscyIsICJNSSDEo2VuZXLEk3RzIHZpZGVvIGFyIHJlxIFsYXMgcGVyc29uYXMgc2VqdSAoZHppxLx2aWx0b2p1bXMpIjogImllcm9iZcW+b3RzIiwgIkRhcmJpbmlla3UgZW1vY2lqdSBhdHBhesSrxaFhbmEgZGFyYmF2aWV0xIEiOiAibmVwaWXFhmVtYW1zIiwgIkJhbmthcyBNSSwga2FzIGl6bGVtaiBwYXIga3JlZMSrdGEgcGllxaHEt2lyxaFhbnUiOiAiYXVnc3RzIn0="
).decode())


def novertet(atbildes):
    pareizi = sum(1 for k, v in atbildes.items() if _PAREIZAS.get(k) == v.strip().lower())
    return pareizi, len(_PAREIZAS)


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
    parbaude("6.1 e-pasts", lambda: masket_epastus("Raksti: anna.berzina@epasts.lv!") == "Raksti: [E-PASTS]!")
    parbaude("6.2 personas kods", lambda: masket_personas_kodus("PK 010203-12345.") == "PK [PERSONAS KODS].")
    parbaude("6.3 tālrunis ar +371", lambda: masket_talrunus("Zvani +371 29123456") == "Zvani [TĀLRUNIS]")
    parbaude("6.3 tālrunis bez +371", lambda: masket_talrunus("tel. 67123456") == "tel. [TĀLRUNIS]")
    parbaude("6.3 neaiztiek gadu 2024", lambda: masket_talrunus("2024. gadā") == "2024. gadā")
    parbaude("6.4 atrast_sensitivus", lambda: atrast_sensitivus("a@b.lv 29123456") == ["e-pasts", "tālrunis"])
    pareizi, kopa = novertet(MANAS_ATBILDES)
    parbaude(f"6.5 riska līmeņi: {pareizi}/{kopa}", lambda: pareizi == kopa)

    print("\nDEMONSTRĀCIJA:")
    vestule = ("Lūdzu, uzraksti atvainošanās vēstuli klientei Annai Bērziņai "
               "(anna.berzina@epasts.lv, tālr. +371 29123456, p.k. 010203-12345) "
               "par kavēto pasūtījumu Nr. 2024-118.")
    print("ORIĢINĀLS:\n  " + vestule)
    print("DROŠĀ VERSIJA:\n  " + drosa_uzvedne(vestule))

# ---------------------------------------------------------------------
# JAUTĀJUMI PĀRDOMĀM:
#  a) Kuri personas dati drošajā versijā PALIKA? Kāpēc regex tos neatrada?
#  b) Kāpēc personas kodus maskējam PIRMS tālruņiem?
#  c) Kāds ir atšķirīgais riska līmenis "čatbotam e-veikalā" un
#     "MI, kas vērtē eksāmenus"? Kāpēc likums tos vērtē atšķirīgi?
# ---------------------------------------------------------------------
