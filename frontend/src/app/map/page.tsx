"use client";

import TransactionMap from "@/app/components/TransactionMap";
import React from "react";

const Map = () => {
  return (
    <div className="mx-auto max-w-7xl">
      <div className="mb-5 mt-5 flex justify-center items-center">
        <h1 className="mr-2 font-extrabold text-3xl text-black dark:text-white">
          Purchases Map
        </h1>
      </div>
      <div className="mt-4 grid grid-cols-1 md:mt-6 md:grid-cols-12 2xl:mt-7.5">
        <div className="rounded-2xl md:col-span-8 p-0">
          <TransactionMap />
        </div>

        <div
          className={`
            col-span-12 border border-stroke bg-white
            shadow-default dark:border-strokedark dark:bg-boxdark
            sm:px-7.5 rounded-2xl bg-white md:col-span-4
            pl-5 pt-5 sm:mt-5 md:mt-0 lg:mt-0 sm:ml-0 md:ml-5 lg:ml-5
            h-[69vh] overflow-y-auto
          `}
        >
          <h3 className="font-semibold text-gray-900 dark:text-white mb-3 text-xl">
            Companies by Tier
          </h3>
          <div className="text-md">
            <p className="mb-3">
              We use a straightforward four-tier scale to classify companies
              based on their ESG (Environmental, Social, and Governance)
              performance:
            </p>
            <p className="mb-3">
              <span className="font-bold text-green-500">Great</span>: Companies
              in the top 25% of ESG ratings, showcasing industry-leading
              sustainability and governance practices.
            </p>
            <p className="mb-3">
              <span className="font-bold text-[#f9d849]">Good</span>: Companies
              in the 25-50% range, performing above average but with room for
              improvement.
            </p>
            <p className="mb-3">
              <span className="font-bold text-orange-500">Okay</span>: Companies
              in the 50-75% range, demonstrating average ESG performance.
            </p>
            <p className="mb-3">
              <span className="font-bold text-orange-500">Not Great</span>:
              Companies in the bottom 25%, indicating significant areas for
              improvement in their ESG practices.
            </p>
            <p className="mb-3">
              While our scale doesn&apos;t cover every factor that makes a
              company sustainable or unsustainable, we provide it as a reference
              to help you ultimately make more informed choices.
            </p>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Map;