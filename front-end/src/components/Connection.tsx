import React, { useContext, useMemo } from "react";
import axios from "axios";
import ModalWrapper from "./ui/ModalWrapper";
import EyeTrackerInfo from "./EyeTrackerInfo";
import { useSnackbar } from "../hooks/useSnackbar";
import { ConnectionStatus, IContextProps, IEyeTracker } from "types/AppTypes";
import {
  dark_primary,
  dark_secondary,
  light_primary,
  light_secondary,
} from "utils/consts";
import { initEyeTracker } from "utils/initData";
import Button from "./ui/Button";
import { getBgSecondary, getFontColorSecondary } from "utils/functions";
import { Context } from "context/Context";

interface ConnectionProps {
  error: string;
  status: ConnectionStatus;
  setConnectionStatus: React.Dispatch<React.SetStateAction<ConnectionStatus>>;
  onStartTracking: () => void;
  eyeTrackers: IEyeTracker[];
  onClose: () => void;
}

const Connection: React.FC<ConnectionProps> = ({
  status,
  error,
  setConnectionStatus,
  onStartTracking,
  eyeTrackers,
  onClose,
}) => {
  const {
    userSettingsApi,
    isCalibrating,
    setIsCalibrating,
    selectedEyeTracker,
    setSelectedEyeTracker,
    setIsEyeTrackerConnected,
  } = useContext<IContextProps>(Context);

  const isDarkTheme = userSettingsApi.theme === "dark";

  const style = useMemo(
    () =>
      isDarkTheme
        ? {
            color: light_secondary,
          }
        : {
            color: dark_primary,
          },
    [isDarkTheme]
  );

  const { triggerSnackbar } = useSnackbar();

  const handleEyeTrackerChange = (e: React.ChangeEvent<HTMLSelectElement>) => {
    const selected = eyeTrackers.find(
      (eye) => eye.device_name === e.target.value
    );
    setSelectedEyeTracker?.(selected || initEyeTracker);
  };

  // Todo: cancel the request if modal closes
  const handleConnect = () => {
    // console.log(`Connecting to ${selectedEyeTracker.device_name}`);
    axios
      .post("http://localhost:5000/api/connect", {
        address: selectedEyeTracker?.address,
      })
      .then((response) => {
        setConnectionStatus("connected");
        setIsEyeTrackerConnected?.(true);
        // setIsCalibrating?.(true);
        triggerSnackbar({
          message: response.data.message,
          status: "success",
          open: true,
        });
      })
      .catch((err) => {
        console.error(err);
        setConnectionStatus("error");
        triggerSnackbar({
          message: "Connection failed!",
          status: "error",
          open: true,
        });
      });
  };

  const onClickRecalibrate = () => {
    setIsCalibrating?.(true);
  };

  return (
    <ModalWrapper
      className={`w-[700px] h-[28rem] px-12 py-12 ${
        isCalibrating ? "pointer-events-none" : ""
      }`}
      shouldShowConfirm={false}
      style={{ backgroundColor: getBgSecondary(isDarkTheme) }}
      onConfirm={() => {}}
      onClose={onClose}
    >
      <div className='flex flex-col w-full h-full'>
        {status === "searching" && (
          <h1
            className='text-xl'
            style={{ color: getFontColorSecondary(isDarkTheme) }}
          >
            Searching...
          </h1>
        )}
        {status === "connected" && (
          <>
            <h1
              className='text-xl'
              style={{ color: getFontColorSecondary(isDarkTheme) }}
            >
              Eye Tracker connected!
            </h1>
            <div className='w-full h-full flex justify-center items-center'>
              <div className='w-full flex space-x-4 justify-evenly items-center '>
                <Button
                  label='Start Tracking'
                  style={{ color: light_secondary }}
                  className={`bg-blue-500 flex justify-center items-center text-xl px-8 py-4 hover:scale-105 active:scale-95 transform transition focus:outline-none shadow-lg`}
                  onClick={onStartTracking}
                ></Button>
                {/* <Button
                  label='Recalibrate'
                  style={{ color: light_secondary }}
                  className={`bg-blue-500 flex justify-center items-center text-xl px-8 py-4 hover:scale-105 active:scale-95 transform transition focus:outline-none shadow-lg`}
                  onClick={onClickRecalibrate}
                ></Button> */}
              </div>
            </div>
          </>
        )}
        {status === "selection" && (
          <div className='flex flex-col w-full'>
            <h1 className=' text-xl font-bold text-blue-500  mb-8'>
              Found {eyeTrackers.length} eye trackers.
            </h1>
            <div className='flex w-full items-center text-lg'>
              <div className='mr-4' style={style}>
                Select:
              </div>
              <select
                style={
                  isDarkTheme
                    ? {
                        backgroundColor: dark_secondary,
                        color: light_secondary,
                      }
                    : {
                        backgroundColor: light_primary,
                        color: dark_primary,
                      }
                }
                value={selectedEyeTracker?.device_name || ""}
                className='text-gray-800 text-base p-2 w-[26rem] rounded border border-gray-300'
                onChange={handleEyeTrackerChange}
              >
                {[{ device_name: "" }, ...eyeTrackers].map((tracker, index) => (
                  <option
                    style={
                      isDarkTheme
                        ? {
                            color: light_secondary,
                          }
                        : {
                            color: dark_primary,
                          }
                    }
                    className='text-gray-800 p-2 border border-gray-300 '
                    key={index}
                    // value={`${tracker.device_name}/${tracker.address}`}
                  >
                    {`${tracker.device_name}`}
                  </option>
                ))}
              </select>
              <Button
                label='Connect'
                className={`bg-blue-500 w-24 h-10 flex justify-center items-center mx-8 text-base  active:scale-95 transform transition focus:outline-none  shadow-lg`}
                style={{ color: light_secondary }}
                onClick={handleConnect}
                disabled={!selectedEyeTracker?.device_name}
              />
            </div>
            {selectedEyeTracker && (
              <EyeTrackerInfo tracker={selectedEyeTracker} />
            )}
          </div>
        )}
        {status === "error" && <div className='text-red-800'> {error} </div>}
      </div>
    </ModalWrapper>
  );
};

export default Connection;
