import { render, screen } from '@testing-library/react';
import TransactionsTable from '@/app/components/TransactionsTable';
import { Transaction } from '@/app/types/Transaction';

describe('TransactionsTable', () => {
  const mockTransactions: Transaction[] = [
    {
      merchant_name: 'Test Store',
      amount: 100,
      time_completed: '2024-03-15T10:00:00Z',
      esg_score: '450',
      action: 'purchase',
      longitude: -122.4194,
      latitude: 37.7749,
      customerID: 123,
      ip_address: '192.168.1.1'
    }
  ];

  it('renders table headers', () => {
    render(<TransactionsTable transactions={mockTransactions} />);
    expect(screen.getByText('Company Name')).toBeInTheDocument();
    expect(screen.getByText('Amount ($)')).toBeInTheDocument();
    expect(screen.getByText('Date')).toBeInTheDocument();
  });

  it('renders transaction data correctly', () => {
    render(<TransactionsTable transactions={mockTransactions} />);
    expect(screen.getByText('Test Store')).toBeInTheDocument();
    expect(screen.getByText('100.00')).toBeInTheDocument();
  });

  it('handles empty transactions array', () => {
    render(<TransactionsTable transactions={[]} />);
    expect(screen.getByText('No transactions available.')).toBeInTheDocument();
  });
}); 