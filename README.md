![Numida](../logo.numida.png)

# What are we looking for in an engineer?

We are looking for an full stack engineer who is familiar with contemporary Native & Server landscape and can contribute to the evolution of our codebase.

Now, before we start. Let's apply the algorithm of success:

```js
while(noSuccess) {
    tryAgain();
    if(Dead) {
        break;
    }
}
```

## What are we testing for in this assessment?

- Your skill as a frontend & backend developer.
- Your ability to structure your code.
- Your ability to refactor efficient data relationships & endpoints
- Your ability to write well-typed code.
- Your ability to write reusable components.
- Your ability to write readable and extendable code by following the right design principles.
- Your familiarity with contemporary frameworks and libraries.

## Expectations

- Although we strive for perfection we don't expect everything to be perfect, **just do you**.
- Given the size of the assignment we don't expect everything to be done, **do what you can given the time**.

> The assignment should take about a maximum of **3 hours** to complete.

# Assessment:

## Objective:

Update a basic server & web app to display some loan statuses.

## Setting Up Local Server

Please refer to the server [README](server/README.md) file in the root directory of the project to set up the local server.

## Requirements

1. **Data Refactor & Fetching with GraphQL**:
   - Update the Graphql schema to expose loan_payments.
   - Fetch a list of loans & their related loan_payments using a GraphQL query.

2. **Web App**:
   - Display the loans and payments in a user-friendly format.
   - Style loan payment status based on criteria.

## Instructions:

1. **Setup**: All the resources you require to do this assessment will be provided along with this README.

2. **GraphQL Data Refactor & Fetching**:
   - Update GraphQL Schema to expose loan_payments
     - (Note the GraphIQL tool can be useful for debugging by visiting localhost:2024/grqphql in your browser)
   - Consume the updated graphql schema from the web app

3. **Web App Fetch & Render**:
   - Update the web app to consume the loan and loanPayment data from the server
   - Display this data together using well-designed components & conditional styling
   - Note that `npm run compile` will update the generated typescript types within the `__generated__` folder.

4. **Problem Solving**:

    - Problem Statement:
        - A borrower repays a loan in monthly installments. Each installment falls into one of three categories:
            - `"On Time"` → If the payment is made within 5 days of the due date. (GREEN)
            - `"Late"` → If the payment is made between 6 and 30 days after the due date. (ORANGE)
            - `"Defaulted"` → If the payment is more than 30 days late. (RED)
            - `"Unpaid"` is included for cases where there is no payment date. (GREY)
    - Task:
        - Write a function that categorizes loan payments and returns a new list/array where each payment including existing loan  information is combined & categorized as "On Time", "Late", "Defaulted" or "Unpaid".
        - You should not use any external libraries.
        - NOTE: When displaying these on the UI - use the colors next to each status as a visual indication.


    **Expected Output**:

    ```tsx
    [
        { id: 1, name: "Tom's Loan", interest_rate: 5.0, principal: 10000, dueDate: '2025-03-01', paymentDate: '2025-03-04', status: 'On Time' },
        { id: 2, name: "Chris Wailaka", interest_rate: 3.5, principal: 500000, dueDate: '2025-03-01', dueDate: '2025-03-01', paymentDate: '2025-03-15', status: 'Late' },
        { id: 3, name: "NP Mobile Money", interest_rate: 4.5, principal: 30000, dueDate: '2025-03-01', dueDate: '2025-03-01', paymentDate: '2025-04-05', status: 'Defaulted'},
        { id: 4, name: "Esther's Autoparts", interest_rate: 1.5, principal: 40000, dueDate: '2025-03-01', dueDate: '2025-03-01', paymentDate: null, status: 'Unpaid'},
    ]
    ```

5. **Debugging & Code Refactoring**:

    - Based on this project, demonstrate your ability in refactoring this component `LoanCalculator.tsx`.

6. **Bonus**:

   - Build a REST Endpoint on the server that adds payments to the payments list. Use this endpoint in the web application's AddPayment component to make the call.
   - Implement a loading spinner or some form of feedback while data is being fetched or the form is being submitted.
   - Add error handling for both the GraphQL query and the REST API call.
   - Any form of tests (unit/functional)
   - Note down additional suggestions, given more time
   - Recording of your project

5. **Submission**:
   - Ensure your code is well-documented and formatted.
   - Push your code to your GitHub repository.
   - Provide a link to your repository and a brief description of your approach.

6. **Follow-Up Questions**:
   - Be prepared to explain your code, discuss your approach, and suggest improvements during a follow-up session.
   - You may be asked to extend the functionality of your application during the follow-up.

## Evaluation Criteria:

- Correctness and completeness of the implementation.
- Code quality and organization.
- User experience and interface design.
- Ability to handle errors and edge cases.
- Explanation and understanding of your approach during the follow-up session.

## Resources:

- [GraphQL Documentation](https://graphql.org/learn/)
- [Vite Scaffolding](https://vite.dev/guide/#scaffolding-your-first-vite-project)
- [Vite React TS Template](https://github.com/vitejs/vite/tree/main/packages/create-vite/template-react-ts)
- [Apollo Client](https://www.apollographql.com/docs/react/get-started)

## Hints

- Clear and easy to understand setup instructions.
- Keep it simple...
- Have fun!

Good luck! We look forward to reviewing your application.
