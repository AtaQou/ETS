import { createContext, useEffect, useReducer } from "react";
import axios from "axios";
import { apiURL } from "../utils/consts";
import {
  IAction,
  IContextProps,
  ID,
  IEyeTracker,
  File,
  IUserInfo,
  IUserSettings,
} from "types/AppTypes";
import React from "react";
import {
  initEyeTracker,
  initFile,
  initPdfDimensions,
  initSettings,
  initUserInfo,
} from "utils/initData";

const selectedDocID = localStorage.getItem("selectedDocID") || "";

const userInfoFromStorage = localStorage.getItem("userInfo");
const userInfo = userInfoFromStorage
  ? JSON.parse(userInfoFromStorage)
  : initUserInfo;

const userSettingsFromStorage = localStorage.getItem("userSettingsUi");
const userSettingsUi = userSettingsFromStorage
  ? JSON.parse(userSettingsFromStorage)
  : initSettings;

const eyeTrackerFromStorage = localStorage.getItem("eyeTracker");
const selectedEyeTracker = eyeTrackerFromStorage
  ? JSON.parse(eyeTrackerFromStorage)
  : initEyeTracker;

const initialState: IContextProps = {
  file: initFile,
  selectedDocID,
  currentPage: 0,
  pageCount: 0,
  scrollTop: 0,
  loading: false,
  pdfDimensions: initPdfDimensions,
  userInfo,
  userSettingsApi: userSettingsUi,
  userSettingsUi,
  isMenuOpen: false,
  selectedEyeTracker,
  isEyeTrackerConnected: false,
  isCalibrating: false,
  shouldSubscribe: false,
  calibrationProcess: null,
  pageMounted: false,
  shouldTranslate: false,
  logout: () => {},
};

const reducer = (state: IContextProps, action: IAction): IContextProps => {
  const container = document.getElementById("pdf-container");
  let scrollTop: number;
  switch (action.type) {
    case "LOAD_FILE":
      return {
        ...state,
        file: action.payload,
        currentPage: 1,
      };
    case "SET_DOCUMENT_ID":
      localStorage.setItem("selectedDocID", action.payload);
      return {
        ...state,
        selectedDocID: action.payload,
      };
    case "GO_TO_PREV_PAGE":
      if (container) {
        scrollTop = (state.currentPage - 2) * state.pdfDimensions.height;
        container.scrollTop = scrollTop;
      }
      return {
        ...state,
        currentPage: state.currentPage - 1,
      };

    case "GO_TO_NEXT_PAGE":
      if (container) {
        scrollTop = state.currentPage * state.pdfDimensions.height;
        container.scrollTop = scrollTop;
      }
      return {
        ...state,
        currentPage: state.currentPage + 1,
      };
    case "SET_PAGE_COUNT":
      return {
        ...state,
        pageCount: action.payload,
      };
    case "SET_CURRENT_PAGE":
      return {
        ...state,
        currentPage: action.payload,
      };
    case "SET_LOADING":
      return {
        ...state,
        loading: action.payload,
      };
    case "SET_SESSION":
      localStorage.setItem("userInfo", JSON.stringify(action.payload));
      return {
        ...state,
        userInfo: action.payload,
      };
    case "SET_USER_SETTINGS_UI":
      localStorage.setItem(
        "userSettingsUi",
        JSON.stringify({ ...state.userSettingsUi, ...action.payload })
      );
      return {
        ...state,
        userSettingsUi: { ...state.userSettingsUi, ...action.payload },
      };
    case "SET_USER_SETTINGS_API":
      return {
        ...state,
        userSettingsApi: { ...state.userSettingsApi, ...action.payload },
      };
    case "SET_PDF_DIMENSIONS":
      return {
        ...state,
        pdfDimensions: {
          ...state.pdfDimensions,
          ...action.payload,
        },
      };
    case "SET_IS_MENU_OPEN":
      return {
        ...state,
        isMenuOpen: action.payload,
      };
    case "SET_SELECTED_EYE_TRACKER":
      localStorage.setItem("eyeTracker", JSON.stringify(action.payload));
      return {
        ...state,
        selectedEyeTracker: action.payload,
      };
    case "SET_IS_EYE_TRACKER_CONNECTED":
      return {
        ...state,
        isEyeTrackerConnected: action.payload,
      };
    case "SET_IS_CALIBRATING":
      return {
        ...state,
        isCalibrating: action.payload,
      };
    case "SET_CALIBRATION_PROCESS":
      return {
        ...state,
        calibrationProcess: action.payload,
      };
    case "SCROLL":
      if (container) {
        return {
          ...state,
          scrollTop: action.payload,
        };
      }
      return state;
    case "SET_SHOULD_SUBSCRIBE":
      return {
        ...state,
        shouldSubscribe: action.payload,
      };

    case "SET_ELEMENT_MOUNTED":
      return { ...state, pageMounted: true };
    case "LOGOUT":
      localStorage.removeItem("userInfo");
      return {
        ...state,
        userInfo: initUserInfo,
      };
    case "SET_SHOULD_TRANSLATE":
      return { ...state, shouldTranslate: action.payload };
    default:
      return state;
  }
};

export const Context = createContext<IContextProps>(initialState);

export const ContextProvider = ({
  children,
}: {
  children: React.ReactNode;
}) => {
  const [state, dispatch] = useReducer(reducer, initialState);

  console.log({ state });

  // -------------------- DOCUMENT ACTIONS -----------------------

  const loadFile = (file?: File) => {
    dispatch({ type: "LOAD_FILE", payload: file });
  };

  const setSelectedDocID = (id: ID) => {
    dispatch({ type: "SET_DOCUMENT_ID", payload: id });
  };

  const setCurrentPage = (pageNumber: number) => {
    dispatch({ type: "SET_CURRENT_PAGE", payload: pageNumber });
  };

  const setPageCount = (pageCount: number) => {
    dispatch({ type: "SET_PAGE_COUNT", payload: pageCount });
  };

  const setPdfDimensions = (dimensions: { width: number; height: number }) => {
    dispatch({ type: "SET_PDF_DIMENSIONS", payload: dimensions });
  };

  const goToNextPage = () => {
    dispatch({ type: "GO_TO_NEXT_PAGE" });
  };

  const goToPrevPage = () => {
    dispatch({ type: "GO_TO_PREV_PAGE" });
  };
  // -------------------- OTHER ACTIONS -----------------------

  const setLoading = (loading: boolean) => {
    dispatch({ type: "SET_LOADING", payload: loading });
  };

  const setUserInfo = (userInfo: IUserInfo) => {
    dispatch({ type: "SET_SESSION", payload: userInfo });
  };

  const setUserSettingsUi = (userSettings: Partial<IUserSettings>) => {
    dispatch({ type: "SET_USER_SETTINGS_UI", payload: userSettings });
  };
  const setUserSettingsApi = (userSettings: Partial<IUserSettings>) => {
    dispatch({ type: "SET_USER_SETTINGS_API", payload: userSettings });
  };

  const setIsMenuOpen = (isOpen: boolean) => {
    dispatch({ type: "SET_IS_MENU_OPEN", payload: isOpen });
  };

  const setSelectedEyeTracker = (eyeTracker: IEyeTracker) => {
    dispatch({ type: "SET_SELECTED_EYE_TRACKER", payload: eyeTracker });
  };

  const setIsEyeTrackerConnected = (isConnected: boolean) => {
    dispatch({ type: "SET_IS_EYE_TRACKER_CONNECTED", payload: isConnected });
  };

  const setIsCalibrating = (isCalibrating: boolean) => {
    dispatch({ type: "SET_IS_CALIBRATING", payload: isCalibrating });
  };

  const setCalibrationProcess = (payload: Record<string, any> | null) => {
    dispatch({ type: "SET_CALIBRATION_PROCESS", payload });
  };

  const setShouldSubscribe = (shouldSubscribe: boolean) => {
    dispatch({ type: "SET_SHOULD_SUBSCRIBE", payload: shouldSubscribe });
  };

  const setScrollTop = (scrollTop: number) => {
    dispatch({ type: "SCROLL", payload: scrollTop });
  };

  const setPageMounted = () => {
    dispatch({ type: "SET_ELEMENT_MOUNTED" });
  };

  const setShouldTranslate = (payload: boolean) => {
    dispatch({ type: "SET_SHOULD_TRANSLATE", payload });
  };

  const logout = () => {
    dispatch({ type: "LOGOUT" });
  };

  useEffect(() => {
    if (state.file && state.file?.size === 0 && state.selectedDocID) {
      setLoading(true);
      axios
        .get(`${apiURL}/get_file`, {
          params: {
            docID: state.selectedDocID,
            userID: state.userInfo.userID,
          },
          responseType: "blob",
        })
        .then((response) => {
          const fileBlob = new Blob([response.data], {
            type: response.data.type,
          });
          loadFile(fileBlob);
        })
        .catch((error) => {
          alert("Failed to load file.");
        })
        .finally(() => {
          setLoading(false);
        });
    }
  }, [
    state.file,
    state.file?.size,
    state.selectedDocID,
    state.userInfo.userID,
  ]);

  const contextValue = {
    file: state.file,
    selectedDocID: state.selectedDocID,
    setSelectedDocID,
    currentPage: state.currentPage,
    setCurrentPage,
    pageCount: state.pageCount,
    setPageCount,
    loadFile,
    scrollTop: state.scrollTop,
    setScrollTop,
    isLoggedIn: state.userInfo.isLoggedIn,
    userInfo: state.userInfo,
    setUserInfo,
    loading: state.loading,
    setLoading,
    logout,
    userSettingsUi: state.userSettingsUi,
    setUserSettingsUi,
    userSettingsApi: state.userSettingsApi,
    setUserSettingsApi,
    pdfDimensions: state.pdfDimensions,
    setPdfDimensions,
    goToNextPage,
    goToPrevPage,
    isMenuOpen: state.isMenuOpen,
    setIsMenuOpen,
    selectedEyeTracker: state.selectedEyeTracker,
    setSelectedEyeTracker,
    isEyeTrackerConnected: state.isEyeTrackerConnected,
    setIsEyeTrackerConnected,
    isCalibrating: state.isCalibrating,
    setIsCalibrating,
    shouldSubscribe: state.shouldSubscribe,
    setShouldSubscribe,
    calibrationProcess: state.calibrationProcess,
    setCalibrationProcess,
    pageMounted: state.pageMounted,
    setPageMounted,
    shouldTranslate: state.shouldTranslate,
    setShouldTranslate,
  };

  return <Context.Provider value={contextValue}>{children}</Context.Provider>;
};
