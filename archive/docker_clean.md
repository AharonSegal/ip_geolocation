### **1️⃣ Bash Script: `docker-clean.sh`**

```bash
#!/bin/bash

echo "Stopping all running containers..."
docker stop $(docker ps -q) 2>/dev/null

echo "Removing all containers..."
docker rm $(docker ps -a -q) 2>/dev/null

echo "Removing all images..."
docker rmi -f $(docker images -q) 2>/dev/null

echo "Removing all volumes..."
docker volume rm $(docker volume ls -q) 2>/dev/null

echo "Removing all networks (optional)..."
docker network rm $(docker network ls -q | grep -v "bridge\|host\|none") 2>/dev/null

echo "Full Docker cleanup complete!"

```

* Save this file as `docker-clean.sh`.
* Give it execute permission:

```bash
chmod +x docker-clean.sh
```

* Run it:

```bash
./docker-clean.sh
```

---

### **2️⃣ One-liner Commands (no script needed)**

If you just want quick commands in the terminal:

```bash
# Stop all running containers
docker stop $(docker ps -q)

# Remove all containers
docker rm $(docker ps -a -q)

# Remove all images
docker rmi -f $(docker images -q)

# Remove all unused volumes
docker volume prune -f
```

