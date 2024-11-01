// src/app/page.tsx

"use client";

import React, { useEffect, useState } from "react";
import Navbar from "@/app/components/Navbar"; // Import Navbar
import { MainContainer, MainHeading, SubHeading, TransactionsWrapper } from './main-site/styles';
import { GlobalStyle } from '@/app/styles/globalStyles';
import Transactions from "@/app/components/transactions";

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
    <>
      <GlobalStyle /> {/* Apply the global styles */}
      <Navbar /> {/* Add Navbar here */}
      <MainContainer>
        <MainHeading>Welcome to RATTM&apos;s CO2 Calculator!</MainHeading>
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
    </>
  );
};

export default MainSite;
