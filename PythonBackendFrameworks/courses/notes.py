"""
HANDS-ON 1 - TASK 1
Request-Response Cycle, Middleware, WSGI vs ASGI, MVC vs MVT
"""

# ─────────────────────────────────────────────
# 1. REQUEST-RESPONSE CYCLE
# ─────────────────────────────────────────────
# Journey of a GET /api/courses/ request through Django:
#
# Browser sends GET /api/courses/
#       ↓
# Django URL Router (urls.py)
#       → matches the URL pattern to a View
#       ↓
# View (views.py / CourseViewSet)
#       → receives the request
#       → calls the Model to fetch data
#       ↓
# Model (Course.objects.all())
#       → Django ORM translates this to SQL
#       → SQL runs against the database
#       → rows are returned as Python objects
#       ↓
# View (continued)
#       → passes Python objects to Serializer
#       → Serializer converts them to JSON
#       ↓
# Response
#       → JSON sent back to the browser as an HTTP response


# ─────────────────────────────────────────────
# 2. MIDDLEWARE
# ─────────────────────────────────────────────
# Middleware sits BETWEEN the request arriving and the View running,
# and again between the View's response and it leaving Django.
# Every middleware runs on EVERY request, in order, before the URL router
# hands off to the view, and again (in reverse order) on the way out.
#
# Two built-in Django middleware classes:
#
# 1. SecurityMiddleware
#    - Enforces HTTPS redirects
#    - Sets security-related HTTP headers (e.g. HSTS, X-Content-Type-Options)
#
# 2. SessionMiddleware
#    - Manages user sessions across requests
#    - Attaches request.session so views can read/write session data


# ─────────────────────────────────────────────
# 3. WSGI vs ASGI
# ─────────────────────────────────────────────
# WSGI (Web Server Gateway Interface):
#    - Synchronous standard for Python web servers
#    - Handles ONE request at a time per worker
#    - Django's DEFAULT interface (wsgi.py)
#
# ASGI (Asynchronous Server Gateway Interface):
#    - Asynchronous standard, can handle many requests concurrently
#    - Needed for WebSockets, long-lived connections, and async views
#    - Django supports this via asgi.py, but it is OPT-IN, not default
#
# When to switch to ASGI:
#    - When the app needs WebSockets (real-time chat, live notifications)
#    - When using async views / async ORM calls for high-concurrency workloads
#    - NOT needed for simple CRUD APIs like this Course Management API


# ─────────────────────────────────────────────
# 4. MVC vs DJANGO'S MVT
# ─────────────────────────────────────────────
# MVC (Model-View-Controller) - traditional pattern:
#    - Model      → manages data and business logic
#    - View       → what the user sees (UI)
#    - Controller → handles input, talks to Model, picks a View
#
# Django's MVT (Model-View-Template):
#    - Model    → SAME as MVC's Model (data & DB logic)
#    - Template → equivalent to MVC's View (what the user sees - HTML/JSON)
#    - View     → equivalent to MVC's Controller (business logic, request handling)
#
# Mapping:
#    MVC Model      == Django Model
#    MVC View       == Django Template
#    MVC Controller == Django View
#
# In other words: Django's "View" does the job of a Controller.
# The naming overlap is just a historical naming difference, not a different pattern.