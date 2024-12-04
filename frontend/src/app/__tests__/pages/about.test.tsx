import { render, screen } from '@testing-library/react';
import About from '@/app/about/page';

jest.mock('@/app/firebase/firebaseConfig', () => ({
  auth: {
    onAuthStateChanged: jest.fn((callback) => {
      callback(null);
      // Return a proper unsubscribe function
      return () => {};
    })
  }
}));

describe('About Page', () => {
  it('renders the about page content', () => {
    render(<About />);
    expect(screen.getByText('About Your Eco-Score')).toBeInTheDocument();
    expect(screen.getByText(/Our goal with the Eco-Score/)).toBeInTheDocument();
  });

  it('displays the algorithm explanation', () => {
    render(<About />);
    expect(screen.getByText(/Our algorithm prioritizes simplicity/)).toBeInTheDocument();
  });
}); 