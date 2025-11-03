import React, { useContext } from "react";
import ReactDOM from "react-dom";
import { RiCloseFill } from "react-icons/ri";
import { FaCheck } from "react-icons/fa";
import { Context } from "../../context/Context";
import { getBgPrimary, getBgPrimaryReverse, getFontColorSecondary } from "../../utils/functions";
import Button from "./Button";

interface DialogProps {
  title: string;
  content: string;
  onClose: () => void;
  onConfirm: () => void;
}

// 2. Use these types when declaring your component function
const Dialog: React.FC<DialogProps> = ({ title, content, onClose, onConfirm }) => {
  const { userSettingsApi } = useContext(Context);
  const modalRoot = document.getElementById("modal-root");
  const isDarkTheme = userSettingsApi.theme === "dark";

  const dialogContent = (
    <div className='fixed inset-0 w-full flex items-center justify-center z-50'>
      <div className='absolute inset-0 opacity-30' style={{ backgroundColor: getBgPrimaryReverse(isDarkTheme) }}></div>
      <div
        className={`rounded w-[500px] pt-4 pb-24 px-7 m-2 relative shadow-lg`}
        style={{ backgroundColor: getBgPrimary(isDarkTheme) }}
      >
        <div className='flex items-center mt-2 '>
          <h1 className='text-xl font-bold text-blue-500'>{title}</h1>
        </div>
        <div className='flex items-center mt-2 text-base' style={{ color: getFontColorSecondary(isDarkTheme) }}>
          {content}
        </div>
        <Button className='text-red-800 hover:text-red-700 absolute right-14 bottom-8' onClick={onClose}>
          <RiCloseFill className='text-3xl' />
        </Button>
        <Button
          className='text-green-800 hover:text-green-700 absolute right-6 bottom-9   active:scale-95 transform transition focus:outline-none'
          onClick={onConfirm}
        >
          <FaCheck className='text-xl' />
        </Button>
      </div>
    </div>
  );
  if (modalRoot !== null) {
    return ReactDOM.createPortal(dialogContent, modalRoot);
  }
  return null;
};

export default Dialog;
