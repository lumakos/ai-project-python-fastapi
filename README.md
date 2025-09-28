## Run commands

```docker compose run --rm fastapi_app bash```

python --version      # θα δείξει Python 3.13
pip list              # θα δείξει τι έχει εγκατασταθεί
fastapi dev main.py   # μπορείς να τρέξεις manual


## Documentation
https://fastapi.tiangolo.com/tutorial/#run-the-code

## Stack

1. fastAPI
2. PostGres
3. Python 3.13.7
4. SQLAlchemy ORM
5. Alembic

## Κάθε φορα που αλλάζεις τα models 
```
docker compose exec fastapi_app alembic revision --autogenerate -m "init schema"
```

```
docker compose exec fastapi_app alembic upgrade head
```

## Use PostGres DB
```
docker compose exec db psql -U postgres -d postgres
```

```
\dt
```

### docker compose up -d --build
### docker compose down -v