// src/app/components/Navbar.tsx

import Image from "next/image";
import React, { useEffect, useState } from "react";
import Link from "next/link";
import { auth } from "@/app/firebase/firebaseConfig";
import { useRouter } from "next/navigation";
import { User } from "firebase/auth";

const navBarLinks = [
  { name: "Home", link: "/", access_restricted: false },
  { name: "About", link: "/about", access_restricted: false },
  { name: "Eco-Score Dashboard", link: "/dashboard", access_restricted: true },
  { name: "Transactions", link: "/transactions", access_restricted: true },
  { name: "Map", link: "/map", access_restricted: true },
];

const Navbar = () => {
  const [menuOpen, setMenuOpen] = useState(false);
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
      router.push("/");
    } catch (error) {
      console.error("Error signing out:", error);
    }
  };

  return (
    <header className="sticky top-0 z-50 w-full bg-white">
      <div className="flex items-center justify-between px-3 py-3 md:px-6 2xl:px-11">
        <Link href="/" className="flex-shrink-0">
          <Image
            src="/images/logo/rattm-logo.png"
            width={50}
            height={50}
            alt="Logo"
          />
        </Link>

        <div className="hidden max-w-full flex-grow justify-end overflow-clip sm:flex">
          <ul className="flex items-center gap-2 2xsm:gap-6">
            {navBarLinks.map(({ name, link, access_restricted }) =>
              user || !access_restricted ? (
                <li key={name}>
                  <a href={link} className="text-sm font-extrabold text-black">
                    {name.toUpperCase()}
                  </a>
                </li>
              ) : null
            )}
            <li className="flex items-center gap-2 2xsm:gap-6">
              {user ? (
                <button
                  onClick={handleSignOut}
                  className="text-sm font-extrabold text-black"
                >
                  SIGN OUT
                </button>
              ) : (
                <>
                  <Link
                    href="/main-site/auth/SignInWithGoogle"
                    className="text-sm font-extrabold text-black"
                  >
                    SIGN IN
                  </Link>
                  <Link
                    href="/main-site/auth/SignInWithGoogle"
                    className="text-sm font-extrabold text-black"
                  >
                    SIGN UP
                  </Link>
                </>
              )}
            </li>
          </ul>
        </div>

        <div className="flex-shrink-0 sm:hidden">
          <button
            onClick={() => setMenuOpen(!menuOpen)}
            className="focus:outline-none"
            aria-label="Toggle Menu"
          >
            <svg
              className="h-6 w-6 text-black"
              fill="none"
              stroke="currentColor"
              viewBox="0 0 24 24"
              xmlns="http://www.w3.org/2000/svg"
            >
              <path
                strokeLinecap="round"
                strokeLinejoin="round"
                strokeWidth={2}
                d="M4 6h16M4 12h16m-7 6h7"
              />
            </svg>
          </button>
        </div>
      </div>

      {menuOpen && (
        <div className="bg-white shadow-md sm:hidden">
          <ul className="flex flex-col items-center gap-4 py-4">
            {navBarLinks.map(({ name, link }) => (
              <li key={name}>
                <a
                  href={link}
                  onClick={() => setMenuOpen(false)}
                  className="text-sm font-extrabold text-black"
                >
                  {name.toUpperCase()}
                </a>
              </li>
            ))}
          </ul>
        </div>
      )}
    </header>
  );
};

export default Navbar;