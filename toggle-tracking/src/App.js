import React, { useEffect, useRef, useState } from "react";

function App() {
  const socketRef = useRef(null);
  const [shouldInitialize, setShouldInitialize] = useState(true);

  const initializeWebSocket = () => {
    const serverURL = "ws://localhost:5001";

    console.log("Attempting to open WebSocket connection.");
    if (!socketRef.current || socketRef.current.readyState !== WebSocket.OPEN) {
      socketRef.current = new WebSocket(serverURL);

      socketRef.current.onopen = () => {
        console.log("WebSocket connection opened.");
      };

      socketRef.current.onclose = () => {
        console.log("WebSocket connection closed.");
        // socketRef.current = null;
        setShouldInitialize(true);
      };

      socketRef.current.onerror = (error) => {
        console.error("WebSocket encountered an error: ", error);
        // socketRef.current = null;
        setShouldInitialize(true);
      };
    }
  };

  useEffect(() => {
    if (shouldInitialize) {
      initializeWebSocket();
      setShouldInitialize(false);
    }
  }, [shouldInitialize]);

  const sendStartTracking = () => {
    if (socketRef.current.readyState === WebSocket.OPEN) {
      const messageData = {
        action: "startTracking",
        address: "tet-tcp://169.254.6.50",
        userID: "test-user-id",
      };
      socketRef.current.send(JSON.stringify(messageData));
    } else {
      console.error(
        "WebSocket is not open. readyState: ",
        socketRef.current.readyState
      );
    }
  };

  const sendStopTracking = () => {
    if (socketRef.current.readyState === WebSocket.OPEN) {
      const messageData = {
        action: "stopTracking",
        address: "tet-tcp://169.254.6.50",
      };
      socketRef.current.send(JSON.stringify(messageData));
    } else {
      console.error(
        "WebSocket is not open. readyState: ",
        socketRef.current.readyState
      );
    }
  };

  return (
    <div className='App'>
      <button onClick={sendStartTracking}>Start Tracking</button>
      <button onClick={sendStopTracking}>Stop Tracking</button>
    </div>
  );
}

export default App;
