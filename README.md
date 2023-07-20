# threads-tda
Performing Topological Data Analysis on top of the new [Threads](https://www.threads.net/) platform.

## Docker Container

```bash

docker run -it -e MONGODB_HOST_URL="192.168.86.113" \
    -e MONGODB_HOST_PORT="27017" \
    -e MONGODB_DATABASE="threadsdb" \
    -e MONGODB_USERNAME="user" \
    -e MONGODB_PASSWORD="password" \
    zacharybloss/threads-collection

```

## Argo Workflow via Metaflow

```bash

python src/run_flow.py --with retry argo-workflows create --with kubernetes:cpu=2,memory=1000,namespace=metaflow,image=zacharybloss/threads-collection
```