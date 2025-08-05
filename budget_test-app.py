import streamlit as st
import pandas as pd
import datetime

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
