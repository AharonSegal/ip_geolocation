Given this compose:

```yaml
services:
  redis:
    build:
      context: ..
      dockerfile: Dockerfile.redis
    container_name: redis
    ports:
      - "6379:6379"
    restart: unless-stopped

  server-b:
    build:
      context: ..
      dockerfile: Dockerfile.server_b
    container_name: server-b
    depends_on:
      - redis
    ports:
      - "8000:8000"
    restart: unless-stopped

  server-a:
    build:
      context: ..
      dockerfile: Dockerfile.server_a
    container_name: server-a
    depends_on:
      - server-b
    ports:
      - "8080:8000"
    restart: unless-stopped
```

here’s the **step‑by‑step flow** to turn it into K8s YAMLs.

---

## Step 1 – Build images (compose `build:` → docker image)

Kubernetes **does not** build from `build.context` / `dockerfile`. You must:

1. Build images from your Dockerfiles.
2. Either:
   - Push them to a registry (Docker Hub, GHCR, etc.), **or**
   - Build them directly into Minikube’s Docker daemon (`eval $(minikube docker-env)`).

For your case (from project root):

```bash
# If using Minikube's docker-env, these will be visible in the cluster
docker build -f Dockerfile.redis    -t redis-local:latest   .
docker build -f Dockerfile.server_b -t server-b:latest      .
docker build -f Dockerfile.server_a -t server-a:latest      .
```

You’ll then reference `redis-local:latest`, `server-b:latest`, `server-a:latest` in your K8s manifests.

---

## Step 2 – Decide which ports need to be internal vs external

From compose:

- `redis`:
  - `ports: "6379:6379"` – you exposed Redis to host for dev.
  - In K8s: likely only **internal** (ClusterIP).
- `server-b`:
  - `ports: "8000:8000"` – internal service for other services.
  - In K8s: **internal** (ClusterIP).
- `server-a`:
  - `ports: "8080:8000"` – external entrypoint for clients.
  - In K8s: **external** via NodePort or Ingress.

So mapping:

- `redis` → `Service type: ClusterIP, port 6379`
- `server-b` → `Service type: ClusterIP, port 8000`
- `server-a` → `Service type: NodePort (or Ingress), targetPort 8000`

---

## Step 3 – Convert each `service` to **Deployment + Service**

### 3.1 redis

Compose fields used:

- `container_name: redis`
- `ports: "6379:6379"`

K8s:

- **Deployment**:
  - `spec.template.spec.containers[0].image: redis-local:latest`
  - `containerPort: 6379`
- **Service**:
  - `metadata.name: redis`
  - `spec.selector.app: redis`
  - `spec.type: ClusterIP`
  - `port: 6379`

### 3.2 server-b

Compose fields used:

- `container_name: server-b`
- `ports: "8000:8000"`
- `depends_on: redis` (no direct equivalent; Kubernetes uses DNS + health)

K8s:

- **Deployment**:
  - `image: server-b:latest`
  - `containerPort: 8000`
  - `env`:
    - `REDIS_HOST=redis` (so it can reach Redis Service)
    - `REDIS_PORT=6379`
- **Service**:
  - `name: server-b`
  - `type: ClusterIP`
  - `port: 8000`

### 3.3 server-a

Compose fields used:

- `container_name: server-a`
- `ports: "8080:8000"`
- `depends_on: server-b`

K8s:

- **Deployment**:
  - `image: server-a:latest`
  - `containerPort: 8000`
  - `env`:
    - `SERVICE_B_URL=http://server-b:8000/list-ip-from-server-a`
- **Service**:
  - `name: server-a`
  - `type: NodePort` (for Minikube)
  - `port: 8000`
  - `targetPort: 8000`
  - `nodePort: 30800` (or some 30000–32767 port)

---

## Step 4 – Put those into actual YAML files

You usually split them like:

- `k8s/redis-deployment.yaml`
- `k8s/redis-service.yaml`
- `k8s/server-b-deployment.yaml`
- `k8s/server-b-service.yaml`
- `k8s/server-a-deployment.yaml`
- `k8s/server-a-service.yaml`

You already saw concrete examples earlier; the **conversion mapping** is:

- `build.context` / `dockerfile` → build image first, then set `spec.template.spec.containers[].image`.
- `ports: "host:container"` → `Service` (`port`/`targetPort`) + optionally `nodePort` for external access.
- `container_name` → just a label / name; in K8s, you use:
  - `metadata.name` (Deployment/Service)
  - `labels.app` to tie Service ↔ Deployment.
- `depends_on` → usually ignored; K8s manages ordering and connectivity via:
  - DNS (Service names like `redis`, `server-b`)
  - Readiness/liveness probes if needed.

---

## Step 5 – Apply manifests and test

Assuming Minikube and a namespace `ip-geolocation`:

```bash
kubectl apply -f k8s/namespace.yaml
kubectl apply -n ip-geolocation -f k8s/
```

Then:

```bash
kubectl get pods -n ip-geolocation
kubectl get svc  -n ip-geolocation
```

Access server‑a from your host via:

```bash
minikube ip
# suppose it's 192.168.49.2
curl http://192.168.49.2:30800/docs
```

---

### Super short conversion “recipe”

1. **Build images** from each `build:` block (`docker build ... -t server-a:latest`, etc.).
2. For each `service`:
   - Create a **Deployment** with that image and `containerPort` from the **container** side of the compose `ports`.
   - Create a **Service**:
     - `ClusterIP` if only internal (redis, server-b).
     - `NodePort` / Ingress if external (server-a).
3. Translate hostnames:
   - `REDIS_HOST=redis` (K8s Service name instead of `localhost`).
   - `SERVICE_B_URL=http://server-b:8000/...`.
4. `depends_on` → ignore; rely on Service DNS + health instead.

If you want, next step I can literally take your **exact** `Dockerfile.server_a` and `Dockerfile.server_b` image names and generate the 6 YAML files ready to paste into a `k8s/` folder.