"use client";

import mapboxgl from "mapbox-gl";
import "mapbox-gl/dist/mapbox-gl.css";
import React, { useEffect, useRef } from "react";

const colorMap: { [key: number]: { textColor: string; description: string } } =
  {
    1: { textColor: "red", description: "Awful" },
    2: { textColor: "orange", description: "Pretty Bad" },
    3: { textColor: "gold", description: "Decent" },
    4: { textColor: "green", description: "Great" },
  };

interface MapPoint {
  location: Array<number>;
  merchant_name: string;
  merchant_percentile: number;
}

mapboxgl.accessToken = process.env.NEXT_PUBLIC_MAPBOX_KEY || "";

const TransactionMap: React.FC = () => {
  const mapContainer = useRef<HTMLDivElement | null>(null);

  useEffect(() => {
    const fetchData = async () => {
      const response = await fetch(
        "https://rattm-f300025e7172.herokuapp.com/map/get_map_data/",
        {
          method: "GET",
          headers: {
            "Content-Type": "application/json",
          },
        }
      );
      const data = await response.json();

      const map = new mapboxgl.Map({
        container: mapContainer.current || "",
        style: "mapbox://styles/mapbox/streets-v11",
        center: [-79.390889, 43.667331],
        zoom: 3,
      });

      data.forEach(
        ({ location, merchant_name, merchant_percentile }: MapPoint) => {
          const [latitude, longitude] = location;
          const { textColor, description } = colorMap[merchant_percentile];
          new mapboxgl.Marker()
            .setLngLat([longitude, latitude])
            .setPopup(
              new mapboxgl.Popup({ offset: 25 }).setHTML(`
                <h3 className='text-3xl' style='text-align: center; font-weight: bold;'>
                  ${merchant_name}
                </h3>
                <p className="text-lg">
                  Rating:
                  <span style='color: ${textColor}'>${description}</span>
                </p>
              `)
            )
            .addTo(map);
        }
      );

      return () => map.remove();
    };

    fetchData();
  }, []);

  return (
    <>
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
    </>
  );
};

export default TransactionMap;
