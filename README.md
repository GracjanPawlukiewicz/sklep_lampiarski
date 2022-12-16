# LampexPol

Repozytorium zawiera kod źródłowy skryptów pomocnicznych oraz część danych wejściowych i konfiguracyjnych dla fikcyjnego sklepu internetowego z oświetleniem LampexPol.
Projekt realizowany był w ramach przedmiotu Biznes elektroniczny prowadzonego na 3 semetrze niestacjonarnych studiów magisterskich na kierunku Informatyka, na Politechnice Gdańskiej.
Asortyment źródłowy pochodzi z rzeczywistego sklepu:
https://www.skleplampy.pl/.

## Zawartość repozytorium

* `scrapper.py` - skrypt scrappujący zawartość sklepu bazowego do plików JSON z metadanymi produktów oraz pobierający ich zdjęcia
* `images/`, `products_data/` - katalogi zawierające wynik działania skryptu `scrapper.py`
* `backoffice/importmyproduct.php` - skrypt PHP pozwalający na umieszczenie wyników scrappowania w skonfigurowanym sklepie
* `add_attributes.py` - skrypt dodający "atrybuty" tj. warianty produktów do istniejącej bazy danych Prestashop
* `tests/` - testy funkcjonalne witryny wykorzystujące bibliotekę Sellenium
* `requirements.txt` - dependencje dla skryptów Python
* `backup/` - katalog z kopiami zapasowymi bazy danych Prestashop.

Szczegółowe informacje dotyczące wykorzystania każdego z nich znajdują się w komentarzach i dokumentacji wykorzystanych bibliotek.