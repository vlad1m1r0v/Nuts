# 🥜 Nuts — E-Commerce Platform for a Nut Manufacturer

A full-featured, production-oriented e-commerce web application for a Ukrainian nut producer, built on **Django + Wagtail CMS**. It combines a CMS-managed marketing site with a complete storefront: product catalog, session/account shopping cart, checkout, order management, and a simulated payment lifecycle — all wrapped in a multilingual (EN/RU/UK) experience.

![Python](https://img.shields.io/badge/Python-3.13-3776AB?logo=python&logoColor=white)
![Django](https://img.shields.io/badge/Django-5.2-092E20?logo=django&logoColor=white)
![Wagtail](https://img.shields.io/badge/Wagtail-7.2-43B1B0?logo=wagtail&logoColor=white)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-4169E1?logo=postgresql&logoColor=white)
![Redis](https://img.shields.io/badge/Redis-DC382D?logo=redis&logoColor=white)
![Celery](https://img.shields.io/badge/Celery-37814A?logo=celery&logoColor=white)
![Docker](https://img.shields.io/badge/Docker-2496ED?logo=docker&logoColor=white)

---

## About The Project

**Nuts** is a commercial-grade online store for a nut producer and distributor that sells to both end consumers and business buyers (legal entities and individual entrepreneurs / FOPs). The platform solves the classic B2B+B2C e-commerce problem: a single codebase must handle content marketing pages, a filterable product catalog, two account types, and an order-to-payment workflow — without sacrificing maintainability.

It is a **custom solution** built from scratch on top of Wagtail CMS, rather than a clone of an existing storefront engine, which gives the business full editorial control over its site pages while keeping the storefront logic in a clean, modular Django codebase.

## Key Tech Stack

| Layer | Technology |
| --- | --- |
| **Backend** | Python 3.13 · Django 5.2 · Wagtail 7.2 (CMS) · gunicorn |
| **Database** | PostgreSQL (psycopg2) · `django.contrib.postgres` |
| **Caching / Broker** | Redis · Celery 5.6 (worker + beat) |
| **Emails** | django-anymail · Mailjet (transactional HTML emails) |
| **Admin** | django-unfold (modern admin theme) · Wagtail admin |
| **i18n** | wagtail-modeltranslation · django-modeltranslation (EN/RU/UK) |
| **Frontend** | Vite 7 · django-vite · Sass/SCSS · jQuery · htmx 2.0 |
| **DevOps** | Docker · Poetry · `manage.py` based CI-ready workflows |

## Core Features

- **CMS-powered marketing site** — home, about, news, gallery, customers, payment & delivery, and thank-you pages built with Wagtail `Page` models and `StreamField` blocks (image/video jumbotrons, statistics).
- **Product catalog** — searchable product pages with SKU, weight, calories, shelf life, ingredients, features (flavor tags), gallery images, and optional discounts (`discounted_price`).
- **Catalog filtering & sorting** — filter by product feature and weight range; sort by actual (discounted-aware) price.
- **Shopping cart** — session-based for guests and account-bound for registered users, with htmx-powered live popup, counter, and table partials (`HX-Trigger: cartUpdated`).
- **Cart merging** — anonymous carts are merged into the user's cart (quantities combined) atomically at registration/login.
- **Dual-account registration** — individual and business (Legal Entity / FOP) registration flows with profile-specific forms and validation.
- **Email-based authentication** — custom `CustomerAuthBackend` (login with email + password), signed-token password reset (`PasswordResetTokenGenerator` subclass), HTML emails via Mailjet.
- **Checkout & orders** — checkout page with prefilled profile data, order + order items inline formset, transactional order creation with price snapshots.
- **Order/payment state machine** — `NEW → PROCESSING → PAID → SHIPPED → COMPLETED/CANCELED/FAILED` lifecycle simulated by a scheduled Celery beat task.
- **Site-wide settings** — company info, social links, discount banner, statistics, and contact details managed from the Wagtail admin.
- **Multilingual** — EN/RU/UK content translation with locale-prefixed URLs (`i18n_patterns`).

## Architecture & Engineering Highlights

- **Modular monolith** — ~18 focused Django apps (`products`, `cart`, `orders`, `auth`, `profiles`, `locations`, `payment_transactions`, etc.), each with its own models, views, forms, admin, tests, and migrations (65 migrations).
- **Custom manager + annotated queries** — `CartQuerySet` computes per-item `actual_price` (fallback from `discounted_price` to `price` via `Case/When`) and cart totals with `ExpressionWrapper`, minimizing Python-side math and N+1 queries (`prefetch_related`).
- **Wagtail page-driven e-commerce** — storefront flows (shop, cart, checkout) are modeled as Wagtail `Page` subclasses, letting editors place content while business logic lives in dedicated Django `View` classes.
- **Price snapshotting** — `OrderItem` stores `price` at the moment of ordering (`on_delete=PROTECT`), so historical orders are immune to later catalog changes.
- **Guarded checkout** — `CustomerProfileRequiredMixin` redirects anonymous/staff users to the login page before they reach checkout.
- **Asynchronous background work** — Celery beat schedules `orders.tasks.simulate_order_processing` every 10 seconds; the task drives the order and `PaymentTransaction` lifecycle inside `transaction.atomic()` blocks.
- **Custom admin experience** — django-unfold with custom list filters (multi-select features, price range, weight range), inline product images, and tabbed translation fields.
- **Security & data integrity** — atomic transactions for multi-model writes (registration, checkout, cart merge), Ukrainian phone-number validation, signed reset tokens, and site-wide password validators.

## Quick Start

### Prerequisites

- **Python 3.13+** and **Poetry**
- **PostgreSQL** (15+) and **Redis**
- **Node.js 20+** and **npm** (frontend build)
- **Docker** (optional, containerized deployment)

### 1. Clone & install dependencies

```bash
git clone git@github.com:vlad1m1r0v/Nuts.git
cd Nuts
python3.13 -m venv .venv && source .venv/bin/activate
poetry install
```

> The Docker image expects a `requirements.txt`; generate it from Poetry before a container build:
> `poetry export -f requirements.txt --output requirements.txt`

### 2. Configure environment

Copy the template and fill in every variable (`settings/base.py` reads them via `django-environ`):

```bash
cp .env.example .env
```

```dotenv
# Django
SECRET_KEY=your-secret-key

# PostgreSQL
POSTGRES_HOST=127.0.0.1
POSTGRES_PORT=5432
POSTGRES_USER=nuts
POSTGRES_PASSWORD=change-me
POSTGRES_DB=nuts

# Celery / Redis (also required by settings/base.py)
CELERY_BROKER_URL=redis://127.0.0.1:6379/0
CELERY_RESULT_BACKEND=redis://127.0.0.1:6379/0

# Mailjet (optional — used by ANYMAIL email backend)
MAILJET_API_KEY=
MAILJET_SECRET_KEY=
DEFAULT_FROM_EMAIL=
```

### 3. Prepare the database & admin

```bash
python manage.py migrate
python manage.py createsuperuser
```

### 4. Run the frontend (Vite dev server)

```bash
cd frontend
npm install
npm run dev   # serves on http://localhost:5173
```

### 5. Run the app

```bash
python manage.py runserver            # app (dev)
celery -A nuts worker -l info          # async worker
celery -A nuts beat -l info            # order/payment simulator scheduler
```

Open http://localhost:8000 — Wagtail CMS admin lives at `/admin/`, the Django (unfold) admin at `/unfold/`.

### 6. Docker (single-container app)

The repository ships a **production Dockerfile** for the Django app (Python 3.12-slim, gunicorn, `collectstatic`, auto-migrate on start):

```bash
docker build -t nuts:latest .
docker run -p 8000:8000 --env-file .env nuts:latest
```

> **Note:** a full `docker-compose.yml` (app + PostgreSQL + Redis) is not committed yet. A minimal orchestration example:

```yaml
services:
  db:
    image: postgres:16-alpine
    environment:
      POSTGRES_DB: ${POSTGRES_DB}
      POSTGRES_USER: ${POSTGRES_USER}
      POSTGRES_PASSWORD: ${POSTGRES_PASSWORD}
  redis:
    image: redis:7-alpine
  web:
    build: ./nuts
    command: gunicorn nuts.wsgi:application
    ports:
      - "8000:8000"
    env_file: .env
    depends_on: [db, redis]
```

## API Endpoints Overview

> **Note:** This is a server-rendered Django/Wagtail application — there is **no REST API** and therefore no Swagger/ReDoc (`/docs`) endpoint. The "API" surface consists of the HTML application routes and the htmx partial endpoints listed below.

| Method | Endpoint | Description |
| --- | --- | --- |
| `POST` | `/auth/login/` | Customer login (email + password) |
| `POST` | `/auth/registration/individual/` | Individual account registration |
| `POST` | `/auth/registration/business/` | Business (Legal Entity / FOP) registration |
| `POST` | `/cart/add-item/<product_id>/` | Add product to cart (htmx partial) |
| `POST` | `/cart/update-item/<item_id>/<action>/` | Update quantity or remove cart item (`plus` / `minus` / `remove`) |
| `GET` | `/cart/popup/`, `/cart/counter/`, `/cart/table/` | Live cart popup, item counter, and table partials |
| `POST` | `/orders/create/` | Create order from the checkout page |
| `GET` | `/search/` | Site search (placeholder — see Roadmap) |

All shop/auth/cart/order routes are wrapped in `i18n_patterns` and are therefore locale-prefixed (e.g. `/en/shop/`, `/uk/shop/`).

## Future Roadmap

1. **Real payment gateway integration** — replace the simulated Celery-beat transaction lifecycle with actual LiqPay (already present in `PaymentMethod` choices) / bank-transfer settlement and idempotent payment callbacks.
2. **Full-text product search** — implement the current `/search/` stub with a Postgres full-text backend (or Elasticsearch) covering product names, ingredients, and features.
3. **Hardened delivery & DevOps** — commit a full `docker-compose.yml` (app + PostgreSQL + Redis + Celery), add CI/CD (lint + test matrix via GitHub Actions), and expand automated test coverage for the cart and order workflows.

---

*Dependencies are managed with Poetry (`pyproject.toml`). No license is specified yet.*
