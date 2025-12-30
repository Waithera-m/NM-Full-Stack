import datetime
from flask import Flask
from flask_graphql import GraphQLView
from flask_cors import CORS
import graphene

app = Flask(__name__)
CORS(app)

loans = [
    {
        "id": 1,
        "name": "Tom's Loan",
        "interest_rate": 5.0,
        "principal": 10000,
        "due_date": datetime.date(2025, 3, 1),
    },
    {
        "id": 2,
        "name": "Chris Wailaka",
        "interest_rate": 3.5,
        "principal": 500000,
        "due_date": datetime.date(2025, 3, 1),
    },
    {
        "id": 3,
        "name": "NP Mobile Money",
        "interest_rate": 4.5,
        "principal": 30000,
        "due_date": datetime.date(2025, 3, 1),
    },
    {
        "id": 4,
        "name": "Esther's Autoparts",
        "interest_rate": 1.5,
        "principal": 40000,
        "due_date": datetime.date(2025, 3, 1),
    },
]

loan_payments = [
    {"id": 1, "loan_id": 1, "payment_date": datetime.date(2024, 3, 4)},
    {"id": 2, "loan_id": 2, "payment_date": datetime.date(2024, 3, 15)},
    {"id": 3, "loan_id": 3, "payment_date": datetime.date(2024, 4, 5)},
]

#Define loan payments class to be used in the schema
class LoanPayments(graphene.ObjectType):
    id = graphene.Int()
    loan_id = graphene.Int()
    payment_date = graphene.Date()

class ExistingLoans(graphene.ObjectType):
    id = graphene.Int()
    name = graphene.String()
    interest_rate = graphene.Float()
    principal = graphene.Int()
    due_date = graphene.Date()
    payment_date = graphene.Date()
    status = graphene.String()

    # Add resolver for last payment date associated with each individual loan
    def resolve_payment_date(self, info):
        payment_dates = [payment['payment_date'] for payment in loan_payments if payment['loan_id'] == self['id']]
        return max(payment_dates) if payment_dates else None
    
    # Add resolver to determine loan repayment status based on last payment date
    def resolve_status(self, info):
        # print("*****Resolving status for loan id:", self['id'])
        payment_dates = [payment['payment_date'] for payment in loan_payments if payment['loan_id'] == self['id']]
        last_payment_date = max(payment_dates) if payment_dates else None

        # print("Last payment date:", last_payment_date)

        if last_payment_date:
            days_since_payment = (last_payment_date - self['due_date']).days
            # print("Days since payment:", days_since_payment)
            # print("=================================")
            if days_since_payment <= 5:
                return "On Time"
            elif 6 <= days_since_payment <= 30:
                return "Late"
            else:
                return "Defaulted"
        else:
            return "Unpaid"
        
class UpdateLoanPayment(graphene.Mutation):
    class Arguments:
        loan_id = graphene.Int(required=True)
        amount = graphene.Float(required=True)
        payment_date = graphene.Date(default_value=datetime.date.today())
    
    loan_payment = graphene.Field(LoanPayments)
    success = graphene.Boolean()
    message = graphene.String()

    def mutate(self, info, loan_id, amount=None, payment_date=None):
        payment = next((p for p in loan_payments if p['loan_id'] == loan_id), None)
        currentLoan = next((l for l in loans if l['id'] == loan_id), None)

        if not currentLoan:
            return UpdateLoanPayment(
                success=False,
                message="Loan with the provided ID does not exist.",
                loan_payment=None
            )

        if not payment:

            loan_payments.append({
                "id": len(loan_payments) + 1,
                "loan_id": loan_id,
                "payment_date": payment_date
            })
            return UpdateLoanPayment(
                success=True, 
                message="Loan payment record created successfully.",
                loan_payment=loan_payments[-1]
            )

        if loan_id is not None:
            payment['loan_id'] = loan_id
        if payment_date is not None:
            payment['payment_date'] = payment_date

        return UpdateLoanPayment(
            success=True,
            message="Loan payment updated successfully.",
            loan_payment=payment
        )


class Query(graphene.ObjectType):
    loans = graphene.List(ExistingLoans)
    loan_payments = graphene.List(LoanPayments)

    def resolve_loans(self, info):
        return loans

    # Add query resolver for loan payments entries
    def resolve_loan_payments(self, info):
        return loan_payments
    

class Mutation(graphene.ObjectType):
    update_loan_payment = UpdateLoanPayment.Field()

schema = graphene.Schema(query=Query, mutation=Mutation)


app.add_url_rule(
    "/graphql", view_func=GraphQLView.as_view("graphql", schema=schema, graphiql=True)
)


@app.route("/")
def home():
    return "Welcome to the Loan Application API"


if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)
