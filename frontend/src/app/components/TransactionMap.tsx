"use client";

import mapboxgl from "mapbox-gl";
import React, { useEffect, useRef } from "react";

mapboxgl.accessToken =
  "pk.eyJ1IjoiZ2FicmllbGV6cmF0aG9tcHNvbiIsImEiOiJjbTJ6OWpwcTQwOTh2MmxvZ3BpaW5wajhkIn0.BFA_fvxSDOBkZkAdXjnxiQ";

const TransactionMap: React.FC = () => {
  const mapContainer = useRef(null);

  useEffect(() => {
    // Initialize the Mapbox map
    const map = new mapboxgl.Map({
      container: mapContainer.current || "",
      style: "mapbox://styles/mapbox/streets-v11", 
      center: [-74.5, 40], 
      zoom: 9, 
    });

    return () => map.remove(); 
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
        borderRadius: "20px", 
        overflow: "hidden",
      }}
    />
  );
};

export default TransactionMap;
