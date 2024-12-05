import { render } from '@testing-library/react';
import TransactionMap from '@/app/components/TransactionMap';

// Mock mapboxgl
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

describe('TransactionMap', () => {
  it('renders without crashing', () => {
    const { container } = render(<TransactionMap />);
    expect(container.firstChild).toBeInTheDocument();
  });
}); 