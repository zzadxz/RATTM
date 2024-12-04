import { render, screen } from '@testing-library/react';
import SignInWithGoogle from '@/app/main-site/auth/SignInWithGoogle/page';
import { auth } from '@/app/firebase/firebaseConfig';
import { useRouter } from 'next/navigation';
import { User } from 'firebase/auth';

// Mock Firebase auth before importing any modules that use it
jest.mock('@/app/firebase/firebaseConfig', () => {
  const mockSignInWithPopup = jest.fn();
  const mockGoogleAuthProvider = jest.fn();
  
  return {
    auth: {
      onAuthStateChanged: jest.fn((callback: (user: User | null) => void) => {
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
    const mockReplace = jest.fn();
    jest.mocked(useRouter).mockImplementation(() => ({
      replace: mockReplace,
      push: jest.fn()
    }));

    const mockUser: Partial<User> = {
      uid: 'test-uid',
      email: 'test@example.com',
      displayName: 'Test User'
    };

    jest.mocked(auth.onAuthStateChanged).mockImplementation((callback) => {
      callback(mockUser as User);
      return () => {};
    });

    render(<SignInWithGoogle />);
    expect(mockReplace).toHaveBeenCalledWith('/dashboard');
  });
}); 