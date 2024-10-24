import styled from 'styled-components';

export const TableContainer = styled.div`
  width: 100%;
  max-width: 900px;
  margin: 0 auto;
  padding: 0; /* Ensure no extra padding */
  background-color: transparent; /* Transparent to avoid box effect */
  border-radius: 16px;
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.12);
`;

export const TransactionsTable = styled.table`
  width: 100%;
  border-collapse: collapse;
  border-radius: 12px;
  overflow: hidden;
  background-color: #ffffff; /* Ensure table has a distinct background */
  border: 1px solid #e0e0e0; /* Consistent border color */
`;

export const TableHeader = styled.th`
  background-color: #00D632;
  color: white;
  padding: 15px;
  text-align: left;
  font-size: 1.3rem;
  font-weight: 600;
`;

export const TableRow = styled.tr`
  &:nth-child(even) {
    background-color: #F9F9F9;
  }
  
  &:hover {
    background-color: #e1f7e5;
  }
`;

export const TableData = styled.td`
  padding: 15px;
  text-align: left;
  font-size: 1rem;
  color: #333;
  border-bottom: 1px solid #eaeaea;
  font-family: 'Roboto', sans-serif;
`;
