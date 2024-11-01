// src/app/components/Navbar.tsx

"use client";

import React, { useEffect, useState } from "react";
import Link from "next/link";
import { auth } from "@/app/firebase/firebaseConfig";
import { useRouter } from "next/navigation";
import { User } from "firebase/auth";

const Navbar: React.FC = () => {
  const [user, setUser] = useState<User | null>(null);
  const [loading, setLoading] = useState(true);
  const router = useRouter();

  useEffect(() => {
    const unsubscribe = auth.onAuthStateChanged((currentUser) => {
      setUser(currentUser);
      setLoading(false);
    });

    return () => unsubscribe();
  }, []);

  if (loading) return null;

  const handleSignOut = async () => {
    try {
      await auth.signOut();
      router.push("/main-site/auth/SignInWithGoogle");
    } catch (error) {
      console.error("Error signing out:", error);
    }
  };

  return (
    <nav className="bg-gray-900 text-white p-4 fixed top-0 left-0 w-full shadow-md z-10">
      <div className="container mx-auto flex justify-between items-center">
        <div className="text-xl font-bold">
          <Link href="/">RATTM</Link>
        </div>
        <div className="flex space-x-6">
          <Link href="/" className="hover:text-green-400">Home</Link>
          <Link href="/about" className="hover:text-green-400">About</Link>
          <Link href="/transactions" className="hover:text-green-400">Transactions</Link>
          <Link href="/contact" className="hover:text-green-400">Contact</Link>
          {user ? (
            <>
              <Link href="/dashboard" className="hover:text-green-400">
                Dashboard
              </Link>
              <button onClick={handleSignOut} className="hover:text-red-400">
                Sign Out
              </button>
            </>
          ) : (
            <Link href="/main-site/auth/SignInWithGoogle" className="hover:text-green-400">
              Sign In
            </Link>
          )}
        </div>
      </div>
    </nav>
  );
};

Navbar.displayName = "Navbar";

export default Navbar;
