import { Metadata } from "next";
import TransactionMap from "@/app/components/TransactionMap";

export const metadata: Metadata = {
  title: "Next.js Calender | TailAdmin - Next.js Dashboard Template",
  description:
    "This is Next.js Calender page for TailAdmin  Tailwind CSS Admin Dashboard Template",
};

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
