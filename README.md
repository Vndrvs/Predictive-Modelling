# GDE Projekt feladat - Mesterséges intelligencia alapú fejlesztés tárgy

##Feladat bevezető, áttekintés
Az elemzés a Központi Statisztikai Hivatal nyilvánosan elérhető adatain alapul. A feladat célja, a
közlekedési balesetek alakulásának elemzése, valamint az alkoholos befolyásoltság és egyéb tényezők
közötti összefüggések trendek feldolgozása és vizualizálása.
Az elemzés során több különböző adatforrás került felhasználásra, amelyek a következő mutatókat
tartalmazzák:
- regisztrált személygépkocsik száma
- összes közúti baleset száma
- ittas vezetők által okozott balesetek száma
- alkoholfüggő sofőrök közelítőleges / becsült száma
Az adatok kombinálása lehetővé teszi, a közlekedési balesetek és az alkoholfogyasztással összefüggő
tényezők közötti kapcsolatok vizsgálatát.

##A projekt munkafolyamat alapvető felépítés igénye

###Adattisztítás és adatintegráció
Az esetlegesen, nem 1 az 1 adatformák közös formára hozatala, a feldolgozáshoz.
Jellemzőmérnökség (trend, késleltetési változók, normalizálás)
Az elemzés során új változók kerültek kialakításra, például trendmutatók, késleltetett változók
(lag variables) és normalizált értékek. Ezek nélkül nem lehetséges, a hatékony – koherens
feldolgozás.

###Exploratory Data Analysis
Az adatok vizsgálata során statisztikai és vizuális megoldásokat alkalmaztunk a mintázatok, trendek
azonosítására.

###Strukturális töréselemzés
Az elemzés központi eleme, a 2008-ban bevezetett közlekedésbiztonsági szabályozás. Köznyelven, zéró
tolerancia elve.

###Lineáris regressziós modellezés
A projekt során lineáris regressziós modellek kerülnek alkalmazásra annak érdekében, hogy
feltárható legyen a különböző változók közötti kapcsolat


##Analízis iránya - Fő kérdése
A témában rendelkezésünkre álló nyilvános adatok feldolgozása és értelmezése. Valamint ezen
állományból alkotott információ megjelenítésé, vizualizálása.
A központi kérdéskör, melykörül mozog a projekt:
Hozzájárult-e, a 2008-ban bevezetett zéró tolerancia szabályozás az alkoholhoz köthető közúti
balesetek számának csökkentéséhez

##Módszertan
A feladatmegoldáshoz, az irányadó megközelítési technika a CRISP-DM módszertan.
Normalizálás:
A baleseteket 100 000 járműre skálázzák, hogy figyelembe vegyék a növekvő autópopulációt. Így, a
hónapok-évek alatt keletkező további adatok is hatékonyan feldolgozhatók és kimutatható standard
számok, trendek állapíthatók meg.
Késleltetett hatás vizsgálata:
Az alkoholfüggőség becsült értékeit egyéves késleltetéssel vettük figyelembe. Számba venni ildomos,
hogy a társadalom, a változáshoz való hozzáállása klasszikusan lassan mozdul. Ez kiváltképp igaz, a
magyar társadalomra.
Politikai tényező:
A 2008-ban bevezetett zéró tolerancia szabályozás hatásának vizsgálatához, egy bináris változó
került bevezetésre. Ez a változó megkülönbözteti, a 2008 előtti és a 2008 utáni időszakot, lehetővé
téve a szabályozás potenciális hatásának statisztikai vizsgálatát.
Modellezési megközelítés
Az elemzés során többszörös lineáris regressziós modellt alkalmaztunk. Ennek az oka, hogy az
analízis komplexitása ne legyen végtelen, de az általa megmutatott eredmény jól értelmezhető legyen.

 

##Eredmények összefoglalása
A projekt keretein belül lefutatott elemzés több markánsan azonosítható tendenciát mutatnak a
közúti balesetek alakulásával kapcsolatban.
2008 után egyértelmű csökkenő tendencia figyelhető meg a közúti balesetek számában.
Ez az időszak egybeesik a zéró tolerancia szabályozás bevezetésével.
A zéró tolerancia bevezetése strukturális törésként jelenik meg az adatsorban, Ez rámutat, hogy a
szabályozás jelentős hatással volt a baleseti trendek alakulására
A regressziós modellek eredményei alapján a szakpolitikai intézkedések hatása erősebbnek
mutatkozik, mint az alkoholfüggőségi mutatók hosszabb távú trendjei.
Az elemzés kimutatja, hogy a járműállomány növekedése önmagában nem magyarázza a megfigyelt
változásokat. A forgalomban lévő járművek száma növekszik, ennek ellenére a balesetek száma
csökken. Ehhez feltétlen hozzá kell tenni, hogy nem pusztán, a zéró szabályozás eredménye, hanem a
fejlettebb/fiatalabb gépjárművek műszaki tartalma is közrejátszik elég erősen vélhetően.

##Forrás:
Személysérüléses közúti közlekedési balesetek az okozók szerint:
 https://www.ksh.hu/stadat_files/ege/hu/ege0064.html
A személygépkocsi-állomány gyártmány és üzemanyag-felhasználás szerint: 
https://www.ksh.hu/stadat_files/sza/hu/sza0025.html
Ittasan okozott személysérüléses közúti közlekedési balesetek: 
https://www.ksh.hu/stadat_files/ege/hu/ege0066.html
Az alkoholisták gondozása:
 https://www.ksh.hu/stadat_files/ege/hu/ege0030.html
Alkohol okozta mentális és viselkedészavar miatt egészségügyi járóbeteg szakellátásban részesülők: 
https://www.ksh.hu/stadat_files/ege/hu/ege0085.html

Github:
https://github.com/Vndrvs/Predictive-Modelling/
 

##Feladatkörök megosztása
Kovács Dániel (KN5YJF): Projektmenedzsment, projekt dokumentáció elkészítése
Kocsis Attila (KIHD0W): Témamegjelölés, eredmények utólagos áttekintése, konklúziók helyességének
értékelése
Radácsi András (T798N6): Adatelemzés, prediktív modell programozás
Kocsis Krisztián (TSW9K9): Videó összeállítása és vágása

Készült: 2025/2026 2 - Tavaszi félév
