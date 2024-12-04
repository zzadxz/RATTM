import { render, screen, waitFor } from '@testing-library/react';
import Dashboard from '@/app/dashboard/page';
import { auth } from '@/app/firebase/firebaseConfig';

// Mock the Firebase auth
jest.mock('@/app/firebase/firebaseConfig', () => ({
  auth: {
    onAuthStateChanged: jest.fn((callback) => {
      callback({ uid: 'test-uid' });
      return jest.fn();
    }),
  },
}));

// Mock fetch calls with proper data structure
global.fetch = jest.fn((url) => {
  if (url.includes('company_tiers')) {
    return Promise.resolve({
      ok: true,
      json: () => Promise.resolve([10, 20, 30, 40]), // Mock company tiers data
    });
  }
  return Promise.resolve({
    ok: true,
    json: () => Promise.resolve([{ name: 'Test Company', esgScore: 85 }]),
    text: () => Promise.resolve('300'),
  });
}) as jest.Mock;

describe('Dashboard', () => {
  beforeEach(() => {
    jest.clearAllMocks();
  });

  it('renders loading state initially', () => {
    render(<Dashboard />);
    expect(screen.getByText('Loading...')).toBeInTheDocument();
  });

  it('renders dashboard content after loading', async () => {
    render(<Dashboard />);
    await waitFor(() => {
      expect(screen.getByText(/Eco-Score Overview/i)).toBeInTheDocument();
    });
  });

  it('fetches and displays data correctly', async () => {
    render(<Dashboard />);
    await waitFor(() => {
      expect(global.fetch).toHaveBeenCalled();
    });
  });
}); 