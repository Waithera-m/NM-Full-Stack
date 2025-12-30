import { useState } from 'react'
import './App.css'
import { LoanPayments } from './components/LoanPayments'

type UpdateLoanPaymentProps = {
    onSuccess: () => void;
}

const AddNewPayment = ({onSuccess}: UpdateLoanPaymentProps) => {

    const submitPayment = (form: HTMLFormElement) => {
        const formData = new FormData(form);   
        const loanId = Number(formData.get('loan-id')); //Get passed loan id
        const paymentAmount = Number(formData.get('payment-amount')); //Get passed payment amount

        /**Send payment update result to the backend */
        fetch('http://localhost:2024/graphql', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },  
            body: JSON.stringify({
                query: `
                mutation {
                    updateLoanPayment(loanId: ${loanId}, amount: ${paymentAmount}) {
                        success,
                        message
                    }
                }
                `   
            })
        })
        .then((response) => response.json())
        .then((data) => {
            // console.log('Update Payment Response::::', data);
            const result = data.data.updateLoanPayment;
            if (result.success) {
                alert('Payment updated successfully!');
                form.reset(); //Reset form field on successful loan payment update
                onSuccess(); //Update refresh flag state on successful payment update to trigger loan payments list refresh
            } else {
                alert(`Failed to update payment: ${result.message}`);
            }
        });
    }

    return (
        <div>
            <form
                onSubmit={(e) => {
                    e.preventDefault()
                    submitPayment(e.currentTarget)
                }}
            >
                <p>
                    <label className="label-text">Payment Loan Id</label>
                    <input name="loan-id" onChange={() => {}} />
                </p>

                <p>
                    <label className="label-text">Payment Amount</label>
                    <input
                        name="payment-amount"
                        type="number"
                        onChange={() => {}}
                    />
                </p>
                <p>
                    <button type="submit">Add Payment</button>
                </p>
            </form>
        </div>
    )
}

function App() {
    const [refreshFlag, setRefreshFlag] = useState(0);

    const refreshLoansArray = () => setRefreshFlag(f => f + 1);

    return (
        <>
            <div>
                <h1>Existing Loans & Payments</h1>
                <LoanPayments refreshFlag={refreshFlag} />

                <h1>Add New Payment</h1>
                <AddNewPayment onSuccess={refreshLoansArray} />
            </div>
        </>
    )
}

export default App
