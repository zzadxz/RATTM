"use client";
// import jsVectorMap from "jsvectormap";
// import "jsvectormap/dist/jsvectormap.css";
import mapboxgl from "mapbox-gl";
import React, { useEffect, useRef } from "react";
// import "../../js/us-aea-en";

mapboxgl.accessToken =
  "pk.eyJ1IjoiZ2FicmllbGV6cmF0aG9tcHNvbiIsImEiOiJjbTJ6OWpwcTQwOTh2MmxvZ3BpaW5wajhkIn0.BFA_fvxSDOBkZkAdXjnxiQ";

const TransactionMap: React.FC = () => {
  const mapContainer = useRef(null);

  useEffect(() => {
    // Initialize the Mapbox map
    const map = new mapboxgl.Map({
      container: mapContainer.current || "",
      style: "mapbox://styles/mapbox/streets-v11", // Map style
      center: [-74.5, 40], // Initial position [lng, lat]
      zoom: 9, // Initial zoom level
    });

    return () => map.remove(); // Clean up on unmount
  }, []);

  return (
    <div
      ref={mapContainer}
      className="map-container"
      style={{
        margin: "auto",
        width: "80vw",
        height: "69vh",
        minHeight: "400px",
        maxHeight: "100%",
        borderRadius: "20px", // Added rounded corners
        overflow: "hidden", // Ensures the map content does not overflow the rounded edges
      }}
    />
  );
};

export default TransactionMap;
