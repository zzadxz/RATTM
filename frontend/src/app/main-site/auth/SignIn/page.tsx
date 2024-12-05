// src/app/main-site/auth/SignIn/page.tsx

"use client";

import React, { useState } from "react";
import { signIn } from "@/app/firebase/authService";

const SignIn: React.FC = () => {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState<string | null>(null);

  const handleSignIn = async (e: React.FormEvent) => {
    e.preventDefault();
    try {
      await signIn(email, password);
      // Redirect or handle successful sign-in
    } catch (err: unknown) {
      if (err instanceof Error) {
        setError(err.message);
      }
    }
  };

  return (
    <div className="flex items-center justify-center min-h-screen bg-gray-100">
      <form onSubmit={handleSignIn} className="bg-white p-8 rounded shadow-md w-full max-w-md">
        <h2 className="text-2xl font-bold mb-6 text-center">Sign In</h2>
        {error && <p className="text-red-500">{error}</p>}
        <input
          type="email"
          placeholder="Email"
          value={email}
          onChange={(e) => setEmail(e.target.value)}
          className="w-full p-3 border rounded mb-4"
        />
        <input
          type="password"
          placeholder="Password"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
          className="w-full p-3 border rounded mb-4"
        />
        <button type="submit" className="w-full bg-green-500 text-white p-3 rounded font-bold">
          Sign In
        </button>
      </form>
    </div>
  );
};

export default SignIn;
