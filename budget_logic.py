import datetime
import json

class BudgetApp:
    def __init__(self):
        self.goals = {}
        self.expenses = []
        self.reminders = []

    def set_goal(self, name, amount, deadline):
        self.goals[name] = {
            'amount': amount,
            'deadline': deadline,
            'saved': 0
        }
        print(f"Goal '{name}' set for ${amount} by {deadline}.")

    def add_expense(self, category, amount, date=None):
        if not date:
            date = datetime.date.today().isoformat()
        self.expenses.append({'category': category, 'amount': amount, 'date': date})
        print(f"Added expense: {category} - ${amount} on {date}")

    def add_savings(self, goal_name, amount):
        if goal_name in self.goals:
            self.goals[goal_name]['saved'] += amount
            print(f"Added ${amount} to '{goal_name}'. Total saved: ${self.goals[goal_name]['saved']}")
        else:
            print("Goal not found.")

    def set_reminder(self, message, date):
        self.reminders.append({'message': message, 'date': date})
        print(f"Reminder set for {date}: {message}")

    def analyze_spending(self):
        summary = {}
        for exp in self.expenses:
            summary[exp['category']] = summary.get(exp['category'], 0) + exp['amount']
        print("Spending Analysis:")
        for cat, amt in summary.items():
            print(f"{cat}: ${amt}")

    def show_goals(self):
        print("Goals:")
        for name, data in self.goals.items():
            print(f"{name} - Target: ${data['amount']}, Deadline: {data['deadline']}, Saved: ${data['saved']}")

    def show_reminders(self):
        print("Reminders:")
        for reminder in self.reminders:
            print(f"{reminder['date']}: {reminder['message']}")

def main():
    app = BudgetApp()
    while True:
        cmd = input("Enter command: ").strip()
        if cmd == 'set_goal':
            name = input("Goal name: ")
            amount = float(input("Goal amount: "))
            deadline = input("Deadline (YYYY-MM-DD): ")
            app.set_goal(name, amount, deadline)
        elif cmd == 'add_expense':
            category = input("Expense category: ")
            amount = float(input("Amount: "))
            app.add_expense(category, amount)
        elif cmd == 'add_savings':
            goal_name = input("Goal name: ")
            amount = float(input("Amount to add: "))
            app.add_savings(goal_name, amount)
        elif cmd == 'set_reminder':
            message = input("Reminder message: ")
            date = input("Reminder date (YYYY-MM-DD): ")
            app.set_reminder(message, date)
        elif cmd == 'analyze_spending':
            app.analyze_spending()
        elif cmd == 'show_goals':
            app.show_goals()
        elif cmd == 'show_reminders':
            app.show_reminders()
        elif cmd == 'quit':
            print("Goodbye!")
            break
        else:
            print("Unknown command.")

if __name__ == "__main__":
    main()
