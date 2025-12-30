import sys
from pathlib import Path

SERVER_DIR = Path(__file__).resolve().parents[1]
if str(SERVER_DIR) not in sys.path:
    sys.path.insert(0, str(SERVER_DIR))

import datetime
import app as loan_app

def init_loan_obj(loan_id: int, name: str, interest_rate: float, principal: int, due_date: datetime.date, payment_date=None):
    return {
        "id": loan_id,
        "name": name,
        "interest_rate": interest_rate,
        "principal": principal,
        "due_date": due_date,
        "payment_date": payment_date,
    }


def test_resolve_payment_date_null_when_no_payment_list_available(monkeypatch):
    '''
    Test that resolve_payment_date only returns dates for loan whose loan payment history exists
    '''
    monkeypatch.setattr(loan_app, "loan_payments", [])
    loan = init_loan_obj(1, "Test Loan", 3.0, 100000, datetime.date(2025, 5, 1))

    result = loan_app.ExistingLoans.resolve_payment_date(loan, info=None)
    assert result is None

def test_resolve_payment_status_unpaid(monkeypatch):
    '''
    Test that resolve_payment_status returns 'Unpaid' for loans with no payment history
    '''
    monkeypatch.setattr(loan_app, "loan_payments", [])
    loan = init_loan_obj(1, "Test Loan", 3.0, 100000, datetime.date(2025, 5, 1))

    status = loan_app.ExistingLoans.resolve_status(loan, info=None)
    assert status == "Unpaid"

def test_resolve_payment_status_on_time(monkeypatch):
    '''
    Test that resolve_payment_status returns 'On Time' for loan payments made within 5 days of due date
    '''
    due_date = datetime.date(2025, 12, 12)
    last_payment_date = due_date - datetime.timedelta(days=4)

    monkeypatch.setattr(loan_app, "loan_payments", [{"id": 1, "loan_id": 1, "payment_date": last_payment_date}])
    loan = init_loan_obj(1, "Test Loan", 3.0, 100000, due_date)

    status = loan_app.ExistingLoans.resolve_status(loan, info=None)
    assert status == "On Time"

def test_resolve_payment_status_late(monkeypatch):
    '''
    Test that resolve_payment_status returns 'Late' for loan payments made within 6 and 30 days of due date
    '''
    due_date = datetime.date(2025, 12, 12)
    payment_date = due_date + datetime.timedelta(days=17)

    monkeypatch.setattr(loan_app, "loan_payments", [{"id": 1, "loan_id": 1, "payment_date": payment_date}])
    loan = init_loan_obj(1, "Test Loan", 3.0, 100000, due_date, payment_date=payment_date)

    status = loan_app.ExistingLoans.resolve_status(loan, info=None)
    assert status == "Late"

def test_resolve_payment_status_defaulted(monkeypatch):
    '''
    Test that resolve_payment_status returns 'Defaulted' for loan payments made 31 days after due date
    '''
    due_date = datetime.date(2025, 12, 12)
    payment_date = due_date + datetime.timedelta(days=31)

    monkeypatch.setattr(loan_app, "loan_payments", [{"id": 1, "loan_id": 1, "payment_date": payment_date}])
    loan = init_loan_obj(1, "Test Loan", 3.0, 100000, due_date, payment_date=payment_date)

    status = loan_app.ExistingLoans.resolve_status(loan, info=None)
    assert status == "Defaulted"

def test_update_loan_payment_returns_error_for_nonexistent_loan(monkeypatch):
    '''
    Test that UpdateLoanPayment mutation returns error message when a user tries to update payment for a non-existent loan
    '''
    current_loans = [
        {"id": 2, "name": "Loan 2", "interest_rate": 2.5, "principal": 20000, "due_date": datetime.date(2025, 4, 1)},
        {"id": 3, "name": "Loan 3", "interest_rate": 3.0, "principal": 30000, "due_date": datetime.date(2025, 5, 1)},
    ]

    monkeypatch.setattr(loan_app, "loans", current_loans)

    result = loan_app.UpdateLoanPayment().mutate(None, loan_id=1, amount=5000, payment_date=datetime.date(2024, 6, 1))

    assert result.success is False
    assert result.loan_payment is None
    assert result.message == "Loan with the provided ID does not exist."

def test_update_loan_payment_creates_new_payment(monkeypatch):
    '''
    Test that UpdateLoanPayment mutation creates a new payment record when none exists for the given loan_id
    '''
    current_loans = [
        {"id": 1, "name": "Loan 1", "interest_rate": 2.5, "principal": 20000, "due_date": datetime.date(2025, 4, 1)},
    ]
    monkeypatch.setattr(loan_app, "loans", current_loans)
    monkeypatch.setattr(loan_app, "loan_payments", [])

    result = loan_app.UpdateLoanPayment().mutate(None, loan_id=1, amount=5000, payment_date=datetime.date(2024, 6, 1))


    assert result.success is True
    assert result.loan_payment is not None
    assert result.loan_payment['loan_id'] == 1
    assert result.loan_payment['payment_date'] == datetime.date(2024, 6, 1)
    assert result.message == "Loan payment record created successfully."
