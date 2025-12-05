# Pomodoro Tanulást Segítő Alkalmazás
## Projektlabor I. – Suba-Kiss Beáta – 2025

## Projekt leírása

A Pomodoro tanulási technika egy fókusznövelő módszer, amely rövid, intenzív tanulási szakaszokra és rendszeres szünetekre bontja a tanulást. 25 perc tanulást 5 perc szünet követ, ez ismétlődik négyszer, majd következik egy hosszabb, 15 perces szünet. A módszer segít növelni a koncentrációt, és csökkenti a túlterheltséget.

Ez az alkalmazás egy **asztali Pomodoro időzítő**, amelyet felsős, leginkább 8. osztályos tanulók számára készítettem, hogy könnyebben be tudják osztani a tanulási idejüket, és visszajelzést kapjanak arról, melyik tantárgyra mennyi időt fordítottak.

A nap végén (amikor végzett a tanulással) CSV fájlba exportálhatja a statisztikát, amely excel-ben is megnyitható. 

A program teljes egészében **Python nyelven, TOGA GUI keretrendszerrel** készült.

## A projekt célja

 - működő, platformfüggetlen GUI alkalmazás készüljön Pythonban
 - helyesen kezelje az időzítést, felhasználói interakciókat
 - fájlkezeléssel naplót vezessen (JSON)
 - exportálja az adatokat megfelelő formátumban (CSV)
 - felhasználóbarát, átlátható kezelőfelületet biztosítson
 - gyerekbarát, egyszerű szövegekkel támogassa a használatot

## Az alkalmazás működése

A program elindítása után a felhasználó:

 1. Tantárgy kiválasztása

    A lenyíló menüből kiválasztható, hogy éppen melyik tantárgyból indul a tanulási egyperces blokk.

 2. Tanulási idő visszaszámlálása

     - 1 perc tanulás (teszt mód)
     - automatikusan követi 5 másodperc szünet
     - minden 4. blokk után hosszabb szünet indul
     - a kijelző színe vált:
        tanulás → fekete
        rövid szünet → zöld
        hosszú szünet → kék

 3. Tanulási idő lejárása
 
    Az alkalmazás a tanulási szakasz végén értesítést küld (felugró ablak + hangjelzés). 
    A szünet automatikusan elindul, lejártáról szintén értesítés érkezik.

 4. Statisztika vezetése (JSON)

    Minden befejezett tanulási blokk mentésre kerül:
     - dátum
     - tantárgy
     - blokkonkénti tanult percek

    A JSON fájl többnapos naplót tartalmaz.

 5. Napi összesítés

    A jobb oldali panelen a mai nap összesített tanulási ideje látható tantárgyanként.

    Automatikusan frissül: minden tantárgyhoz tartozó mai tanulási idő

 6. CSV export

    A „Statisztika mentése” gombra kattintva:
     - a napló összesített formában kerül kiírásra
     - ha egy tantárgyból többször is tanult valaki, a program automatikusan összeadja
     - ha a CSV meg van nyitva Excelben, a program udvarias hibaüzenetet jelenít meg

 7. Súgó

    Minden funkcióhoz gyermekbarát szövegezésű tájékoztató tartozik.

## Fő funkciók

 1. Időzítő funkciók

    - tanulási idő számolása
    - rövid és hosszú szünetek automatikus váltása
    - a fázisok végén felugró értesítés
    - hosszú szünet minden 4. blokk után

 2. Statisztika panel

    - napi bontású tanult percek megjelenítése
    - tantárgyankénti összesítés
    - automatikus frissítés minden blokk után
    - váltakozó sorszínezés a könnyebb olvashatóságért

 3. Mentési funkciók

    - napló mentése JSON formátumban
    - CSV export (összevont napi adatok: Dátum – Tantárgy – Összes perc)
    - Excelben megnyitható formátum
    - védelem: ha a CSV meg van nyitva, hibaüzenet figyelmeztet rá

## Használt technológiák

 - Python 3.12+
 - Toga GUI (BeeWare projekt)
 - JSON fájlkezelés
 - CSV export UTF-8 kódolással

## Telepítés és futtatás

 1. Python telepítése (3.10+ ajánlott)

 2. Toga telepítése: pip install toga

 3. Az alkalmazás futtatása: python main.py

A program Windows / macOS / Linux rendszeren is működik.

## Fájlok rövid leírása

 1. main.py
    A teljes alkalmazás forráskódja.
    Tartalmazza:

     - a GUI elemeket
     - az időzítő logikát
     - a statisztika frissítését
     - a JSON/CSV mentést
     - a menük és párbeszédablakok működését

 2. pomodoro_session_log.json
    A tanulási blokkok részletes naplója (minden egyes blokk külön sorban).

 3. Pomodoro_teljes_naplo.csv
    CSV export: dátum + tantárgy szerint összegzett tanulási percek.

## Tesztelési eredmények

 - minden gomb megfelelően reagál
 - statisztika automatikusan frissül
 - a CSV fájl jól kezelhető Excelben
 - nyitott fájl esetén működik a hibaüzenet
 - felhasználói élmény letisztult, átlátható

## Személyes reflexió

 Ez a projekt sokat segített abban, hogy jobban megértsem a GUI-fejlesztés alapjait Pythonban, és valós alkalmazást készítsek gyakorlati funkciókkal (mentés, exportálás, időzítő).
 Különösen hasznos volt számomra a fájlkezelés, a komponensek együttműködése és a Toga keretrendszer megismerése.

## Összefoglalás

 A Pomodoro Tanulást Segítő App egy letisztult, könnyen használható asztali alkalmazás, amely támogatja a diákokat abban, hogy hatékonyabban osszák be a tanulási idejüket, és visszajelzést kapjanak a napi teljesítményükről.
 



