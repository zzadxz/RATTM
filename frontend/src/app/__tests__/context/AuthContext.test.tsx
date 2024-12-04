import { render, screen, act } from '@testing-library/react';
import { AuthContext, AuthProvider } from '@/app/context/AuthContext';
import { useContext } from 'react';
import { User, NextOrObserver } from 'firebase/auth';

jest.mock('@/app/firebase/firebaseConfig', () => ({
  auth: {
    onAuthStateChanged: (callback: NextOrObserver<User>) => {
      if (typeof callback === 'function') {
        callback(null);
      }
      return () => {};
    }
  }
}));

const TestComponent = () => {
  const { user, loading } = useContext(AuthContext);
  return (
    <div>
      <div data-testid="loading">{loading.toString()}</div>
      <div data-testid="user">{user ? 'logged-in' : 'logged-out'}</div>
    </div>
  );
};

describe('AuthContext', () => {
  beforeEach(() => {
    jest.clearAllMocks();
  });

  it('provides authentication state', () => {
    render(
      <AuthProvider>
        <TestComponent />
      </AuthProvider>
    );

    expect(screen.getByTestId('loading')).toHaveTextContent('false');
    expect(screen.getByTestId('user')).toHaveTextContent('logged-out');
  });

  it('updates auth state when user logs in', async () => {
    const mockUser = { uid: 'test-uid', email: 'test@example.com' } as User;
    jest.spyOn(require('@/app/firebase/firebaseConfig').auth, 'onAuthStateChanged')
      .mockImplementation((...args: unknown[]) => {
        const callback = args[0] as NextOrObserver<User>;
        if (typeof callback === 'function') {
          callback(mockUser);
        }
        return () => {};
      });

    render(
      <AuthProvider>
        <TestComponent />
      </AuthProvider>
    );

    await act(async () => {
      await new Promise(resolve => setTimeout(resolve, 0));
    });

    expect(screen.getByTestId('user')).toHaveTextContent('logged-in');
  });
}); 