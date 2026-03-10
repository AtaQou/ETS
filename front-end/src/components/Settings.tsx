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
    const {
        zoom,
        theme,
        language,
        baseGazeSamples = 60,
        translationMode = "word",
        showBoxes = false,
        hoverTranslateDebug = false,
        showGazeCursor = false,
        gazeYOffsetPx = 8,
    } = userSettingsUi;
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
        if (key === "baseGazeSamples") {
            newValue = Math.max(1, Math.round(value as number));
        }
        if (key === "gazeYOffsetPx") {
            newValue = Math.max(0, Math.min(100, Math.round(value as number)));
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
                {/* Zoom Level */}
                <div className='mb-4 flex justify-between '>
                    <label
                        className='text-base'
                        style={{ color: getFontColorSecondary(isDarkTheme) }}
                    >
                        Zoom Level
                    </label>
                    <div
                        className='flex items-center'
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
                        {/* numeric input για ακριβές zoom */}
                        <input
                            type='number'
                            min={10}
                            max={200}
                            value={Number((zoom * 100).toFixed())}
                            onChange={(e) => {
                                const raw = Number(e.target.value);
                                if (Number.isNaN(raw)) return;
                                const clamped = Math.max(10, Math.min(200, raw));
                                handleSettingsChange("zoom", clamped);
                            }}
                            className='ml-4 w-16 text-right text-gray-900 p-1 h-10 rounded border border-gray-300'
                        />
                        <span className='ml-1 text-base'>%</span>
                    </div>
                </div>

                {/* Base gaze samples before translation */}
                <div className='mb-4 flex justify-between'>
                    <label
                        className='text-base'
                        style={{ color: getFontColorSecondary(isDarkTheme) }}
                    >
                        Base gaze time before translation
                    </label>
                    <div
                        className='flex items-center'
                        style={{ color: getFontColorSecondary(isDarkTheme) }}
                    >
                        <input
                            type='range'
                            min='1'
                            max='600'
                            value={baseGazeSamples}
                            onChange={(e) =>
                                handleSettingsChange(
                                    "baseGazeSamples",
                                    Number(e.target.value)
                                )
                            }
                            className='slider text-gray-900 p-1 h-10 rounded border border-gray-300'
                        />
                        <input
                            type='number'
                            min={1}
                            max={600}
                            value={baseGazeSamples}
                            onChange={(e) => {
                                const raw = Number(e.target.value);
                                if (Number.isNaN(raw)) return;
                                const clamped = Math.max(1, Math.min(600, raw));
                                handleSettingsChange("baseGazeSamples", clamped);
                            }}
                            className='ml-4 w-20 text-right text-gray-900 p-1 h-10 rounded border border-gray-300'
                        />
                        <span className='ml-2 text-base'>samples</span>
                        <span className='ml-2 text-sm'>
                            ({(baseGazeSamples / 300).toFixed(2)} sec @ 300 samples/sec)
                        </span>
                    </div>
                </div>

                {/* Theme */}
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

                {/* Language */}
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

                {/* Translation mode */}
                <div className='mb-4 flex justify-between'>
                    <label
                        className='text-base'
                        style={{ color: getFontColorSecondary(isDarkTheme) }}
                    >
                        Translation mode
                    </label>
                    <select
                        value={translationMode}
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
                        onChange={(e) =>
                            handleSettingsChange(
                                "translationMode",
                                e.target.value as IUserSettings["translationMode"]
                            )
                        }
                    >
                        <option value='word'>Word</option>
                        <option value='sentence'>Sentence</option>
                    </select>
                </div>

                {/* Show word boxes (debug) */}
                <div className='mb-4 flex justify-between'>
                    <label
                        className='text-base'
                        style={{ color: getFontColorSecondary(isDarkTheme) }}
                    >
                        Show word boxes (debug)
                    </label>
                    <input
                        type='checkbox'
                        checked={!!showBoxes}
                        onChange={(e) =>
                            handleSettingsChange("showBoxes", e.target.checked as any)
                        }
                    />
                </div>

                {/* Hover-to-translate (debug) */}
                <div className='mb-4 flex justify-between'>
                    <label
                        className='text-base'
                        style={{ color: getFontColorSecondary(isDarkTheme) }}
                    >
                        Hover translate (debug)
                    </label>
                    <input
                        type='checkbox'
                        checked={!!hoverTranslateDebug}
                        onChange={(e) =>
                            handleSettingsChange(
                                "hoverTranslateDebug",
                                e.target.checked as any
                            )
                        }
                    />
                </div>

                {/* Gaze cursor visualization */}
                <div className='mb-4 flex justify-between'>
                    <label
                        className='text-base'
                        style={{ color: getFontColorSecondary(isDarkTheme) }}
                    >
                        Show gaze cursor
                    </label>
                    <input
                        type='checkbox'
                        checked={!!showGazeCursor}
                        onChange={(e) =>
                            handleSettingsChange("showGazeCursor", e.target.checked as any)
                        }
                    />
                </div>

                {/* Gaze Y offset */}
                <div className='mb-4 flex justify-between'>
                    <label
                        className='text-base'
                        style={{ color: getFontColorSecondary(isDarkTheme) }}
                    >
                        Gaze Y offset
                    </label>
                    <div
                        className='flex items-center'
                        style={{ color: getFontColorSecondary(isDarkTheme) }}
                    >
                        <input
                            type='range'
                            min='0'
                            max='100'
                            value={gazeYOffsetPx}
                            onChange={(e) =>
                                handleSettingsChange("gazeYOffsetPx", Number(e.target.value))
                            }
                            className='slider text-gray-900 p-1 h-10 rounded border border-gray-300'
                        />
                        <input
                            type='number'
                            min={0}
                            max={100}
                            value={gazeYOffsetPx}
                            onChange={(e) => {
                                const raw = Number(e.target.value);
                                if (Number.isNaN(raw)) return;
                                const clamped = Math.max(0, Math.min(100, raw));
                                handleSettingsChange("gazeYOffsetPx", clamped);
                            }}
                            className='ml-4 w-20 text-right text-gray-900 p-1 h-10 rounded border border-gray-300'
                        />
                        <span className='ml-2 text-base'>px</span>
                    </div>
                </div>

                <div className='flex justify-end py-2'></div>
            </div>
        </div>
    );
};

export default Settings;
