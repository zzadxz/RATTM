"use client";
import "jsvectormap/dist/jsvectormap.css";
import "flatpickr/dist/flatpickr.min.css";
import "@/css/satoshi.css";
import "@/css/style.css";
import React from "react";
import Navbar from "@/app/components/Navbar";
import Head from "next/head";

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en">
      <Head>
        <title>Cash App Eco-Score</title>
        <meta name="description" content="Calculate and improve your Eco-Score with RATTM's innovative tool." />
        <meta name="viewport" content="width=device-width, initial-scale=1" />
        <link rel="icon" href="/favicon.ico" />
      </Head>
      <body suppressHydrationWarning={true}>
        <div className="dark:bg-boxdark-2 dark:text-bodydark">
          <div className="relative flex flex-1 flex-col">
            <Navbar />
            <main>
              <div className="mx-auto max-w-screen-2xl px-10 md:px-20 2xl:px-24">
                {children}
              </div>
            </main>
          </div>
        </div>
      </body>
    </html>
  );
}
