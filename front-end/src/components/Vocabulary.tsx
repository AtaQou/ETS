import React, { useContext, FC } from "react";
import { Context } from "../context/Context";
import { getFontColorSecondary } from "../utils/functions";
import { IContextProps } from "types/AppTypes";

const Vocabulary: FC = () => {
  const { userSettingsApi } = useContext<IContextProps>(Context);
  const isDarkTheme = userSettingsApi.theme === "dark";

  return (
    <div className='flex flex-col  m-2 p-4'>
      <h1
        className='py-1 mb-4 text-xl font-bold text-gray-900 border-b border-gray-300'
        style={{ color: getFontColorSecondary(isDarkTheme) }}
      >
        Vocabulary
      </h1>
      <div className='mb-8 text-gray-600' style={{ color: getFontColorSecondary(isDarkTheme) }}>
        Here is your vocabulary.
      </div>
    </div>
  );
};

export default Vocabulary;
