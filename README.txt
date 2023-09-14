Några rader python-kod genererar en QR-kod baserat på information i en config-fil och en bild i jpg- eller png-format.
För att på enklaste sätt köra python-koden har jag kompilerat ihop en 'executable'. Det ska bara vara att ställa in config-filen och lägga en logga i samma katalog som skriptet och sedan dubbelklicka skriptet.

 
Skriptet läser alltså in inställningar från en json-fil som måste ligga i samma katalog som skriptet genQR_code.

Filen ska heta config.json
Json-filen ska innehålla nycklarna "url" och "logo".
Json är lite petigt med mellanslag, citationstecken och dylikt.
Om det krånglar, öppna config.json i en textredigerare (notepad), ta bort allt innehåll och kopiera in exemplet nedan.

{
  "url": "www.klockren.nu",
  "logo": "logga.jpg",
  "project": "my_project"
}

"Project" kan vara en tom sträng, så här: "project": ""

Under nyckeln "logo" anges filnamnet på den logga som ska hamna mitt i QR-koden. Skriptet kommer att generara en QR-kod med och en utan logga. En QR-kod utan logga är lättare att läsa, mindre risk för att läsningen kommer att misslyckas.


Om det av någon anledning slutar att fungera i framtiden kan ni antingen använda en gratistjänst på nätet eller ge er på python-koden själva eller med hjälp av IT-firma eller en driftig ungdom kanske. Med informationen nedan löser ni det!
För att komma till en exekverbar fil har jag använt pyinstaller
$> pyinstaller --onefile --distpath ../executable --workpath ../tmp genQR_code.py 
