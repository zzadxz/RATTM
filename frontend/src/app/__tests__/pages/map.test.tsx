import { render, screen } from '@testing-library/react';
import MapPage from '@/app/map/page';

jest.mock('mapbox-gl', () => ({
  Map: jest.fn(),
  Marker: jest.fn()
}));

describe('Map Page', () => {
  it('renders map container', () => {
    render(<MapPage />);
    expect(screen.getByTestId('map-container')).toBeInTheDocument();
  });

  it('renders map title', () => {
    render(<MapPage />);
    expect(screen.getByText('Purchases Map')).toBeInTheDocument();
  });
}); 