import { render, screen } from '@testing-library/react';
import AboutYourScore from '@/app/components/AboutYourScore';

describe('AboutYourScore', () => {
  it('renders without hover effect', () => {
    render(<AboutYourScore isHovered={false} />);
    expect(screen.getByText('About your Eco-Score')).toBeInTheDocument();
    expect(screen.getByText(/We calculate based on normalized/)).toBeInTheDocument();
  });

  it('applies hover effect when isHovered is true', () => {
    render(<AboutYourScore isHovered={true} />);
    const container = screen.getByText('About your Eco-Score').closest('div');
    expect(container).toHaveClass('scale-105');
    expect(container).toHaveClass('shadow-lg');
  });

  it('contains a learn more button with correct link', () => {
    render(<AboutYourScore isHovered={false} />);
    const button = screen.getByText('LEARN MORE');
    expect(button).toBeInTheDocument();
    expect(button.closest('a')).toHaveAttribute('href', '/about');
  });
}); 