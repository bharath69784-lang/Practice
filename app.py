"""Smart Expense Tracker API.

Endpoints:
  GET    /                        health check
  POST   /expenses                add an expense
  GET    /expenses                list all expenses (optional ?category=)
  GET    /expenses/summary        overall total + breakdown by category
  GET    /expenses/total          overall total (optional ?category=)
  GET    /expenses/<id>           get a single expense
  DELETE /expenses/<id>           delete an expense
"""
from flask import Flask, request, jsonify

from src.storage import ExpenseStore
from src.validators import validate_expense_payload


def create_app(store=None):
    app = Flask(__name__)
    app.config["STORE"] = store if store is not None else ExpenseStore()

    @app.get("/")
    def health():
        return jsonify({"status": "ok", "service": "Smart Expense Tracker API"})

    @app.post("/expenses")
    def add_expense():
        data = request.get_json(silent=True)
        is_valid, error = validate_expense_payload(data)
        if not is_valid:
            return jsonify({"error": error}), 400

        expense = app.config["STORE"].add(
            title=data["title"].strip(),
            amount=float(data["amount"]),
            category=data["category"].strip(),
            date=data["date"],
        )
        return jsonify(expense), 201

    @app.get("/expenses")
    def list_expenses():
        category = request.args.get("category")
        expenses = app.config["STORE"].get_all(category=category)
        return jsonify(expenses), 200

    @app.get("/expenses/summary")
    def summary():
        return jsonify(app.config["STORE"].summary()), 200

    @app.get("/expenses/total")
    def total():
        category = request.args.get("category")
        return (
            jsonify(
                {
                    "category": category,
                    "total": app.config["STORE"].total(category=category),
                }
            ),
            200,
        )

    @app.get("/expenses/<expense_id>")
    def get_expense(expense_id):
        expense = app.config["STORE"].get(expense_id)
        if expense is None:
            return jsonify({"error": "Expense not found"}), 404
        return jsonify(expense), 200

    @app.delete("/expenses/<expense_id>")
    def delete_expense(expense_id):
        deleted = app.config["STORE"].delete(expense_id)
        if not deleted:
            return jsonify({"error": "Expense not found"}), 404
        return jsonify({"deleted": True, "id": expense_id}), 200

    @app.errorhandler(404)
    def not_found(e):
        return jsonify({"error": "Not found"}), 404

    return app


if __name__ == "__main__":
    flask_app = create_app()
    flask_app.run(host="0.0.0.0", port=5000, debug=True)
