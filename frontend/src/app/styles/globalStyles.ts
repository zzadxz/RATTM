// src/app/styles/globalStyles.ts
import { createGlobalStyle } from 'styled-components';

export const GlobalStyle = createGlobalStyle`
  *, *::before, *::after {
    margin: 0;
    padding: 0;
    box-sizing: border-box;
  }

  html, body {
    width: 100%;
    height: 100%;
    overflow-x: hidden;
    background: linear-gradient(135deg, #5500ff 0%, #30009c 100%);
    background-attachment: fixed; /* Ensures the background stays fixed */
  }

  #__next {
    width: 100%;
    height: 100%;
  }
`;
