// frontend/src/app/components/charts/FootprintLineGraph.tsx

"use client";

import { ApexOptions } from "apexcharts";
import React, { useEffect, useState } from "react";
import dynamic from "next/dynamic";

const ReactApexChart = dynamic(() => import("react-apexcharts"), {
  ssr: false,
});

const FootprintLineGraph: React.FC = () => {
  const [series, setSeries] = useState([
    {
      name: "Green Transactions",
      data: [],
      color: "#08d116",
    },
    {
      name: "Eco-Score",
      data: [],
      color: "#7d91f5",
    },
  ]);

  const [categories, setCategories] = useState([]);

  useEffect(() => {
    const fetchData = async () => {
      try {
        const response = await fetch(
          "https://rattm-f300025e7172.herokuapp.com/dashboard/get_line_graph_data/"
        );
        const data = await response.json();

        setCategories(data.months);
        setSeries([
          {
            name: "Green Transactions",
            data: data.green_transactions,
            color: "#08d116",
          },
          {
            name: "Eco-Score",
            data: data.carbon_scores,
            color: "#7d91f5",
          },
        ]);
      } catch (error) {
        console.error("Error fetching data:", error);
      }
    };

    fetchData();
  }, []);

  const options: ApexOptions = {
    legend: {
      show: false,
      position: "top",
      horizontalAlign: "left",
    },
    colors: ["#7d91f5", "#08d116"],
    chart: {
      fontFamily: "Satoshi, sans-serif",
      height: 335,
      type: "area",
      dropShadow: {
        enabled: true,
        color: "#623CEA14",
        top: 10,
        blur: 4,
        left: 0,
        opacity: 0.1,
      },

      toolbar: {
        show: false,
      },
    },
    responsive: [
      {
        breakpoint: 1024,
        options: {
          chart: {
            height: 300,
          },
        },
      },
      {
        breakpoint: 1366,
        options: {
          chart: {
            height: 350,
          },
        },
      },
    ],
    stroke: {
      width: [2, 2],
      curve: "straight",
    },
    // labels: {
    //   show: false,
    //   position: "top",
    // },
    grid: {
      xaxis: {
        lines: {
          show: true,
        },
      },
      yaxis: {
        lines: {
          show: true,
        },
      },
    },
    dataLabels: {
      enabled: false,
    },
    markers: {
      size: 6,
      colors: "#fff",
      strokeColors: ["#08d116", "#7d91f5"],
      strokeWidth: 3,
      strokeOpacity: 0.9,
      strokeDashArray: 0,
      fillOpacity: 1,
      discrete: [],
      hover: {
        size: undefined,
        sizeOffset: 5,
      },
    },
    xaxis: {
      type: "category",
      categories: categories,
      axisBorder: {
        show: false,
      },
      axisTicks: {
        show: false,
      },
    },
    yaxis: [
      {
        title: {
          text: "Green Transactions",
        },
        min: 0,
        max: 5,
        tickAmount: 5,
      },
      {
        opposite: true,
        title: {
          text: "Eco-Score",
        },
        min: 0,
        max: 600,
        tickAmount: 6,
      },
    ],
  };

  return (
    <div className="col-span-12 rounded-sm border border-stroke bg-white px-5 pb-5 pt-7.5 dark:border-strokedark dark:bg-boxdark sm:px-7.5 xl:col-span-8">
      <h1 className="text-3xl font-extrabold text-black dark:text-white">
        Your footprint over time
      </h1>
      <p className="pt-4 text-xl">
        See how your Eco-Score varied in the last 12 months
      </p>
      <br />
      <div className="flex flex-wrap items-start justify-between gap-3 sm:flex-nowrap">
        <div className="flex w-full flex-wrap gap-3 sm:gap-5">
          {series.map(({ name, color }) => (
            <div className="flex min-w-47.5" key={name}>
              <span
                className="mr-2 mt-1 flex h-4 w-full max-w-4 items-center justify-center rounded-full border"
                style={{ borderColor: color }}
              >
                <span
                  className="block h-2.5 w-full max-w-2.5 rounded-full"
                  style={{ backgroundColor: color }}
                ></span>
              </span>
              <div className="w-full">
                <p className="font-semibold" style={{ color: color }}>
                  {name}
                </p>
                <p className="text-sm font-medium">10/01/2023 - 10/01/2024</p>
              </div>
            </div>
          ))}
          {/* <div className="flex w-full max-w-45 justify-end">
            <div className="inline-flex items-center rounded-md bg-whiter p-1.5 dark:bg-meta-4">
              <button className="rounded px-3 py-1 text-xs font-medium text-black hover:bg-white hover:shadow-card dark:text-white dark:hover:bg-boxdark">
                By Week
              </button>
              <button className="rounded bg-white px-3 py-1 text-xs font-medium text-black shadow-card hover:bg-white hover:shadow-card dark:bg-boxdark dark:text-white dark:hover:bg-boxdark">
                By Month
              </button>
            </div>
          </div> */}
        </div>
      </div>

      <div>
        <div id="chartOne" className="-ml-5">
          <ReactApexChart
            options={options}
            series={series}
            type="area"
            height={350}
            width={"100%"}
          />
        </div>
      </div>
    </div>
  );
};

export default FootprintLineGraph;