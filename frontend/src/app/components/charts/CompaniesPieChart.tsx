// frontend/src/app/components/charts/CompaniesPieChart.tsx

import { ApexOptions } from "apexcharts";
import React, { useState } from "react";
import ReactApexChart from "react-apexcharts";

interface CompaniesPieChartProps {
  companyTiers: number[];
}

const options: ApexOptions = {
  chart: {
    fontFamily: "Satoshi, sans-serif",
    type: "donut",
  },
  colors: [ "#4BAE50", "#CCDA38", "#FEC005", "#FE5620"],
  labels: ["Tier 1", "Tier 2", "Tier 3", "Tier 4"],
  legend: {
    show: false,
    position: "bottom",
  },

  plotOptions: {
    pie: {
      donut: {
        size: "65%",
        background: "transparent",
      },
    },
  },
  dataLabels: {
    enabled: false,
  },
  responsive: [
    {
      breakpoint: 2600,
      options: {
        chart: {
          width: 380,
        },
      },
    },
    {
      breakpoint: 640,
      options: {
        chart: {
          width: 200,
        },
      },
    },
  ],
};

const CompaniesPieChart: React.FC<CompaniesPieChartProps> = ({ companyTiers }) => {
  const series = companyTiers;
  const [isPopoverVisible, setPopoverVisible] = useState(false);

  const handleMouseEnter = () => {
    setPopoverVisible(true);
  };

  const handleMouseLeave = () => {
    setPopoverVisible(false);
  };

  return (
    <div className="col-span-12 rounded-2xl border border-stroke bg-white px-5 pb-5 pt-7.5 shadow-default dark:border-strokedark dark:bg-boxdark sm:px-7.5 xl:col-span-5">
      <div className="mb-3 flex flex-col flex-wrap gap-4 sm:flex-row sm:justify-between">
        <div className="mb-3 flex items-center sm:mb-0">
          <h5 className="text-lg font-semibold text-black dark:text-white">
            Companies
          </h5>
        </div>
        <div className="flex items-center">
          <span 
            className="relative z-20 cursor-pointer"
            onMouseEnter={handleMouseEnter}
            onMouseLeave={handleMouseLeave}
          >
            <svg
              className="transition-transform duration-300 hover:scale-110"
              width="20"
              height="20"
              viewBox="0 0 10 10"
              fill="none"
              xmlns="http://www.w3.org/2000/svg"
            >
              <circle cx="5" cy="5" r="5" fill="#08d116" />
              <text
                x="5"
                y="5"
                textAnchor="middle"
                dy=".3em"
                fontSize="6"
                fill="white"
              >
                ?
              </text>
            </svg>
            {isPopoverVisible && (
              <div
                className="absolute z-50 w-64 text-sm text-gray-500 transition-opacity duration-300 bg-white border border-gray-200 rounded-lg shadow-sm dark:text-gray-400 dark:border-gray-600 dark:bg-gray-800"
                style={{ top: '50%', right: '30px', transform: 'translateY(-50%)' }}
              >
                <div className="px-3 py-2 bg-gray-100 border-b border-gray-200 rounded-t-lg dark:border-gray-600 dark:bg-gray-700">
                  <h3 className="font-semibold text-gray-900 dark:text-white">
                    Companies by Tier
                  </h3>
                </div>
                <div className="px-3 py-2">
                  <p>Here are the companies you purchased from last month organized by their tier. Tier 1 companies are the most sustainable, and Tier 4 companies are the least sustainable.</p>
                </div>
              </div>
            )}
          </span>
        </div>
      </div>

      <div className="mb-2">
        <div id="chartThree" className="mx-auto flex justify-center">
          <ReactApexChart
            options={options}
            series={series}
            type="donut"
            width={`90%`}
            height={`90%`}
          />
        </div>
      </div>

      <div className="-mx-8 flex flex-wrap items-center justify-center gap-y-3">
        <div className="w-full px-8 sm:w-1/2">
          <div className="flex w-full items-center">
            <span className="mr-2 block h-3 w-full max-w-3 rounded-full bg-[#4BAE50]"></span>
            <p className="flex w-full justify-between text-sm font-medium text-black dark:text-white">
              <span> Tier 1 </span>
              <span> {Math.round(companyTiers[0]/companyTiers.reduce((a, b) => a + b, 0) * 100)}% </span>
            </p>
          </div>
        </div>
        <div className="w-full px-8 sm:w-1/2">
          <div className="flex w-full items-center">
            <span className="mr-2 block h-3 w-full max-w-3 rounded-full bg-[#CCDA38]"></span>
            <p className="flex w-full justify-between text-sm font-medium text-black dark:text-white">
              <span> Tier 2 </span>
              <span> {Math.round(companyTiers[1]/companyTiers.reduce((a,b) => a + b, 0) * 100)}% </span>
            </p>
          </div>
        </div>
        <div className="w-full px-8 sm:w-1/2">
          <div className="flex w-full items-center">
            <span className="mr-2 block h-3 w-full max-w-3 rounded-full bg-[#FEC005]"></span>
            <p className="flex w-full justify-between text-sm font-medium text-black dark:text-white">
              <span> Tier 3 </span>
              <span>{Math.round(companyTiers[2]/companyTiers.reduce((a,b) => a + b, 0) * 100)}% </span>
            </p>
          </div>
        </div>
        <div className="w-full px-8 sm:w-1/2">
          <div className="flex w-full items-center">
            <span className="mr-2 block h-3 w-full max-w-3 rounded-full bg-[#FE5620]"></span>
            <p className="flex w-full justify-between text-sm font-medium text-black dark:text-white">
              <span> Tier 4 </span>
                <span>{Math.round(companyTiers[3]/companyTiers.reduce((a,b) => a + b, 0) * 100)}% </span>
            </p>
          </div>
        </div>
      </div>
    </div>
  );
};

export default CompaniesPieChart;