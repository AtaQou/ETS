import React, {
  useCallback,
  useContext,
  useEffect,
  useMemo,
  useState,
  FC,
} from "react";
import { MdCastConnected, MdDensityMedium } from "react-icons/md";
import { BsFillPersonFill } from "react-icons/bs";
import { AiOutlineDisconnect } from "react-icons/ai";
import Profile from "./Profile";
import Menu from "./Menu";
import { Context } from "../context/Context";
import axios from "axios";
import Connection from "./Connection";
import { useSnackbar } from "../hooks/useSnackbar";
import { isEqual } from "lodash";
import Tooltip from "./ui/Tooltip";
import {
  getBgSecondaryReverse,
  getFontColorSecondary,
  saveToFile,
} from "../utils/functions";
import { FiDownload } from "react-icons/fi";
import Button from "./ui/Button";
import { ConnectionStatus, IContextProps } from "types/AppTypes";
import Dialog from "./ui/Dialog";
import { apiURL, dark_secondary, light_secondary } from "utils/consts";
// import { useEyeTrackingData } from "context/EyeTrackingContext";
import useEyeTrackingStore from "store/store";
import { BiFullscreen } from "react-icons/bi";

const HeaderMenu: FC = () => {
  const {
    file,
    logout,
    isMenuOpen,
    setIsMenuOpen,
    isCalibrating,
    userSettingsUi,
    userSettingsApi,
    setIsCalibrating,
    setShouldSubscribe,
    isEyeTrackerConnected,
    setIsEyeTrackerConnected,
  } = useContext<IContextProps>(Context);
  // const { eyeData } = useEyeTrackingData();
  // const { eyeData } = useEyeTrackingStore();
  const [showProfile, setShowProfile] = useState(false);
  const [connectionStatus, setConnectionStatus] =
    useState<ConnectionStatus>("");
  const [showConnectionModal, setShowConnectionModal] =
    useState<boolean>(false);
  const [eyeTrackers, setEyeTrackers] = useState([]);
  const [error, setError] = useState("");
  const { triggerSnackbar } = useSnackbar();
  const [showDiscardDialog, setShowDiscardDialog] = useState(false);

  const areSettingsEqual = useMemo(
    () => isEqual(userSettingsUi, userSettingsApi),
    [userSettingsApi, userSettingsUi]
  );

  const isDarkTheme = userSettingsApi.theme === "dark";

  const btnClass = () => {
    return isDarkTheme
      ? "bg-dark_primary hover:bg-darkHoverColor"
      : "bg-light_secondary hover:bg-lightHoverColor";
  };

  const toggleOpen = () => {
    if (isMenuOpen) {
      setIsMenuOpen?.(false);
    } else {
      setIsMenuOpen?.(true);
    }
  };

  const toggleProfile = () => {
    setShowProfile((prev) => !prev);
  };

  const toggleEyeTrackerSearch = useCallback(() => {
    axios
      .post(`${apiURL}/search`)
      .then((response) => {
        setConnectionStatus("selection");
        if (response.data.length) {
          setEyeTrackers(response.data);
        }
      })
      .catch((error) => {
        // setConnectionStatus("error");
        setConnectionStatus("selection");
        triggerSnackbar({
          message: "Search failed!",
          status: "error",
          open: true,
        });
        setError(error.message);
        console.error(error);
      });
  }, [triggerSnackbar]);

  const handleClick = useCallback(() => {
    setShowConnectionModal(true);
    setConnectionStatus("searching");
    toggleEyeTrackerSearch();
  }, [toggleEyeTrackerSearch]);

  const onClickLogout = () => {
    logout();
  };

  const onCloseConnectionModal = () => {
    if (connectionStatus === "connected") {
      setShowConnectionModal(false);
    } else {
      setConnectionStatus("");
      setShowConnectionModal(false);
    }
  };

  const onCloseSocketConnection = () => {
    setIsEyeTrackerConnected?.(false);
    setShouldSubscribe?.(false);
    setIsCalibrating?.(false);
  };

  const onStartTracking = () => {
    setShouldSubscribe?.(true);
    setShowConnectionModal(false);
  };

  const onToggleFullscreen = () => {
    const elem = document.documentElement;
    if (elem.requestFullscreen) {
      elem.requestFullscreen();
    }
    if (document.fullscreenElement) {
      document.exitFullscreen().catch((err) => {
        console.log(
          `Error attempting to disable full-screen mode: ${err.message} (${err.name})`
        );
      });
    }
  };

  const onDownloadDataClick = () => {
    // saveToFile(eyeData as Record<string, any>, "output.txt");
  };

  const onCloseMenu = () => {
    if (!areSettingsEqual) {
      setShowDiscardDialog(true);
    } else {
      setIsMenuOpen?.(false);
    }
  };

  const onDialogConfirm = () => {
    setShowDiscardDialog(false);
    setIsMenuOpen?.(false);
  };

  const onDialogClose = () => {
    setShowDiscardDialog(false);
  };

  useEffect(() => {
    if (connectionStatus === "connected") {
      setTimeout(() => {
        // setShowConnectionModal(false);
      }, 1000);
    }
  }, [connectionStatus]);

  return (
    <>
      {showDiscardDialog && (
        <Dialog
          title='Discard'
          content='Are you sure you want to discard your changes?'
          onClose={onDialogClose}
          onConfirm={onDialogConfirm}
        />
      )}
      <div className='ml-4 flex space-x-8'>
        <Tooltip
          content='Menu'
          position='right'
          color={getBgSecondaryReverse(isDarkTheme)}
        >
          <Button
            className={`py-2 px-2 rounded-full hover:scale-110 ${
              isDarkTheme
                ? "bg-dark_primary hover:bg-darkHoverColor"
                : "bg-light_secondary hover:bg-lightHoverColor"
            } transform transition-transform duration-300 active:scale-95 focus:outline-none`}
            onClick={toggleOpen}
          >
            <MdDensityMedium
              className='text-xl'
              style={{ color: getFontColorSecondary(isDarkTheme) }}
            />
          </Button>
        </Tooltip>
        {file?.size !== 0 && (
          <>
            {!isEyeTrackerConnected && (
              <Tooltip
                content='Connection'
                position='right'
                color={getBgSecondaryReverse(isDarkTheme)}
              >
                <Button
                  className={`py-2 px-2 rounded-full hover:scale-110 ${btnClass} transform transition-transform duration-300 active:scale-95 focus:outline-none`}
                  onClick={handleClick}
                >
                  <MdCastConnected
                    className='text-xl'
                    style={{ color: getFontColorSecondary(isDarkTheme) }}
                  />
                </Button>
              </Tooltip>
            )}
            {isEyeTrackerConnected && (
              <>
                <Tooltip
                  content='Close connection'
                  position='left'
                  color={isDarkTheme ? light_secondary : dark_secondary}
                >
                  <Button
                    className={`py-2 px-2 rounded-full hover:scale-110 ${
                      isDarkTheme
                        ? "bg-darkBg_primary hover:bg-darkHoverColor"
                        : "bg-lightBg_secondary hover:bg-lightHoverColor"
                    } transform transition-transform duration-300 active:scale-95 focus:outline-none`}
                    onClick={onCloseSocketConnection}
                  >
                    <AiOutlineDisconnect
                      className='text-xl'
                      style={{
                        ...(isDarkTheme
                          ? { color: light_secondary }
                          : { color: dark_secondary }),
                        color: isCalibrating ? "green" : "red",
                      }}
                    />
                  </Button>
                </Tooltip>
              </>
            )}
          </>
        )}
        {/* {isEyeTrackerConnected && (
          <div className='text-green-400 font-bold text-base self-center'>{`Connected to ${selectedEyeTracker.device_name}`}</div>
        )} */}
        {showConnectionModal && (
          <Connection
            error={error}
            status={connectionStatus}
            eyeTrackers={eyeTrackers}
            onStartTracking={onStartTracking}
            setConnectionStatus={setConnectionStatus}
            onClose={onCloseConnectionModal}
          />
        )}
        {isMenuOpen && <Menu onCloseMenu={onCloseMenu} />}
      </div>
      <div className='ml-[-35px]'>
        <img
          src={isDarkTheme ? "./logo5.png" : "./logo_light.png"}
          alt=''
          className='h-[2.3rem]'
        />
      </div>
      <div className='mr-4 flex space-x-8'>
        {showProfile && <Profile onClick={onClickLogout} />}
        <Tooltip
          content='Fullscreen'
          position='left'
          color={isDarkTheme ? light_secondary : dark_secondary}
        >
          <Button
            className={`py-2 px-2 rounded-full hover:scale-110 transform transition-transform duration-300 active:scale-95 focus:outline-none `}
            onClick={onToggleFullscreen}
          >
            <BiFullscreen
              className='text-xl text-blue-500'
              color={isDarkTheme ? light_secondary : dark_secondary}
            />
          </Button>
        </Tooltip>
        <Tooltip
          content='Download Eye data'
          position='left'
          color={isDarkTheme ? light_secondary : dark_secondary}
        >
          <Button
            className={`py-2 px-2 rounded-full hover:scale-110 transform transition-transform duration-300 active:scale-95 focus:outline-none `}
            onClick={onDownloadDataClick}
          >
            <FiDownload className='text-xl text-blue-500' />
          </Button>
        </Tooltip>
        <Tooltip
          content='Profile'
          position='left'
          color={getBgSecondaryReverse(isDarkTheme)}
        >
          <Button
            className={`py-2 px-2 rounded-full hover:scale-110 ${btnClass} transform transition-transform duration-300 active:scale-95 focus:outline-none`}
            onClick={toggleProfile}
          >
            <BsFillPersonFill
              className='text-xl'
              style={{ color: getFontColorSecondary(isDarkTheme) }}
            />
          </Button>
        </Tooltip>
      </div>
    </>
  );
};

export default HeaderMenu;
