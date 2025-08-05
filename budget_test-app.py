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

    def get_savings_curve(self, goal_name):
        if goal_name not in self.goals:
            return pd.DataFrame()

        goal = self.goals[goal_name]
        today = datetime.date.today()
        deadline = goal['deadline']
        total_days = (deadline - today).days

        if total_days <= 0:
            return pd.DataFrame()

        dates = pd.date_range(start=today, end=deadline)
        daily_saving = goal['amount'] / len(dates)

        curve = pd.DataFrame({
            "Date": dates,
            "Required_Cumulative_Saving": [daily_saving * (i + 1) for i in range(len(dates))],
            "Actual_Saving": [goal['saved']] * len(dates)
        })

        return curve

    def calculate_required_daily_saving(self, goal_name, earnings, start_date):
        if goal_name not in self.goals:
            return "Goal not found."

        goal = self.goals[goal_name]
        end_date = goal['deadline']
        today = datetime.date.today()
        start_date = max(start_date, today)

        # Filter expenses within the timeline
        df_expenses = pd.DataFrame(self.expenses)
        df_expenses['date'] = pd.to_datetime(df_expenses['date']).dt.date
        expenses_in_range = df_expenses[
            (df_expenses['date'] >= start_date) & (df_expenses['date'] <= end_date)
        ]['amount'].sum()

        # Net savings potential
        net_available = earnings - expenses_in_range + goal['saved']
        remaining_needed = max(goal['amount'] - net_available, 0)

        total_days = (end_date - start_date).days
        if total_days <= 0:
            return "Invalid timeline."

        daily_required = remaining_needed / total_days
        return round(daily_required, 2)

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

    def get_reminders(self):
        today = datetime.date.today()
        return [r for r in self.reminders if r['date'] >= today]

# --- Streamlit App ---
def run_budget_app():
    st.title("💰 Dynamic Budget & Savings Planner")

    app = BudgetManager()

    # --- Goal Setup ---
    st.sidebar.header("🎯 Add or Update Goal")
    goal_name = st.sidebar.text_input("Goal Name")
    goal_amount = st.sidebar.number_input("Target Amount", min_value=0)
    deadline = st.sidebar.date_input("Deadline")

    if st.sidebar.button("Set Goal"):
        app.add_goal(goal_name, goal_amount, deadline)
        st.sidebar.success(f"Goal '{goal_name}' set!")

    # --- Savings Update ---
    if app.goals:
        selected_goal = st.selectbox("Choose a Goal to Track", list(app.goals.keys()))
        update_amount = st.number_input("Add to Savings", min_value=0.0, step=0.01)
        if st.button("Update Savings"):
            app.update_savings(selected_goal, update_amount)
            st.success("Savings updated!")

        # --- Display Savings Curve ---
        st.write(f"📊 Tracking savings for goal: **{selected_goal}**")
        savings_df = app.get_savings_curve(selected_goal)
        if not savings_df.empty:
            st.line_chart(savings_df.set_index("Date")[["Required_Cumulative_Saving", "Actual_Saving"]])

        # --- Progress Bar ---
        goal = app.goals[selected_goal]
        progress = goal['saved'] / goal['amount'] if goal['amount'] > 0 else 0
        st.progress(progress)
        if progress >= 1.0:
            st.balloons()
            st.success("🎉 Goal reached!")

        # --- Daily Saving Requirement ---
        st.subheader("📈 Daily Savings Estimator")
        income = st.number_input("Total Earnings in Goal Timeline", min_value=0)
        start_date = st.date_input("Start Date")
        daily_needed = app.calculate_required_daily_saving(selected_goal, income, start_date)
        st.info(f"Required Daily Saving: ₹{daily_needed}")

    # --- Expense Entry ---
    st.sidebar.header("📉 Add Expense")
    expense_cat = st.sidebar.text_input("Category")
    expense_amt = st.sidebar.number_input("Amount", min_value=0)
    if st.sidebar.button("Add Expense"):
        app.add_expense(expense_cat, expense_amt)
        st.sidebar.success(f"Expense '{expense_cat}' added!")

    # --- Spending Summary ---
    st.subheader("📁 Spending Summary")
    summary = app.spending_summary()
    if summary:
        st.write(pd.DataFrame.from_dict(summary, orient='index', columns=["Total Spent"]))
    else:
        st.info("No expenses recorded yet.")

    # --- Reminders ---
    st.sidebar.header("⏰ Set Reminder")
    reminder_text = st.sidebar.text_input("Reminder Message")
    reminder_date = st.sidebar.date_input("Reminder Date")
    if st.sidebar.button("Add Reminder"):
        app.set_reminder(reminder_text, reminder_date)
        st.sidebar.success("Reminder set!")

    st.subheader("📌 Upcoming Reminders")
    reminders = app.get_reminders()
    if reminders:
        st.write(pd.DataFrame(reminders))
    else:
        st.info("No upcoming reminders.")

# Run the app
if __name__ == "__main__":
    run_budget_app()


