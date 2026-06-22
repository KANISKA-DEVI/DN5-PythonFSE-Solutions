# ============================================================
# Hands-On 1: Web Framework Foundations
# File: notes.py
# ============================================================

# ---- TASK 1: Request-Response Cycle ----

# Journey of GET /api/courses/ through Django:
#
# 1. Browser sends HTTP GET request to http://127.0.0.1:8000/api/courses/
#
# 2. URL ROUTER (coursemanager/urls.py):
#    Django reads urls.py and matches the path 'api/courses/' to a view function.
#
# 3. MIDDLEWARE (sits between the router and the view):
#    Middleware runs BEFORE the view (request processing) and AFTER the view (response processing).
#    Examples:
#    - SecurityMiddleware: enforces HTTPS, sets security headers
#    - SessionMiddleware: manages user sessions using cookies
#    - AuthenticationMiddleware: attaches request.user to every request
#
# 4. VIEW (courses/views.py):
#    The matched view function receives the request object.
#    It queries the database via the Model layer.
#
# 5. MODEL (courses/models.py):
#    Django ORM translates Python code to SQL.
#    e.g., Course.objects.all() → SELECT * FROM courses_course;
#    Returns Python objects.
#
# 6. VIEW constructs a Response:
#    Serializes the Python objects to JSON.
#    Returns HttpResponse or JsonResponse.
#
# 7. Browser receives the JSON response and renders it.

# ---- WSGI vs ASGI ----
#
# WSGI (Web Server Gateway Interface):
#   - The traditional Python web server standard.
#   - Synchronous: handles one request at a time per worker process.
#   - Django uses WSGI by default (wsgi.py is generated automatically).
#   - Good for: standard web apps, REST APIs without real-time features.
#
# ASGI (Asynchronous Server Gateway Interface):
#   - The modern async Python web server standard.
#   - Supports async/await, WebSockets, long-polling.
#   - Django supports ASGI since version 3.0 (asgi.py is generated).
#   - Switch to ASGI when you need: WebSockets, SSE, high concurrency async endpoints.

# ---- MVC vs Django MVT ----
#
# MVC (used by Rails, Laravel, Spring):
#   M = Model        → handles data and business logic
#   V = View         → HTML template shown to user
#   C = Controller   → receives request, calls model, returns response
#
# Django MVT:
#   M = Model        → same as MVC Model (courses/models.py)
#   V = View         → does what the Controller does in MVC (courses/views.py)
#   T = Template     → does what the View does in MVC (HTML files)
#
# Confusing? Yes. Django's "View" = MVC's "Controller". Django's "Template" = MVC's "View".