import React, { useContext, useMemo, useState } from "react";
import ModalWrapper from "./ui/ModalWrapper";
import Documents from "./Documents";
import { Context } from "../context/Context";
import axios from "axios";
import FileUpload from "./FileUpload";
import Settings from "./Settings";
import Vocabulary from "./Vocabulary";
import { useSnackbar } from "../hooks/useSnackbar";
import { FiArrowLeft } from "react-icons/fi";
import { isEqual } from "lodash";
import { apiURL, dark_primary, light_primary } from "../utils/consts";
import { getBgSecondary, getFontColorPrimary } from "../utils/functions";
import { IContextProps, ID } from "types/AppTypes";
import Button from "./ui/Button";

interface MenuProps {
  onCloseMenu: () => void;
}

function Menu({ onCloseMenu }: MenuProps) {
  const {
    file,
    loadFile,
    setLoading,
    selectedDocID,
    userInfo,
    setIsMenuOpen,
    userSettingsUi,
    userSettingsApi,
    setSelectedDocID,
    setUserSettingsApi,
  } = useContext<IContextProps>(Context);
  const { zoom, theme, language } = userSettingsUi;
  const { userID } = userInfo;
  const [selectedOption, setSelectedOption] = useState("settings");
  const [loadingMenu, setLoadingMenu] = useState(false);
  const { triggerSnackbar } = useSnackbar();
  const [docID, setDocID] = useState<ID>(selectedDocID)

  const settingsHaveChanges = useMemo(
    () => !isEqual(userSettingsUi, userSettingsApi),
    [userSettingsApi, userSettingsUi]
  );

  const shouldDisableConfirm =
    ((selectedOption === "documents" || selectedOption === "upload") &&
    docID === "") ||
    (selectedOption === "settings" && !settingsHaveChanges);

  const isDarkTheme = userSettingsApi.theme === "dark";

  const onConfirm = (id: ID) => {
    setLoadingMenu(true);
    setLoading?.(true);
    setSelectedDocID?.(docID)
    if (selectedOption === "settings") {
      if (!settingsHaveChanges) {
      } else {
        axios
          .post(`${apiURL}/settings`, {
            userID,
            zoomLevel: zoom,
            theme,
            language,
          })
          .then((res) => {
            setLoadingMenu(false);
            loadFile?.(file);
            setUserSettingsApi?.({
              zoom,
              theme,
              language,
            });
            triggerSnackbar({
              message: "Settings saved successfully!",
              status: "success",
              open: true,
            });
            setLoading?.(false);
          })
          .catch((err) => {
            console.error(err);
            setLoadingMenu(false);
          });
      }
    }
    if (selectedOption === "documents" || selectedOption === "upload") {
      axios
        .get(`${apiURL}/get_file`, {
          params: {
            docID: id || docID,
            userID,
          },
          responseType: "blob",
        })
        .then((response) => {
          const fileBlob = new Blob([response.data], {
            type: response.data.type,
          });
          setLoadingMenu(false);
          loadFile?.(fileBlob);
          setLoading?.(false);
        })
        .catch((error) => {
          console.log({ error });
          alert("Failed to load file.");
        });
    }
    setIsMenuOpen?.(false);
  };

  const onClickUpload = () => {
    setSelectedOption("upload");
  };

  const renderContent = () => {
    switch (selectedOption) {
      case "settings":
        return <Settings />;
      case "vocabulary":
        return <Vocabulary />;
      case "documents":
        return <Documents docID={docID} setDocID={setDocID} onConfirm={onConfirm} />;
      case "upload":
        return <FileUpload />;
      default:
        return <div>Please select an option.</div>;
    }
  };

  return (
    <>
      <ModalWrapper
        loading={loadingMenu}
        className='xl:w-[70%] lg:w-[80%] h-[80vh]'
        title='Menu'
        style={{ backgroundColor: getBgSecondary(isDarkTheme) }}
        onConfirm={onConfirm}
        onClickUpload={onClickUpload}
        shouldDisableConfirm={shouldDisableConfirm}
        shouldShowUpload={selectedOption === "documents"}
        onClose={onCloseMenu}
      >
        <div
          className={`flex h-[64vh]`}
          style={{ color: getFontColorPrimary(isDarkTheme) }}
        >
          <div
            className={`rounded`}
            style={
              isDarkTheme
                ? {
                    border: `2px solid ${dark_primary}`,
                    backgroundColor: dark_primary,
                  }
                : {
                    border: `2px solid ${light_primary}`,
                    backgroundColor: light_primary,
                  }
            }
          >
            <div
              className={`cursor-pointer p-1 xl:w-48 lg:w-[12rem] text-base hover:text-blue-500 px-4 py-2`}
              style={
                selectedOption === "settings"
                  ? {
                      backgroundColor: getBgSecondary(isDarkTheme),
                      color: "rgb(59 130 246)",
                    }
                  : {}
              }
              onClick={() => setSelectedOption("settings")}
            >
              Settings
            </div>
            <div
              className={`cursor-pointer p-1 xl:w-48 lg:w-[12rem] text-base hover:text-blue-500 px-4 py-2`}
              style={
                selectedOption === "documents" || selectedOption === "upload"
                  ? {
                      backgroundColor: getBgSecondary(isDarkTheme),
                      color: "rgb(59 130 246)",
                    }
                  : {}
              }
              onClick={() => setSelectedOption("documents")}
            >
              Documents
            </div>
            <div
              className={`cursor-pointer p-1 xl:w-48 lg:w-[12rem] text-base hover:text-blue-500 px-4 py-2`}
              style={
                selectedOption === "vocabulary"
                  ? {
                      backgroundColor: getBgSecondary(isDarkTheme),
                      color: "rgb(59 130 246)",
                    }
                  : {}
              }
              onClick={() => setSelectedOption("vocabulary")}
            >
              Vocabulary
            </div>
          </div>
          <div className={`w-full rounded max-h-[64vh] lg`}>
            <div
              className={`h-full w-full rounded overflow-y-scroll border-[1rem] relative`}
              style={
                isDarkTheme
                  ? {
                      borderColor: dark_primary,
                    }
                  : {
                      borderColor: light_primary,
                    }
              }
            >
              {renderContent()}
              {selectedOption === "upload" && (
                <Button
                  label='Back to Documents'
                  className={`absolute right-4 top-4 flex justify-center items-center p-2`}
                  onClick={() => setSelectedOption("documents")}
                >
                  <FiArrowLeft className='text-xl mr-2' />
                </Button>
              )}
            </div>
          </div>
        </div>
      </ModalWrapper>
    </>
  );
}

export default Menu;
