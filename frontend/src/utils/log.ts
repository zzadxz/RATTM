const isDevelopment = process.env.NODE_ENV === "development";

export const log = (...args: unknown[]) => {
  if (isDevelopment) {
    log(...args);
  }
};
