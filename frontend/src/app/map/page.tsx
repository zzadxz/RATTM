"use client";

import TransactionMap from "@/app/components/TransactionMap";
import React from "react";

const Map = () => {
  return (
    <div className="mx-auto max-w-7xl">
      <h1 className="mb-5 mt-5 text-center text-3xl font-extrabold text-black dark:text-white">
        Purchases Map
      </h1>
      <TransactionMap />
    </div>
  );
};

export default Map;
