// src/app/pages/main-site/styles.ts
import styled from 'styled-components';

export const MainContainer = styled.div`
  padding: 60px 0;
  min-height: 100vh;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
`;

export const MainHeading = styled.h1`
  color: #00d632;
  font-size: 3.5rem;
  font-weight: bold;
  margin-bottom: 10px;
  text-align: center;
`;

export const SubHeading = styled.h2`
  color: #ffffff;
  font-size: 1.5rem;
  font-weight: 400;
  margin-bottom: 40px;
  text-align: center;
`;

export const TransactionsWrapper = styled.div`
  width: 90%;
  max-width: 1200px;
  padding: 30px;
  margin-top: 20px;
  background-color: transparent;
  border: none; 
  box-shadow: none;
`;
