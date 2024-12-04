import { render, screen } from '@testing-library/react';
import SignInWithGoogle from '@/app/main-site/auth/SignInWithGoogle/page';

// Mock Firebase auth before importing any modules that use it
jest.mock('@/app/firebase/firebaseConfig', () => {
  const mockSignInWithPopup = jest.fn();
  const mockGoogleAuthProvider = jest.fn();
  
  return {
    auth: {
      onAuthStateChanged: jest.fn((callback) => {
        callback(null);
        return () => {};
      }),
      signInWithPopup: mockSignInWithPopup,
      GoogleAuthProvider: mockGoogleAuthProvider
    }
  };
});

// Mock next/navigation
jest.mock('next/navigation', () => ({
  useRouter: () => ({
    push: jest.fn(),
    replace: jest.fn()
  })
}));

describe('SignInWithGoogle Page', () => {
  beforeEach(() => {
    jest.clearAllMocks();
  });

  it('renders sign in with google button', () => {
    render(<SignInWithGoogle />);
    const button = screen.getByRole('button');
    expect(button).toHaveTextContent(/sign in with google/i);
  });

  it('redirects to dashboard when user is already authenticated', async () => {
    const { auth } = require('@/app/firebase/firebaseConfig');
    const mockReplace = jest.fn();
    jest.spyOn(require('next/navigation'), 'useRouter').mockImplementation(() => ({
      replace: mockReplace
    }));

    auth.onAuthStateChanged.mockImplementation((callback) => {
      callback({ uid: 'test-uid' });
      return () => {};
    });

    render(<SignInWithGoogle />);
    expect(mockReplace).toHaveBeenCalledWith('/dashboard');
  });
}); 