import { render, screen, waitFor, act } from '@testing-library/react';
import TransactionsPage from '@/app/transactions/page';
import { auth } from '@/app/firebase/firebaseConfig';
import { User } from 'firebase/auth';

jest.mock('@/app/firebase/firebaseConfig', () => ({
  auth: {
    onAuthStateChanged: (callback: (user: User | null) => void) => {
      callback({ uid: 'test-uid' } as User);
      return () => {};
    }
  }
}));

const mockTransactions = [
  {
    merchant_name: 'Test Store',
    amount: 100,
    time_completed: '2024-03-15T10:00:00Z',
    esg_score: '450',
    action: 'purchase',
    longitude: -122.4194,
    latitude: 37.7749,
    customerID: '123',
    ip_address: '192.168.1.1'
  }
];

describe('TransactionsPage', () => {
  beforeEach(() => {
    jest.clearAllMocks();
    global.fetch = jest.fn(() =>
      Promise.resolve({
        ok: true,
        json: () => Promise.resolve(mockTransactions)
      })
    ) as jest.Mock;
  });

  it('renders loading state initially', () => {
    render(<TransactionsPage />);
    expect(screen.getByText(/Loading/i)).toBeInTheDocument();
  });

  it('renders transactions after loading', async () => {
    await act(async () => {
      render(<TransactionsPage />);
    });

    await waitFor(() => {
      expect(screen.getByText('Test Store')).toBeInTheDocument();
      expect(screen.getByText('100.00')).toBeInTheDocument();
    }, { timeout: 3000 });
  });
}); 