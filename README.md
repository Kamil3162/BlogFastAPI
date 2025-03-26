# Backend API

## Struktura projektu
```
├── .github/workflows/      # Pliki konfiguracyjne dla GitHub Actions
├── .idea/                  # Konfiguracja IDE
├── alembic/                # Migracje bazy danych
├── app/                    # Kod źródłowy aplikacji
│   └── s3 storage for post images
├── tests/                  # Testy napisane przy użyciu pytest
├── .gitignore              # Lista ignorowanych plików przez Git
├── Dockerfile              # Konfiguracja kontenera Docker
├── README.md               # Ten plik
├── __init__.py             # Inicjalizacja pakietu Python
├── alembic.ini             # Konfiguracja Alembic do migracji DB
├── docker-compose.yml      # Konfiguracja usług (aplikacja, baza danych, itp.)
├── entrypoint.sh           # Skrypt startowy dla kontenera
└── requirements.txt        # Lista wymaganych pakietów Pythona
```

## Funkcjonalności
- Backend API z obsługą bazy danych
- Integracja z pamięcią S3 dla przechowywania obrazków postów
- System migracji bazy danych (Alembic)
- Testy z wykorzystaniem pytest
- Dockeryzacja całego środowiska

## Wymagania
- Python
- Docker i Docker Compose
- Git

## Instalacja i uruchomienie

### Uruchomienie z Dockerem
Cały projekt wraz z bazą danych można uruchomić za pomocą Dockera:

```bash
# Klonowanie repozytorium
git clone https://github.com/Kamil3162/BlogFastAPI.git
cd BlogFastAPI

# Budowanie i uruchamianie kontenerów
docker-compose up -d
```

Aplikacja zostanie automatycznie uruchomiona wraz z bazą danych dzięki skryptowi `entrypoint.sh`.

## Testy
Projekt wykorzystuje pytest do testów:

```bash
pytest
```

## CI/CD Pipeline

Projekt wykorzystuje GitHub Actions do automatyzacji procesów CI/CD. Workflow jest skonfigurowany w katalogu `.github/workflows/`.

### Główne etapy pipeline'u:

1. **Build** - budowanie obrazu Docker
2. **Test** - uruchamianie testów pytest
3. **Deploy** - wdrażanie aplikacji

