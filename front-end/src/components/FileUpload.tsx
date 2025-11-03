import React, { ChangeEvent, FormEvent } from "react";
import { useContext, useMemo, useState } from "react";
import axios from "axios";
import { Context } from "../context/Context";
import { useSnackbar } from "../hooks/useSnackbar";
import { apiURL, light_secondary } from "../utils/consts";
import { getFontColorSecondary } from "../utils/functions";
import { IContextProps } from "types/AppTypes";
import Button from "./ui/Button";

const FileUpload: React.FC = () => {
  const [pdfFile, setPdfFile] = useState<File | null>(null);

  const { userInfo, setSelectedDocID, userSettingsApi } =
    useContext<IContextProps>(Context);

  const { userID } = userInfo;
  const { triggerSnackbar } = useSnackbar();

  const isDarkTheme = userSettingsApi.theme === "dark";

  const fontStyle = useMemo(
    () => ({ color: getFontColorSecondary(isDarkTheme) }),
    [isDarkTheme]
  );

  const submitFile = (event: FormEvent<HTMLFormElement>) => {
    event.preventDefault();
    const formData = new FormData();

    if (pdfFile) {
      formData.append("file", pdfFile);
    }

    formData.append("userID", userID);

    axios
      .post(`${apiURL}/upload_file`, formData, {
        headers: {
          "Content-Type": "multipart/form-data",
        },
      })
      .then((response) => {
        triggerSnackbar({
          message: response.data.message,
          status: "success",
          open: true,
        });
        setSelectedDocID?.(response.data.docID);
      })
      .catch((error) => {
        console.error(error);
        triggerSnackbar({
          message: error.response.data.message,
          status: "error",
          open: true,
        });
      });
  };

  const handleFileUpload = (event: ChangeEvent<HTMLInputElement>) => {
    const file = event.target.files ? event.target.files[0] : null;
    setPdfFile(file);
  };

  return (
    <div className='flex flex-col m-2 p-4'>
      <h1
        className='py-1 mb-4 text-xl font-bold text-gray-900 border-b border-gray-300'
        style={fontStyle}
      >
        Upload File
      </h1>
      <div className='mb-6 text-gray-600' style={fontStyle}>
        Choose a pdf file to upload and click Confirm to load the document.
      </div>
      <form onSubmit={submitFile} className='flex'>
        <input
          className={`w-96 bg-gray-500 hover:bg-gray-400 text-slate-200 py-1 px-2 rounded cursor-pointer text-base`}
          style={{ color: light_secondary }}
          type='file'
          id='file'
          accept='.pdf'
          onChange={handleFileUpload}
        />
        <Button
          type='submit'
          label='Upload'
          disabled={pdfFile === null}
          className={`bg-blue-500 p-4 mx-4 text-base active:scale-95 transform transition focus:outline-none shadow-lg`}
          style={{ color: light_secondary }}
        />
      </form>
    </div>
  );
};

export default FileUpload;
