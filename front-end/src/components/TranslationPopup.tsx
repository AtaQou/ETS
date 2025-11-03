import Button from "components/ui/Button";
import { Context } from "context/Context";
import React, { useContext, useState, useEffect } from "react";
import { RiCloseFill } from "react-icons/ri";
import { IContextProps } from "types/AppTypes";
import {
  getBgPrimary,
  getBgSecondary,
  getFontColorPrimary,
} from "utils/functions";

interface TranslationPopupProps {
  offset: number;
  translation: string;
  setShouldTranslate?: (payload: boolean) => void;
}

const TranslationPopup: React.FC<TranslationPopupProps> = ({
  offset,
  translation,
  setShouldTranslate,
}) => {
  const { userSettingsApi } = useContext<IContextProps>(Context);
  const left = offset - 40;

  const onClose = () => {
    setShouldTranslate?.(false);
  };

  const isDarkTheme = userSettingsApi.theme === "dark";

  useEffect(() => {
    const currentTime = new Date();
    let milli = currentTime.getMilliseconds();
    let f_milli = String(milli).padStart(3, "0");
    console.log(
      "translation rendereed!!!!!!!!!!",
      `${currentTime.getHours()}:${currentTime.getMinutes()}:${currentTime.getSeconds()}.${f_milli}`
    );
  }, []);

  return (
    <>
      <div
        id='translation'
        className={`absolute transform -translate-y-1/2 w-4 h-4 border border-[${getBgPrimary(
          isDarkTheme
        )}] opacity-80 rotate-45 shadow-xl`}
        style={{
          left: left / 2,
          top: -3,
          backgroundColor: getBgSecondary(isDarkTheme),
        }}
      ></div>
      <div
        className={`flex flex-col z-10 absolute w-auto h-auto rounded-lg  shadow-xl`}
        style={{
          backgroundColor: getBgSecondary(isDarkTheme),
          color: getFontColorPrimary(isDarkTheme),
          top: `-${30}px`,
          left: "20px",
        }}
      >
        <Button className='absolute right-0 top-0' onClick={onClose}>
          <RiCloseFill className='text-xl' />
        </Button>
        <div
          className='text-sm pl-3 py-1 pr-8 whitespace-nowrap'
          id='translation'
        >
          {translation.toLowerCase()}
        </div>
      </div>
    </>
  );
};

export default TranslationPopup;
