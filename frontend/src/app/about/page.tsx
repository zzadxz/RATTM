import { Metadata } from "next";
import Image from "next/image";

export const metadata: Metadata = {
  title:
    "Next.js E-commerce Dashboard | TailAdmin - Next.js Dashboard Template",
  description: "This is Next.js Home for TailAdmin Dashboard Template",
};

export default function About() {
  return (
    <div className="ml-20 mr-20 mt-4 grid grid-cols-1 gap-4 md:mt-6 md:grid-cols-12 md:gap-6 2xl:mt-7.5 2xl:gap-7.5">
      <div id="left-col" className="rounded-2xl md:col-span-6">
        <h1 className="mb-7 mt-10 text-5xl font-extrabold text-black dark:text-white">
          About Your Score
        </h1>
        <p className="mb-7 mt-2 text-lg font-medium text-black">
          Our goal with the Environmental Friendliness Score is to give you
          insight into the environmental impact of your purchases, helping you
          understand how your spending aligns with sustainability goals.
        </p>
        <p className="mt-2 text-lg font-medium text-black">
          Our algorithm prioritizes simplicity and transparency and provides you
          with a quick look at how eco-friendly your purchases are. By
          normalizing the Environmental Impact Score (EIS) of common companies
          and tying it directly to spending, we give you a straightforward,
          actionable score that reflects your individual impact. It keeps you
          informed about how your purchases affect the environment without
          making specific recommendations, empowering you to make decisions in
          line with your values.
        </p>
        <button className="mt-5 w-1/3 rounded-2xl border border-stroke bg-green-400 px-5 pb-3 pt-3 font-bold text-white sm:px-7.5 xl:col-span-8">
          SIGN IN
        </button>
      </div>
      <div
        id="right-col"
        className="flex h-full flex-col items-center justify-center rounded-2xl md:col-span-6"
      >
        <Image
          src="/images/logo/woman-holding-grlobe.svg"
          alt="RATTM CO2 Calculator"
          width={634}
          height={538}
          className="w-full"
        />
      </div>
    </div>
  );
}
