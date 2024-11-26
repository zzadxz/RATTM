// src/app/transactions/page.tsx
"use client";

import React, { useState, useMemo } from "react";
import TransactionsTable from "@/app/components/TransactionsTable";
import useTransactions from "@/hooks/useTransactions";
import Datepicker from "react-tailwindcss-datepicker";
import dayjs from "dayjs";

// Define the structure for filters
interface FilterState {
  action: string;
  company: string;
  dateRange: {
    startDate: Date | null;
    endDate: Date | null;
  };
}

const INITIAL_VISIBLE_COUNT = 20;
const LOAD_MORE_INCREMENT = 20;

const TransactionsPage: React.FC = () => {
  const { transactions, loading, error } = useTransactions();
  const [filters, setFilters] = useState<FilterState>({
    action: "All",
    company: "",
    dateRange: {
      startDate: null,
      endDate: null,
    },
  });
  const [visibleCount, setVisibleCount] = useState<number>(
    INITIAL_VISIBLE_COUNT
  );

  // Handle filter updates
  const updateFilter = <K extends keyof FilterState>(
    key: K,
    value: FilterState[K]
  ) => {
    setFilters((prev) => ({ ...prev, [key]: value }));
    setVisibleCount(INITIAL_VISIBLE_COUNT);
  };

  // Handle date range selection
  const handleDateChange = (
    newValue: { startDate: Date | null; endDate: Date | null } | null
  ) => {
    if (newValue) {
      setFilters((prev) => ({ ...prev, dateRange: newValue }));
    } else {
      setFilters((prev) => ({
        ...prev,
        dateRange: { startDate: null, endDate: null },
      }));
    }
    setVisibleCount(INITIAL_VISIBLE_COUNT);
  };

  // Filter transactions based on filters
  const filteredTransactions = useMemo(() => {
    return transactions.filter((txn) => {
      const txnDate = dayjs(txn.time_completed);

      // Action Filter
      const matchesAction =
        filters.action === "All" ||
        txn.action.toLowerCase() === filters.action.toLowerCase();

      // Company Filter
      const matchesCompany =
        !filters.company.trim() ||
        txn.merchant_name.toLowerCase().includes(filters.company.toLowerCase());

      // Date Range Filter
      const { startDate, endDate } = filters.dateRange;
      const afterStartDate =
        !startDate || txnDate.isAfter(dayjs(startDate).subtract(1, "day"));
      const beforeEndDate =
        !endDate || txnDate.isBefore(dayjs(endDate).add(1, "day"));

      return matchesAction && matchesCompany && afterStartDate && beforeEndDate;
    });
  }, [transactions, filters]);

  // Transactions to display based on visible count
  const displayedTransactions = useMemo(() => {
    return filteredTransactions.slice(0, visibleCount);
  }, [filteredTransactions, visibleCount]);

  const hasMore = visibleCount < filteredTransactions.length;

  const handleLoadMore = () => {
    setVisibleCount((prev) => prev + LOAD_MORE_INCREMENT);
  };

  return (
    <div className="mx-auto max-w-7xl p-6">
      <h1 className="mb-8 text-center text-5xl font-extrabold text-gray-900 dark:text-white">
        All Recent Transactions
      </h1>

      {/* Filter Section */}
      <div className="flex flex-col sm:flex-row sm:justify-between sm:items-start gap-6 mb-8">
        {/* Left Filters: Action and Company */}
        <div className="flex flex-col sm:flex-row sm:gap-6 w-full sm:w-2/3">
          {/* Action Filter */}
          <div className="relative w-full sm:w-1/2">
            <label
              htmlFor="action"
              className="block text-sm font-semibold text-gray-700 dark:text-gray-200 mb-1"
            >
              Action
            </label>
            <select
              id="action"
              value={filters.action}
              onChange={(e) => updateFilter("action", e.target.value)}
              className="block w-full appearance-none rounded-md border border-stroke bg-white px-3 py-2 pr-10 shadow-default focus:border-green-500 focus:outline-none focus:ring-2 focus:ring-green-500 dark:bg-boxdark dark:border-strokedark dark:text-gray-200"
            >
              <option value="All">All Actions</option>
              <option value="declined">Declined</option>
              <option value="approved">Approved</option>
            </select>
            {/* Custom Arrow Icon */}
            <div className="pointer-events-none absolute inset-y-0 right-0 flex items-center pr-2">
              <svg
                className="h-5 w-5 text-gray-400 dark:text-gray-300"
                xmlns="http://www.w3.org/2000/svg"
                viewBox="0 0 20 20"
                fill="currentColor"
                aria-hidden="true"
              >
                <path
                  fillRule="evenodd"
                  d="M10 12a1 1 0 01-.7-.3l-3-3a1 1 0 111.4-1.4L10 9.586l2.3-2.3a1 1 0 111.4 1.4l-3 3A1 1 0 0110 12z"
                  clipRule="evenodd"
                />
              </svg>
            </div>
          </div>

          {/* Company Name Filter */}
          <div className="relative w-full sm:w-1/2">
            <label
              htmlFor="company"
              className="block text-sm font-semibold text-gray-700 dark:text-gray-200 mb-1"
            >
              Company
            </label>
            <input
              type="text"
              id="company"
              value={filters.company}
              onChange={(e) => updateFilter("company", e.target.value)}
              placeholder="Search by company name"
              className="block w-full rounded-md border border-stroke bg-white px-3 py-2 shadow-default focus:border-green-500 focus:outline-none focus:ring-2 focus:ring-green-500 dark:bg-boxdark dark:border-strokedark dark:text-gray-200"
            />
          </div>
        </div>

        {/* Date Range Picker */}
        <div className="relative w-full sm:w-1/3">
          <label
            htmlFor="dateRange"
            className="block text-sm font-semibold text-gray-700 dark:text-gray-200 mb-1"
          >
            Date Range
          </label>
          <div className="relative overflow-visible z-50">
            <Datepicker
              primaryColor={"green"}
              asSingle={false}
              value={filters.dateRange}
              onChange={handleDateChange}
              showShortcuts={true}
              placeholder="Select date range"
              displayFormat="DD/MM/YYYY"
              containerClassName="relative w-full rounded-md border border-stroke bg-white dark:bg-boxdark px-3 py-2 shadow-default focus-within:border-green-500 focus-within:ring-2 focus:ring-green-500 flex items-center h-10"
              inputClassName="block w-full bg-transparent border-none focus:outline-none dark:text-gray-200 h-full leading-normal"
            />
          </div>
        </div>
      </div>
      {/* End Filter Section */}

      {/* Transactions Table */}
      {loading && (
        <div className="flex items-center justify-center">
          <p className="text-lg text-gray-600">Loading transactions...</p>
        </div>
      )}

      {error && (
        <div className="flex items-center justify-center mb-5">
          <svg
            width="20"
            height="20"
            xmlns="http://www.w3.org/2000/svg"
            viewBox="0 0 24 24"
            fill="none"
            stroke="#9b3628"
            strokeWidth="2"
            className="inline-block mr-2"
          >
            <circle cx="12" cy="12" r="10" fill="#c04532" />
            <line
              x1="12"
              y1="8"
              x2="12"
              y2="13"
              stroke="#fff"
              strokeLinecap="round"
            />
            <line
              x1="12"
              y1="16"
              x2="12"
              y2="16"
              stroke="#fff"
              strokeLinecap="round"
            />
          </svg>
          <p className="text-lg text-red-600">{error}</p>
        </div>
      )}

      {!loading && (
        <>
          {filteredTransactions.length > 0 ? (
            <>
              <TransactionsTable transactions={displayedTransactions} />

              {hasMore && (
                <div className="flex justify-center mt-6">
                  <button
                    onClick={handleLoadMore}
                    className="bg-green-500 hover:bg-green-600 text-white font-semibold py-2 px-4 rounded-md transition-colors duration-200 focus:outline-none focus:ring-2 focus:ring-green-500"
                  >
                    Load More
                  </button>
                </div>
              )}
            </>
          ) : (
            <div className="flex items-center justify-center">
              <p className="text-lg text-gray-500">
                No transactions match the filters.
              </p>
            </div>
          )}
        </>
      )}
    </div>
  );
};

export default TransactionsPage;
