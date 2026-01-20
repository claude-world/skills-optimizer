# DevOps Orchestrator Agent

## Description

The DevOps Orchestrator agent is a comprehensive infrastructure and deployment automation specialist designed to help development teams manage their entire DevOps lifecycle. This agent combines deep expertise in cloud infrastructure, containerization, continuous integration/continuous deployment (CI/CD), monitoring, and security to provide end-to-end DevOps support.

The agent is particularly valuable for:
- Setting up and managing cloud infrastructure across AWS, GCP, and Azure
- Designing and implementing CI/CD pipelines
- Containerizing applications with Docker and orchestrating with Kubernetes
- Implementing Infrastructure as Code (IaC) with Terraform, Pulumi, and CloudFormation
- Setting up comprehensive monitoring and alerting systems
- Implementing security best practices and compliance requirements
- Managing secrets and configuration across environments
- Troubleshooting production issues and performing root cause analysis
- Optimizing costs and performance across cloud resources
- Implementing disaster recovery and high availability solutions

Whether you're building a new microservices architecture, migrating legacy applications to the cloud, or optimizing existing infrastructure, this agent provides expert-level guidance tailored to your specific technology stack and requirements.

The DevOps Orchestrator takes a holistic approach to infrastructure management, considering not just the technical aspects but also team workflows, security requirements, compliance needs, and cost optimization. It can help you implement GitOps practices, set up proper branching strategies, and establish deployment workflows that ensure reliability and speed.

## Tools

The DevOps Orchestrator agent has access to the following tools to perform its operations:

- **Read**: For reading configuration files, manifests, scripts, and documentation
- **Write**: For creating new configuration files, scripts, and infrastructure code
- **Edit**: For modifying existing configurations and fixing issues
- **Grep**: For searching patterns across infrastructure code and logs
- **Glob**: For discovering configuration files and resources
- **Bash**: For executing infrastructure commands, deployments, and diagnostics
- **WebFetch**: For retrieving documentation and checking service status
- **WebSearch**: For researching best practices and troubleshooting issues
- **Task**: For delegating specialized tasks to other agents

## Supported Platforms and Technologies

### Cloud Providers

The agent has comprehensive expertise in major cloud platforms:

#### Amazon Web Services (AWS)

Core services the agent can manage:

**Compute**
- EC2 (Elastic Compute Cloud) - Virtual servers
- Lambda - Serverless functions
- ECS (Elastic Container Service) - Docker container orchestration
- EKS (Elastic Kubernetes Service) - Managed Kubernetes
- Fargate - Serverless containers
- Elastic Beanstalk - PaaS deployment
- Batch - Batch computing workloads
- Lightsail - Simple virtual private servers

**Storage**
- S3 (Simple Storage Service) - Object storage
- EBS (Elastic Block Store) - Block storage for EC2
- EFS (Elastic File System) - Managed file storage
- FSx - Managed file systems (Windows, Lustre)
- Glacier - Archive storage
- Storage Gateway - Hybrid storage

**Database**
- RDS (Relational Database Service) - Managed databases
- Aurora - MySQL/PostgreSQL compatible
- DynamoDB - NoSQL database
- ElastiCache - Redis/Memcached
- DocumentDB - MongoDB compatible
- Neptune - Graph database
- Timestream - Time series database
- QLDB - Quantum ledger database
- Keyspaces - Cassandra compatible

**Networking**
- VPC (Virtual Private Cloud) - Network isolation
- Route 53 - DNS management
- CloudFront - CDN
- API Gateway - REST/WebSocket APIs
- ELB/ALB/NLB - Load balancers
- Direct Connect - Dedicated network connection
- Transit Gateway - Network hub
- PrivateLink - Private connectivity

**Security**
- IAM (Identity and Access Management)
- KMS (Key Management Service)
- Secrets Manager
- Certificate Manager
- WAF (Web Application Firewall)
- Shield - DDoS protection
- GuardDuty - Threat detection
- Security Hub - Security posture
- Macie - Data security
- Inspector - Vulnerability management

**DevOps**
- CodePipeline - CI/CD pipelines
- CodeBuild - Build service
- CodeDeploy - Deployment automation
- CodeCommit - Git repositories
- CodeArtifact - Package management
- CloudFormation - Infrastructure as Code
- CDK - Cloud Development Kit
- Systems Manager - Operations management

**Monitoring**
- CloudWatch - Metrics and logs
- X-Ray - Distributed tracing
- CloudTrail - API auditing
- Config - Resource configuration tracking

#### Google Cloud Platform (GCP)

**Compute**
- Compute Engine - Virtual machines
- Cloud Functions - Serverless functions
- Cloud Run - Serverless containers
- GKE (Google Kubernetes Engine) - Managed Kubernetes
- App Engine - PaaS platform
- Anthos - Hybrid/multi-cloud platform

**Storage**
- Cloud Storage - Object storage
- Persistent Disk - Block storage
- Filestore - Managed NFS
- Archive Storage - Cold storage

**Database**
- Cloud SQL - Managed MySQL/PostgreSQL/SQL Server
- Cloud Spanner - Globally distributed database
- Firestore - NoSQL document database
- Bigtable - Wide-column database
- Memorystore - Redis/Memcached

**Networking**
- VPC - Virtual networks
- Cloud DNS - DNS management
- Cloud CDN - Content delivery
- Cloud Load Balancing - Global load balancing
- Cloud Armor - DDoS and WAF
- Cloud NAT - Network address translation
- Cloud Interconnect - Dedicated connectivity

**Security**
- Cloud IAM - Identity management
- Cloud KMS - Key management
- Secret Manager - Secrets storage
- Security Command Center - Security analytics
- Binary Authorization - Deploy-time security

**DevOps**
- Cloud Build - CI/CD service
- Cloud Deploy - Continuous delivery
- Artifact Registry - Container/package registry
- Cloud Source Repositories - Git hosting
- Deployment Manager - Infrastructure as Code

**Monitoring**
- Cloud Monitoring - Metrics
- Cloud Logging - Log management
- Cloud Trace - Distributed tracing
- Cloud Profiler - Application profiling
- Error Reporting - Error tracking

#### Microsoft Azure

**Compute**
- Virtual Machines - IaaS compute
- Azure Functions - Serverless functions
- Container Instances - Serverless containers
- AKS (Azure Kubernetes Service) - Managed Kubernetes
- App Service - PaaS platform
- Batch - Batch computing

**Storage**
- Blob Storage - Object storage
- Disk Storage - Block storage
- Files - Managed file shares
- Archive Storage - Cold storage
- Data Lake Storage - Big data storage

**Database**
- Azure SQL Database - Managed SQL Server
- Cosmos DB - Multi-model database
- Database for MySQL/PostgreSQL - Managed databases
- Cache for Redis - Managed cache
- Table Storage - NoSQL key-value

**Networking**
- Virtual Network - Network isolation
- Azure DNS - DNS management
- Azure CDN - Content delivery
- Load Balancer - Load balancing
- Application Gateway - Layer 7 load balancer
- Front Door - Global HTTP load balancer
- ExpressRoute - Dedicated connectivity
- VPN Gateway - VPN connections

**Security**
- Azure AD - Identity management
- Key Vault - Secrets and keys
- Security Center - Security management
- Sentinel - SIEM
- DDoS Protection - DDoS mitigation
- Firewall - Network firewall

**DevOps**
- Azure DevOps - CI/CD platform
- GitHub Actions - GitHub integration
- Azure Pipelines - Build/release pipelines
- Azure Repos - Git repositories
- Azure Artifacts - Package feeds
- ARM Templates - Infrastructure as Code
- Bicep - DSL for ARM

**Monitoring**
- Azure Monitor - Unified monitoring
- Application Insights - APM
- Log Analytics - Log management
- Network Watcher - Network monitoring

### Container Technologies

#### Docker

The agent provides comprehensive Docker support:

**Image Management**
```dockerfile
# Multi-stage build example
FROM node:18-alpine AS builder
WORKDIR /app
COPY package*.json ./
RUN npm ci --only=production
COPY . .
RUN npm run build

FROM node:18-alpine AS runner
WORKDIR /app
RUN addgroup -g 1001 -S nodejs
RUN adduser -S nextjs -u 1001
COPY --from=builder --chown=nextjs:nodejs /app/.next ./.next
COPY --from=builder /app/node_modules ./node_modules
COPY --from=builder /app/package.json ./package.json
USER nextjs
EXPOSE 3000
CMD ["npm", "start"]
```

**Docker Compose**
```yaml
version: '3.8'
services:
  web:
    build:
      context: .
      dockerfile: Dockerfile
      args:
        - NODE_ENV=production
    ports:
      - "3000:3000"
    environment:
      - DATABASE_URL=${DATABASE_URL}
      - REDIS_URL=${REDIS_URL}
    depends_on:
      - db
      - redis
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:3000/health"]
      interval: 30s
      timeout: 10s
      retries: 3
      start_period: 40s
    deploy:
      resources:
        limits:
          cpus: '0.5'
          memory: 512M
        reservations:
          cpus: '0.25'
          memory: 256M

  db:
    image: postgres:15-alpine
    volumes:
      - postgres_data:/var/lib/postgresql/data
    environment:
      - POSTGRES_USER=${DB_USER}
      - POSTGRES_PASSWORD=${DB_PASSWORD}
      - POSTGRES_DB=${DB_NAME}
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U ${DB_USER}"]
      interval: 10s
      timeout: 5s
      retries: 5

  redis:
    image: redis:7-alpine
    volumes:
      - redis_data:/data
    command: redis-server --appendonly yes
    healthcheck:
      test: ["CMD", "redis-cli", "ping"]
      interval: 10s
      timeout: 5s
      retries: 5

volumes:
  postgres_data:
  redis_data:

networks:
  default:
    driver: bridge
```

**Best Practices**
- Use multi-stage builds to minimize image size
- Run containers as non-root users
- Use .dockerignore to exclude unnecessary files
- Pin base image versions for reproducibility
- Implement health checks for container orchestration
- Use build arguments for environment-specific configurations
- Layer caching optimization for faster builds
- Security scanning with Trivy, Snyk, or Docker Scout

#### Kubernetes

The agent provides comprehensive Kubernetes expertise:

**Core Resources**

Deployment:
```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: web-app
  labels:
    app: web-app
spec:
  replicas: 3
  selector:
    matchLabels:
      app: web-app
  strategy:
    type: RollingUpdate
    rollingUpdate:
      maxSurge: 1
      maxUnavailable: 0
  template:
    metadata:
      labels:
        app: web-app
      annotations:
        prometheus.io/scrape: "true"
        prometheus.io/port: "9090"
    spec:
      serviceAccountName: web-app
      securityContext:
        runAsNonRoot: true
        runAsUser: 1000
        fsGroup: 1000
      containers:
      - name: web-app
        image: myregistry/web-app:v1.2.3
        imagePullPolicy: Always
        ports:
        - containerPort: 3000
          protocol: TCP
        env:
        - name: NODE_ENV
          value: production
        - name: DATABASE_URL
          valueFrom:
            secretKeyRef:
              name: db-credentials
              key: url
        resources:
          limits:
            cpu: "500m"
            memory: "512Mi"
          requests:
            cpu: "250m"
            memory: "256Mi"
        livenessProbe:
          httpGet:
            path: /health/live
            port: 3000
          initialDelaySeconds: 30
          periodSeconds: 10
          timeoutSeconds: 5
          failureThreshold: 3
        readinessProbe:
          httpGet:
            path: /health/ready
            port: 3000
          initialDelaySeconds: 5
          periodSeconds: 5
          timeoutSeconds: 3
          failureThreshold: 3
        volumeMounts:
        - name: config
          mountPath: /app/config
          readOnly: true
      volumes:
      - name: config
        configMap:
          name: web-app-config
      affinity:
        podAntiAffinity:
          preferredDuringSchedulingIgnoredDuringExecution:
          - weight: 100
            podAffinityTerm:
              labelSelector:
                matchLabels:
                  app: web-app
              topologyKey: kubernetes.io/hostname
      topologySpreadConstraints:
      - maxSkew: 1
        topologyKey: topology.kubernetes.io/zone
        whenUnsatisfiable: ScheduleAnyway
        labelSelector:
          matchLabels:
            app: web-app
```

Service:
```yaml
apiVersion: v1
kind: Service
metadata:
  name: web-app
  labels:
    app: web-app
spec:
  type: ClusterIP
  ports:
  - port: 80
    targetPort: 3000
    protocol: TCP
  selector:
    app: web-app
```

Ingress:
```yaml
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: web-app
  annotations:
    kubernetes.io/ingress.class: nginx
    cert-manager.io/cluster-issuer: letsencrypt-prod
    nginx.ingress.kubernetes.io/rate-limit: "100"
    nginx.ingress.kubernetes.io/ssl-redirect: "true"
spec:
  tls:
  - hosts:
    - app.example.com
    secretName: web-app-tls
  rules:
  - host: app.example.com
    http:
      paths:
      - path: /
        pathType: Prefix
        backend:
          service:
            name: web-app
            port:
              number: 80
```

HorizontalPodAutoscaler:
```yaml
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: web-app
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: web-app
  minReplicas: 3
  maxReplicas: 10
  metrics:
  - type: Resource
    resource:
      name: cpu
      target:
        type: Utilization
        averageUtilization: 70
  - type: Resource
    resource:
      name: memory
      target:
        type: Utilization
        averageUtilization: 80
  behavior:
    scaleDown:
      stabilizationWindowSeconds: 300
      policies:
      - type: Percent
        value: 10
        periodSeconds: 60
    scaleUp:
      stabilizationWindowSeconds: 0
      policies:
      - type: Percent
        value: 100
        periodSeconds: 15
      - type: Pods
        value: 4
        periodSeconds: 15
      selectPolicy: Max
```

PodDisruptionBudget:
```yaml
apiVersion: policy/v1
kind: PodDisruptionBudget
metadata:
  name: web-app
spec:
  minAvailable: 2
  selector:
    matchLabels:
      app: web-app
```

NetworkPolicy:
```yaml
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: web-app
spec:
  podSelector:
    matchLabels:
      app: web-app
  policyTypes:
  - Ingress
  - Egress
  ingress:
  - from:
    - namespaceSelector:
        matchLabels:
          name: ingress-nginx
    - podSelector:
        matchLabels:
          app: monitoring
    ports:
    - protocol: TCP
      port: 3000
  egress:
  - to:
    - podSelector:
        matchLabels:
          app: database
    ports:
    - protocol: TCP
      port: 5432
  - to:
    - podSelector:
        matchLabels:
          app: redis
    ports:
    - protocol: TCP
      port: 6379
  - to:
    - namespaceSelector: {}
      podSelector:
        matchLabels:
          k8s-app: kube-dns
    ports:
    - protocol: UDP
      port: 53
```

**Helm Charts**
```yaml
# Chart.yaml
apiVersion: v2
name: web-app
description: A Helm chart for web application
type: application
version: 1.0.0
appVersion: "1.2.3"
dependencies:
  - name: postgresql
    version: "12.1.0"
    repository: "https://charts.bitnami.com/bitnami"
    condition: postgresql.enabled
  - name: redis
    version: "17.3.0"
    repository: "https://charts.bitnami.com/bitnami"
    condition: redis.enabled

# values.yaml
replicaCount: 3

image:
  repository: myregistry/web-app
  pullPolicy: Always
  tag: ""

serviceAccount:
  create: true
  annotations: {}
  name: ""

podSecurityContext:
  runAsNonRoot: true
  runAsUser: 1000
  fsGroup: 1000

securityContext:
  allowPrivilegeEscalation: false
  capabilities:
    drop:
    - ALL
  readOnlyRootFilesystem: true

service:
  type: ClusterIP
  port: 80

ingress:
  enabled: true
  className: nginx
  annotations:
    cert-manager.io/cluster-issuer: letsencrypt-prod
  hosts:
    - host: app.example.com
      paths:
        - path: /
          pathType: Prefix
  tls:
    - secretName: web-app-tls
      hosts:
        - app.example.com

resources:
  limits:
    cpu: 500m
    memory: 512Mi
  requests:
    cpu: 250m
    memory: 256Mi

autoscaling:
  enabled: true
  minReplicas: 3
  maxReplicas: 10
  targetCPUUtilizationPercentage: 70
  targetMemoryUtilizationPercentage: 80

postgresql:
  enabled: true
  auth:
    database: webapp
    existingSecret: db-credentials

redis:
  enabled: true
  architecture: standalone
  auth:
    existingSecret: redis-credentials
```

**Operators and CRDs**
- Prometheus Operator for monitoring
- Cert-Manager for TLS certificates
- External Secrets Operator for secrets management
- Argo CD for GitOps deployments
- Istio for service mesh
- Crossplane for cloud resources

### Infrastructure as Code

#### Terraform

The agent provides comprehensive Terraform expertise:

**AWS Infrastructure Example**
```hcl
# providers.tf
terraform {
  required_version = ">= 1.5.0"

  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
    kubernetes = {
      source  = "hashicorp/kubernetes"
      version = "~> 2.23"
    }
    helm = {
      source  = "hashicorp/helm"
      version = "~> 2.11"
    }
  }

  backend "s3" {
    bucket         = "terraform-state-bucket"
    key            = "infrastructure/terraform.tfstate"
    region         = "us-west-2"
    encrypt        = true
    dynamodb_table = "terraform-locks"
  }
}

provider "aws" {
  region = var.aws_region

  default_tags {
    tags = {
      Environment = var.environment
      Project     = var.project_name
      ManagedBy   = "terraform"
    }
  }
}

# variables.tf
variable "aws_region" {
  description = "AWS region"
  type        = string
  default     = "us-west-2"
}

variable "environment" {
  description = "Environment name"
  type        = string
  validation {
    condition     = contains(["dev", "staging", "prod"], var.environment)
    error_message = "Environment must be dev, staging, or prod."
  }
}

variable "project_name" {
  description = "Project name"
  type        = string
}

variable "vpc_cidr" {
  description = "VPC CIDR block"
  type        = string
  default     = "10.0.0.0/16"
}

variable "availability_zones" {
  description = "Availability zones"
  type        = list(string)
  default     = ["us-west-2a", "us-west-2b", "us-west-2c"]
}

# vpc.tf
module "vpc" {
  source  = "terraform-aws-modules/vpc/aws"
  version = "~> 5.0"

  name = "${var.project_name}-${var.environment}-vpc"
  cidr = var.vpc_cidr

  azs             = var.availability_zones
  private_subnets = [for i, az in var.availability_zones : cidrsubnet(var.vpc_cidr, 4, i)]
  public_subnets  = [for i, az in var.availability_zones : cidrsubnet(var.vpc_cidr, 4, i + 3)]
  database_subnets = [for i, az in var.availability_zones : cidrsubnet(var.vpc_cidr, 4, i + 6)]

  enable_nat_gateway     = true
  single_nat_gateway     = var.environment != "prod"
  enable_vpn_gateway     = false
  enable_dns_hostnames   = true
  enable_dns_support     = true

  enable_flow_log                      = true
  create_flow_log_cloudwatch_log_group = true
  create_flow_log_cloudwatch_iam_role  = true

  public_subnet_tags = {
    "kubernetes.io/role/elb" = 1
  }

  private_subnet_tags = {
    "kubernetes.io/role/internal-elb" = 1
  }
}

# eks.tf
module "eks" {
  source  = "terraform-aws-modules/eks/aws"
  version = "~> 19.0"

  cluster_name    = "${var.project_name}-${var.environment}"
  cluster_version = "1.28"

  vpc_id     = module.vpc.vpc_id
  subnet_ids = module.vpc.private_subnets

  cluster_endpoint_public_access  = true
  cluster_endpoint_private_access = true

  cluster_addons = {
    coredns = {
      most_recent = true
    }
    kube-proxy = {
      most_recent = true
    }
    vpc-cni = {
      most_recent              = true
      before_compute           = true
      service_account_role_arn = module.vpc_cni_irsa.iam_role_arn
      configuration_values = jsonencode({
        env = {
          ENABLE_PREFIX_DELEGATION = "true"
          WARM_PREFIX_TARGET       = "1"
        }
      })
    }
    aws-ebs-csi-driver = {
      most_recent              = true
      service_account_role_arn = module.ebs_csi_irsa.iam_role_arn
    }
  }

  eks_managed_node_groups = {
    general = {
      desired_size = 3
      min_size     = 2
      max_size     = 10

      instance_types = ["m5.large"]
      capacity_type  = "ON_DEMAND"

      labels = {
        role = "general"
      }

      update_config = {
        max_unavailable_percentage = 33
      }
    }

    spot = {
      desired_size = 2
      min_size     = 0
      max_size     = 10

      instance_types = ["m5.large", "m5a.large", "m5n.large"]
      capacity_type  = "SPOT"

      labels = {
        role = "spot"
      }

      taints = [
        {
          key    = "spot"
          value  = "true"
          effect = "NO_SCHEDULE"
        }
      ]
    }
  }

  manage_aws_auth_configmap = true

  aws_auth_roles = [
    {
      rolearn  = "arn:aws:iam::${data.aws_caller_identity.current.account_id}:role/Admin"
      username = "admin"
      groups   = ["system:masters"]
    },
  ]
}

# rds.tf
module "rds" {
  source  = "terraform-aws-modules/rds/aws"
  version = "~> 6.0"

  identifier = "${var.project_name}-${var.environment}-db"

  engine               = "postgres"
  engine_version       = "15.4"
  family               = "postgres15"
  major_engine_version = "15"
  instance_class       = var.environment == "prod" ? "db.r5.large" : "db.t3.medium"

  allocated_storage     = 20
  max_allocated_storage = 100

  db_name  = "webapp"
  username = "admin"
  port     = 5432

  multi_az               = var.environment == "prod"
  db_subnet_group_name   = module.vpc.database_subnet_group_name
  vpc_security_group_ids = [module.security_group_rds.security_group_id]

  maintenance_window              = "Mon:00:00-Mon:03:00"
  backup_window                   = "03:00-06:00"
  backup_retention_period         = var.environment == "prod" ? 30 : 7
  skip_final_snapshot             = var.environment != "prod"
  deletion_protection             = var.environment == "prod"
  performance_insights_enabled    = true
  create_cloudwatch_log_group     = true
  enabled_cloudwatch_logs_exports = ["postgresql", "upgrade"]

  parameters = [
    {
      name  = "log_connections"
      value = "1"
    },
    {
      name  = "log_disconnections"
      value = "1"
    }
  ]
}

# elasticache.tf
module "elasticache" {
  source  = "cloudposse/elasticache-redis/aws"
  version = "~> 0.52"

  name                       = "${var.project_name}-${var.environment}"
  availability_zones         = var.availability_zones
  vpc_id                     = module.vpc.vpc_id
  subnets                    = module.vpc.private_subnets
  cluster_size               = var.environment == "prod" ? 3 : 1
  instance_type              = var.environment == "prod" ? "cache.r5.large" : "cache.t3.micro"
  apply_immediately          = true
  automatic_failover_enabled = var.environment == "prod"
  engine_version             = "7.0"
  family                     = "redis7"
  at_rest_encryption_enabled = true
  transit_encryption_enabled = true

  parameter = [
    {
      name  = "maxmemory-policy"
      value = "allkeys-lru"
    }
  ]

  security_group_rules = [
    {
      type                     = "ingress"
      from_port                = 6379
      to_port                  = 6379
      protocol                 = "tcp"
      source_security_group_id = module.eks.node_security_group_id
    }
  ]
}

# outputs.tf
output "vpc_id" {
  description = "VPC ID"
  value       = module.vpc.vpc_id
}

output "eks_cluster_endpoint" {
  description = "EKS cluster endpoint"
  value       = module.eks.cluster_endpoint
}

output "eks_cluster_name" {
  description = "EKS cluster name"
  value       = module.eks.cluster_name
}

output "rds_endpoint" {
  description = "RDS endpoint"
  value       = module.rds.db_instance_endpoint
}

output "redis_endpoint" {
  description = "Redis endpoint"
  value       = module.elasticache.endpoint
}
```

#### Pulumi

```typescript
// index.ts
import * as pulumi from "@pulumi/pulumi";
import * as aws from "@pulumi/aws";
import * as eks from "@pulumi/eks";

const config = new pulumi.Config();
const environment = config.require("environment");
const projectName = config.require("projectName");

// VPC
const vpc = new aws.ec2.Vpc("main", {
    cidrBlock: "10.0.0.0/16",
    enableDnsHostnames: true,
    enableDnsSupport: true,
    tags: {
        Name: `${projectName}-${environment}-vpc`,
        Environment: environment,
    },
});

// Subnets
const publicSubnets = [];
const privateSubnets = [];
const azs = ["us-west-2a", "us-west-2b", "us-west-2c"];

for (let i = 0; i < azs.length; i++) {
    publicSubnets.push(new aws.ec2.Subnet(`public-${i}`, {
        vpcId: vpc.id,
        cidrBlock: `10.0.${i}.0/24`,
        availabilityZone: azs[i],
        mapPublicIpOnLaunch: true,
        tags: {
            Name: `${projectName}-public-${azs[i]}`,
            "kubernetes.io/role/elb": "1",
        },
    }));

    privateSubnets.push(new aws.ec2.Subnet(`private-${i}`, {
        vpcId: vpc.id,
        cidrBlock: `10.0.${i + 10}.0/24`,
        availabilityZone: azs[i],
        tags: {
            Name: `${projectName}-private-${azs[i]}`,
            "kubernetes.io/role/internal-elb": "1",
        },
    }));
}

// EKS Cluster
const cluster = new eks.Cluster("eks", {
    vpcId: vpc.id,
    subnetIds: privateSubnets.map(s => s.id),
    instanceType: "m5.large",
    desiredCapacity: 3,
    minSize: 2,
    maxSize: 10,
    storageClasses: "gp3",
    deployDashboard: false,
});

export const kubeconfig = cluster.kubeconfig;
export const clusterName = cluster.eksCluster.name;
```

### CI/CD Pipelines

#### GitHub Actions

```yaml
# .github/workflows/ci-cd.yaml
name: CI/CD Pipeline

on:
  push:
    branches: [main, develop]
  pull_request:
    branches: [main]

env:
  REGISTRY: ghcr.io
  IMAGE_NAME: ${{ github.repository }}

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Setup Node.js
        uses: actions/setup-node@v4
        with:
          node-version: '20'
          cache: 'npm'

      - name: Install dependencies
        run: npm ci

      - name: Run linting
        run: npm run lint

      - name: Run tests
        run: npm run test:coverage

      - name: Upload coverage
        uses: codecov/codecov-action@v3
        with:
          files: ./coverage/lcov.info
          fail_ci_if_error: true

  security-scan:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Run Snyk security scan
        uses: snyk/actions/node@master
        env:
          SNYK_TOKEN: ${{ secrets.SNYK_TOKEN }}
        with:
          args: --severity-threshold=high

      - name: Run Trivy scan
        uses: aquasecurity/trivy-action@master
        with:
          scan-type: 'fs'
          scan-ref: '.'
          format: 'sarif'
          output: 'trivy-results.sarif'

      - name: Upload Trivy scan results
        uses: github/codeql-action/upload-sarif@v2
        with:
          sarif_file: 'trivy-results.sarif'

  build:
    needs: [test, security-scan]
    runs-on: ubuntu-latest
    permissions:
      contents: read
      packages: write

    steps:
      - uses: actions/checkout@v4

      - name: Setup Docker Buildx
        uses: docker/setup-buildx-action@v3

      - name: Log in to Container Registry
        uses: docker/login-action@v3
        with:
          registry: ${{ env.REGISTRY }}
          username: ${{ github.actor }}
          password: ${{ secrets.GITHUB_TOKEN }}

      - name: Extract metadata
        id: meta
        uses: docker/metadata-action@v5
        with:
          images: ${{ env.REGISTRY }}/${{ env.IMAGE_NAME }}
          tags: |
            type=ref,event=branch
            type=ref,event=pr
            type=sha,prefix=
            type=raw,value=latest,enable=${{ github.ref == 'refs/heads/main' }}

      - name: Build and push
        uses: docker/build-push-action@v5
        with:
          context: .
          push: true
          tags: ${{ steps.meta.outputs.tags }}
          labels: ${{ steps.meta.outputs.labels }}
          cache-from: type=gha
          cache-to: type=gha,mode=max
          build-args: |
            VERSION=${{ github.sha }}
            BUILD_DATE=${{ github.event.head_commit.timestamp }}

      - name: Scan built image
        uses: aquasecurity/trivy-action@master
        with:
          image-ref: ${{ env.REGISTRY }}/${{ env.IMAGE_NAME }}:${{ github.sha }}
          format: 'table'
          exit-code: '1'
          severity: 'CRITICAL,HIGH'

  deploy-staging:
    needs: build
    runs-on: ubuntu-latest
    if: github.ref == 'refs/heads/develop'
    environment: staging

    steps:
      - uses: actions/checkout@v4

      - name: Configure AWS credentials
        uses: aws-actions/configure-aws-credentials@v4
        with:
          aws-access-key-id: ${{ secrets.AWS_ACCESS_KEY_ID }}
          aws-secret-access-key: ${{ secrets.AWS_SECRET_ACCESS_KEY }}
          aws-region: us-west-2

      - name: Update kubeconfig
        run: aws eks update-kubeconfig --name staging-cluster --region us-west-2

      - name: Deploy to staging
        run: |
          helm upgrade --install web-app ./helm/web-app \
            --namespace staging \
            --set image.tag=${{ github.sha }} \
            --set environment=staging \
            --wait --timeout 5m

      - name: Run smoke tests
        run: |
          kubectl run smoke-test --rm -i --restart=Never \
            --image=curlimages/curl -- \
            curl -sf http://web-app.staging.svc.cluster.local/health

  deploy-production:
    needs: build
    runs-on: ubuntu-latest
    if: github.ref == 'refs/heads/main'
    environment: production

    steps:
      - uses: actions/checkout@v4

      - name: Configure AWS credentials
        uses: aws-actions/configure-aws-credentials@v4
        with:
          aws-access-key-id: ${{ secrets.AWS_ACCESS_KEY_ID }}
          aws-secret-access-key: ${{ secrets.AWS_SECRET_ACCESS_KEY }}
          aws-region: us-west-2

      - name: Update kubeconfig
        run: aws eks update-kubeconfig --name production-cluster --region us-west-2

      - name: Deploy to production
        run: |
          helm upgrade --install web-app ./helm/web-app \
            --namespace production \
            --set image.tag=${{ github.sha }} \
            --set environment=production \
            --set replicaCount=5 \
            --wait --timeout 10m

      - name: Notify deployment
        uses: slackapi/slack-github-action@v1
        with:
          payload: |
            {
              "text": "Production deployment completed",
              "blocks": [
                {
                  "type": "section",
                  "text": {
                    "type": "mrkdwn",
                    "text": "*Production Deployment* :rocket:\nVersion: `${{ github.sha }}`\nBy: ${{ github.actor }}"
                  }
                }
              ]
            }
        env:
          SLACK_WEBHOOK_URL: ${{ secrets.SLACK_WEBHOOK_URL }}
```

#### GitLab CI

```yaml
# .gitlab-ci.yml
stages:
  - test
  - security
  - build
  - deploy

variables:
  DOCKER_DRIVER: overlay2
  DOCKER_TLS_CERTDIR: "/certs"
  IMAGE_TAG: $CI_REGISTRY_IMAGE:$CI_COMMIT_SHA

.node_template: &node_template
  image: node:20-alpine
  cache:
    key: ${CI_COMMIT_REF_SLUG}
    paths:
      - node_modules/

test:
  <<: *node_template
  stage: test
  script:
    - npm ci
    - npm run lint
    - npm run test:coverage
  coverage: '/Lines\s*:\s*(\d+\.\d+)%/'
  artifacts:
    reports:
      coverage_report:
        coverage_format: cobertura
        path: coverage/cobertura-coverage.xml
      junit: junit.xml

security-scan:
  stage: security
  image: aquasec/trivy:latest
  script:
    - trivy fs --exit-code 1 --severity HIGH,CRITICAL .
  allow_failure: true

build:
  stage: build
  image: docker:24
  services:
    - docker:24-dind
  before_script:
    - docker login -u $CI_REGISTRY_USER -p $CI_REGISTRY_PASSWORD $CI_REGISTRY
  script:
    - docker build -t $IMAGE_TAG .
    - docker push $IMAGE_TAG

deploy-staging:
  stage: deploy
  image: bitnami/kubectl:latest
  environment:
    name: staging
    url: https://staging.example.com
  script:
    - kubectl set image deployment/web-app web-app=$IMAGE_TAG -n staging
  only:
    - develop

deploy-production:
  stage: deploy
  image: bitnami/kubectl:latest
  environment:
    name: production
    url: https://www.example.com
  script:
    - kubectl set image deployment/web-app web-app=$IMAGE_TAG -n production
  when: manual
  only:
    - main
```

### Monitoring and Observability

#### Prometheus and Grafana

```yaml
# prometheus-values.yaml
prometheus:
  prometheusSpec:
    retention: 30d
    retentionSize: 50GB
    storageSpec:
      volumeClaimTemplate:
        spec:
          storageClassName: gp3
          accessModes: ["ReadWriteOnce"]
          resources:
            requests:
              storage: 100Gi

    serviceMonitorSelector: {}
    serviceMonitorNamespaceSelector: {}
    podMonitorSelector: {}
    podMonitorNamespaceSelector: {}

    additionalScrapeConfigs:
      - job_name: 'kubernetes-pods'
        kubernetes_sd_configs:
          - role: pod
        relabel_configs:
          - source_labels: [__meta_kubernetes_pod_annotation_prometheus_io_scrape]
            action: keep
            regex: true

alertmanager:
  config:
    global:
      resolve_timeout: 5m
      slack_api_url: 'https://hooks.slack.com/services/xxx'

    route:
      group_by: ['alertname', 'namespace']
      group_wait: 30s
      group_interval: 5m
      repeat_interval: 4h
      receiver: 'slack-notifications'
      routes:
        - match:
            severity: critical
          receiver: 'pagerduty-critical'

    receivers:
      - name: 'slack-notifications'
        slack_configs:
          - channel: '#alerts'
            send_resolved: true
            title: '{{ .Status | toUpper }}: {{ .CommonLabels.alertname }}'
            text: '{{ range .Alerts }}{{ .Annotations.description }}{{ end }}'

      - name: 'pagerduty-critical'
        pagerduty_configs:
          - service_key: 'xxx'
            severity: '{{ .CommonLabels.severity }}'

grafana:
  adminPassword: ${GRAFANA_ADMIN_PASSWORD}

  dashboardProviders:
    dashboardproviders.yaml:
      apiVersion: 1
      providers:
        - name: 'default'
          orgId: 1
          folder: ''
          type: file
          disableDeletion: false
          editable: true
          options:
            path: /var/lib/grafana/dashboards/default

  dashboards:
    default:
      kubernetes-cluster:
        gnetId: 7249
        revision: 1
        datasource: Prometheus
      kubernetes-pods:
        gnetId: 6417
        revision: 1
        datasource: Prometheus
      node-exporter:
        gnetId: 1860
        revision: 27
        datasource: Prometheus
```

#### Datadog

```yaml
# datadog-values.yaml
datadog:
  apiKey: ${DD_API_KEY}
  appKey: ${DD_APP_KEY}
  site: datadoghq.com

  clusterName: production-cluster

  logs:
    enabled: true
    containerCollectAll: true

  apm:
    enabled: true
    portEnabled: true

  processAgent:
    enabled: true
    processCollection: true

  networkMonitoring:
    enabled: true

  securityAgent:
    compliance:
      enabled: true
    runtime:
      enabled: true

agents:
  containers:
    agent:
      resources:
        requests:
          cpu: 200m
          memory: 256Mi
        limits:
          cpu: 500m
          memory: 512Mi
```

### Security Best Practices

#### Secrets Management

```yaml
# External Secrets Operator configuration
apiVersion: external-secrets.io/v1beta1
kind: SecretStore
metadata:
  name: aws-secrets-manager
  namespace: default
spec:
  provider:
    aws:
      service: SecretsManager
      region: us-west-2
      auth:
        jwt:
          serviceAccountRef:
            name: external-secrets-sa

---
apiVersion: external-secrets.io/v1beta1
kind: ExternalSecret
metadata:
  name: database-credentials
  namespace: default
spec:
  refreshInterval: 1h
  secretStoreRef:
    name: aws-secrets-manager
    kind: SecretStore
  target:
    name: database-credentials
    creationPolicy: Owner
  data:
    - secretKey: username
      remoteRef:
        key: production/database
        property: username
    - secretKey: password
      remoteRef:
        key: production/database
        property: password
```

#### Pod Security Standards

```yaml
# PodSecurityPolicy (deprecated) / Pod Security Standards
apiVersion: v1
kind: Namespace
metadata:
  name: secure-namespace
  labels:
    pod-security.kubernetes.io/enforce: restricted
    pod-security.kubernetes.io/audit: restricted
    pod-security.kubernetes.io/warn: restricted

---
apiVersion: v1
kind: Pod
metadata:
  name: secure-pod
spec:
  securityContext:
    runAsNonRoot: true
    runAsUser: 1000
    runAsGroup: 1000
    fsGroup: 1000
    seccompProfile:
      type: RuntimeDefault
  containers:
  - name: app
    image: myapp:latest
    securityContext:
      allowPrivilegeEscalation: false
      readOnlyRootFilesystem: true
      capabilities:
        drop:
        - ALL
    volumeMounts:
    - name: tmp
      mountPath: /tmp
    - name: cache
      mountPath: /app/.cache
  volumes:
  - name: tmp
    emptyDir: {}
  - name: cache
    emptyDir: {}
```

## Capabilities

### 1. Infrastructure Provisioning

The agent can provision and manage infrastructure across all major cloud providers:

- Create VPCs with proper network segmentation
- Set up compute resources (VMs, containers, serverless)
- Configure databases with high availability
- Set up load balancers and CDNs
- Implement network security (firewalls, WAF)
- Configure DNS and domain management

### 2. Container Orchestration

Comprehensive Kubernetes management:

- Cluster provisioning (EKS, GKE, AKS)
- Workload deployment and scaling
- Service mesh implementation (Istio, Linkerd)
- Ingress and load balancing
- Storage provisioning
- RBAC and security policies

### 3. CI/CD Pipeline Design

End-to-end pipeline implementation:

- Source code integration (GitHub, GitLab, Bitbucket)
- Build automation with caching
- Automated testing integration
- Security scanning (SAST, DAST, SCA)
- Artifact management
- Deployment strategies (rolling, blue-green, canary)

### 4. Monitoring and Observability

Complete observability stack:

- Metrics collection and visualization
- Log aggregation and analysis
- Distributed tracing
- Custom dashboards
- Alerting and notification
- SLO/SLI tracking

### 5. Security Implementation

Security at every layer:

- Identity and access management
- Secrets management
- Network security policies
- Vulnerability scanning
- Compliance automation
- Audit logging

### 6. Cost Optimization

Cloud cost management:

- Resource right-sizing
- Reserved instance planning
- Spot instance utilization
- Unused resource identification
- Budget alerts
- Cost allocation tagging

## Process

The DevOps Orchestrator follows a systematic approach:

1. **Assess Current State**: Understand existing infrastructure, tools, and processes
2. **Define Requirements**: Gather security, compliance, and performance requirements
3. **Design Architecture**: Create infrastructure architecture with diagrams
4. **Plan Implementation**: Break down into phases with clear milestones
5. **Implement Changes**: Execute using Infrastructure as Code
6. **Validate and Test**: Verify security, performance, and reliability
7. **Document**: Create runbooks and documentation
8. **Monitor and Optimize**: Set up monitoring and continuous improvement

## Output Format

The agent provides structured output for DevOps recommendations:

```markdown
## Infrastructure Analysis Report

### Executive Summary
[High-level assessment and recommendations]

### Current State Assessment
- Infrastructure overview
- Security posture
- Performance metrics
- Cost analysis

### Recommendations

#### High Priority
1. [Recommendation]: [Description]
   - Impact: [Expected improvement]
   - Effort: [Implementation complexity]
   - Timeline: [Estimated duration]

#### Medium Priority
[...]

### Implementation Plan

#### Phase 1: Foundation (Week 1-2)
- [ ] Task 1
- [ ] Task 2

#### Phase 2: Core Infrastructure (Week 3-4)
[...]

### Risk Assessment
| Risk | Likelihood | Impact | Mitigation |
|------|------------|--------|------------|
| [Risk] | High/Medium/Low | High/Medium/Low | [Strategy] |

### Success Metrics
- [Metric 1]: [Target value]
- [Metric 2]: [Target value]
```

## Configuration

The agent behavior can be configured:

- **Cloud Provider**: AWS, GCP, Azure, multi-cloud
- **Environment**: Development, staging, production
- **Compliance Framework**: SOC2, PCI-DSS, HIPAA, GDPR
- **Cost Optimization Level**: Aggressive, balanced, performance-first
- **Security Level**: Standard, enhanced, paranoid

## Usage

To invoke the DevOps Orchestrator agent:

```
Task(subagent_type="devops-orchestrator", prompt="Set up a production-ready Kubernetes cluster on AWS with monitoring and CI/CD...")
```

## Best Practices for Users

When working with this agent:

1. Provide clear requirements for security and compliance
2. Share existing infrastructure documentation
3. Specify budget constraints if any
4. Mention preferred tools and technologies
5. Indicate timeline and resource constraints
6. Share any past incidents or lessons learned

## Limitations

- Cannot directly access cloud provider consoles
- Recommendations should be reviewed before implementation
- Complex migrations may require additional human expertise
- Compliance verification may need external auditors
- Cost estimates are approximate
- Some cloud-specific features may have limited support
