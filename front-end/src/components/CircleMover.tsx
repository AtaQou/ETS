// import { useEyeTrackingData } from "context/EyeTrackingContext";
import React, { useState, useEffect, useContext, useRef } from "react";
import useEyeTrackingStore from "store/store";
import { Context } from "context/Context";
import { getAverageGazePointCoordinates2 } from "utils/eyeTracking";

const CircleMover: React.FC = () => {
  // const { eyeData } = useEyeTrackingData();
  const { eyeData } = useEyeTrackingStore();
  const { userSettingsUi } = useContext(Context);
  const [avgPosition, setAvgPosition] = useState<{ x: number; y: number }>({
    x: 0,
    y: 0,
  });
  const gazeDetectionMode = userSettingsUi.gazeDetectionMode ?? "circle";
  const isCircleMode = gazeDetectionMode === "circle";
  const gazeRadiusPx = Math.max(0, Math.min(100, userSettingsUi.gazeHitRadiusPx ?? 20));
  const circleDiameter = isCircleMode ? Math.max(24, gazeRadiusPx * 2) : 10;
  const lastRenderAtRef = useRef<number>(0);

  useEffect(() => {
    const now = performance.now();
    if (now - lastRenderAtRef.current < 16) return;
    lastRenderAtRef.current = now;

    const recentData = eyeData.slice(-5); // get the last 5 data points
    const { pointX, pointY } = getAverageGazePointCoordinates2(recentData);

    setAvgPosition({ x: pointX, y: pointY });
  }, [eyeData]);

  return (
    <div
      className='circle'
      style={{
        opacity: isCircleMode ? 0.3 : 0.9,
        left: `${avgPosition.x}px`,
        top: `${avgPosition.y}px`,
        position: "fixed",
        width: `${circleDiameter}px`,
        height: `${circleDiameter}px`,
        borderRadius: "50%",
        border: isCircleMode ? "2px solid rgb(59 130 246)" : "none",
        transform: "translate(-50%, -50%)",
        zIndex: 999,
        pointerEvents: "none",
        transition: "left 0.1s ease, top 0.1s ease",
        boxShadow: isCircleMode ? "none" : "0 0 0 2px rgba(59,130,246,0.25)",
        background: isCircleMode
          ? "radial-gradient(circle, rgba(59,130,246,0) 0%, rgba(59,130,246,0.6) 40%, rgba(59,130,246,0) 100%)"
          : "rgb(59 130 246)",
      }}
    ></div>
  );
};

export default CircleMover;
