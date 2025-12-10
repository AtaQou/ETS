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
    showBoxes: false, // νέο default
    hoverTranslateDebug: false,
};

export const initPdfDimensions = {
  width: 0,
  height: 0,
  aspectRatio: 0.7097222222222223,
};

export const initFile = {
  size: 0,
};
