import { render, screen } from '@testing-library/react';
import TopCompaniesTable from '@/app/components/TopCompaniesTable';

describe('TopCompaniesTable', () => {
  const mockCompanies = [
    { 
      name: 'Company A',
      esgScore: 85,
      amountSpent: 1000,
      logo: 'https://example.com/logo.png'
    }
  ];

  it('renders loading state when companies are undefined', () => {
    render(<TopCompaniesTable companies={undefined} />);
    expect(screen.getByText('Your most purchased-from companies')).toBeInTheDocument();
  });

  it('renders the table headers correctly', () => {
    render(<TopCompaniesTable companies={mockCompanies} />);
    expect(screen.getByText('Company')).toBeInTheDocument();
    expect(screen.getByText('ESG Score')).toBeInTheDocument();
    expect(screen.getByText('Amount Purchased')).toBeInTheDocument();
  });

  it('renders the see all transactions button', () => {
    render(<TopCompaniesTable companies={mockCompanies} />);
    expect(screen.getByText('See All Transactions')).toBeInTheDocument();
  });
}); 