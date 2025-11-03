import React, { useContext, useEffect } from "react";
import { Context } from "./context/Context";
import UserProfile from "./components/UserProfile";
import MainContent from "./components/MainContent";
import Footer from "./components/ui/Footer";
import Header from "./components/ui/Header";
import useEyeTracking from "./hooks/useEyeTracking";
import CalibrationOverlay from "components/CalibrationOverlay";
// import CircleMover from "components/CircleMover";
import TextBox from "components/ui/TextBox";
import useMockData from "hooks/useMockData";
import CircleMover from "components/CircleMover";

const App: React.FC = () => {
  const context = useContext(Context);
  const { loading, isMenuOpen, file } = context;

  const toggleFullScreen = () => {
    const elem = document.documentElement;
    if (elem.requestFullscreen) {
      elem.requestFullscreen();
    }
  };

  const exitFullscreen = () => {
    if (document.fullscreenElement) {
      document.exitFullscreen().catch((err) => {
        console.log(
          `Error attempting to disable full-screen mode: ${err.message} (${err.name})`
        );
      });
    }
  };

  if (!context) {
    throw new Error("App must be used within a ContextProvider");
  }

  const { userInfo, isCalibrating } = context;
  const { isLoggedIn } = userInfo;

  useEyeTracking();
  // useMockData();

  useEffect(() => {
    if (isCalibrating) {
      toggleFullScreen();
    } else {
      exitFullscreen();
    }
  }, [isCalibrating]);

  const step = 0.1;
  const points = [];

  // Generate grid points
  for (let x = 0; x < 1; x += step) {
    for (let y = 0; y <= 1; y += step) {
      points.push({ x, y });
    }
  }

  return (
    <>
      {/*!!!! Comment out this div to remove grid of points */}
      {/* <div className='absolute top-0 left-0 w-screen h-screen overflow-hidden bg-transparent z-30'>
        {points.map((point, index) => (
          <div
            key={index}
            className='absolute w-2 h-2 bg-blue-500 rounded-full transform -translate-x-1/2 -translate-y-1/2'
            style={{
              left: `${point.x * 100}%`,
              top: `${point.y * 100}%`,
            }}
          >
            {point.x.toFixed(1)},{point.y.toFixed(1)}
          </div>
        ))}
      </div> */}
      {/* <CircleMover /> */}
      {!loading && !isMenuOpen && file?.size !== 0 && <TextBox />}
      {}
      {!isLoggedIn && <UserProfile />}
      {isCalibrating && <CalibrationOverlay />}
      {isLoggedIn && (
        <div className='h-full overflow-hidden'>
          <Header />
          <MainContent />
          <Footer />
        </div>
      )}
    </>
  );
};

export default App;
