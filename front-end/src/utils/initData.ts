import { IUserSettings } from "types/AppTypes";

export const initUserInfo = {
  isLoggedIn: false,
  userID: "",
  username: "",
};

export const initEyeTracker = {
  device_name: "",
};

export const initSettings: IUserSettings = {
    zoom: 0.84,
    theme: "dark",
    language: "en",
    baseGazeSamples: 60,
    translationMode: "word",
    showBoxes: false, // νέο default
    hoverTranslateDebug: false,
    showGazeCursor: false,
    gazeDetectionMode: "circle",
    gazeYOffsetPx: 8,
    gazeHitRadiusPx: 20,
};

export const initPdfDimensions = {
  width: 0,
  height: 0,
  aspectRatio: 0.7097222222222223,
};

export const initFile = {
  size: 0,
};
