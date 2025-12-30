import { useState, useEffect } from "react";

interface LoanPayment {
    id: number;
    name: string;
    principal: number;
    interestRate: number;
    dueDate: string;
    paymentDate: string;
    status: string;
}

type LoanPaymentsRefresProps = {
    refreshFlag?: number;
}

/**Pass refresh key to ensure that the loans list is refreshed on successful form submissions */
export const LoanPayments = ({refreshFlag = 0}: LoanPaymentsRefresProps) => {

    const [payments, setPayments] = useState<LoanPayment[]>([]);

    /**Fetch loan payment entries from the backend */
    const getLoanPayments = () => {

        fetch('http://localhost:2024/graphql', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                query: `
                {
                    loans {
                        id
                        name
                        principal
                        interestRate
                        dueDate
                        paymentDate
                        status
                    }
                }
                `
            })
        })
            .then((response) => response.json())
            .then((data) => {
                // console.log('Loan Payments::::', data);
                setPayments(data.data.loans);
            });
    }

    /**Determine relevant css class based on loan status */
    const getLoanStatus = (status: string) => {
        switch (status) {
            case 'On Time':
                return 'on-time-loan';
            case 'Late':
                return 'late-loan';
            case 'Defaulted':
                return 'defaulted-loan';
            default:
                return 'unpaid-loan';
        }
    };

    useEffect(() => {
        getLoanPayments();
    }, [refreshFlag]);

    return (
        <div>
            {/* Loan entries table */}
            <table className="loan-payments-table">
                <thead>
                    <tr>
                        <th>ID</th>
                        <th>Name</th>
                        <th>Principal</th>
                        <th>Interest Rate</th>
                        <th>Due Date</th>
                        <th>Payment Date</th>
                        <th>Status</th>
                    </tr>
                </thead>
                <tbody>
                    {payments.map((payment) => (
                        <tr key={payment.id}>
                            <td>{payment.id}</td>
                            <td>{payment.name}</td>
                            <td>{payment.principal}</td>
                            <td>{payment.interestRate}</td>
                            <td>{payment.dueDate}</td>
                            <td>{payment.paymentDate ?? '-'}</td>
                            <td className={`${getLoanStatus(payment.status)}`}>{payment.status}</td>
                        </tr>
                    ))}
                </tbody>
            </table>
        </div>
    );
}

