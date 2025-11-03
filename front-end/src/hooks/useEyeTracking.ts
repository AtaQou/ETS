import { useContext, useEffect, useRef, useCallback, useState } from "react";
import { Context } from "../context/Context";
import { isEmpty } from "lodash";
import { IContextProps } from "types/AppTypes";
// import { useEyeTrackingData } from "context/EyeTrackingContext";
import useEyeTrackingStore from "store/store";

const useEyeTracking = (): void => {
  const {
    userInfo,
    isCalibrating,
    selectedEyeTracker,
    setCalibrationProcess,
    isEyeTrackerConnected,
    shouldSubscribe,
  } = useContext<IContextProps>(Context);
  // const { accumulateData } = useEyeTrackingData();
  const { accumulateData } = useEyeTrackingStore();
  const { address } = selectedEyeTracker;
  const [shouldOpenConnection, setShouldOpenConnection] = useState(true);
  const socketRef = useRef<WebSocket | null>(null);

  const initializeWebSocket = useCallback(() => {
    const serverURL = "ws://localhost:5001";

    console.log("Attempting to open WebSocket connection.");
    if (!socketRef.current) {
      socketRef.current = new WebSocket(serverURL);

      socketRef.current.onopen = () => {
        console.log("WebSocket connection opened.");
        setShouldOpenConnection(false);
        if (isCalibrating) {
          const messageData = {
            action: "startCalibration",
            address,
          };
          socketRef.current?.send(JSON.stringify(messageData));
        }
      };

      socketRef.current.onclose = () => {
        console.log("WebSocket connection closed.");
        setShouldOpenConnection(true);
        socketRef.current = null;
      };

      socketRef.current.onerror = (error) => {
        console.error("WebSocket encountered an error: ", error);
        setShouldOpenConnection(true);
        socketRef.current = null;
      };
    }
  }, [address, isCalibrating]);

  useEffect(() => {
    if (shouldOpenConnection) {
      console.log("start socket NOW");

      initializeWebSocket();
      setShouldOpenConnection(false);
    }
  }, [initializeWebSocket, shouldOpenConnection]);

  //----------------------------- Receive messages -----------------------------------------
  useEffect(() => {
    if (isEyeTrackerConnected) {
      if (
        socketRef.current &&
        socketRef.current.readyState === WebSocket.OPEN
      ) {
        socketRef.current.onmessage = (event) => {
          const currentTime = new Date();
          const { data } = event;
          if (!data.includes("NaN")) {
            const parsedData = JSON.parse(data);
            let milli = currentTime.getMilliseconds();
            let f_milli = String(milli).padStart(3, "0");
            parsedData.js_tmp = `${currentTime.getHours()}:${currentTime.getMinutes()}:${currentTime.getSeconds()}.${f_milli}`;
            console.log(
              "data arrived",
              "in js : ",
              parsedData.js_tmp,
              "in python : ",
              parsedData.python_tmp
            );
            const { action } = parsedData;

            if (!isEmpty(data)) {
              if (isCalibrating && action === "calibrationResult") {
                setCalibrationProcess?.({
                  ...parsedData,
                  goToNextPoint: parsedData.message.includes("success"),
                });
              } else if (isCalibrating && action === "startCalibration") {
                setCalibrationProcess?.(parsedData);
              } else if (parsedData.action && parsedData.action === "eyeData") {
                try {
                  accumulateData?.(parsedData.payload);
                } catch (error) {
                  console.error("Error parsing JSON:", error);
                }
              }
            }
          }
        };
      }
    }
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [
    isEyeTrackerConnected,
    isCalibrating,
    address,
    setCalibrationProcess,
    initializeWebSocket,
  ]);

  //----------------------------- Send messages -----------------------------------------

  useEffect(() => {
    if (socketRef.current && socketRef.current.readyState === WebSocket.OPEN) {
      if (isCalibrating) {
        const messageData = {
          action: "startCalibration",
          address,
        };
        socketRef.current?.send(JSON.stringify(messageData));
      }
    }
  }, [address, isCalibrating]);

  useEffect(() => {
    if (socketRef.current && socketRef.current.readyState === WebSocket.OPEN) {
      if (shouldSubscribe) {
        const currentTime = new Date();
        let milli = currentTime.getMilliseconds();
        let f_milli = String(milli).padStart(3, "0");
        console.log(
          "start Tracking",
          `${currentTime.getHours()}:${currentTime.getMinutes()}:${currentTime.getSeconds()}.${f_milli}`
        );
        const messageData = {
          action: "startTracking",
          address,
          userID: userInfo.userID,
        };
        socketRef.current.send(JSON.stringify(messageData));
      }
    }
  }, [address, shouldSubscribe, userInfo.userID]);

  useEffect(() => {
    if (socketRef.current && socketRef.current.readyState === WebSocket.OPEN) {
      if (!shouldSubscribe) {
        const messageData = {
          action: "stopTracking",
          address,
        };
        socketRef.current.send(JSON.stringify(messageData));
      }
    }
  }, [address, shouldSubscribe]);

  useEffect(() => {
    if (socketRef.current && socketRef.current.readyState === WebSocket.OPEN) {
      if (!shouldSubscribe && !isEyeTrackerConnected) {
        socketRef.current.close();
        localStorage.removeItem("eyeTracker");
      }
    }
  }, [isEyeTrackerConnected, shouldSubscribe]);
};

export default useEyeTracking;
