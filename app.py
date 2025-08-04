import streamlit as st
from budget_logic import BudgetApp
import datetime
import json

app = BudgetApp()

st.title("💰 Budget Tracker")

# --- Set Goal Section ---
st.header("🎯 Set a Financial Goal")
with st.form("goal_form"):
    name = st.text_input("Goal Name")
    amount = st.number_input("Target Amount", min_value=0.0, step=100.0)
    deadline = st.date_input("Deadline")
    submit_goal = st.form_submit_button("Set Goal")

    if submit_goal:
        msg = app.set_goal(name, amount, str(deadline))
        st.success(f"Goal '{name}' set for ₹{amount:.2f} by {deadline}")

# --- Add Expense Section ---
st.header("🧾 Add an Expense")
with st.form("expense_form"):
    category = st.text_input("Category")
    exp_amount = st.number_input("Amount", min_value=0.0, step=10.0)
    exp_date = st.date_input("Date", value=datetime.date.today())
    submit_expense = st.form_submit_button("Add Expense")

    if submit_expense:
        app.add_expense(category, exp_amount, str(exp_date))
        st.success(f"Added ₹{exp_amount:.2f} under {category} on {exp_date}")

# --- Add Savings ---
st.header("📥 Contribute to Savings")
with st.form("savings_form"):
    goal_choice = st.selectbox("Select Goal", options=list(app.goals.keys()) or ["(none)"])
    savings_amt = st.number_input("Amount to Save", min_value=0.0, step=50.0)
    submit_savings = st.form_submit_button("Add Savings")

    if submit_savings and goal_choice != "(none)":
        app.add_savings(goal_choice, savings_amt)
        st.success(f"Saved ₹{savings_amt:.2f} towards '{goal_choice}'")

# --- Set Reminder ---
st.header("⏰ Set a Reminder")
with st.form("reminder_form"):
    reminder_text = st.text_input("Reminder Message")
    reminder_date = st.date_input("Reminder Date")
    submit_reminder = st.form_submit_button("Set Reminder")

    if submit_reminder:
        app.set_reminder(reminder_text, str(reminder_date))
        st.success(f"Reminder set for {reminder_date}: {reminder_text}")

# --- Show Goals ---
st.header("📌 Your Goals")
if app.goals:
    for name, data in app.goals.items():
        st.write(f"- **{name}** → ₹{data['saved']:.2f} / ₹{data['amount']} by {data['deadline']}")
else:
    st.info("No goals set yet.")

# --- Show Spending Summary ---
st.header("📊 Spending Analysis")
if app.expenses:
    category_totals = {}
    for exp in app.expenses:
        category_totals[exp["category"]] = category_totals.get(exp["category"], 0) + exp["amount"]
    for cat, amt in category_totals.items():
        st.write(f"- **{cat}**: ₹{amt:.2f}")
else:
    st.info("No expenses recorded.")

# --- Show Reminders ---
st.header("📅 Reminders")
if app.reminders:
    for reminder in app.reminders:
        st.write(f"- {reminder['date']}: {reminder['message']}")
else:
    st.info("No reminders set.")



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
