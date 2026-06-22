# ============================================================
# API Gateway — routes requests to the correct microservice
# Port 5000 — single entry point for all clients
#
# Trade-offs: Synchronous (HTTP) vs Asynchronous (Message Queue):
#
# Synchronous (what we use here):
#   + Simple to implement and debug
#   + Immediate response — client waits for result
#   - Tight coupling: if Course Service is down, enrollment fails
#   - Latency adds up across multiple service calls
#
# Asynchronous (RabbitMQ/Kafka):
#   + Loose coupling: Student Service sends a message and moves on
#   + Resilient: messages queue up if Course Service is temporarily down
#   - Eventual consistency: enrollment confirmed before course verified
#   - More complex infrastructure
#
# Use message queues for: notifications, email, audit logs, analytics
# Use synchronous HTTP for: real-time validation, immediate confirmation
# ============================================================
from flask import Flask, request, jsonify, Response
import requests

app = Flask(__name__)

COURSE_SERVICE_URL  = "http://localhost:5001"
STUDENT_SERVICE_URL = "http://localhost:5002"


def proxy_request(target_url: str):
    """Forward the incoming request to the target service."""
    method  = request.method
    headers = {k: v for k, v in request.headers if k != 'Host'}
    data    = request.get_data()
    params  = request.args

    try:
        response = requests.request(
            method  = method,
            url     = target_url,
            headers = headers,
            data    = data,
            params  = params,
            timeout = 10
        )
        return Response(
            response.content,
            status      = response.status_code,
            headers     = dict(response.headers)
        )
    except requests.ConnectionError:
        return jsonify({"error": "Service unavailable"}), 503


# Route /api/courses/* → Course Service
@app.route('/api/courses/', defaults={'path': ''}, methods=['GET', 'POST'])
@app.route('/api/courses/<path:path>',              methods=['GET', 'PUT', 'DELETE'])
def route_to_course_service(path):
    target = f"{COURSE_SERVICE_URL}/api/courses/{path}"
    print(f"[Gateway] Routing to Course Service: {target}")
    return proxy_request(target)


# Route /api/students/* → Student Service
@app.route('/api/students/', defaults={'path': ''}, methods=['GET', 'POST'])
@app.route('/api/students/<path:path>',              methods=['GET', 'PUT', 'DELETE', 'POST'])
def route_to_student_service(path):
    target = f"{STUDENT_SERVICE_URL}/api/students/{path}"
    print(f"[Gateway] Routing to Student Service: {target}")
    return proxy_request(target)


@app.route('/')
def health():
    return jsonify({
        "service":  "API Gateway",
        "port":     5000,
        "routes": {
            "/api/courses/*":  "→ Course Service (port 5001)",
            "/api/students/*": "→ Student Service (port 5002)"
        }
    })


if __name__ == '__main__':
    print("API Gateway running on port 5000")
    app.run(port=5000, debug=True)