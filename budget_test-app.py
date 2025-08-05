import streamlit as st
import pandas as pd
import datetime

import streamlit as st
import pandas as pd
import datetime
from typing import List, Dict, Any

# --- Budget Manager Class ---
class BudgetManager:
    def __init__(self):
        self.goals: Dict[str, Dict[str, Any]] = {}
        self.expenses: List[Dict[str, Any]] = []
        self.reminders: List[Dict[str, Any]] = []

    # ------------------ Goal Operations ------------------

    def add_goal(self, name: str, amount: float, deadline: datetime.date) -> None:
        """Add a new savings goal."""
        self.goals[name] = {
            'amount': amount,
            'deadline': deadline,
            'saved': 0.0
        }

    def update_savings(self, goal_name: str, amount: float) -> None:
        """Add funds to a savings goal."""
        if goal_name in self.goals:
            self.goals[goal_name]['saved'] += amount
        else:
            st.warning("⚠️ Goal not found.")

    def get_savings_curve(self, goal_name: str) -> pd.DataFrame:
        """Generate savings trajectory considering expenses."""
        if goal_name not in self.goals:
            return pd.DataFrame()

        goal = self.goals[goal_name]
        today = datetime.date.today()
        deadline = goal['deadline']
        total_days = (deadline - today).days

        if total_days <= 0:
            return pd.DataFrame()

        dates = pd.date_range(start=today, end=deadline)
        daily_required = goal['amount'] / len(dates)

        # Build expense DataFrame
        df_exp = pd.DataFrame(self.expenses)
        if not df_exp.empty:
            df_exp['date'] = pd.to_datetime(df_exp['date']).dt.date
            expense_group = df_exp.groupby('date')['amount'].sum().reindex(dates.date, fill_value=0)
            cumulative_expense = expense_group.cumsum()
        else:
            cumulative_expense = pd.Series([0.0] * len(dates), index=dates.date)

        # Calculate adjusted actual savings
        adjusted_saving = goal['saved'] - cumulative_expense

        return pd.DataFrame({
            "Date": dates,
            "Required_Cumulative_Saving": [daily_required * (i + 1) for i in range(len(dates))],
            "Actual_Saving": adjusted_saving.values
        })

    # ------------------ Expense Operations ------------------

    def add_expense(self, category: str, amount: float, date: str = None) -> None:
        """Log an expense under a category."""
        date = date or datetime.date.today().isoformat()
        self.expenses.append({
            'category': category,
            'amount': amount,
            'date': date
        })

    def spending_summary(self) -> Dict[str, float]:
        """Summarize spending by category."""
        df = pd.DataFrame(self.expenses)
        if df.empty:
            return {}
        return df.groupby('category')['amount'].sum().to_dict()

    # ------------------ Reminder Operations ------------------

    def set_reminder(self, message: str, date: datetime.date) -> None:
        """Store a reminder message for a future date."""
        self.reminders.append({
            'message': message,
            'date': date
        })




if app.goals:
    selected_goal = st.selectbox("Choose a Goal to Track", list(app.goals.keys()))
    st.write(f"📊 Tracking adjusted savings for goal: **{selected_goal}**")
    savings_df = app.get_savings_curve(selected_goal)

    if not savings_df.empty:
        st.line_chart(savings_df.set_index("Date")[["Required_Cumulative_Saving", "Actual_Saving"]])
        final_saving = savings_df["Actual_Saving"].iloc[-1]
        goal_amount = app.goals[selected_goal]["amount"]
        if final_saving >= goal_amount:
            st.success("🎉 You're on track to meet your goal despite expenses!")
        elif final_saving < 0:
            st.error("⚠️ Expenses have exceeded savings. Review your spending strategy.")
        else:
            st.info(f"Remaining amount needed: ₹{goal_amount - final_saving:.2f}")
    else:
        st.warning("No savings curve available for the selected goal.")
