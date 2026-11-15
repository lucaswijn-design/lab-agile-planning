# Ontwerpbriefing voor clubhuis-ontwerpen (16 november 2026)

Lees dit helemaal voordat je een ontwerp maakt of verbetert. Alles staat in `/home/user/lab-agile-planning/business-case/panden/`.

## Het concept
Een coöperatieve ledenclub: boekencafé met keuken, coworking (zit-sta bureaus 140 x 70, grote tafel, raambar), vergaderkamers, belcellen,
focuskamers, een functionele gym (afsluitbaar, eigen ingang waar mogelijk), twee sanitairtorens (was en douche), lockers, veel planten.
Stijl: Berlijn/Taghazout, rauw industrieel, sober verbouwd met hergebruikte materialen, strakke vloer en strakke bureaus.
Kleuren per zone komen uit `PALET`/`ZONEPALET` in ontwerp.py (café pistache, bieb avocado, werken en vergaderen rotskust, gym granaatappel, entree kokos, sanitair beton).

## Normen (inrichting/programma.py, capaciteit.py)
- Werkplekken uit capaciteit.vraag(); bureaus + grote tafel (pers) + raambar (w/0,6) tellen.
- Belcellen 1 per 8 werkers op de piek; focuskamers (1 tot 2 personen) 1 per 25 werkers; vergaderkamers uit vergaderuren (circa 1 per 27 uur/week).
- Vergaderkamers: standaard voor 6 (vergaderkamer(..., pers=6)), plus een sta-kamer voor 4 tot 6 (stavergaderkamer()), kamer voor 8 alleen als het echt nodig is.
- Lounge: 25% van de werkers + 4 zachte plekken (veelhoekbank, zitnis, fauteuils, houten zittrap telt mee).
- Lockers: vaste locker per eigenaar + 2x gymsporters op de piek + 10 (16 lockers per meter lockerwand).
- Planten: richtwaarde 1 per 20 m2 en 1 boom per 60 m2; hangplanten en planten op lockers tellen mee; kies soort naar licht.
- Geluid: gym nooit naast werkplekken zonder buffer (torens, toiletgroep, techniek of 6 m afstand) en altijd een dichte wand tot het dak (wand(..., gym=True)) met deur op toegangspas (deur(..., toegang=True)).
- Geluidsvolgorde: entree, café en spel, gym, lounge, werken, stilte en focus.
- Daglicht: bureaus 1,5 tot 3 m van glas, scherm haaks op het raam; café en grote planten aan glas of onder lichtstraat; belcellen, toiletten, lockers in donkere kern.
- Looppaden minimaal 1,1 m; 0,9 m achter elke stoel.
- Geen panden met woningen in hetzelfde gebouw (gym).

## Coördinaten
Lokaal assenstelsel (u, v) in meters uit geo.frame(footprint): u langs de lange as, v haaks erop, rechtshandig zoals oost/noord. De plattegrond
(tekening.py) tekent v omhoog. Bekijk eerst het dossier: `dossiers/<slug>.json` (footprint, context, hoogte) en de luchtfoto
(render_pakket.luchtfoto(slug, dict(hoogte=6, extra=[]), uitpad) met env SCRATCH gezet) om straatkant, buren en daglicht te bepalen.
Lokale footprint: `python3 -c "import json,geo;d=json.load(open('dossiers/S.json'));F=geo.frame(d['footprint']);print([[round(x,1) for x in geo.to_local(q,F)] for q in d['footprint']])"`
Noordrichting in het lokale stelsel: zie tekening.basis(slug)[2] (graden vanaf +u).
Is het pand een unit in een groter complex: snijd de unit uit (zie dossiers/rotterdam-galvanistraat-122.json en -linschotenstraat-20a.json: footprint vervangen,
footprint_complex bewaard, rest als context) en documenteer hoe in 'opmerking'.

## Bouwstenen (ontwerp.py, sectie "Bouwstenen v3" en v2)
zone(naam, type, poly, beschrijving, details, foto=None, prompt="", n=0, cam=dict(t=[u,v], afstand, hoek), palet=None); R(u0,v0,u1,v1)
eiland2(c, a, n=0, k=4|6)  grote_tafel(c, lengte, a, n)  keuken(c, lengte, a, n)  kookeiland(c, a, n)  vergaderkamer(c, w, d, a, pers, n)
stavergaderkamer(c, w, d, a, pers, n)  focuskamer(c, a, n)  pod2(c, n)  lockerwand(c, w, a, n)  achthoektoren(c, R, open_deg, "was"|"douche", n, lockers=(zijdes))
dtoren(p0, p1, diep, "was"|"douche", n)  veelhoekbank(c, R, zijden, open=(..), draai, kleur, haard, n)  zitnis(p0, p1, tafels, kleur, n)
groenwand(p0, p1, h, rots, n)  plant3(c, soort, n, z)  boom3(c, soort, n)  hangplant(c, z, n)  pingpong(c, a, n)  pooltafel(c, a, n)
kasten(u0, u1, v, a, d, h, n)  rack(c, a, n)  roeier(c, a, n)  wand(pts, h, glas, gym, bestaand, n)  deur(c, a, toegang, n, w)  label(c, tekst, n)
dict(t="box", soort="raambar", c, w, d=0.5, h=1.05, a, kleur=HOUT, n)  dict(t="box", soort="trap", c, w, d, h=0.3, a=0, kleur=HOUT (zittrap) of STAAL, n) (trap stijgt altijd naar +v tot 3,6 m)
dict(t="box", soort="toiletgroep", c, w, d, h=2.6, a, kleur="#bdb7aa")  dict(t="kleed", c, w, d, a, kleur)
Plantsoorten (PLANTEN in ontwerp.py): kentia (laag licht), ficus elastica, strelitzia nicolai (hoog licht), monstera, zz-plant, sansevieria, dracaena, schefflera, aspidistra, philodendron; hangplant = pothos.
Let op richting: groenwand en zitnis zitten links van p0 -> p1; achthoektoren-zijde k ligt op hoek open_deg + 45k.

## Een ontwerp toevoegen (nieuw pand)
1. Dossier: `python3 -c "import fetch; fetch.haal('<slug>', '<adres> <plaats>', '<regio>', '<aanbod met prijs, m2, bron, datum>')"` (pas fetch.py niet aan).
   Controleer in de BAG-vbo's in het dossier dat er geen woonfunctie in het pand zit.
2. Ontwerp in `ontwerpen_extra/<slug>.py` (wordt in ontwerp.py geëxecuteerd, alle helpers beschikbaar): definieer een dict zoals
   GALVANI of LINSCHOTEN in ontwerp.py (titel, sub, hoogte, niveaus, pui_h, concept, geluid, pui, zones, buiten, elementen, dak, renders)
   en doe `ONTWERPEN.update({"<slug>": X}); LABELS.update({...}); VIDES.update({...})` indien nodig.
3. Financiën in `layout_extra/<slug>.py`: `LAYOUTS.update({"<slug>": dict(titel, oordeel, samenvatting, koop=dict(totaal=..., label=...), verhuur=[],
   leden=dict(n_vol, n_deel, n_club), bouwjaar_risico, isoleren, pv_kwp, verdieping_m2, zones=[dict(type, naam, r=(u0,v0,u1,v1))...], pui=dict(kant="v0"|"v1", u0, u1, v) of dict(kant="u0"|"u1", v0, v1, u),
   buiten=[dict(type="terras"|"tuin", naam, r)], bomen_buiten=[...], extra_rows=[...], opex_extra=[(naam, bedrag)])})` (zie layout.py voor voorbeelden, ronde 7 en 8).
   Een tussenvloer: zone met tussenvloer=True in het ontwerp (kost € 650/m2 via ontwerp.inbouw_rows) en verdieping_m2 in de layout.
4. Controleer:
   `python3 ontwerp.py && python3 tekening.py && python3 build_ontwerpen.py | grep <slug>`
   `python3 -c "import capaciteit as c; print(c.max_leden('<slug>', 0.5, 30))"`  en  `python3 inrichting/programma.py`
   Plattegrond bekijken: `cd /tmp && node /home/user/lab-agile-planning/business-case/panden/render_svg.js /home/user/lab-agile-planning/business-case/panden/ontwerp/<slug>-n0.svg <uit>.png 1400` en de png lezen.
   Kijk naar overlap, looppaden, botsingen met wanden, en of alle normen gehaald worden. Verbeter en herhaal (minimaal twee rondes).
5. Leden: kies n_vol/n_deel/n_club zo dat capaciteit.max_leden het aankan en het verzorgingsgebied (ronde7/8/9 META leden_breed) minstens 1,2x zo groot is.

## Kosten
pand_case.run(slug, torens=True, sober=True) en pand_case.fee_inleg_terug(...) geven alles in, om te draaien en inleg terug. Alles sober (hergebruikte materialen).

## Taal
Teksten in het Nederlands, geen gedachtestreepjes als leesteken. Prompts in het Engels (zie bestaande zones), beschrijf de achthoekige torens, hergebruikte materialen, strakke vloer.
