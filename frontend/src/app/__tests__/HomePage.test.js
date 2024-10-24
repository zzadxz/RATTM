import React, { useEffect, useState } from "react";
import { render, screen } from '@testing-library/react';
import HomePage from '@/app/page';

describe('HomePage', () => {
  it('renders the main heading', () => {
    render(<HomePage />);
    const heading = screen.getByText(/Welcome to RATTM/i);
    expect(heading).toBeInTheDocument();
  });
});
