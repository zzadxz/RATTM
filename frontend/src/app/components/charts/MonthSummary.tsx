"use client";

import React from "react";

interface MonthSummaryProps {
  monthlyCO2Score: number;
  monthlyCO2ScoreChange: number;
  monthlyGreenTransactions: number;
  monthlyGreenTransactionsChange: number;
}

const MonthSummary: React.FC<MonthSummaryProps>  = ({
  monthlyCO2Score,
  monthlyCO2ScoreChange,
  monthlyGreenTransactions,
  monthlyGreenTransactionsChange,
}) => {
  const getCurrentMonth = () => {
    const months = [
      "January", "February", "March", "April", "May", "June",
      "July", "August", "September", "October", "November", "December"
    ];
    const currentMonth = new Date().getMonth();
    return months[currentMonth];
  };
  
  const getChangeDisplay = (value: number) => ({
    absoluteValue: Math.abs(value),
    color: value >= 0 ? "text-green-600" : "text-red-600",
    isPositive: value >= 0
  });

  const co2Change = getChangeDisplay(monthlyCO2ScoreChange);
  const transactionsChange = getChangeDisplay(monthlyGreenTransactionsChange);

  return (
    <div className="col-span-12 mt-5 rounded-sm border border-stroke bg-white px-5 pb-5 pt-7.5 dark:border-strokedark dark:bg-boxdark sm:px-7.5 xl:col-span-8">
      <h1 className="text-3xl font-extrabold text-black dark:text-white">
        {getCurrentMonth()}&apos;s summary
      </h1>
      <p className="pt-4 text-xl">
        View your key carbon footprint metrics for this month
      </p>
      <br />
      <div className="flex space-x-4">
        <div className="flex-1 rounded-lg border border-gray-200 p-4">
          <h3 className="font-medium text-gray-600">CO2 Score</h3>
          <p className="text-sm text-gray-500">This Month</p>
          <div className="mt-2 flex items-center justify-between">
            <span className="text-4xl font-bold text-gray-900">{monthlyCO2Score}</span>
            <div className={`flex items-center text-sm ${co2Change.color}`}>
              <span>{co2Change.absoluteValue}</span>
              <svg
                xmlns="http://www.w3.org/2000/svg"
                className="ml-1 h-4 w-4"
                fill="none"
                viewBox="0 0 24 24"
                stroke="currentColor"
              >
                <path
                  strokeLinecap="round"
                  strokeLinejoin="round"
                  strokeWidth="2"
                  d={co2Change.isPositive 
                    ? "M5 10l7-7m0 0l7 7m-7-7v18"  // upward arrow
                    : "M19 14l-7 7m0 0l-7-7m7 7V3"  // downward arrow
                  }
                />
              </svg>
            </div>
          </div>
        </div>

        <div className="flex-1 rounded-lg border border-gray-200 p-4">
          <h3 className="font-medium text-gray-600">Green Transactions</h3>
          <p className="text-sm text-gray-500">This Month</p>
          <div className="mt-2 flex items-center justify-between">
            <span className="text-4xl font-bold text-gray-900">{monthlyGreenTransactions}</span>
            <div className={`flex items-center text-sm ${transactionsChange.color}`}>
              <span>{transactionsChange.absoluteValue}</span>
              <svg
                xmlns="http://www.w3.org/2000/svg"
                className="ml-1 h-4 w-4"
                fill="none"
                viewBox="0 0 24 24"
                stroke="currentColor"
              >
                <path
                  strokeLinecap="round"
                  strokeLinejoin="round"
                  strokeWidth="2"
                  d={transactionsChange.isPositive 
                    ? "M5 10l7-7m0 0l7 7m-7-7v18"  // upward arrow
                    : "M19 14l-7 7m0 0l-7-7m7 7V3"  // downward arrow
                  }
                />
              </svg>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default MonthSummary;
