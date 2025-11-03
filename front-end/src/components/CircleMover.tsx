// import { useEyeTrackingData } from "context/EyeTrackingContext";
import React, { useState, useEffect } from "react";
import useEyeTrackingStore from "store/store";
import { getAverageGazePointCoordinates2 } from "utils/eyeTracking";

const CircleMover: React.FC = () => {
  // const { eyeData } = useEyeTrackingData();
  const { eyeData } = useEyeTrackingStore();
  const [avgPosition, setAvgPosition] = useState<{ x: number; y: number }>({
    x: 0,
    y: 0,
  });

  useEffect(() => {
    const recentData = eyeData.slice(-5); // get the last 5 data points
    const { pointX, pointY } = getAverageGazePointCoordinates2(recentData);

    // ! This if is for single data gaze point creation
    // const recentData = eyeData[eyeData.length - 1];
    // const { pointX, pointY } = getGazePointCoordinates(recentData);
    // if (recentData.length === 0) return;
    const currentTime = new Date();
    let milli = currentTime.getMilliseconds();
    let f_milli = String(milli).padStart(3, "0");
    console.log(
      "circle rendered!!!!!!!!",
      `${currentTime.getHours()}:${currentTime.getMinutes()}:${currentTime.getSeconds()}.${f_milli}`
    );

    setAvgPosition({ x: pointX, y: pointY });
  }, [eyeData]);

  return (
    <div
      className='circle'
      style={{
        opacity: 0.3,
        left: `${avgPosition.x}px`,
        top: `${avgPosition.y}px`,
        position: "absolute",
        width: "25px",
        height: "25px",
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
