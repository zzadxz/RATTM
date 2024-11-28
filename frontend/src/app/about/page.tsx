"use client";

import { auth } from "@/app/firebase/firebaseConfig";
import { User } from "firebase/auth";
import { useEffect, useState } from "react";
import Link from "next/link";
import Image from "next/image";

export default function About() {
  const [user, setUser] = useState<User | null>(null);
  const [loaded, setLoaded] = useState(false);

  useEffect(() => {
    const unsubscribe = auth.onAuthStateChanged((currentUser) => {
      setUser(currentUser);
      setLoaded(true);
    });

    return () => unsubscribe();
  }, []);

  return (
    <div className="ml-20 mr-20 mt-4 grid grid-cols-1 gap-4 md:mt-6 md:grid-cols-12 md:gap-6 2xl:mt-7.5 2xl:gap-7.5">
      <div id="left-col" className="rounded-2xl md:col-span-6">
        <h1 className="mb-7 mt-10 text-5xl font-extrabold text-black dark:text-white">
          About Your Eco-Score
        </h1>
        <p className="mb-7 mt-2 text-lg font-medium text-black">
          Our goal with the Eco-Score is to give you insight into the
          environmental impact of your purchases, helping you understand how
          your spending aligns with sustainability goals.
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
        {loaded ? (
          user ? (
            <Link href="/dashboard">
              <button className="mt-4 rounded-lg bg-green-500 px-8 py-3 font-bold text-white transition duration-200 hover:bg-green-600">
                DASHBOARD
              </button>
            </Link>
          ) : (
            <Link href="/main-site/auth/SignInWithGoogle">
              <button className="mt-4 rounded-lg bg-green-500 px-8 py-3 font-bold text-white transition duration-200 hover:bg-green-600">
                SIGN IN
              </button>
            </Link>
          )
        ) : (
          <button className="mt-4 rounded-lg bg-green-500 px-8 py-3 font-bold text-white transition duration-200 hover:bg-green-600">
            Loading...
          </button>
        )}
      </div>
      <div
        id="right-col"
        className="flex h-full flex-col items-center justify-center rounded-2xl md:col-span-6"
      >
        <Image
          src="/images/logo/woman-holding-grlobe.svg"
          alt="RATTM Eco-Score Calculator"
          width={634}
          height={538}
          className="w-full"
        />
      </div>
    </div>
  );
}
