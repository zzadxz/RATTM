// frontend/src/app/__tests__/HomePage.test.tsx

import React from 'react';
import { render, screen } from '@testing-library/react';
import MainSite from '@/app/page';
import { auth } from '@/app/firebase/firebaseConfig';

// Mock useRouter to prevent routing issues, updated for next/navigation
jest.mock('next/navigation', () => ({
  useRouter: jest.fn().mockReturnValue({
    push: jest.fn(),
    replace: jest.fn(),
    pathname: '/',
    query: {},
    asPath: '/',
  }),
}));

// Mock Firebase auth with a function that correctly sets loading state
jest.mock('@/app/firebase/firebaseConfig', () => ({
  auth: {
    onAuthStateChanged: jest.fn((callback) => {
      // Immediately invoke the callback with null to simulate a logged-out user
      callback(null);
      return jest.fn(); // Return a mock unsubscribe function
    }),
  },
}));

describe('MainSite Component', () => {
  it('renders welcome text', async () => {
    render(<MainSite />);
    
    // Debug the component output to check rendering status
    screen.debug();

    // Use findByText to wait for the async rendering to complete
    const welcomeText = await screen.findByText(/Welcome/i);
    expect(welcomeText).toBeInTheDocument();
  });
});
