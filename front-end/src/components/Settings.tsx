import React, { useContext, useEffect, useState, FC } from "react";
import { Context } from "../context/Context";
import {
  dark_primary,
  dark_secondary,
  languageMap,
  light_primary,
  light_secondary,
} from "../utils/consts";
import { getFontColorSecondary } from "../utils/functions";
import { IContextProps, IUserSettings } from "types/AppTypes";

const Settings: FC = () => {
  const { userSettingsUi, setUserSettingsUi, userSettingsApi } =
    useContext<IContextProps>(Context);
  const { zoom, theme, language } = userSettingsUi;
  const [loading, setLoading] = useState(false);
  const isDarkTheme = userSettingsApi.theme === "dark";

  const handleSettingsChange = (
    key: keyof IUserSettings,
    value: IUserSettings[keyof IUserSettings]
  ) => {
    let newValue: IUserSettings[keyof IUserSettings] = value;
    if (key === "zoom") {
      newValue = (value as IUserSettings["zoom"]) / 100;
    }
    if (setUserSettingsUi) {
      setUserSettingsUi({ [key]: newValue });
    }
  };

  useEffect(() => {
    setLoading(true);
    setUserSettingsUi?.(userSettingsApi);
    setLoading(false);
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [userSettingsApi]);

  if (loading) {
    return (
      <div
        className='flex justify-center items-center w-full h-full'
        style={{ color: getFontColorSecondary(isDarkTheme) }}
      >
        Loading documents...
      </div>
    );
  }

  return (
    <div className='flex flex-col m-2 p-4'>
      <h1
        className='py-1 mb-4 text-xl font-bold text-gray-900 border-b border-gray-300'
        style={{ color: getFontColorSecondary(isDarkTheme) }}
      >
        Settings
      </h1>
      <div
        className='mb-8 text-gray-600'
        style={{ color: getFontColorSecondary(isDarkTheme) }}
      >
        Adjust the settings to your preferences and click Confirm to apply them
        to your document.
      </div>
      <div className='xl:w-[500px] lg:w-[350px]'>
        <div className='mb-4 flex justify-between '>
          <label
            className='text-base'
            style={{ color: getFontColorSecondary(isDarkTheme) }}
          >
            Zoom Level
          </label>
          <div
            className='flex '
            style={{ color: getFontColorSecondary(isDarkTheme) }}
          >
            <input
              type='range'
              min='10'
              max='200'
              value={zoom * 100}
              onChange={(e) =>
                handleSettingsChange("zoom", Number(e.target.value))
              }
              className='slider text-gray-900 p-1 h-10 rounded border border-gray-300'
            />
            <p
              className='text-base pl-4 align-middle'
              style={{ color: getFontColorSecondary(isDarkTheme) }}
            >
              {(zoom * 100).toFixed()}%
            </p>
          </div>
        </div>
        <div className='mb-4 flex justify-between'>
          <label
            className='text-base'
            style={{ color: getFontColorSecondary(isDarkTheme) }}
          >
            Theme
          </label>
          <select
            className='text-base  p-1 w-48 rounded border border-gray-300'
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
            value={theme}
            onChange={(e) => handleSettingsChange("theme", e.target.value)}
          >
            <option value='light'>Light</option>
            <option value='dark'>Dark</option>
          </select>
        </div>
        <div className='mb-4 flex justify-between'>
          <label
            className='text-base'
            style={{ color: getFontColorSecondary(isDarkTheme) }}
          >
            Language
          </label>
          <select
            value={language}
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
            className='text-base p-1 w-48 rounded border border-gray-300'
            onChange={(e) => handleSettingsChange("language", e.target.value)}
          >
            {Object.entries(languageMap).map(([code, name]) => (
              <option key={code} value={code}>
                {name}
              </option>
            ))}
          </select>
        </div>
        <div className='flex justify-end py-2'></div>
      </div>
    </div>
  );
};

export default Settings;
