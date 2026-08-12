Me:
Chtěl bych popisovat stav softwareového projektu pomocí stromové struktury abstrakce.
Každá kapitola by měla své číslo. Například #1.5.2 je úroveň vnoření 3 a podrobně rozvíjí vyšší abstrakci v kapitole #1.5.
Ta zase je úroveň vnoření 2 a podrobně rozvíjí vyšší abstrakci v kapitole #1.
Měla by platit pravidla:

Nižší kapitola necituje (neopakuje) nic z jí nadřazené, jen to rozvíjí na nižšší úrovni abstrakce (tedy podrobněji)
Pro celý kontext problému staší řetězec dané kapitoly a jí nadřazených.
Při úpravě dokumentu se striktně dodržují (předchozí) pravidla pro vnoření abstrakcí.
Při jakémkoliv pořadavku na úpravu software se kontroluje, zda odpovídá, nebo porušuje tento strukturovaný dokument.
Pokud ho požadavek porušuje, systém navrhne, jak se tento dokument opraví (přitpůsobí). To musí autor požadavku odsouhlasit.
po odsouhlasení provede systém reimplementaci a testování, ale pouze podlo aktuálního definičního dokumentu.
Vyjádři se prosím k tomutu návrhu konceptu, případně ho vylepši.
---
AI: přesná odpověď není důležitá.
---
Me:
Souhlasím s tvým návrhem na orientovaný graf.
Domnívám se, že požadavek na acykličnost není nutný (dvě části projektu spolu souvisí a jedna odkazuje na druhou).
(Nejde o cyklus v algoritmu, ale cyklus v datech).
časové razítko bych řešil prostě tím, že dokument je uchováván (jako jiné části v sotware) v Gitu.
1. Navrhni tvou úplnou a přitom co nejvíce stručnou formulaci pravidel pro a) definiční dokument b) pravidel pro vývoj sowtware s tímto dokumentem.
Použij vše, co je známo jako "state of art" v této oblasti.
2. Navrhni  nejlepší formát pro zápis definičního dokumentu  (grafu). Markdown soubor? Adresářová struktura? Databáze?
Vyber nejlepší řešení.