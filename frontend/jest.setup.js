// frontend/jest.setup.js

import '@testing-library/jest-dom';
import dotenv from 'dotenv';

dotenv.config();

process.env.NEXT_PUBLIC_FIREBASE_API_KEY = 'test_api_key';
process.env.NEXT_PUBLIC_FIREBASE_AUTH_DOMAIN = 'test_auth_domain';
process.env.NEXT_PUBLIC_FIREBASE_PROJECT_ID = 'test_project_id';
process.env.NEXT_PUBLIC_FIREBASE_STORAGE_BUCKET = 'test_storage_bucket';
process.env.NEXT_PUBLIC_FIREBASE_MESSAGING_SENDER_ID = 'test_messaging_sender_id';
process.env.NEXT_PUBLIC_FIREBASE_APP_ID = 'test_app_id';
process.env.NEXT_PUBLIC_FIREBASE_MEASUREMENT_ID = 'test_measurement_id';

import { useRouter } from 'next/router';

jest.mock('next/router', () => ({
  useRouter: jest.fn(),
}));

useRouter.mockImplementation(() => ({
  push: jest.fn(),
  replace: jest.fn(),
  pathname: '/',
  query: {},
  asPath: '/',
}));

global.window = {};
global.document = {};
