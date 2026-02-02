# 🛍️ Flipkart Cloud-Native AI-Assistant

![Python](https://img.shields.io/badge/Python-3.9%2B-blue)
![Kubernetes](https://img.shields.io/badge/Kubernetes-Minikube-326ce5)
![Docker](https://img.shields.io/badge/Docker-Containerization-2496ed)
![Flask](https://img.shields.io/badge/Flask-API-000000)
![LangChain](https://img.shields.io/badge/LangChain-RAG-green)
![AstraDB](https://img.shields.io/badge/AstraDB-Vector%20Store-purple)
![Prometheus](https://img.shields.io/badge/Prometheus-Monitoring-e6522c)
![Grafana](https://img.shields.io/badge/Grafana-Visualization-F46800)

> **A scalable, microservices-based AI recommendation engine deployed on Kubernetes.** > *Leveraging RAG (Retrieval-Augmented Generation) to deliver context-aware product suggestions.*

---

## 📖 Overview

The **Flipkart Product Recommender** is an intelligent assistant designed to help users discover products using natural language queries. Unlike traditional keyword search, this system understands context (e.g., *"I need a laptop for heavy gaming under 80k"*) and retrieves relevant results using vector similarity search.

This project is not just an AI wrapper; it is a **fully orchestrated cloud-native application**. It demonstrates a complete DevOps pipeline: containerization with Docker, orchestration with Kubernetes, and real-time observability with Prometheus and Grafana.

---

## 🏗️ Architecture & Tech Stack

The application follows a microservices architecture pattern:

| Component | Technology | Description |
| :--- | :--- | :--- |
| **Orchestration** | **Kubernetes (Minikube)** | Manages Pods, Services, and Scaling. |
| **Containerization**| **Docker** | Ensures consistent environments across dev and prod. |
| **Backend API** | **Flask** | Lightweight Python web server handling requests. |
| **LLM Orchestration**| **LangChain** | Manages the RAG pipeline and prompt engineering. |
| **Inference Engine** | **Groq / Hugging Face** | Ultra-fast LLM inference for generating responses. |
| **Vector Database** | **Astra DB (Cassandra)** | Stores product embeddings for semantic search. |
| **Monitoring** | **Prometheus** | Scrapes metrics (latency, request count) from the Flask app. |
| **Visualization** | **Grafana** | Dashboards for real-time system health monitoring. |

---

## 🚀 Features

* **Context-Aware Search:** Uses Vector Embeddings to understand user intent, not just keywords.
* **RAG Pipeline:** Retrieves real product data from Astra DB and synthesizes a human-like response using Groq/Hugging Face.
* **Self-Healing Infrastructure:** Deployed on Kubernetes with `ReplicaSets` to ensure zero downtime.
* **Real-Time Observability:** Custom Prometheus exporters track API latency and 4xx/5xx error rates.
* **Scalable Design:** Stateless architecture allows for horizontal scaling of Flask pods.

---

## 🛠️ Installation & Setup

### Prerequisites
* Docker & Minikube installed.
* `kubectl` configured.
* Python 3.10+.
* Astra DB Account (Token & Endpoint).
* Groq / Hugging Face API Keys.

### 1. Clone the Repository
```bash
git clone [https://github.com/your-username/flipkart-recommender.git](https://github.com/your-username/flipkart-recommender.git)
cd flipkart-recommender


### 1. Initial Setup

- **Push code to GitHub**  
  Push your project code to a GitHub repository.

- **Create a Dockerfile**  
  Write a `Dockerfile` in the root of your project to containerize the app.

- **Create Kubernetes Deployemtn file**  
  Make a file named 'llmops-k8s.yaml' 

- **Create a VM Instance on Google Cloud**

  - Go to VM Instances and click **"Create Instance"**
  - Name: ``
  - Machine Type:
    - Series: `E2`
    - Preset: `Standard`
    - Memory: `16 GB RAM`
  - Boot Disk:
    - Change size to `256 GB`
    - Image: Select **Ubuntu 24.04 LTS**
  - Networking:
    - Enable HTTP and HTTPS traffic

- **Create the Instance**

- **Connect to the VM**
  - Use the **SSH** option provided to connect to the VM from the browser.



### 2. Configure VM Instance

- **Clone your GitHub repo**

  ```bash
  git clone https://github.com/data-guru0/TESTING-9.git
  ls
  cd TESTING-9
  ls  # You should see the contents of your project
  ```

- **Install Docker**

  - Search: "Install Docker on Ubuntu"
  - Open the first official Docker website (docs.docker.com)
  - Scroll down and copy the **first big command block** and paste into your VM terminal
  - Then copy and paste the **second command block**
  - Then run the **third command** to test Docker:

    ```bash
    docker run hello-world
    ```

- **Run Docker without sudo**

  - On the same page, scroll to: **"Post-installation steps for Linux"**
  - Paste all 4 commands one by one to allow Docker without `sudo`
  - Last command is for testing

- **Enable Docker to start on boot**

  - On the same page, scroll down to: **"Configure Docker to start on boot"**
  - Copy and paste the command block (2 commands):

    ```bash
    sudo systemctl enable docker.service
    sudo systemctl enable containerd.service
    ```

- **Verify Docker Setup**

  ```bash
  systemctl status docker       # You should see "active (running)"
  docker ps                     # No container should be running
  docker ps -a                 # Should show "hello-world" exited container
  ```


### 3. Configure Minikube inside VM

- **Install Minikube**

  - Open browser and search: `Install Minikube`
  - Open the first official site (minikube.sigs.k8s.io) with `minikube start` on it
  - Choose:
    - **OS:** Linux
    - **Architecture:** *x86*
    - Select **Binary download**
  - Reminder: You have already done this on Windows, so you're familiar with how Minikube works

- **Install Minikube Binary on VM**

  - Copy and paste the installation commands from the website into your VM terminal

- **Start Minikube Cluster**

  ```bash
  minikube start
  ```

  - This uses Docker internally, which is why Docker was installed first

- **Install kubectl**

  - Search: `Install kubectl`
  - Run the first command with `curl` from the official Kubernetes docs
  - Run the second command to validate the download
  - Instead of installing manually, go to the **Snap section** (below on the same page)

  ```bash
  sudo snap install kubectl --classic
  ```

  - Verify installation:

    ```bash
    kubectl version --client
    ```

- **Check Minikube Status**

  ```bash
  minikube status         # Should show all components running
  kubectl get nodes       # Should show minikube node
  kubectl cluster-info    # Cluster info
  docker ps               # Minikube container should be running
  ```

### 4. Interlink your Github on VSCode and on VM

```bash
git config --global user.email "gyrogodnon@gmail.com"
git config --global user.name "data-guru0"

git add .
git commit -m "commit"
git push origin main
```

- When prompted:
  - **Username**: `data-guru0`
  - **Password**: GitHub token (paste, it's invisible)

---


### 5. Build and Deploy your APP on VM

```bash
## Point Docker to Minikube
eval $(minikube docker-env)

docker build -t flask-app:latest .

kubectl create secret generic llmops-secrets \
  --from-literal=GROQ_API_KEY="" \
  --from-literal=ASTRA_DB_APPLICATION_TOKEN="" \
  --from-literal=ASTRA_DB_KEYSPACE="default_keyspace" \
  --from-literal=ASTRA_DB_API_ENDPOINT="" \
  --from-literal=HF_TOKEN="" \
  --from-literal=HUGGINGFACEHUB_API_TOKEN=""


kubectl apply -f flask-deployment.yaml


kubectl get pods

### U will see pods runiing


kubectl port-forward svc/flask-service 5000:80 --address 0.0.0.0

## Now copy external ip and :5000 and see ur app there....


```

### 6. PROMETHEUS AND GRAFANA MONITORING OF YOUR APP

```bash
## Open another VM terminal 

kubectl create namespace monitoring

kubectl get ns


kubectl apply -f prometheus/prometheus-configmap.yaml

kubectl apply -f prometheus/prometheus-deployment.yaml

kubectl apply -f grafana/grafana-deployment.yaml

## Check target health also..
## On IP:9090
kubectl port-forward --address 0.0.0.0 svc/prometheus-service -n monitoring 9090:9090

## Username:Pass --> admin:admin
kubectl port-forward --address 0.0.0.0 svc/grafana-service -n monitoring 3000:3000



Configure Grafana
Go to Settings > Data Sources > Add Data Source

Choose Prometheus

URL: http://prometheus-service.monitoring.svc.cluster.local:9090

Click Save & Test

Green success mesaage shown....


######################################


Now make a dashboard for different visualization
See course video for that....
```
