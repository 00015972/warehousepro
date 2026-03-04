# WarehousePro

Warehouse Inventory Management System built with Django, containerized with Docker, and deployed with CI/CD.

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

## Live Deployment
The application is live at: http://35.235.104.253/