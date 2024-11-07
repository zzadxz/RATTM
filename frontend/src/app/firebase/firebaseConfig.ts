// src/app/firebase/firebaseConfig.ts
import { log } from "../../utils/log";

log("Firebase Config:", {
  // do keys exist? boolean
  apiKey: process.env.NEXT_PUBLIC_FIREBASE_API_KEY
    ? true
    : console.error("Firebase API Key not found"),
});
log("Firebase Config:", {
  //do keys exist? boolean
  authDomain: process.env.NEXT_PUBLIC_FIREBASE_AUTH_DOMAIN
    ? true
    : console.error("Firebase Auth Domain not found"),
});

import { initializeApp } from "firebase/app";
import { getAuth } from "firebase/auth";
import { getAnalytics } from "firebase/analytics";

const firebaseConfig = {
  apiKey: process.env.NEXT_PUBLIC_FIREBASE_API_KEY,
  authDomain: process.env.NEXT_PUBLIC_FIREBASE_AUTH_DOMAIN,
  projectId: process.env.NEXT_PUBLIC_FIREBASE_PROJECT_ID,
  storageBucket: process.env.NEXT_PUBLIC_FIREBASE_STORAGE_BUCKET,
  messagingSenderId: process.env.NEXT_PUBLIC_FIREBASE_MESSAGING_SENDER_ID,
  appId: process.env.NEXT_PUBLIC_FIREBASE_APP_ID,
  measurementId: process.env.NEXT_PUBLIC_FIREBASE_MEASUREMENT_ID,
};

const app = initializeApp(firebaseConfig);
const auth = getAuth(app);

const analytics = typeof window !== "undefined" ? getAnalytics(app) : null;

export { auth, analytics };
