"""In-memory storage for expenses.

Kept deliberately simple: a dict keyed by expense id. No persistence,
no external database -- everything lives in process memory and resets
when the server restarts.
"""
import uuid


class ExpenseStore:
    def __init__(self):
        self._expenses = {}

    def add(self, title, amount, category, date):
        expense_id = str(uuid.uuid4())
        expense = {
            "id": expense_id,
            "title": title,
            "amount": amount,
            "category": category,
            "date": date,
        }
        self._expenses[expense_id] = expense
        return expense

    def get_all(self, category=None):
        expenses = list(self._expenses.values())
        if category:
            expenses = [
                e for e in expenses if e["category"].lower() == category.lower()
            ]
        # newest first, by date string (YYYY-MM-DD sorts correctly as text)
        return sorted(expenses, key=lambda e: e["date"], reverse=True)

    def get(self, expense_id):
        return self._expenses.get(expense_id)

    def delete(self, expense_id):
        return self._expenses.pop(expense_id, None) is not None

    def total(self, category=None):
        expenses = self.get_all(category=category)
        return round(sum(e["amount"] for e in expenses), 2)

    def summary(self):
        by_category = {}
        for e in self._expenses.values():
            by_category[e["category"]] = by_category.get(e["category"], 0) + e["amount"]
        by_category = {k: round(v, 2) for k, v in by_category.items()}
        return {
            "overall_total": self.total(),
            "by_category": by_category,
        }

    def clear(self):
        self._expenses.clear()
