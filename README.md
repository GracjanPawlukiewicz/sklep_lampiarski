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

## Uruchomenie

### Docker (lokalnie)

Uruchomienie bazy danych (przywrócona baza danych zostanie nadpisana przez instalator):
```
docker network create prestashop-net
docker run -ti --name mysql --network prestashop-net -e MYSQL_ROOT_PASSWORD=student -p 3307:3306 -d mysql:5.7
./init_db.sh createonly
```

Uruchomienie sklepu:
```
docker compose up -d
```

Budowanie obrazu Prestashop:
```
docker build . -t docker.io/mduchalski/lumos
```

Aktualizacja obrazu w registry:
```
docker push docker.io/mduchalski/lumos
```

Inicjalizacja bazy danych (**po uruchomieniu sklepu** - dostępność przez [localhost:8080](http://localhost:8080)):
```
./init_db.sh
```

Dostęp do panelu administracyjnego:
* Adres - [localhost:8080/admin1](http://localhost:8080/admin1)
* Credentials - jan.kowalski@lampexpol.pl:biznes123

Cleanup:
```
docker kill mysql
docker rm mysql
docker compose kill
docker compose rm -vf
```

Szybki rerun - bez restartu MySQL:
```
docker compose kill
docker compose rm -vf
./init_db.sh createonly
docker compose up -d
```
