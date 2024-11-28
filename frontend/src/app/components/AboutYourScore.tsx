"use client";

import React from "react";

interface AboutYourScoreProps {
  isHovered: boolean;
}

const AboutYourScore: React.FC<AboutYourScoreProps> = ({ isHovered }) => {
  return (
    <>
      <div
        className={`about-your-score col-span-12 mt-5 rounded-2xl border border-stroke px-5 pb-5 pt-7.5 dark:border-strokedark dark:bg-boxdark sm:px-7.5 xl:col-span-8 transition-transform duration-300 ${
          isHovered ? "scale-105 shadow-lg" : ""
        }`}
      >
        <h1 className="text-xl font-extrabold text-black dark:text-white">
          About your Eco-Score
        </h1>
        <p className="text-md pt-4">
          We calculate based on normalized company ESG data to provide a quick
          look at how eco-friendly your purchases are.
        </p>
        <p className="text-md pt-4">
          Read more about our algorithm on the About page!
        </p>
      </div>
      <a href="/about">
        <button className="mt-5 w-full rounded-2xl border border-stroke bg-green-400 px-5 pb-3 pt-3 font-bold text-white sm:px-7.5 xl:col-span-8">
          LEARN MORE
        </button>
      </a>
    </>
  );
};

export default AboutYourScore;