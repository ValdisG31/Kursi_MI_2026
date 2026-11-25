# =====================================================================
#  PRAKTISKAIS DARBS 4 — UZDEVUMS  (≈ 35 min)
#  Halucinācijas un aizspriedumi: kā tos atpazīt un mazināt
# =====================================================================
#  A daļa: modelis reizēm "izdomā" faktus ļoti pārliecinošā tonī.
#          Uzbūvēsim divus aizsargus: pārliecības slieksni un faktu pārbaudi.
#  B daļa: ja apmācības dati ir nelīdzsvaroti, modelis atkārto šo
#          nelīdzsvarotību. Izmērīsim to un uztaisīsim godīgāku variantu.
#
#  Aizpildi vietas ar  # TODO  un palaid failu. ✅ = pareizi.
# =====================================================================

# ---------------------------------------------------------------------
# A DAĻA. HALUCINĀCIJAS
# ---------------------------------------------------------------------
# Uzticams avots (piem., enciklopēdija). Atslēga -> pareizā atbilde.
AVOTS = {
    "galvaspilsēta": "Rīga",
    "es_iestāšanās": "2004",
    "augstākais_kalns": "Gaiziņkalns",
    "gaiziņkalna_augstums": "312 m",
    "valūta": "eiro",
}

# Simulēta MI modeļa atbildes: (jautājums, atbilde, pārliecība 0–1, avota atslēga)
MODELA_ATBILDES = [
    ("Kāda ir Latvijas galvaspilsēta?",            "Rīga",                     0.98, "galvaspilsēta"),
    ("Kurā gadā Latvija iestājās ES?",             "2004",                     0.91, "es_iestāšanās"),
    ("Kāds ir augstākais kalns Latvijā?",          "Gaiziņkalns",              0.88, "augstākais_kalns"),
    ("Cik augsts ir Gaiziņkalns?",                 "412 m",                    0.83, "gaiziņkalna_augstums"),
    ("Kāda ir Latvijas valūta?",                   "lats",                     0.62, "valūta"),
    ("Kas izgudroja speķa pīrāgus?",               "Kārlis Pīrāgs 1742. gadā", 0.41, None),
    ("Cik grāmatu uzrakstīja Jānis Zvaigzne?",     "17 grāmatas",              0.35, None),
]


# 4.1 Godīga atbilde
# Ja parlieciba >= slieksnis -> atgriez atbildi.
# Citādi atgriez tekstu: "Neesmu pārliecināts — lūdzu, pārbaudi uzticamā avotā."
def godiga_atbilde(atbilde, parlieciba, slieksnis=0.7):
    if parlieciba >= slieksnis:
        return atbilde
    return "Neesmu pārliecināts — lūdzu, pārbaudi uzticamā avotā."


# 4.2 Faktu pārbaude pret avotu
# Atgriez vienu no trim tekstiem:
#   "⚠️ nav avota"        – ja atslega ir None vai tās nav AVOTS vārdnīcā
#   "✅ apstiprināts"     – ja AVOTS[atslega] sakrīt ar atbildi (neskatoties uz lielajiem burtiem)
#   "❌ pretrunā avotam"  – citādi
# Padoms: salīdzini  AVOTS[atslega].lower() == atbilde.lower()
def parbaudit_faktu(atslega, atbilde):
    if atslega not in AVOTS:
        return "⚠️ nav avota"
    if AVOTS[atslega].lower() == atbilde.lower():
        return "✅ apstiprināts"
    return "❌ pretrunā avotam"


# ---------------------------------------------------------------------
# B DAĻA. AIZSPRIEDUMI (BIAS)
# ---------------------------------------------------------------------
# Iedomājies, ka tulkotājs mācījies no šiem piemēriem (angļu -> latviešu).
# Angļu valodā "doctor" neatklāj dzimti, latviešu valodā jāizvēlas.
TRENINA_DATI = (
    [("doctor", "ārsts")] * 18 + [("doctor", "ārste")] * 2
    + [("nurse", "medmāsa")] * 19 + [("nurse", "medbrālis")] * 1
    + [("programmer", "programmētājs")] * 17 + [("programmer", "programmētāja")] * 3
    + [("teacher", "skolotāja")] * 15 + [("teacher", "skolotājs")] * 5
)


# 4.3 Cik procentos gadījumu katrs tulkojums parādās datos?
# Piemērs: tulkojumu_sadalijums(TRENINA_DATI, "doctor") -> {"ārsts": 90, "ārste": 10}
# 1) Saskaiti latviešu variantus tikai tiem pāriem, kur anglu == vards
# 2) Pārvērt procentos: round(skaits / kopa * 100)
def tulkojumu_sadalijums(dati, vards):
    skaiti = {}
    for anglu, latv in dati:
        if anglu == vards:
            skaiti[latv] = skaiti.get(latv, 0) + 1
    kopa = sum(skaiti.values())
    return {latv: round(skaits / kopa * 100) for latv, skaits in skaiti.items()}


# 4.4 Naivs tulkotājs: vienmēr ņem biežāko variantu
def naivs_tulkotajs(dati, vards):
    sad = tulkojumu_sadalijums(dati, vards)
    return max(sad, key=sad.get, default="")


# 4.5 Godīgāks tulkotājs: ja ir vairāki varianti, parāda visus,
#     sākot ar biežāko, atdalītus ar " / ", piemēram "ārsts / ārste"
# Padoms: sorted(sad, key=lambda v: -sad[v])   un   " / ".join(saraksts)
def godigs_tulkotajs(dati, vards):
    sad = tulkojumu_sadalijums(dati, vards)
    return " / ".join(sorted(sad, key=sad.get, reverse=True))


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
    parbaude("4.1 pārliecināta atbilde paliek", lambda: godiga_atbilde("Rīga", 0.98) == "Rīga")
    parbaude("4.1 nepārliecināta -> brīdinājums", lambda: godiga_atbilde("lats", 0.62).startswith("Neesmu"))
    parbaude("4.2 apstiprināts", lambda: parbaudit_faktu("galvaspilsēta", "rīga") == "✅ apstiprināts")
    parbaude("4.2 pretrunā", lambda: parbaudit_faktu("gaiziņkalna_augstums", "412 m") == "❌ pretrunā avotam")
    parbaude("4.2 nav avota", lambda: parbaudit_faktu(None, "17 grāmatas") == "⚠️ nav avota")
    parbaude("4.3 sadalījums 'doctor'", lambda: tulkojumu_sadalijums(TRENINA_DATI, "doctor") == {"ārsts": 90, "ārste": 10})
    parbaude("4.4 naivs 'nurse' -> 'medmāsa'", lambda: naivs_tulkotajs(TRENINA_DATI, "nurse") == "medmāsa")
    parbaude("4.5 godīgs 'doctor'", lambda: godigs_tulkotajs(TRENINA_DATI, "doctor") == "ārsts / ārste")

    print("\nA DAĻA — MODEĻA ATBILŽU PĀRBAUDE:")
    for jaut, atb, parl, atsl in MODELA_ATBILDES:
        print(f"  {jaut:<40} {atb:<26} {parl:.2f}  -> {godiga_atbilde(atb, parl)[:22]:<23} {parbaudit_faktu(atsl, atb)}")

# ---------------------------------------------------------------------
# JAUTĀJUMI PĀRDOMĀM:
#  a) Kuru kļūdu NENOĶĒRA pārliecības slieksnis, bet noķēra faktu pārbaude?
#  b) Kāpēc modelis atbildēja "lats"? (Padoms: kad Latvija pārgāja uz eiro?
#     Ko tas nozīmē par vecu tekstu daudzumu apmācības datos?)
#  c) B daļā: kāpēc naivais tulkotājs vienmēr raksta "ārsts", bet "medmāsa"?
#     Kas būtu jāmaina DATOS, lai to labotu?
# ---------------------------------------------------------------------
