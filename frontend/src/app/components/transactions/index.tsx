import { useEffect, useState } from 'react';

const Transactions = () => {
  const [transactions, setTransactions] = useState([]);

  useEffect(() => {
    // Fetch transactions data from backend
    fetch('http://localhost:8000/api/get/')
      .then((response) => response.json())
      .then((data) => setTransactions(data))
      .catch((error) => console.error('Error fetching transactions:', error));
  }, []);

  return (
    <div>
      <h1>View Your Recent Transactions</h1>
      <ul>
        {transactions.map((transaction, index) => (
          <li key={index}>
            <strong>ID:</strong> {transaction['Transaction ID']} - 
            <strong>Company Name:</strong> {transaction['Company Name']} - 
            <strong> Amount:</strong> {transaction['Transaction Amount']}
          </li>
        ))}
      </ul>
    </div>
  );
};

export default Transactions;