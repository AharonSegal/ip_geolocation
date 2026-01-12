# ip_geolocation

# Black Coordinates List

## Main Components

1. **Service A** – IP ingestion, resolution, and geolocation.
    HTTP `POST` request to **Service A**, including a list of **IP addresses**
    HTTP `GET`  request to an external IP geolocation service
    HTTP `POST` request to **Service B**, including the resulting **coordinates**

2. **Service B** – Coordinate storage and retrieval.
    HTTP `GET` request to **Service A** for new IP
    HTTP `GET` request to **USER** for saved IP
    HTTP `POST` request to **Redis** to save IP

3. **Redis** – Data store for coordinates.

## Full Data Flow of the System

There are two main data flows:

1. **Primary flow – IP ingestion and coordinate storage**
2. **Secondary flow – Data retrieval for analysis / other tools**

### Primary Flow: IP Ingestion and Coordinate Storage

**SERVER A** 
1. HTTP `POST` request to **Service A**, including a list of **IP addresses**
2. **Service A** receives the request and Validates the IP addresses
3. **Service A** sends an HTTP request to an external IP geolocation service to resolve each IP into **geographic coordinates**
4. The external geolocation service returns to **Service A** data that includes the **geographic coordinates**
5. **Service A** performs **only basic data processing** on the returned data: it extracts and keeps **only the necessary fields** from the     external response.
6. After validating and preparing the data, **Service A** sends an internal HTTP `POST` request to **Service B**, including the resulting **coordinates**.

**SERVER B**
7. **Service B** receives the request and performs VALIDATIONS
TODO: WHAT VALIDATIONS **basic data validation**.
8. **Service B** stores the coordinates in **Redis**, the data store.
9. The process ends when the data is successfully stored in the data store.

### Secondary Flow: Reading / Aggregating Data

1. HTTP `GET` request to **Service B**.
2. **Service B** receives the request and pulls all the stored coordinates from the data store (**Redis**).
3. **Redis** returns the stored data to **Service B**.
4. **Service B** returns a **list of coordinates** (and their associated IPs as relevant) to the requester.


### Overall Project Layout

```text
ip_geolocation/
│
├── service-a/
│   ├── app/
│   │   ├── main.py
│   │   ├── routes.py
│   │   ├── services.py
│   │   ├── Dockerfile
│   │   └── schemas.py
│   │
│   └── requirements.txt
│
├── service-b/
│   ├── app/
│   │   ├── main.py
│   │   ├── routes.py
│   │   ├── storage.py
│   │   ├── Dockerfile
│   │   └── schemas.py
│   │
│   └── requirements.txt
│
├── docker-compose.yml
├── .env
└── README.md
```

Responsibilities per file:

- `main.py`  
  - Creates the FastAPI application and wires routes.
- `routes.py`  
  - Defines HTTP **endpoints** 
- `services.py`  
  - Contains the actual logic:
    - Calls to external services.
    - Data processing.
    - Sending data to Service B.
- `schemas.py`  
  - Pydantic models for requests and responses.
- `Dockerfile`  
  - Container definition for Service A.

#### Service B – Coordinates Storage (`service-b/`)

```text
service-b/
└── app/
    ├── main.py
    ├── routes.py
    ├── storage.py
    ├── Dockerfile
    └── schemas.py
```

Responsibilities per file:

- `main.py`  
  - Creates the FastAPI application and wires routes.
- `routes.py`  
  - Endpoints for:
    - Receiving coordinates.
    - Retrieving stored data.
- `storage.py`  
  - Work with Redis:
    - Connection.
    - Writing.
    - Reading.
- `schemas.py`  
  - Pydantic data models.
- `Dockerfile`  
  - Container definition for Service B.


## 9. Deployment Kubernetes (Minikube)

The **Black Coordinates List** is deployable in a **Kubernetes** environment using **Minikube** locally.

Deployment are defined in **YAML manifests**, applied via the terminal.

### Optional Extensions

In the future, the same system could also be deployed in other managed Kubernetes environments (e.g., OpenShift) using similar YAML manifests, with only environment‑specific adjustments.


