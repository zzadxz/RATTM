export interface Transaction {
  merchant_name: string;
  amount: number;
  time_completed: string;
  esg_score: string;
  action: string;
  longitude: number;
  latitude: number;
  customerID: number;
  ip_address: string;
} 