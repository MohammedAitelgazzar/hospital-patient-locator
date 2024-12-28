import React, { useState, useEffect, useRef } from "react";
import { MapContainer, ImageOverlay, Marker, Tooltip } from "react-leaflet";
import L from "leaflet";
import "leaflet/dist/leaflet.css";
import { getUserDetails, getLocalisations } from "../service/apiService";
import '../style/mapStyle.css'; 

const floorPlanUrl = "/image.png";
const bounds = [
  [500, 0],
  [0, 500],
];

const roomMarkers = [
  { id: 1, position: [350, 90], room: "Room 101" },
  { id: 2, position: [350, 210], room: "Room 102" },
  { id: 3, position: [350, 280], room: "Room 103" },
  { id: 4, position: [330, 380], room: "Room 104" },
  { id: 5, position: [230, 130], room: "Room 105" },
  { id: 6, position: [230, 200], room: "Room 106" },
  { id: 7, position: [110, 100], room: "Toilette 1" },
  { id: 8, position: [70, 230], room: "Toilette 2" },
];

const markerIcon = L.icon({
  iconUrl: "https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.7.1/images/marker-icon.png",
  iconSize: [25, 41],
  iconAnchor: [12, 41],
});

const FloorMapComponent = () => {
  const [localisation, setLocalisation] = useState(null); 
  const [userDetails, setUserDetails] = useState({});
  const [hoveredUsername, setHoveredUsername] = useState(null);
  const [loadingLocalisation, setLoadingLocalisation] = useState(false);
  const [loadingUserDetails, setLoadingUserDetails] = useState(false);
  const [userCache, setUserCache] = useState({});
  const [modalVisible, setModalVisible] = useState(false);
  const [selectedRoomDetails, setSelectedRoomDetails] = useState(null);
  
  const [imageDimensions, setImageDimensions] = useState({ width: 0, height: 0 });
  const mapContainerRef = useRef(null);

  const fetchLocalisations = async () => {
    setLoadingLocalisation(true);
    try {
      const data = await getLocalisations();
      console.log("Fetched localisation data:", data);
      if (data && typeof data === "object") {
        setLocalisation(data);
      } else {
        console.error("Unexpected response format:", data);
        setLocalisation(null);
      }
    } catch (error) {
      console.error("Error fetching localisation:", error);
      alert("Failed to load localisation. Please try again later.");
    } finally {
      setLoadingLocalisation(false);
    }
  };

  const fetchUserDetails = async (username) => {
    if (userCache[username]) {
      setUserDetails(userCache[username]);
      return;
    }
    setLoadingUserDetails(true);
    try {
      const data = await getUserDetails(username);
      setUserCache((prevCache) => ({ ...prevCache, [username]: data }));
      setUserDetails(data);
    } catch (error) {
      console.error("Error fetching user details:", error);
    } finally {
      setLoadingUserDetails(false);
    }
  };

  const openModal = (roomDetails) => {
    setSelectedRoomDetails(roomDetails); 
    setModalVisible(true); 
  };

  const closeModal = () => {
    setModalVisible(false); 
    setSelectedRoomDetails(null); 
  };

  useEffect(() => {
    fetchLocalisations();
  }, []);

  // UseEffect to set the image dimensions
  useEffect(() => {
    const image = new Image();
    image.src = floorPlanUrl;
    image.onload = () => {
      setImageDimensions({ width: image.width, height: image.height });
    };
  }, []);

  const zoomLevel = imageDimensions.width && imageDimensions.height ? 
    Math.min(mapContainerRef.current.offsetWidth / imageDimensions.width, mapContainerRef.current.offsetHeight / imageDimensions.height) : 0;

  return (
    <div className="map-container">
      <h2 className="title">Patients' Localisation</h2>

      {loadingLocalisation && <p>Loading localisation...</p>}

      <MapContainer
        crs={L.CRS.Simple}
        bounds={bounds}
        style={{ height: "500px", width: "100%", backgroundColor: "transparent" }} // Set background to transparent
        zoom={zoomLevel} // Dynamically set zoom level based on image dimensions
        minZoom={zoomLevel} // Disable zoom-out by setting minZoom to the current zoom level
        maxZoom={2}
        ref={mapContainerRef}
      >
        <ImageOverlay url={floorPlanUrl} bounds={bounds} />
        {localisation ? (
          (() => {
            console.log("Localisation ID:", localisation.id); 
            const roomMarker = roomMarkers.find((marker) => marker.id === Number(localisation.id));
            console.log("Room Marker:", roomMarker);

            if (!roomMarker) {
              return <p>Room not found.</p>;
            }

            return (
              <Marker
                key={localisation.id}
                position={roomMarker.position}
                icon={markerIcon}
                eventHandlers={{
                  click: () => openModal({ room: roomMarker.room, localisation }),
                  mouseover: () => setHoveredUsername(localisation.username),
                  mouseout: () => setHoveredUsername(null),
                }}
              >
                <Tooltip>
                  <b>{roomMarker.room}</b>
                  <br />
                  <b>Name:</b> {localisation.username}
                  <br />
                  <b>ID:</b> {localisation.id}
                  <br />
                  <b>Location date:</b> {new Date(localisation.createdAt).toLocaleString()}
                </Tooltip>
              </Marker>
            );
          })()
        ) : (
          <p>No localisation data available.</p>
        )}
      </MapContainer>

      {/* Modal */}
      {modalVisible && selectedRoomDetails && (
        <div
          style={{
            position: "fixed",
            top: "50%",
            left: "50%",
            transform: "translate(-50%, -50%)",
            backgroundColor: "white",
            padding: "20px",
            boxShadow: "0 4px 8px rgba(0, 0, 0, 0.2)",
            zIndex: 1000,
            width: "400px",
            borderRadius: "8px",
          }}
        >
          <h3 style={{ textAlign: "center" }}>Details of the Patient</h3>
          <div>
            <p><b>Room:</b> {selectedRoomDetails.room}</p>
            <p><b>Name:</b> {selectedRoomDetails.localisation.username}</p>
            <p><b>ID:</b> {selectedRoomDetails.localisation.id}</p>
            <p><b>Location date:</b> {new Date(selectedRoomDetails.localisation.createdAt).toLocaleString()}</p>
          </div>
          <button
            onClick={closeModal}
            style={{
              backgroundColor: "#007bff",
              color: "white",
              border: "none",
              padding: "10px 20px",
              borderRadius: "4px",
              cursor: "pointer",
              width: "100%",
              marginTop: "10px",
            }}
          >
            Close
          </button>
        </div>
      )}
      {modalVisible && (
        <div
          onClick={closeModal}
          style={{
            position: "fixed",
            top: 0,
            left: 0,
            width: "100%",
            height: "100%",
            backgroundColor: "rgba(0, 0, 0, 0.5)",
            zIndex: 999,
          }}
        ></div>
      )}
    </div>
  );
};

export default FloorMapComponent;
