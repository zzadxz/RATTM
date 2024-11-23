// src/app/dashboard/page.tsx

"use client";
import dynamic from "next/dynamic";
import React, { useEffect, useState } from "react";
import { auth } from "@/app/firebase/firebaseConfig";
import { useRouter } from "next/navigation";
import FootprintLineGraph from "@/app/components/charts/FootprintLineGraph";
import MonthSummary from "@/app/components/charts/MonthSummary";
import AboutYourScore from "@/app/components/AboutYourScore";
import TableOne from "@/app/components/TopCompaniesTable";
import CardDataStats from "@/app/components/CardDataStats";

const CompaniesPieChart = dynamic(
  () => import("@/app/components/charts/CompaniesPieChart"),
  {
    ssr: false,
  }
);

const Dashboard: React.FC = () => {
  const [loading, setLoading] = useState(true);
  const [totalCO2Score, setTotalCO2Score] = useState<string>("Loading...");
  const [monthlyCO2Score, setMonthlyCO2Score] = useState<number>(0);
  const [monthlyCO2ScoreChange, setMonthlyCO2ScoreChange] = useState<number>(0);
  const [monthlyGreenTransactions, setMonthlyGreenTransactions] = useState<number>(0);
  const [monthlyGreenTransactionsChange, setMonthlyGreenTransactionsChange] = useState<number>(0);
  const [circleColor, setCircleColor] = useState<string>("#7d91f5");
  const [isHovered, setIsHovered] = useState(false);
  const router = useRouter();

  useEffect(() => {
    const fetchDashboardData = async () => {
      try {
        const [
          totalCO2Response,
          monthlyCO2Response,
          co2ChangeResponse,
          greenTransactionsResponse,
          greenTransactionsChangeResponse
        ] = await Promise.all([
          fetch("https://rattm-f300025e7172.herokuapp.com/dashboard/get_total_co2_score/"),
          fetch("https://rattm-f300025e7172.herokuapp.com/dashboard/get_this_month_co2_score/"),
          fetch("https://rattm-f300025e7172.herokuapp.com/dashboard/get_co2_score_change/"),
          fetch("https://rattm-f300025e7172.herokuapp.com/dashboard/get_this_month_green_transactions/"),
          fetch("https://rattm-f300025e7172.herokuapp.com/dashboard/get_green_transaction_change/")
        ]);

        const [totalCO2Data, monthlyCO2Data, co2ChangeData, greenTransactionsData, greenTransactionsChangeData] = 
          await Promise.all([
            totalCO2Response.text(),
            monthlyCO2Response.text(),
            co2ChangeResponse.text(),
            greenTransactionsResponse.text(),
            greenTransactionsChangeResponse.text()
          ]);

        setTotalCO2Score(totalCO2Data);
        setMonthlyCO2Score(Number(monthlyCO2Data));
        setMonthlyCO2ScoreChange(Number(co2ChangeData));
        setMonthlyGreenTransactions(Number(greenTransactionsData));
        setMonthlyGreenTransactionsChange(Number(greenTransactionsChangeData));
        
        const totalValue = parseFloat(totalCO2Data);
        setCircleColor(totalValue > 200 ? "#08d116" : "#FE4A49");
      } catch (error) {
        console.error("Failed to fetch dashboard data:", error);
      }
    };

    const unsubscribe = auth.onAuthStateChanged((user) => {
      if (user) {
        fetchDashboardData();
        setLoading(false);
      } else {
        router.replace("/main-site/auth/SignInWithGoogle");
      }
    });

    return () => unsubscribe();
  }, [router]);

  if (loading) {
    return (
      <div className="flex items-center justify-center h-screen">
        <p className="text-2xl font-bold animate-pulse text-gray-600">
          Loading...
        </p>
      </div>
    );
  }

  return (
    <div className="mt-4 grid grid-cols-1 gap-4 md:mt-6 md:grid-cols-12 md:gap-6 2xl:mt-7.5 2xl:gap-7.5">
      <div className="dashboard-box rounded-2xl md:col-span-8">
        <h1 className="text-3xl font-extrabold text-black dark:text-white">
          Overview of your carbon footprint
        </h1>
        <p className="pt-4 text-xl">
          See how your carbon footprint varied in the last 12 months
        </p>
        <br />
        <FootprintLineGraph />
        <MonthSummary 
          monthlyCO2Score={monthlyCO2Score}
          monthlyCO2ScoreChange={monthlyCO2ScoreChange}
          monthlyGreenTransactions={monthlyGreenTransactions}
          monthlyGreenTransactionsChange={monthlyGreenTransactionsChange}
        />
        <TableOne />
      </div>

      <div className="col-span-12 rounded-2xl bg-white pt-5 md:col-span-4 lg:pl-10 lg:pr-10">
        <CardDataStats
          title="(out of 500)"
          total={totalCO2Score}
          circleColor={circleColor}
          onHoverChange={setIsHovered}
        >
          <p className="text-center text-xl font-black text-black">
            Carbon Score
          </p>
        </CardDataStats>
        <AboutYourScore isHovered={isHovered} />
        <div className="mt-5">
          <CompaniesPieChart />
        </div>
      </div>
    </div>
  );
};

export default Dashboard;
