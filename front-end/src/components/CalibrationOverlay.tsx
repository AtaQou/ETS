import { Context } from "context/Context";
import React, {
  useState,
  useEffect,
  FunctionComponent,
  useContext,
} from "react";
import { CalibrationPoint, IContextProps } from "types/AppTypes";
import { getBgPrimaryReverse, getFontColorSecondary } from "utils/functions";
import Button from "./ui/Button";

const calibrationPoints: CalibrationPoint[] = [
  { x: 50, y: 50 },
  { x: 10, y: 10 },
  { x: 10, y: 90 },
  { x: 90, y: 10 },
  { x: 90, y: 90 },
];

const timeFrame = 3000;
const CalibrationOverlay: FunctionComponent = () => {
  const [currentIndex, setCurrentIndex] = useState<number>(0);
  const {
    isCalibrating,
    setIsCalibrating,
    userSettingsApi,
    calibrationProcess,
  } = useContext<IContextProps>(Context);
  const [showInitialScreen, setShowInitialScreen] = useState(true);
  const [calibrationFailed, setCalibrationFailed] = useState(false);
  const [key, setKey] = useState(Math.random());
  const isDarkTheme = userSettingsApi.theme === "dark";

  const onCalibrationExitClick = () => {
    setIsCalibrating?.(false);
  };

  useEffect(() => {
    const initialTimer = setTimeout(() => {
      setShowInitialScreen(false);
    }, timeFrame);

    return () => clearTimeout(initialTimer);
  }, []);

  useEffect(() => {
    console.log("Current calibrationProcess:", calibrationProcess); // Debugging

    if (showInitialScreen || !isCalibrating) {
      return;
    }

    if (calibrationProcess && currentIndex >= calibrationPoints.length) {
      setTimeout(() => {
        setIsCalibrating?.(false);
      }, 2000);
      return;
    }

    if (calibrationProcess?.goToNextPoint === true) {
      const timer = setTimeout(() => {
        setCurrentIndex((prevIndex) => prevIndex + 1);
        setKey(Math.random());
      }, timeFrame);

      return () => clearTimeout(timer);
    }

    if (calibrationProcess && calibrationProcess?.goToNextPoint === false) {
      setCalibrationFailed(true);
    }
  }, [
    currentIndex,
    showInitialScreen,
    calibrationProcess,
    isCalibrating,
    setIsCalibrating,
  ]);

  return (
    <div className='fixed inset-0 z-50 bg-black'>
      {showInitialScreen ? (
        <div className='absolute inset-0 flex flex-col items-center justify-center'>
          {calibrationProcess &&
            calibrationProcess.action === "startCalibration" && (
              <div className='text-2xl text-blue-500 m-8'>
                {calibrationProcess.message}
              </div>
            )}
          <span className='text-lg text-white'>
            Stare at the dots until they disappear.
          </span>
        </div>
      ) : (
        <>
          {calibrationFailed ? (
            <div className='absolute inset-0 flex flex-col items-center justify-center text-xl text-red-500'>
              Calibration Failed!
              <Button
                className='bg-red-500 m-8 text-base'
                style={{ color: getFontColorSecondary(isDarkTheme) }}
                onClick={onCalibrationExitClick}
              >
                Exit
              </Button>
            </div>
          ) : currentIndex < calibrationPoints.length ? (
            <div
              key={key}
              className='absolute rounded-full w-8 h-8'
              style={{
                top: `${calibrationPoints[currentIndex].y}%`,
                left: `${calibrationPoints[currentIndex].x}%`,
                transform: "translate(-50%, -50%)",
                backgroundColor: getBgPrimaryReverse(isDarkTheme),
                animation: "explode 3s forwards",
              }}
            ></div>
          ) : (
            <div className='absolute inset-0 flex items-center justify-center text-xl text-green-500'>
              Calibration Successful.
            </div>
          )}
        </>
      )}
    </div>
  );
};

export default CalibrationOverlay;
