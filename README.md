### Deployment

https://slmdummyversion-production-3402.up.railway.app/



### Local host guide 

```
# Add Visual Studio Code (code)
export PATH="$PATH:/Applications/Visual Studio Code.app/Contents/Resources/app/bin"
# Add Docker Desktop for Mac (docker)
export PATH="$PATH:/Applications/Docker.app/Contents/Resources/bin/"
```

### Create migrations 

`export POSTGRES_URL=postgresql://slm_user:slm@127.0.0.1:5432/slm-db`

`alembic revision --autogenerate -m "migration_message"`

`make db-migrate`