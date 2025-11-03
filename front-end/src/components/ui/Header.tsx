import React, { FC, useContext } from "react";
import { Context } from "../../context/Context";
import { dark_primary, light_secondary } from "../../utils/consts";
import { IContextProps } from "types/AppTypes";
import HeaderMenu from "components/HeaderMenu";

const Header: FC = () => {
  const { userSettingsApi } = useContext<IContextProps>(Context);
  const isDarkTheme = userSettingsApi.theme === "dark";

  return (
    <header
      className={`relative shadow-lg z-30 flex justify-between items-center w-full text-xl h-10`}
      id='header'
      style={{
        backgroundColor: isDarkTheme ? dark_primary : light_secondary,
      }}
    >
      <HeaderMenu />
    </header>
  );
};

export default Header;
