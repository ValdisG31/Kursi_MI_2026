# =====================================================================
#  PRAKTISKAIS DARBS 5 — UZDEVUMS  (≈ 40 min)
#  Uzbūvē savu MI aģentu: plāns → darbība (rīki) → novērojums → atmiņa
# =====================================================================
#  Īstā aģentā plānu sastāda valodas modelis. Šeit plānotājs ir vienkāršs
#  (meklē atslēgvārdus), lai varētu saprast, KĀ aģents strādā.
#
#  Tavi uzdevumi:
#   5.1  izpildit_soli()      – aģents izsauc pareizo rīku
#   5.2  sastadit_atbildi()   – aģents no atmiņas sastāda atbildi
#   5.3  riks_valuta()        – pievieno aģentam jaunu rīku
#   5.4  drošība              – soļu limits un cilvēka apstiprinājums
#
#  Aizpildi vietas ar  # TODO  un palaid failu. ✅ = pareizi.
# =====================================================================
import re

# ---------------------------------------------------------------------
# RĪKI — funkcijas, ko aģents drīkst izsaukt
# ---------------------------------------------------------------------
LAIKAPSTAKLI = {
    "rīga": "rīt lietus, +6 °C",
    "liepāja": "rīt vējains, +8 °C",
    "daugavpils": "rīt saulains, +4 °C",
}

VALUTAS_KURSI = {"usd": 1.08, "gbp": 0.86}   # 1 EUR = ... (izdomāti kursi mācībām)


def riks_laikapstakli(pilseta):
    return LAIKAPSTAKLI.get(pilseta, "nav datu par šo pilsētu")


def riks_kalkulators(izteiksme):
    # Drošība: atļaujam tikai ciparus, punktu, atstarpes un + - * / ( )
    if not re.fullmatch(r"[\d\.\s\+\-\*/\(\)]+", izteiksme):
        return "kļūda: neatļauti simboli"
    return round(eval(izteiksme, {"__builtins__": {}}), 2)


# ---------------------------------------------------------------------
# 5.3 Jauns rīks: valūtas konvertētājs
# ---------------------------------------------------------------------
# Ievade ir pāris (summa, valuta), piemēram (10.0, "usd").
# 1) summa, valuta = summa_un_valuta
# 2) kurss = VALUTAS_KURSI.get(valuta)   -> ja None, atgriez "nezināma valūta"
# 3) atgriez tekstu:  f"{summa} EUR = {round(summa * kurss, 2)} {valuta.upper()}"
# 4) NEAIZMIRSTI pievienot rīku vārdnīcā RIKI zemāk ar atslēgu "valūta"!
def riks_valuta(summa_un_valuta):
    summa, valuta = summa_un_valuta
    kurss = VALUTAS_KURSI.get(valuta)
    if kurss is None:
        return "nezināma valūta"
    return f"{summa} EUR = {round(summa * kurss, 2)} {valuta.upper()}"


# Bīstams rīks: e-pasta sūtīšana — vajag cilvēka apstiprinājumu (gatavs)
def riks_sutit_epastu(teksts, apstiprinat):
    if not apstiprinat(f"Sūtīt e-pastu ar tekstu: '{teksts}'?"):
        return "ATCELTS: cilvēks neapstiprināja"
    return "e-pasts nosūtīts (simulācija)"


RIKI = {
    "laikapstākļi": riks_laikapstakli,
    "kalkulators": riks_kalkulators,
    "valūta": riks_valuta,
}


# ---------------------------------------------------------------------
# PLĀNOTĀJS — sadala mērķi soļos (gatavs; izlasi un saproti!)
# ---------------------------------------------------------------------
def planot(merkis):
    m = merkis.lower()
    plans = []
    for pilseta in LAIKAPSTAKLI:
        if pilseta[:-1] in m:                    # "rīg" atrod "Rīgā", "Rīgas"
            plans.append(("laikapstākļi", pilseta))
    for izteiksme in re.findall(r"\d[\d\.\s\+\-\*/\(\)]*\d", m):
        if any(op in izteiksme for op in "+-*/"):
            plans.append(("kalkulators", izteiksme.strip()))
    atrasts = re.search(r"(\d+(?:\.\d+)?)\s*(?:eiro|eur)\w*\s+(?:uz\s+)?(dolār|mārciņ)", m)
    if atrasts:
        valuta = "usd" if atrasts.group(2) == "dolār" else "gbp"
        plans.append(("valūta", (float(atrasts.group(1)), valuta)))
    if "e-past" in m or "epast" in m:
        plans.append(("sūtīt_epastu", "kopsavilkums"))
    return plans


# ---------------------------------------------------------------------
# 5.1 Izpildi vienu soli: atrodi rīku un izsauc to
# ---------------------------------------------------------------------
# 1) Ja riks == "sūtīt_epastu"  -> atgriez riks_sutit_epastu(arguments, apstiprinat)
# 2) Ja riks nav vārdnīcā RIKI   -> atgriez f"kļūda: nav rīka '{riks}'"
# 3) Citādi                      -> atgriez RIKI[riks](arguments)
def izpildit_soli(riks, arguments, apstiprinat=lambda jautajums: False):
    if riks == "sūtīt_epastu":
        return riks_sutit_epastu(arguments, apstiprinat)
    if riks not in RIKI:
        return f"kļūda: nav rīka '{riks}'"
    return RIKI[riks](arguments)


# ---------------------------------------------------------------------
# 5.2 Sastādi galīgo atbildi no atmiņas
# ---------------------------------------------------------------------
# atmina ir saraksts ar tekstiem, piemēram ["laikapstākļi: rīt lietus, +6 °C"]
# 1) Ja atmina ir tukša -> atgriez "Nezinu, kā palīdzēt ar šo mērķi."
# 2) Citādi izveido rindas: "Lūk, ko noskaidroju:" un katram ierakstam " • ..."
# 3) Ja kādā ierakstā ir vārds "lietus" -> pievieno "Ieteikums: paņem lietussargu! ☔"
# 4) Atgriez "\n".join(rindas)
def sastadit_atbildi(atmina):
    if not atmina:
        return "Nezinu, kā palīdzēt ar šo mērķi."
    rindas = ["Lūk, ko noskaidroju:"]
    rindas.extend(f" • {ieraksts}" for ieraksts in atmina)
    if any(re.search(r"\blietus\b", ieraksts, re.IGNORECASE) for ieraksts in atmina):
        rindas.append("Ieteikums: paņem lietussargu! ☔")
    return "\n".join(rindas)


# ---------------------------------------------------------------------
# AĢENTA CIKLS
# ---------------------------------------------------------------------
def agents(merkis, max_soli=5, apstiprinat=lambda jautajums: False, runat=True):
    atmina = []
    plans = planot(merkis)
    if runat:
        print(f"\n🎯 MĒRĶIS: {merkis}")
        print(f"🗺️  PLĀNS: {plans}")
    for nr, (riks, arguments) in enumerate(plans, start=1):
        if nr > max_soli:
            atmina.append("apstājos: sasniegts soļu limits")
            break
        noverojums = izpildit_soli(riks, arguments, apstiprinat)
        if runat:
            print(f"  {nr}. DARBĪBA: {riks}({arguments})  →  NOVĒROJUMS: {noverojums}")
        atmina.append(f"{riks}: {noverojums}")
    atbilde = sastadit_atbildi(atmina)
    if runat:
        print("💬 ATBILDE:\n" + str(atbilde))
    return atbilde, atmina


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
    parbaude("5.1 kalkulators caur izpildit_soli", lambda: izpildit_soli("kalkulators", "3 * 2.50") == 7.5)
    parbaude("5.1 nezināms rīks", lambda: izpildit_soli("lidmašīna", "x").startswith("kļūda"))
    parbaude("5.2 lietus -> lietussargs", lambda: "lietussargu" in sastadit_atbildi(["laikapstākļi: rīt lietus, +6 °C"]))
    parbaude("5.2 tukša atmiņa", lambda: sastadit_atbildi([]).startswith("Nezinu"))
    parbaude("5.3 valūtas rīks", lambda: izpildit_soli("valūta", (10.0, "usd")) == "10.0 EUR = 10.8 USD")
    parbaude("5.4 e-pasts bez apstiprinājuma tiek atcelts",
             lambda: izpildit_soli("sūtīt_epastu", "x", apstiprinat=lambda j: False).startswith("ATCELTS"))
    parbaude("5.4 soļu limits", lambda: "limits" in agents("Rīgā, Liepājā, Daugavpilī 1+1", max_soli=2, runat=False)[0])
    parbaude("5.4 kalkulators bloķē bīstamu kodu", lambda: riks_kalkulators("__import__('os')").startswith("kļūda"))

    print("\n" + "=" * 60)
    agents("Vai rīt Rīgā vajadzēs lietussargu? Un cik maksās 3 * 2.50 eiro biļetes?")
    agents("Kādi laikapstākļi rīt Liepājā? Cik ir 25 eiro uz dolāriem?")
    agents("Uzzini laiku Daugavpilī un nosūti e-pastu kolēģim.",
           apstiprinat=lambda jautajums: input(f"🙋 {jautajums} (j/n): ").strip().lower() == "j")

# ---------------------------------------------------------------------
# JAUTĀJUMI PĀRDOMĀM:
#  a) Uzraksti savu mērķi (piem., par Daugavpili un 2 * 4.20). Vai aģents
#     to saprot? Kad plānotājs "neredz" uzdevumu?
#  b) Kāpēc kalkulators pārbauda simbolus pirms eval()? Kas notiktu bez tā?
#  c) Kuras darbības īstā dzīvē VIENMĒR prasītu cilvēka apstiprinājumu?
# ---------------------------------------------------------------------
