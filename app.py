"""A deliberately small Leave Management application used for DevOps learning."""

import os
from datetime import date

from flask import Flask, jsonify, render_template, request


EMPLOYEES = [
    {"id": 1, "name": "Asha Patel", "department": "Engineering"},
    {"id": 2, "name": "Ravi Kumar", "department": "Operations"},
    {"id": 3, "name": "Meera Singh", "department": "Finance"},
]


def create_app(test_config=None):
    """Create the Flask app so tests can use an isolated application instance."""
    app = Flask(__name__)
    app.config.from_mapping(LEAVE_REQUESTS=[])

    if test_config:
        app.config.update(test_config)

    @app.get("/")
    def index():
        return render_template("index.html")

    @app.get("/api/health")
    def health_check():
        return jsonify(status="healthy")

    @app.get("/api/employees")
    def list_employees():
        return jsonify(employees=EMPLOYEES)

    @app.get("/api/leaves")
    def list_leave_requests():
        return jsonify(leaves=app.config["LEAVE_REQUESTS"])

    @app.post("/api/leaves")
    def create_leave_request():
        payload = request.get_json(silent=True) or {}
        required_fields = ("employee_id", "start_date", "end_date", "reason")
        missing_fields = [field for field in required_fields if not payload.get(field)]

        if missing_fields:
            return jsonify(error=f"Missing required fields: {', '.join(missing_fields)}"), 400

        if not any(employee["id"] == payload["employee_id"] for employee in EMPLOYEES):
            return jsonify(error="Employee does not exist"), 400

        try:
            start_date = date.fromisoformat(payload["start_date"])
            end_date = date.fromisoformat(payload["end_date"])
        except ValueError:
            return jsonify(error="Dates must use YYYY-MM-DD format"), 400

        if end_date < start_date:
            return jsonify(error="End date cannot be before start date"), 400

        leave_requests = app.config["LEAVE_REQUESTS"]
        leave = {
            "id": len(leave_requests) + 1,
            "employee_id": payload["employee_id"],
            "start_date": payload["start_date"],
            "end_date": payload["end_date"],
            "reason": payload["reason"],
            "status": "pending",
        }
        leave_requests.append(leave)
        return jsonify(leave), 201

    return app


app = create_app()


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.getenv("PORT", "5050")), debug=True)
