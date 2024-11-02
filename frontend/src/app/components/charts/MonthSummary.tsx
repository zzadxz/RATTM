"use client";

import React from "react";

const MonthSummary: React.FC = () => {
  return (
    <div className="col-span-12 mt-5 rounded-sm border border-stroke bg-white px-5 pb-5 pt-7.5 dark:border-strokedark dark:bg-boxdark sm:px-7.5 xl:col-span-8">
      <h1 className="text-3xl font-extrabold text-black dark:text-white">
        September&apos;s summary
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
            <span className="text-4xl font-bold text-gray-900">690</span>
            <div className="flex items-center text-sm text-green-600">
              <span>1.2%</span>
              <svg
                xmlns="http://www.w3.org/2000/svg"
                className="ml-1 h-4 w-4"
                fill="none"
                viewBox="0 0 24 24"
                stroke="currentColor"
              >
                <path
                  stroke-linecap="round"
                  stroke-linejoin="round"
                  stroke-width="2"
                  d="M5 10l7-7m0 0l7 7m-7-7v18"
                />
              </svg>
            </div>
          </div>
        </div>

        <div className="flex-1 rounded-lg border border-gray-200 p-4">
          <h3 className="font-medium text-gray-600">Green Transactions</h3>
          <p className="text-sm text-gray-500">This Month</p>
          <div className="mt-2 flex items-center justify-between">
            <span className="text-4xl font-bold text-gray-900">17</span>
            <div className="flex items-center text-sm text-green-600">
              <span>4.3%</span>
              <svg
                xmlns="http://www.w3.org/2000/svg"
                className="ml-1 h-4 w-4"
                fill="none"
                viewBox="0 0 24 24"
                stroke="currentColor"
              >
                <path
                  stroke-linecap="round"
                  stroke-linejoin="round"
                  stroke-width="2"
                  d="M5 10l7-7m0 0l7 7m-7-7v18"
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
