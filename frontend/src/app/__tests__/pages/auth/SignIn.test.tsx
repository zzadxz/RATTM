import { render, screen, fireEvent } from '@testing-library/react';
import SignIn from '@/app/main-site/auth/SignIn/page';

jest.mock('next/navigation', () => ({
  useRouter: jest.fn(() => ({
    push: jest.fn(),
  }))
}));

jest.mock('@/app/firebase/firebaseConfig', () => ({
  auth: {
    onAuthStateChanged: jest.fn((callback) => {
      callback(null);
      return () => {};
    }),
    signInWithEmailAndPassword: jest.fn(),
    currentUser: null
  },
  analytics: null
}));

describe('SignIn Page', () => {
  it('renders sign in form', () => {
    render(<SignIn />);
    expect(screen.getByRole('heading', { name: 'Sign In' })).toBeInTheDocument();
    expect(screen.getByPlaceholderText('Email')).toBeInTheDocument();
    expect(screen.getByPlaceholderText('Password')).toBeInTheDocument();
  });

  it('handles form submission', () => {
    render(<SignIn />);
    const emailInput = screen.getByPlaceholderText('Email');
    const passwordInput = screen.getByPlaceholderText('Password');
    const submitButton = screen.getByRole('button', { name: 'Sign In' });

    fireEvent.change(emailInput, { target: { value: 'test@example.com' } });
    fireEvent.change(passwordInput, { target: { value: 'password123' } });
    fireEvent.click(submitButton);
  });
}); 