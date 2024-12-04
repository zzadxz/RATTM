import { render, screen, fireEvent } from '@testing-library/react';
import Navbar from '@/app/components/Navbar';
import { User } from 'firebase/auth';

jest.mock('@/app/firebase/firebaseConfig', () => ({
  auth: {
    onAuthStateChanged: jest.fn((callback) => {
      callback(null);
      return () => {};
    }),
    signOut: jest.fn().mockResolvedValue(true),
    currentUser: null
  }
}));

describe('Navbar', () => {
  beforeEach(() => {
    jest.clearAllMocks();
  });

  it('renders logo and navigation links', () => {
    render(<Navbar />);
    expect(screen.getByAltText('Logo')).toBeInTheDocument();
    expect(screen.getByText('HOME')).toBeInTheDocument();
    expect(screen.getByText('ABOUT')).toBeInTheDocument();
  });

  it('shows login button when user is not authenticated', () => {
    render(<Navbar />);
    expect(screen.getByText('SIGN IN')).toBeInTheDocument();
  });

  it('handles mobile menu toggle', () => {
    render(<Navbar />);
    const menuButton = screen.getByRole('button', { name: /toggle menu/i });
    fireEvent.click(menuButton);
    const lists = screen.getAllByRole('list');
    expect(lists[1]).toBeVisible();
  });
}); 