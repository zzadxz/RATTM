import { Metadata } from "next";

export const metadata: Metadata = {
  title:
    "Next.js E-commerce Dashboard | TailAdmin - Next.js Dashboard Template",
  description: "This is Next.js Home for TailAdmin Dashboard Template",
};

export default function Transactions() {
  return (
    <div className="mx-auto max-w-7xl">
      <h1 className="mb-5 mt-5 text-center text-3xl font-extrabold text-black dark:text-white">
        All recent transactions
      </h1>
      <p className="text-center">I'll put stuff here later</p>
    </div>
  );
}
