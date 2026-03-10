# WarehousePro

Warehouse Inventory Management System

## Features

- **User Authentication** — Register, login, logout, user profiles
- **Product Management** — Full CRUD for products with categories, suppliers, pricing
- **Purchase Orders** — Create and manage purchase orders with line items
- **Sales Orders** — Create and manage sales orders with line items
- **Stock Dashboard** — Real-time stock levels, low stock alerts, recent movements
- **Auto Stock Movements** — Stock auto-updates when PO is received or SO is shipped
- **Admin Panel** — Full Django admin for all models

## Tech Stack

- **Backend:** Django 6.0, Gunicorn
- **Database:** PostgreSQL 16
- **Containerization:** Docker, Docker Compose
- **CI/CD:** GitHub Actions
- **Deployment:** Google Cloud Platform (GCP)

## Database Schema

| Model | Relationships |
|-------|--------------|
| Category | One-to-Many → Product |
| Supplier | Many-to-Many ↔ Product |
| Customer | One-to-Many → SalesOrder |
| Product | FK → Category, M2M → Supplier |
| PurchaseOrder | FK → Supplier, FK → User |
| PurchaseOrderItem | FK → PurchaseOrder, FK → Product |
| SalesOrder | FK → Customer, FK → User |
| SalesOrderItem | FK → SalesOrder, FK → Product |
| StockMovement | FK → Product, FK → User |

## Local Setup

### Prerequisites

- Python 3.12+
- Docker & Docker Compose

### Option 1: Docker (Recommended)

```bash
# Clone the repository
git clone https://github.com/00015972/warehousepro.git
cd warehousepro

# Start all services
docker compose up -d --build

# Run migrations
docker compose exec web python manage.py migrate

# Create superuser
docker compose exec web python manage.py createsuperuser

# App available at http://localhost:8090
```

### Option 2: Local Development

```bash
# Clone and enter project
git clone https://github.com/00015972/warehousepro.git
cd warehousepro

# Create virtual environment
python3 -m venv .venv
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run migrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser

# Start dev server
python manage.py runserver
```

## Testing

```bash
# Run all tests
pytest

# Run tests with verbose output
pytest -v

# Run specific test file
pytest stock/tests/test_stock.py
```

Test coverage includes:
- Stock calculation logic
- Stock movement IN/OUT operations
- Low stock detection
- Multiple movements aggregation

## CI/CD Pipeline

GitHub Actions workflow runs automatically on push to `main`:

1. **Code Quality Check** - Runs `flake8` linting
2. **Run Tests** - Executes `pytest` test suite
3. **Build & Push Docker Image** - Builds and pushes to Docker Hub
4. **Deploy to Server** - SSH deployment to production server

View the workflow: `.github/workflows/deploy.yml`

## Production Deployment

### Server Setup

1. **Provision server** (GCP, AWS, etc.)
2. **Install Docker & Docker Compose**
3. **Configure firewall** (ports 22, 80, 443)
4. **Clone repository**

```bash
git clone https://github.com/00015972/warehousepro.git
cd warehousepro
```

```bash
docker compose up -d --build
```

## Live Deployment

**Production URL:** https://warehousepro.ddns.net/  
**Admin Panel:** https://warehousepro.ddns.net/admin/

### Test Credentials

| Role | Username | Password |
|------|----------|----------|
| Admin | `admin` | `admin123` |
| User | `manager` | `whatisgoing123` |

## Project Structure

```
warehousepro/
├── accounts/          # User authentication app
├── config/            # Django settings
├── inventory/         # Products, categories, suppliers
├── orders/            # Purchase & sales orders
├── stock/             # Stock movements & tracking
├── templates/         # HTML templates
├── nginx/             # Nginx configuration
├── .github/workflows/ # CI/CD pipeline
├── Dockerfile         # Multi-stage Docker build
├── docker-compose.yml # Service orchestration
├── requirements.txt   # Python dependencies
└── manage.py          # Django management script
```


**Database connection error:**
```bash
# Check if PostgreSQL container is running
docker compose ps

# Check logs for database container