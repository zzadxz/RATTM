// src/hooks/useTransactions.ts

import { useEffect, useState } from "react";
import { Transaction, TransactionService } from "@/services/transactionService";

/**
 * useTransactions Hook
 * 
 * This custom hook manages the fetching and state of transaction data.
 * It abstracts the logic for data retrieval, making it reusable across
 * different components or pages.
 *
 * @returns {Object} An object containing transactions, loading, and error states.
 */
const useTransactions = () => {
  const [transactions, setTransactions] = useState<Transaction[]>([]);
  const [loading, setLoading] = useState<boolean>(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    /**
     * fetchData
     * 
     * Fetches transaction data using the TransactionService.
     * Updates state based on the success or failure of the fetch.
     */
    const fetchData = async () => {
      try {
        const data = await TransactionService.fetchTransactions();
        setTransactions(data);
      } catch (err) { // 'err' is now used
        console.warn("Failed to fetch transactions. Using mock data.", err);
        const mockData = TransactionService.getMockTransactions();
        setTransactions(mockData);
        setError("Failed to fetch real transactions. Displaying mock data.");
      } finally {
        setLoading(false);
      }
    };

    fetchData();
  }, []);

  return { transactions, loading, error };
};

export default useTransactions;