// src/app/main-site/auth/SignInWithGoogle/page.tsx

"use client";
import React, { useEffect, useState } from "react";
import { signInWithGoogle } from "@/app/firebase/authService";
import { useRouter } from "next/navigation";
import { auth } from "@/app/firebase/firebaseConfig";

const SignInWithGoogle: React.FC = () => {
  const router = useRouter();
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const unsubscribe = auth.onAuthStateChanged((user) => {
      if (user) {
        router.replace("/dashboard"); // Use replace instead of push
      }
      setLoading(false);
    });
    return () => unsubscribe();
  }, [router]);

  const handleGoogleSignIn = async () => {
    try {
      setLoading(true);
      await signInWithGoogle();
      // Don't redirect here - let the auth state listener handle it
    } catch (error) {
      console.error("Google sign-in error:", error);
      setLoading(false);
    }
  };

  if (loading) {
    return <div className="flex items-center justify-center min-h-screen bg-gray-100">
      <p>Loading...</p>
    </div>;
  }

  return (
    <div className="flex items-center justify-center min-h-screen bg-gray-100">
      <div className="text-center">
        <h2 className="text-2xl font-bold mb-6">Sign In with Google</h2>
        <button
          onClick={handleGoogleSignIn}
          className="px-6 py-3 bg-blue-500 text-white font-semibold rounded-md hover:bg-blue-600 transition duration-300"
        >
          Sign In with Google
        </button>
      </div>
    </div>
  );
};

export default SignInWithGoogle;
