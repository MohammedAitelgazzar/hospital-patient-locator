import React, { useState } from "react";
import { MapContainer, ImageOverlay, Marker, Tooltip } from "react-leaflet";
import L from "leaflet";
import "leaflet/dist/leaflet.css";

// Path to the floor plan image in the public folder
const floorPlanUrl = "/image.png";

// Define the bounds of the image (custom coordinate space)
const bounds = [
  [500, 0], // Top-left corner (flipped Y)
  [0, 500], // Bottom-right corner (flipped Y)
];

// Room positions with patient details (adjust positions based on your map)
// Set a fixed Y value for horizontal arrangement and vary the X values for each room
const roomMarkers = [
  { id: 1, position: [350, 90], room: "Room 101" },
  { id: 2, position: [350, 210], room: "Room 102" },
  { id: 3, position: [350, 280], room: "Room 103" },
  { id: 4, position: [330, 380], room: "Room 104" },
  { id: 5, position: [230, 130], room: "Room 105" },
  { id: 6, position: [230, 200], room: "Room 106" },
];

// Create a custom marker icon
const markerIcon = L.icon({
  iconUrl: "https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.7.1/images/marker-icon.png",
  iconSize: [25, 41],
  iconAnchor: [12, 41],
});

const FloorMapComponent = () => {
  // Manually set the patient names and room IDs
  const patients = [
    { name: "Chayma", roomId: 5 }, 
    { name: "Marouane", roomId: 6 }, 
  ];

  // Filter the room markers based on the patients' room IDs
  const filteredMarkers = roomMarkers.filter((marker) =>
    patients.some((patient) => patient.roomId === marker.id)
  );

  return (
    <div>
      {/* Map container */}
      <MapContainer
        crs={L.CRS.Simple} // Use a simple CRS for 2D image mapping
        bounds={bounds}
        style={{ height: "500px", width: "100%" }}
        zoom={0} // Initial zoom level
        minZoom={-2} // Allow zooming out for a better overview
        maxZoom={2} // Allow zooming in for details
      >
        {/* Add the floor plan as an overlay */}
        <ImageOverlay url={floorPlanUrl} bounds={bounds} />

        {/* Add the filtered markers */}
        {filteredMarkers.map((marker) => {
          // Find the patient for the current room marker
          const patient = patients.find((p) => p.roomId === marker.id);
          return (
            <Marker key={marker.id} position={marker.position} icon={markerIcon}>
              <Tooltip>
                <b>{marker.room}</b>
                <br />
                Patient: {patient ? patient.name : "No patient assigned"}
              </Tooltip>
            </Marker>
          );
        })}
      </MapContainer>
    </div>
  );
};

export default FloorMapComponent;
