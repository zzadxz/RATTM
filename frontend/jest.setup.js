// frontend/jest.setup.js

import '@testing-library/jest-dom';
import 'jest-environment-jsdom';
import { jest } from '@jest/globals';

// Suppress console errors and warnings in tests
const originalError = console.error;
const originalWarn = console.warn;

beforeAll(() => {
  console.error = (...args) => {
    if (
      /Warning.*not wrapped in act/.test(args[0]) ||
      /Warning.*validateDOMNesting/.test(args[0]) ||
      /Failed to fetch dashboard data/.test(args[0]) ||
      /Google sign-in error/.test(args[0])
    ) {
      return;
    }
    originalError.call(console, ...args);
  };

  console.warn = (...args) => {
    if (
      /Warning.*not wrapped in act/.test(args[0]) ||
      /punycode/.test(args[0])
    ) {
      return;
    }
    originalWarn.call(console, ...args);
  };
});

afterAll(() => {
  console.error = originalError;
  console.warn = originalWarn;
});

// Mock CSS modules
jest.mock('mapbox-gl/dist/mapbox-gl.css', () => ({}));
jest.mock('jsvectormap/dist/css/jsvectormap.css', () => ({}));
jest.mock('@/css/satoshi.css', () => ({}));
jest.mock('@/css/style.css', () => ({}));

// Mock next/navigation
jest.mock('next/navigation', () => ({
  useRouter: () => ({
    push: jest.fn(),
    replace: jest.fn(),
    pathname: '/',
  }),
  usePathname: () => '/',
}));

// Mock mapbox-gl
jest.mock('mapbox-gl', () => ({
  Map: jest.fn(() => ({
    on: jest.fn(),
    remove: jest.fn(),
  })),
  Marker: jest.fn(() => ({
    setLngLat: jest.fn().mockReturnThis(),
    addTo: jest.fn().mockReturnThis(),
  })),
}));

// Mock react-apexcharts
jest.mock('react-apexcharts', () => ({
  __esModule: true,
  default: () => <div>Chart</div>,
}));

// Mock environment variables
process.env.NEXT_PUBLIC_MAPBOX_KEY = 'test_key';
process.env.NEXT_PUBLIC_API_BASE_URL = 'http://localhost:8000';
process.env.NEXT_PUBLIC_FIREBASE_API_KEY = 'test-api-key';
process.env.NEXT_PUBLIC_FIREBASE_AUTH_DOMAIN = 'test.firebaseapp.com';
process.env.NEXT_PUBLIC_FIREBASE_PROJECT_ID = 'test-project';
process.env.NEXT_PUBLIC_FIREBASE_STORAGE_BUCKET = 'test.appspot.com';
process.env.NEXT_PUBLIC_FIREBASE_MESSAGING_SENDER_ID = '123456789';
process.env.NEXT_PUBLIC_FIREBASE_APP_ID = '1:123456789:web:abcdef';
process.env.NEXT_PUBLIC_FIREBASE_MEASUREMENT_ID = 'G-ABCDEF123';

// Mock fetch globally
global.fetch = jest.fn(() =>
  Promise.resolve({
    ok: true,
    json: () => Promise.resolve([]),
    text: () => Promise.resolve(''),
  })
);
