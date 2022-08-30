```
chmod +x ./init.sh
```

```
chmod +x ./src/services/database/run_db.sh
```

```
docker-compose -f docker-compose.yaml -f docker-compose.local.yaml up --build
```