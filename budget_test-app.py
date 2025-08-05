import streamlit as st
import pandas as pd
import datetime

# --- Budget Manager Class ---
class BudgetManager:
    def __init__(self):
        self.goals = {}
        self.expenses = []
        self.reminders = []

    # Goal operations
    def add_goal(self, name, amount, deadline):
        self.goals[name] = {
            'amount': amount,
            'deadline': deadline,
            'saved': 0
        }

    def update_savings(self, goal_name, amount):
        if goal_name in self.goals:
            self.goals[goal_name]['saved'] += amount
        else:
            st.warning("Goal not found.")

    def get_savings_curve(self, goal_name):
        if goal_name not in self.goals:
            st.warning("Goal not found.")
            return pd.DataFrame()

        goal = self.goals[goal_name]
        today = datetime.date.today()
        deadline = goal['deadline']
        total_days = (deadline - today).days

        if total_days <= 0:
            st.warning("Deadline must be in the future.")
            return pd.DataFrame()

        dates = pd.date_range(start=today, end=deadline)
        daily_saving = goal['amount'] / len(dates)

        curve = pd.DataFrame({
            "Date": dates,
            "Required_Cumulative_Saving": [daily_saving * (i + 1) for i in range(len(dates))],
            "Actual_Saving": [goal['saved']] * len(dates)
        })

        return curve

    # Expense operations
    def add_expense(self, category, amount, date=None):
        date = date or datetime.date.today().isoformat()
        self.expenses.append({'category': category, 'amount': amount, 'date': date})

    def spending_summary(self):
        df = pd.DataFrame(self.expenses)
        if df.empty:
            return {}
        return df.groupby('category')['amount'].sum().to_dict()

    # Reminder operations
    def set_reminder(self, message, date):
        self.reminders.append({'message': message, 'date': date})


# --- Streamlit App ---
def run_budget_app():
    st.title("💰 Dynamic Budget & Savings Planner")

    app = BudgetManager()

    # Goal Setup Section
    st.sidebar.header("🎯 Add or Update Goal")
    goal_name = st.sidebar.text_input("Goal Name")
    goal_amount = st.sidebar.number_input("Target Amount", min_value=0)
    deadline = st.sidebar.date_input("Deadline")

    if st.sidebar.button("Set Goal"):
        app.add_goal(goal_name, goal_amount, deadline)
        st.sidebar.success(f"Goal '{goal_name}' set!")

    # Show Goal Tracker
    if app.goals:
        selected_goal = st.selectbox("Choose a Goal to Track", list(app.goals.keys()))
        new_amount = st.number_input("Update Goal Amount", value=app.goals[selected_goal]['amount'])

        if new_amount != app.goals[selected_goal]['amount']:
            app.goals[selected_goal]['amount'] = new_amount

        st.write(f"📊 Tracking savings for goal: **{selected_goal}**")
        savings_df = app.get_savings_curve(selected_goal)
        if not savings_df.empty:
            st.line_chart(savings_df.set_index("Date")[["Required_Cumulative_Saving", "Actual_Saving"]])

    # Expense Input
    st.sidebar.header("📉 Add Expense")
    expense_cat = st.sidebar.text_input("Category")
    expense_amt = st.sidebar.number_input("Amount", min_value=0)
    if st.sidebar.button("Add Expense"):
        app.add_expense(expense_cat, expense_amt)
        st.sidebar.success(f"Expense '{expense_cat}' added!")

    # Show Spending Summary
    st.subheader("📁 Spending Summary")
    summary = app.spending_summary()
    if summary:
        st.write(summary)
    else:
        st.info("No expenses recorded yet.")

run_budget_app()
