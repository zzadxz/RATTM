// src/services/transactionService.ts

export interface Transaction {
  action: string;
  time_completed: string;
  longitude: number;
  merchant_name: string;
  latitude: number;
  customerID: number;
  amount: number;
  esg_score: string;
  ip_address: string;
}

export class TransactionService {
  /**
   * Fetches all transactions from the backend API.
   *
   * @returns {Promise<Transaction[]>} A promise that resolves to an array of transactions.
   */
  static async fetchTransactions(): Promise<Transaction[]> {
    try {
      const response = await fetch(`${process.env.NEXT_PUBLIC_API_BASE_URL}/transaction/get/`);
      if (!response.ok) {
        const errorDetails = await response.text();
        console.error('Fetch failed with details:', {
          status: response.status,
          statusText: response.statusText,
          body: errorDetails,
        });
        throw new Error('Network response was not ok');
      }
      const data: Transaction[] = await response.json();
      return data;
    } catch (error) {
      console.error('Error fetching transactions:', error);
      throw error;
    }
  }

  /**
   * Provides mock transactions.
   * Useful for testing or when the backend is not yet implemented.
   *
   * @returns {Transaction[]} An array of mock transactions.
   */
  static getMockTransactions(): Transaction[] {
    return [
      {
        action: "declined",
        time_completed: "2024-08-31T06:02:27.687Z",
        longitude: -113.807658,
        merchant_name: "Starbucks",
        latitude: -42.372604,
        customerID: 52,
        amount: 860.27,
        esg_score: "N/A",
        ip_address: "179.152.194.186",
      },
      {
        action: "declined",
        time_completed: "2023-12-07T08:07:20.451Z",
        longitude: -1.121183,
        merchant_name: "Target",
        latitude: 11.962175,
        customerID: 74,
        amount: 144.53,
        esg_score: "300",
        ip_address: "173.64.65.25",
      },
      // Add more mock transactions as needed
    ];
  }
}