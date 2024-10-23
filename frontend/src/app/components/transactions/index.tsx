import React from 'react';
import styled from 'styled-components';

interface Transaction {
  "Transaction ID": string;
  "Company Name": string;
  "Transaction Amount": string;
  Date: string;
  rating: number;
}

const TableContainer = styled.div`
  width: 100%;
  max-width: 900px;
  margin: 40px auto;
  padding: 20px;
  background-color: #f8f9fa; /* Light background for contrast */
  border-radius: 16px;
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.12); /* Deeper shadow */
`;

const TransactionsTable = styled.table`
  width: 100%;
  border-collapse: collapse;
  border-radius: 12px;
  overflow: hidden;
  background-color: white;
`;

const TableHeader = styled.th`
  background-color: #00D632; /* Cash App green */
  color: white;
  padding: 15px;
  text-align: left;
  font-size: 1.3rem;
  font-weight: 600;
`;

const TableRow = styled.tr`
  &:nth-child(even) {
    background-color: #F9F9F9; /* Slightly different color for striped rows */
  }
  
  &:hover {
    background-color: #e1f7e5; /* Subtle green hover effect */
  }
`;

const TableData = styled.td`
  padding: 15px;
  text-align: left;
  font-size: 1rem;
  color: #333;
  border-bottom: 1px solid #eaeaea;
  font-family: 'Roboto', sans-serif;
`;

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
