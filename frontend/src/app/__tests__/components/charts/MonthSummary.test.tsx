import { render, screen } from '@testing-library/react';
import MonthSummary from '@/app/components/charts/MonthSummary';

describe('MonthSummary', () => {
  const defaultProps = {
    monthlyCO2Score: 300,
    monthlyCO2ScoreChange: 50,
    monthlyGreenTransactions: 10,
    monthlyGreenTransactionsChange: -2,
  };

  beforeAll(() => {
    // Mock Date to return a specific date for consistent testing
    jest.useFakeTimers();
    jest.setSystemTime(new Date('2024-03-15'));
  });

  afterAll(() => {
    jest.useRealTimers();
  });

  it('renders the current month correctly', () => {
    render(<MonthSummary {...defaultProps} />);
    expect(screen.getByText("March's summary")).toBeInTheDocument();
  });

  it('displays the monthly CO2 score', () => {
    render(<MonthSummary {...defaultProps} />);
    expect(screen.getByText('300')).toBeInTheDocument();
  });

  it('displays the monthly green transactions count', () => {
    render(<MonthSummary {...defaultProps} />);
    expect(screen.getByText('10')).toBeInTheDocument();
  });

  describe('change indicators', () => {
    it('shows positive change in green', () => {
      render(<MonthSummary {...defaultProps} />);
      const co2ChangeElement = screen.getByText('50').closest('div');
      expect(co2ChangeElement).toHaveClass('text-green-600');
    });

    it('shows negative change in red', () => {
      render(<MonthSummary {...defaultProps} />);
      const transactionsChangeElement = screen.getByText('2').closest('div');
      expect(transactionsChangeElement).toHaveClass('text-red-600');
    });

    it('displays correct arrow direction for positive change', () => {
      render(<MonthSummary {...defaultProps} />);
      const upwardArrowPath = screen.getByText('50')
        .closest('div')
        ?.querySelector('path');
      expect(upwardArrowPath).toHaveAttribute(
        'd',
        'M5 10l7-7m0 0l7 7m-7-7v18'
      );
    });

    it('displays correct arrow direction for negative change', () => {
      render(<MonthSummary {...defaultProps} />);
      const downwardArrowPath = screen.getByText('2')
        .closest('div')
        ?.querySelector('path');
      expect(downwardArrowPath).toHaveAttribute(
        'd',
        'M19 14l-7 7m0 0l-7-7m7 7V3'
      );
    });
  });

  it('renders all static text elements', () => {
    render(<MonthSummary {...defaultProps} />);
    expect(screen.getByText('Eco-Score')).toBeInTheDocument();
    expect(screen.getByText('Green Transactions')).toBeInTheDocument();
    expect(screen.getAllByText('This Month')).toHaveLength(2);
    expect(
      screen.getByText('View your key carbon footprint metrics for this month')
    ).toBeInTheDocument();
  });

  describe('edge cases', () => {
    it('handles zero values correctly', () => {
      render(
        <MonthSummary
          monthlyCO2Score={0}
          monthlyCO2ScoreChange={0}
          monthlyGreenTransactions={0}
          monthlyGreenTransactionsChange={0}
        />
      );
      expect(screen.getAllByText('0')).toHaveLength(4);
    });

    it('handles large numbers correctly', () => {
      render(
        <MonthSummary
          monthlyCO2Score={999999}
          monthlyCO2ScoreChange={999999}
          monthlyGreenTransactions={999999}
          monthlyGreenTransactionsChange={999999}
        />
      );
      expect(screen.getAllByText('999999')).toHaveLength(4);
    });
  });
}); 