import React, { useContext } from "react";
import { dark_primary, light_primary } from "../utils/consts";
import { Context } from "../context/Context";
import { getFontColorSecondary } from "../utils/functions";
import { IEyeTracker } from "types/AppTypes";

interface EyeTrackerInfoProps {
  tracker: IEyeTracker;
}

const EyeTrackerInfo: React.FC<EyeTrackerInfoProps> = ({ tracker }) => {
  const { userSettingsApi } = useContext(Context);
  const isDarkTheme = userSettingsApi.theme === "dark";
  return (
    <div
      className={`tracker-info mt-8 p-4 w-full rounded text-lg`}
      style={
        isDarkTheme
          ? {
              backgroundColor: dark_primary,
            }
          : {
              backgroundColor: light_primary,
            }
      }
    >
      <h2 className='text-xl font-semibold mb-4 text-blue-500'>Eye tracker details</h2>
      <p className='mb-2 text-base' style={{ color: getFontColorSecondary(isDarkTheme) }}>
        <span className='font-semibold' style={{ color: getFontColorSecondary(isDarkTheme) }}>
          Model:
        </span>{" "}
        {tracker.model}
      </p>
      <p className='mb-2 text-base' style={{ color: getFontColorSecondary(isDarkTheme) }}>
        <span className='font-semibold' style={{ color: getFontColorSecondary(isDarkTheme) }}>
          Address:
        </span>{" "}
        {tracker.address}
      </p>
      <p className='mb-2 text-base' style={{ color: getFontColorSecondary(isDarkTheme) }}>
        <span className='font-semibold' style={{ color: getFontColorSecondary(isDarkTheme) }}>
          Name:
        </span>{" "}
        {tracker.device_name}
      </p>
      <p className='mb-2 text-base' style={{ color: getFontColorSecondary(isDarkTheme) }}>
        <span className='font-semibold' style={{ color: getFontColorSecondary(isDarkTheme) }}>
          Serial Number:
        </span>{" "}
        {tracker.serial_number}
      </p>
      <p className='mb-2 text-base' style={{ color: getFontColorSecondary(isDarkTheme) }}>
        <span className='font-semibold' style={{ color: getFontColorSecondary(isDarkTheme) }}>
          Firmware version:
        </span>{" "}
        {tracker.firmware_version}
      </p>
    </div>
  );
};

export default EyeTrackerInfo;
