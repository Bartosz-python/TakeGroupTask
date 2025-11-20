# TakeGroupTask - Automatyczne Testy E2E i API

## Instalacja

1. Zainstaluj zależności:

```bash
pip install -r requirements.txt
```

2. Zainstaluj przeglądarki Playwright:

```bash
playwright install
```

## Uruchomienie testów

Wszystkie testy (E2E + API):

```bash
pytest Tests/ -v -n 3
```

Tylko testy E2E:

```bash
pytest Tests/E2E/ -v -n 2
```

Tylko testy API:

```bash
pytest Tests/API/ -v
```
Do każdego testu, jest możliwość zastosowania flagi --browser_name (przeglądarka). Dostępne opcje to chrome, firefox, webkit.

## Wybrana biblioteka - Playwright

Zdecydowałem się na Playwright zamiast Selenium, ponieważ jest szybszy, ma lepsze API do asercji (`expect()`), wsparcie dla kilku przeglądarek jednocześnie i wbudowany debugging z tracingiem (screenshots, snapshots). Playwright jest też bardziej stabilny i mniej podatny na flaky testy.

## Endpoint API

**POST `/pl/search-route`**

Endpoint wyszukiwania filmów na platformie vod.film. Przyjmuje dane wyszukiwania (host, locale, searchTerm) i zwraca listę filmów.

W teście weryfikuję, że endpoint zwraca HTTP 200 i że wyniki zawierają film o tytule "the pickup".

## Założenia i problemy

- Testy działają na produkcji vod.film; jeśli strona się zmieni, testy mogą przestać działać.
- Film "The Pickup" zawsze powinien być dostępny w wyszukiwaniu.
- Strona wyświetla modal RODO przy pierwszym wejściu; dodałem krok, żeby go zaakceptować.
- Selektory są dynamiczne; użyłem `get_by_text()` z regexem na nieczułość wielkości liter zamiast klas CSS.
- Wyszukiwanie jest asynchroniczne; bez `expect().to_be_visible()` testy mogą być niestabilne.

## Raporty błędów

### Błąd #1: "Clear" button lacks functionality in the Sort feature (High priority)

**Summary:**
The "Clear" button in the Sort feature does not reset applied sorting criteria.

**Description:**
When navigating to vod.film and entering the Movies subtab, selecting sorting options and clicking the "Clear" button, the applied criteria are not removed or reset.

**Steps:**

1. Launch the browser.
2. Navigate to https://vod.film/.
3. Go to the Movies subtab.
4. Open the Sort feature.
5. Choose any sorting criteria.
6. Press the "Clear" button.
7. Observe that sorting criteria remain applied.

**Expected Results:**
The "Clear" button should reset all sorting criteria to their default state, and the list should show unfiltered movies.

**Actual Results:**
The "Clear" button has no effect. Applied sorting criteria remain active and movies continue to be filtered.

**Environment:**
Reproduced on Chrome and Firefox on Windows 11 (10.0.26100)

### Błąd #2: "Popularity" criteria stops working with "Oldest/Newest Productions" (Medium priority)

**Summary:**
"Popularity" criteria stops working with "Oldest/Newest Productions" in the Sort Feature

**Description:**
After navigating to various subtabs (Movies, Series, Popular, Genre) and applying either "Oldest Production" or "Newest Production" sorting, clicking the "Popularity" criteria stops working.

**Steps:**

1. Launch the browser.
2. Navigate to https://vod.film/.
3. Go to any of these subtabs: Movies, Series, Popular, or any Genre subtab.
4. Open the Sort feature.
5. Choose either "Oldest Production" or "Newest Production".
6. Click the "Popularity" criteria.
7. Observe that "Popularity" criteria stops working.

**Expected Results:**
All sorting criteria should work independently or in combination. Selecting "Popularity" should filter and sort movies by popularity regardless of other applied criteria.

**Actual Results:**
"Popularity" criteria stops working while either "Oldest Productions" or "Newest Productions" 
sorting criteria are applied.

**Environment:**
Reproduced on Chrome and Firefox on Windows 11 (10.0.26100)

## Bonus: Docker

**dockerfile:**

```dockerfile
FROM python:3.11-slim
RUN apt-get update && apt-get install -y \
    wget \
    gnupg \
    ca-certificates \
    && rm -rf /var/lib/apt/lists/*
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
RUN playwright install --with-deps chromium firefox webkit
COPY . .
RUN mkdir -p test-reports traces
CMD ["pytest", "--html=test-reports/test_report.html", "--self-contained-html"]
```
Uruchomienie dockerfile:
```
docker build -t "nazwa-dowolna" .
docker run "wyżej wpisana nazwa"
```
**docker-compose.yml:**

```yaml
version: '3.8'
services:
  playwright-tests:
    build:
      context: .
      dockerfile: dockerfile
    volumes:
      - ./test-reports:/app/test-reports
      - ./traces:/app/traces
      - ./Tests:/app/Tests
    environment:
      - PYTHONUNBUFFERED=1
    command: >
      pytest
      --html=test-reports/report.html
      --self-contained-html
      --browser_name=chrome
      -v
```
Uruchomienie docker-compose.yml:

```bash
docker-compose up --build
```

## Bonus: CI/CD - GitHub Actions

Plik `.github/workflows/main.yml`:

```yaml
name: Tests
on: [push, pull_request]
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-python@v4
        with:
          python-version: "3.11"
      - run: pip install -r requirements.txt
      - run: playwright install
      - run: pytest Tests/ -v
```

## Bonus: SQL - Weryfikacja relacji filmu z kategorią

Sprawdzenie, że film "The Pickup" jest przypisany do kategorii:

```sql
SELECT m.title, c.name
FROM movies m
INNER JOIN movie_categories mc ON m.id = mc.movie_id
INNER JOIN categories c ON mc.category_id = c.id
WHERE LOWER(m.title) LIKE '%the pickup%';
```

To zapytanie łączy tabelę filmów (`movies`), tabelę pośrednią (`movie_categories`) i tabelę kategorii (`categories`). Zwraca tytuł filmu oraz nazwę kategorii, do której jest przypisany. Dzięki `INNER JOIN` otrzymujemy tylko filmy, które mają przypisane kategorie.
