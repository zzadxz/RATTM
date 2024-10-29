// src/app/components/transactions/index.tsx
import React from 'react';
import {
  TableContainer,
  TransactionsTable,
  TableHeader,
  TableRow,
  TableData
} from './transactions.styles';

interface Transaction {
  "Transaction ID": string;
  "Company Name": string;
  "Transaction Amount": string;
  Date: string;
  rating: number;
}

const Transactions: React.FC<{ transactions: Transaction[] }> = ({ transactions }) => {
  return (
    <TableContainer>
      <TransactionsTable>
        <thead>
          <tr>
            <TableHeader>ID</TableHeader>
            <TableHeader>Company Name</TableHeader>
            <TableHeader>Amount</TableHeader>
            <TableHeader>Date</TableHeader>
            <TableHeader>Rating</TableHeader>
          </tr>
        </thead>
        <tbody>
          {transactions.map((transaction) => (
            <TableRow key={transaction['Transaction ID']}>
              <TableData>{transaction['Transaction ID']}</TableData>
              <TableData>{transaction['Company Name']}</TableData>
              <TableData>${parseFloat(transaction['Transaction Amount']).toFixed(2)}</TableData>
              <TableData>{transaction.Date}</TableData>
              <TableData>{transaction.rating}</TableData>
            </TableRow>
          ))}
        </tbody>
      </TransactionsTable>
    </TableContainer>
  );
};

export default Transactions;
