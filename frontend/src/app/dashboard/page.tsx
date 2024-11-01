// src/app/dashboard/page.tsx

"use client";
import React, { useEffect, useState } from "react";
import { auth } from "@/app/firebase/firebaseConfig";
import { useRouter } from "next/navigation";

const Dashboard: React.FC = () => {
  const [displayName, setDisplayName] = useState<string | null>(null);
  const [loading, setLoading] = useState(true);
  const router = useRouter();

  useEffect(() => {
    const unsubscribe = auth.onAuthStateChanged((user) => {
      if (user) {
        setDisplayName(user.displayName || "User");
        setLoading(false);
      } else {
        router.replace("/main-site/auth/SignInWithGoogle"); // Use replace instead of push
      }
    });

    return () => unsubscribe();
  }, [router]);

  const handleSignOut = async () => {
    try {
      await auth.signOut();
      router.replace("/"); // Use replace instead of push
    } catch (error) {
      console.error("Sign out error:", error);
    }
  };

  if (loading) {
    return (
      <div className="flex items-center justify-center h-screen">
        <p className="text-2xl font-bold animate-pulse text-gray-600">Loading...</p>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gradient-to-r from-blue-500 to-indigo-700 flex flex-col items-center justify-center p-6">
      <div className="bg-white rounded-lg shadow-lg p-8 max-w-lg w-full text-center">
        <h1 className="text-4xl font-extrabold text-gray-800 mb-4">
          Welcome, {displayName}!
        </h1>
        <p className="text-gray-600 mb-6">This is your personalized dashboard.</p>
        <button
          onClick={handleSignOut}
          className="px-6 py-3 bg-red-500 text-white font-semibold rounded-md hover:bg-red-600 transition duration-300"
        >
          Sign Out
        </button>
      </div>
    </div>
  );
};

export default Dashboard;
