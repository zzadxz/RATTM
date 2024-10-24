"use client";

import React, { useEffect, useState } from "react";
import styled from 'styled-components';
import Transactions from "@/app/components/transactions";

const MainContainer = styled.div`
  background: linear-gradient(135deg, #5500ff 0%, #30009c 100%);
  padding: 60px 0;
  min-height: 100vh;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
`;

const MainHeading = styled.h1`
  color: #00d632;
  font-size: 3.5rem;
  font-weight: bold;
  margin-bottom: 10px;
  text-align: center;
`;

const SubHeading = styled.h2`
  color: #ffffff;
  font-size: 1.5rem;
  font-weight: 400;
  margin-bottom: 40px;
  text-align: center;
`;

const TransactionsWrapper = styled.div`
  width: 90%;
  max-width: 1200px;
  background-color: #ffffff;
  padding: 30px;
  border-radius: 20px;
  box-shadow: 0px 16px 32px rgba(0, 0, 0, 0.2);
  border: 1px solid #e0e0e0;
`;

interface Transaction {
  "Transaction ID": string;
  "Company Name": string;
  "Transaction Amount": string;
  Date: string;
  rating: number;
}

const MainSite: React.FC = () => {
  const [data, setData] = useState<Transaction[] | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const apiUrl = process.env.NEXT_PUBLIC_API_URL;
    console.log('API URL:', apiUrl);
    if (!apiUrl) {
        console.error("API URL is not defined in production");
        setError("API URL is not defined");
        setLoading(false);
        return;
      }

    const fetchData = async () => {
    try {
        const response = await fetch(apiUrl);
        if (!response.ok) {
        throw new Error(`Failed to fetch data: ${response.status} ${response.statusText}`);
        }
        const result = await response.json();
        setData(result);
    } catch (err: unknown) {
        if (err instanceof Error) {
        setError(err.message);
        } else {
        setError("An unknown error occurred");
        }
    } finally {
        setLoading(false);
    }
    };
      

    fetchData();
  }, []);

  return (
    <MainContainer>
      <MainHeading>Welcome ALL HAHAHHAHAHA &apos;s CO2 Calculator!</MainHeading>
      <SubHeading>View Your Recent Transactions</SubHeading>

      {/* if there is an error, show it here */}
      {error && <p>Error: {error}</p>}

      {/* if still loading, show a loading message */}
      {loading && <p>Loading...</p>}

      {/* ONLY ONLY render the Transactions component if the data is successfully fetched */}
      {!loading && !error && data && (
        <TransactionsWrapper>
          <Transactions transactions={data} />
        </TransactionsWrapper>
      )}
    </MainContainer>
  );
};

export default MainSite;
