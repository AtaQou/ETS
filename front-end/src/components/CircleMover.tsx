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
  const gazeRadiusPx = Math.max(0, Math.min(100, userSettingsUi.gazeHitRadiusPx ?? 20));
  const circleDiameter = Math.max(24, gazeRadiusPx * 2);
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
        opacity: 0.3,
        left: `${avgPosition.x}px`,
        top: `${avgPosition.y}px`,
        position: "fixed",
        width: `${circleDiameter}px`,
        height: `${circleDiameter}px`,
        borderRadius: "50%",
        border: "2px solid rgb(59 130 246)",
        transform: "translate(-50%, -50%)",
        zIndex: 999,
        transition: "left 0.1s ease, top 0.1s ease",
        background:
          "radial-gradient(circle, rgba(59,130,246,0) 0%, rgba(59,130,246,0.6) 40%, rgba(59,130,246,0) 100%)",
      }}
    ></div>
  );
};

export default CircleMover;
