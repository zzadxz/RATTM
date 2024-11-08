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
  const [displayName, setDisplayName] = useState<string | null>(null);
  const [loading, setLoading] = useState(true);
  const router = useRouter();

  useEffect(() => {
    const unsubscribe = auth.onAuthStateChanged((user) => {
      if (user) {
        setDisplayName(user.displayName || "User");
        setLoading(false);
      } else {
        router.replace("/main-site/auth/SignInWithGoogle"); // Use replace instead of push
      }
    });

    return () => unsubscribe();
  }, [router]);

  const handleSignOut = async () => {
    try {
      await auth.signOut();
      router.replace("/"); // Use replace instead of push
    } catch (error) {
      console.error("Sign out error:", error);
    }
  };

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
        <MonthSummary />
        <TableOne />
      </div>

      <div className="col-span-12 rounded-2xl bg-white pt-5 md:col-span-4 lg:pl-10 lg:pr-10">
        <CardDataStats title="(out of 850)" total="840" rate="23" levelUp>
          <p className="text-center text-xl font-black text-black">
            Carbon Score
          </p>
        </CardDataStats>
        <AboutYourScore />
        <div className="mt-5">
          <CompaniesPieChart />
        </div>
      </div>
    </div>
  );
};

export default Dashboard;
