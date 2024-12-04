import { render } from '@testing-library/react';
import RootLayout from '@/app/layout';

// Mock all CSS imports
jest.mock('@/css/style.css', () => ({}));
jest.mock('@/css/satoshi.css', () => ({}));
jest.mock('mapbox-gl/dist/mapbox-gl.css', () => ({}));
jest.mock('jsvectormap/dist/css/jsvectormap.css', () => ({}));

// Mock Firebase
jest.mock('@/app/firebase/firebaseConfig', () => ({
  auth: {
    onAuthStateChanged: jest.fn((callback) => {
      callback(null);
      return () => {};
    }),
    currentUser: null
  },
  analytics: null
}));

describe('RootLayout', () => {
  it('renders children within the layout', () => {
    const { container } = render(
      <RootLayout>
        <div data-testid="test-child">Test Content</div>
      </RootLayout>
    );
    
    expect(container.querySelector('html')).toBeInTheDocument();
    expect(container.querySelector('body')).toBeInTheDocument();
  });

  it('includes necessary meta tags', () => {
    const { container } = render(
      <RootLayout>
        <div>Test Content</div>
      </RootLayout>
    );
    
    const html = container.querySelector('html');
    expect(html).toHaveAttribute('lang', 'en');
  });
}); 