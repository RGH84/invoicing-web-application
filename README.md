# invoicing-web-application

### Alkuperäinen ajatus:

Tarkoitus oli luoda yksinkertainen web-pohjainen laskutussovellus. Käyttäjä voi sovelluksella pitää yllä mm. asiakasrekisteriä, tuoterekisteriä ja luoda/arkistoida pdf- laskuja. Käyttäjä voi myös lähettää viestejä sovelluksessa kehittäjälle. Käyttäjä voi pitää yllä muistilistaa, mitä pitää muistaa laskuttaa ym. 

Sovelluksen ominaisuuksia tulee olemaan ainakin seuraavat:

* Käyttäjärekisteri.
* Käyttäjä voi kirjautua sisään ja ulos sekä luoda uuden tunnuksen.
* Kirjauduttuaan sisään käyttäjä näkee etusivulla käytettävissä olevat toiminnot, joita ovat:
  - Luo uusi asiakas
  - Luo uusi tuote
  - Luo uusi lasku
  - Asiakasrekisteri
  - Tuoterekisteri
  - Laskuarkisto
  - Muistilista
  - Lähetä viesti kehittäjälle

Ominaisuudet voivat vielä hivenen elää kurssin aikana. Esim. verkkolaskujen sisään luku ja lähetys, olisivat hyviä ominaisuuksia, mutta voi olla, että aika ja taidot ei riitä niiden toteuttamiseen tämän kurssin aikana. Ohjelmointitaso ei ole itselleni kurssin esitietovaatimuksia korkeampi ja kaikkea joutuu niistäkin kertaamaan. Ohjelmaa on tarkoitus jatkokehittää kurssin jälkeen omalla ajalla ja ottaa mahdollisesti tulevaisuudessa oman pienyrityksen käyttöön. 

## Välipalautus 2:
Sovellusta voi testata tuotannossa fly.io:n kautta osoitteessa https://invoicing-web-application.fly.dev/ 

Käyttäjä voi tällä hetkellä luoda tunnuksen ja kirjautua sisään, luoda asiakkaita ja tuotteita, katsella omia asiakkaitaan ja tuotteitaan rekistereistä sekä poistaa omia asiakkaita/tuotteita. Muut toiminnot ovat vielä kesken.

Ulkoasuun ja teksteihin ei sen kummemmin ole vielä tässä vaiheessa panostettu. 

Seuraavaksi alan työstämään laskun luontia ja laskuarkistoa. Se taitaakin olla tämän sovelluksen haastavin osuus.

## Välipalautus 3:
Sovelluksessa voi välipalautus 2 ominaisuuksien lisäksi luoda uuden laskun ja tarkastella laskuja laskuarkistosta. Lasku ominaisuudet ovat vasta ensimmäisiä versioita. 

Lisäksi ohjelman ulkoasua on hivenen paranneltu, mutta siihen ei kuitenkaan vielä ole hirveästi panostettu.

Ohjelmaan on myös lisätty JavaScript tarkastukset syötteille rekisteröinnin, sisäänkirjautumisen ja laskujen tarkastelun yhteydessä. Muille tapahtumille tarkastukset tullaan lisäämään lopulliseen versioon .

Muut toiminnot ovat vielä kesken ja lisää ominaisuuksia ja entisten parannuksia tulee lopulliseen versioon.

Sovellusta voi edelleen testata tuotannossa fly.io:n kautta osoitteessa https://invoicing-web-application.fly.dev/ .

## Lopullinen palautus:
Lopulliseen palautukseen tuli isoimpina muutoksina CSRF-haavoittuvuuden korjaus, ulkoasu on toteutettu CSS:llä, lisätty mahdollisuus poistaa lasku, to do listiin voi lisätä omia muistiinpanoja ja viesti osiossa voi keskustella sovelluksen muiden käyttäjien kanssa ja poistaa viestejä tarpeen mukaan. Sivustoille on lisätty myös JavaScript tarkistukset ja korjailtu myös tarkistuksia, jos JavaScript on pois päältä. Sivustoilla kehotetaan pitämään JavaScript päällä, jotta käyttökokemus olisi parempi.

Sivustoilla lukee, että sivustot ovat kehitteillä. Sovellusta on tarkoitus jatkokehittää omalla ajalla, kunhan kokemusta tulee ohjelmoinnista lisää ja aikaa on. Esim. sovelluksen lasku ominaisuudet ovat tällä hetkellä hyvin alkeellisia.  

Sovellusta voi edelleen testata tuotannossa Fly.io:n kautta osoitteessa https://invoicing-web-application.fly.dev/ . 

Fly:lta on tullut ainakin yhden kerran sähköpostia, että sovellus on kaatunut muistin vähyyden vuoksi ja tarjoaa maksullista lisämuistia. Sitä en tässä vaiheessa ala ostamaan, joten jos sovellus on jostain syystä alhaalla, niin voitte käynnistää sovelluksen myös paikallisesti kurssimateriaalin ohjeiden mukaisesti. 

## Tilannepäivitys:
Sovellus ei ole enää testattavissa Fly.io:n kautta. Sovellusta ei ole kehitetty eteenpäin. 






