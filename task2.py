"""
DecodeLabs Internship - Task 2: EXPENSE TRACKER
--------------------------------------------------
Goal: Let users enter expense amounts (e.g., 100, 50, 20).
      The program adds them up and displays the Total Spent.
Key Skill: Math operations & the Accumulator Pattern
           (total = total + new_expense)

IPO Model:
    Input   -> user types an expense amount
    Process -> amount is validated, then added to a running total
               (the "accumulator") and stored in a list for the record
    Output  -> running total shown after each entry, final summary at the end

Defensive coding notes (the "gatekeeper"):
    - Non-numeric input is rejected instead of crashing the program.
    - Negative numbers are rejected (an expense can't be negative).
    - "done"/"exit" acts as the kill switch to stop entry and see the summary.
"""

import json
import os

FILE_NAME = "expenses.json"   # persistence, same idea as Project 1


# -------------------- Persistence helpers --------------------

def load_expenses():
    """Load previously saved expenses, or start fresh with an empty list."""
    if os.path.exists(FILE_NAME):
        with open(FILE_NAME, "r") as f:
            return json.load(f)
    return []


def save_expenses(expenses):
    """Save the expenses list to disk so nothing is lost between runs."""
    with open(FILE_NAME, "w") as f:
        json.dump(expenses, f, indent=4)


# -------------------- Core Logic --------------------

def get_expense_input():
    """
    Ask the user for one expense amount.
    Returns a float, or None if the user wants to stop.
    This is the 'gatekeeper' - it never lets bad data through.
    """
    raw = input("Enter an expense amount (or type 'done' to finish): ").strip()

    if raw.lower() in ("done", "exit", "quit"):
        return None  # kill switch

    try:
        amount = float(raw)
    except ValueError:
        print("⚠️ That's not a valid number. Try again.")
        return get_expense_input()

    if amount < 0:
        print("⚠️ Expenses can't be negative. Try again.")
        return get_expense_input()

    return amount


def add_expense(expenses, amount):
    """Append the new expense to the record (the 'ledger')."""
    expenses.append(amount)
    print(f"✅ Added expense: {amount:.2f}")


def calculate_total(expenses):
    """
    THE ACCUMULATOR PATTERN:
    Start a total at 0, then loop through every expense and add it in.
    total = total + new_expense
    """
    total = 0
    for expense in expenses:
        total = total + expense   # <-- the accumulator in action
    return total


def show_summary(expenses):
    """Display every expense plus the final accumulated total."""
    print("\n--- EXPENSE SUMMARY ---")
    if not expenses:
        print("No expenses recorded.")
    else:
        for i, expense in enumerate(expenses, start=1):
            print(f"{i}. {expense:.2f}")
    total = calculate_total(expenses)
    print("------------------------")
    print(f"💰 TOTAL SPENT: {total:.2f}")
    print("------------------------\n")
    return total


# -------------------- Main Program --------------------

def main():
    expenses = load_expenses()  # restore any expenses saved from before

    print("========= DECODELABS EXPENSE TRACKER =========")
    print("Enter your expenses one at a time.")
    print("Type 'done' when you're finished.\n")

    running_total = calculate_total(expenses)
    if expenses:
        print(f"(Loaded {len(expenses)} saved expense(s). Running total so far: {running_total:.2f})\n")

    while True:
        amount = get_expense_input()

        if amount is None:   # kill switch triggered
            break

        add_expense(expenses, amount)
        running_total = calculate_total(expenses)
        print(f"👉 Running total: {running_total:.2f}\n")

        save_expenses(expenses)  # persist after every entry

    show_summary(expenses)
    print("👋 Session saved. See you next time!")


if __name__ == "__main__":
    main()