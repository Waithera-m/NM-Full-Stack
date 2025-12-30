// import { useEffect, useState } from 'react'
import { useMemo } from 'react'

// SECTION 4 Debugging & Code Refactoring

/**Add inline type annotation for props */
export const LoanCalculator = ({ principal, rate, months }: { principal: number; rate: number; months: number }) => {
    /**Comment out this since it's dependent on renders and hence will execute just once on mount */
    // const [interest, setInterest] = useState(0)

    // useEffect(() => {
    //     setInterest((principal * rate * months) / 100)
    // }, [])

    /**Transition to useMemo to optimise performance (caching) and prevent unnecessary recalculations */
    const interest = useMemo(() => (principal * rate * months) / 100, [principal, rate, months]);

    return (
        <div>
            <h3>Loan Interest: {interest}</h3>
        </div>
    )
}
