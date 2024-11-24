// src/components/TransactionsTable.tsx

import React from 'react';
import { Transaction } from "@/services/transactionService";

interface TransactionsTableProps {
  transactions: Transaction[];
}

const TransactionsTable: React.FC<TransactionsTableProps> = ({ transactions }) => {
  return (
    <div className="overflow-x-auto shadow-md rounded-lg">
      <table
        className="min-w-full bg-white"
        role="table"
        aria-label="Recent Transactions"
      >
        <thead className="bg-gray-50">
          <tr>
            <th
              scope="col"
              className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider"
            >
              Action
            </th>
            <th
              scope="col"
              className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider"
            >
              Company Name
            </th>
            <th
              scope="col"
              className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider"
            >
              Amount ($)
            </th>
            <th
              scope="col"
              className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider"
            >
              Date
            </th>
          </tr>
        </thead>
        <tbody className="bg-white divide-y divide-gray-200" role="rowgroup">
          {transactions.length > 0 ? (
            transactions.map((txn, index) => (
              <tr key={index} role="row" className="hover:bg-gray-100">
                <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900" role="cell">
                  {txn.action.charAt(0).toUpperCase() + txn.action.slice(1)}
                </td>
                <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900" role="cell">
                  {txn.merchant_name}
                </td>
                <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900" role="cell">
                  {txn.amount.toFixed(2)}
                </td>
                <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900" role="cell">
                  {new Date(txn.time_completed).toLocaleDateString()}
                </td>
              </tr>
            ))
          ) : (
            <tr role="row">
              <td
                className="px-6 py-4 whitespace-nowrap text-sm text-gray-500 text-center"
                colSpan={4}
                role="cell"
              >
                No transactions available.
              </td>
            </tr>
          )}
        </tbody>
      </table>
    </div>
  );
};

export default TransactionsTable;