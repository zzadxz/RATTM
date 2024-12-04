import { render, screen, fireEvent } from '@testing-library/react';
import CardDataStats from '@/app/components/CardDataStats';

describe('CardDataStats', () => {
  const mockProps = {
    title: 'Test Title',
    total: '100',
    children: <div>Test Children</div>,
    circleColor: '#000',
    onHoverChange: jest.fn(),
  };

  it('renders with correct props', () => {
    render(<CardDataStats {...mockProps} />);
    expect(screen.getByText('Test Title')).toBeInTheDocument();
    expect(screen.getByText('100')).toBeInTheDocument();
    expect(screen.getByText('Test Children')).toBeInTheDocument();
  });

  it('calls onHoverChange when hovering', () => {
    render(<CardDataStats {...mockProps} />);
    const questionMark = screen.getByText('?');
    
    fireEvent.mouseEnter(questionMark.closest('span')!);
    expect(mockProps.onHoverChange).toHaveBeenCalledWith(true);
    
    fireEvent.mouseLeave(questionMark.closest('span')!);
    expect(mockProps.onHoverChange).toHaveBeenCalledWith(false);
  });
}); 