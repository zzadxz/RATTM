"use client";
import Image from "next/image";
import React, { useEffect, useState } from "react";
import Link from "next/link";
import { auth } from "@/app/firebase/firebaseConfig";
import { User } from "firebase/auth";

export default function Home() {
  const [user, setUser] = useState<User | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const unsubscribe = auth.onAuthStateChanged((currentUser) => {
      setUser(currentUser);
      setLoading(false);
    });

    return () => unsubscribe();
  }, []);

  if (loading) return null;

  return (
    <div className="ml-20 mr-20 mt-4 grid grid-cols-1 gap-4 md:mt-6 md:grid-cols-12 md:gap-6 2xl:mt-7.5 2xl:gap-7.5">
      <div id="left-col" className="rounded-2xl md:col-span-6">
        <Image
          src="/images/logo/rootpage-logo.png"
          alt="Eco-Score by RATTM"
          width={872}
          height={774}
          className="w-full"
        />
      </div>
      <div
        id="right-col"
        className="flex h-full flex-col items-center justify-center rounded-2xl md:col-span-6"
      >
        <div className="max-w-sm rounded-lg bg-green-100 p-6 text-center shadow-md w-full">
          <h1 className="text-xl font-bold text-gray-900">
            Welcome to RATTM&apos;s
            <br />
            Eco-Score calculator
          </h1>
          <p className="mt-2 text-gray-700">Improve your Eco-Score today!</p>
        </div>
        {user ? (
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
        )}
      </div>
    </div>
  );
}
