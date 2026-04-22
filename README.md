# Mini Commander (Python)

Prosta aplikacja do zarządzania plikami inspirowana Midnight Commanderem.  
Projekt został wykonany w Pythonie z wykorzystaniem biblioteki PyQt5.

---

## Opis projektu

Aplikacja umożliwia przeglądanie systemu plików w dwóch panelach oraz wykonywanie podstawowych operacji na plikach i folderach przy użyciu klawiatury.

Program posiada interfejs graficzny stylizowany na klasyczne środowisko DOS.

---

## Funkcjonalności

- Dwupanelowy menedżer plików (lewy i prawy panel)
- Nawigacja po folderach (ENTER, BACKSPACE)
- Kopiowanie plików i folderów (F5)
- Przenoszenie plików i folderów (F6)
- Sortowanie plików według rozszerzeń (F7)
- Edycja reguł sortowania (F8)
- Automatyczne tworzenie folderów docelowych
- Obsługa konfliktów nazw plików (automatyczna zmiana nazwy)
- Zmiana aktywnego panelu (TAB)

---

## Sterowanie

| Klawisz     | Funkcja                     |
|------------|----------------------------|
| TAB        | Zmiana aktywnego panelu    |
| ENTER      | Otwarcie folderu/pliku     |
| BACKSPACE  | Powrót do folderu wyżej    |
| F5         | Kopiowanie                 |
| F6         | Przenoszenie               |
| F7         | Sortowanie plików          |
| F8         | Edycja reguł               |
| DEL        | Usuwanie plików\folderów   |
| F10        | Zamknięcie programu        |

---

## Technologie

- Python 3
- PyQt5
- Biblioteki standardowe:
  - os
  - shutil
  - json

---

## Uruchomienie

1. Zainstaluj wymagane biblioteki:
pip install PyQt5


2. Uruchom aplikację:

python script.py


---

## Konfiguracja

Plik `config.json` zawiera reguły sortowania plików, np.:


{
"Obrazy": [".jpg", ".png"],
"Dokumenty": [".pdf", ".txt"],
"Inne": []
}


Można go edytować ręcznie lub z poziomu aplikacji (F8).

---
Projekt wykonany w celach edukacyjnych.
