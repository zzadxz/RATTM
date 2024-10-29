// frontend/src/app/__tests__/HomePage.test.tsx

import React from 'react';
import { render, screen } from '@testing-library/react';
import MainSite from '@/app/page'; // Import MainSite as a component

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

describe('MainSite Component', () => {
  it('renders welcome text', () => {
    render(<MainSite />);
    const welcomeText = screen.getByText(/Welcome/i);
    expect(welcomeText).toBeInTheDocument();
  });
});
