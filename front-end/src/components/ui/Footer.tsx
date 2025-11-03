import React, {
  useContext,
  useEffect,
  useMemo,
  useState,
  ChangeEvent,
} from "react";
import { Context } from "../../context/Context";
import { BiSolidLeftArrow } from "react-icons/bi";
import { BiSolidRightArrow } from "react-icons/bi";
import {
  dark_primary,
  dark_secondary,
  light_primary,
  light_secondary,
  shadowLgTop,
} from "../../utils/consts";
import { getBgPrimary, getFontColorSecondary } from "../../utils/functions";
import Button from "./Button";

const Footer = () => {
  const {
    loading,
    goToPrevPage,
    goToNextPage,
    pageCount,
    currentPage,
    setCurrentPage,
    pdfDimensions,
    userSettingsApi,
  } = useContext(Context);
  const isDarkTheme = userSettingsApi.theme === "dark";
  const [inputValue, setInputValue] = useState(0);

  const style = useMemo(
    () =>
      isDarkTheme
        ? {
            backgroundColor: dark_secondary,
            color: light_secondary,
          }
        : {
            backgroundColor: light_primary,
            color: dark_primary,
          },
    [isDarkTheme]
  );

  const handlePageChange = (e: ChangeEvent<HTMLInputElement>) => {
    const { value } = e.target;
    const pageNumber = Number(value);

    if (pageNumber > 0 && pageNumber <= pageCount) {
      setInputValue(Number(pageNumber));
      setCurrentPage?.(pageNumber);
      const container = document.getElementById("pdf-container");
      const scrollTop = (pageNumber - 1) * pdfDimensions.height;
      if (container) {
        container.scrollTop = scrollTop;
      }
    }
  };

  const onPrevClick = (e: React.MouseEvent<HTMLButtonElement, MouseEvent>) => {
    goToPrevPage?.();
  };

  const onNextClick = (e: React.MouseEvent<HTMLButtonElement, MouseEvent>) => {
    goToNextPage?.();
  };

  useEffect(() => {
    setInputValue(currentPage);
  }, [currentPage]);

  return (
    <footer
      className={`z-10 w-full flex items-center justify-center px-4 absolute bottom-0 h-12`}
      id='footer'
      style={{
        ...(isDarkTheme
          ? {
              backgroundColor: dark_primary,
            }
          : {
              backgroundColor: light_secondary,
            }),
        ...shadowLgTop,
      }}
    >
      <div>
        <Button
          className={`bg-blue-500 text-[${getBgPrimary(
            isDarkTheme
          )}] text-sm rounded-full hover:scale-110 py-2 px-1 active:scale-95 transform transition focus:outline-none shadow-lg`}
          style={{ color: light_secondary }}
          onClick={onPrevClick}
          disabled={currentPage === 1 || currentPage === 0 || loading}
        >
          <BiSolidLeftArrow />
        </Button>

        <span
          className='mx-2 text-sm'
          style={{ color: getFontColorSecondary(isDarkTheme) }}
        >
          Page
          <input
            className='slider text-gray-900 p-1 h-7 rounded  w-10 my-3 mx-1 active:scale-95 transform transition focus:outline-none'
            style={style}
            type='number'
            min='1'
            disabled={currentPage === pageCount || currentPage === 0 || loading}
            max={pageCount}
            value={inputValue}
            onChange={handlePageChange}
          />
          of {pageCount}
        </span>
        <Button
          className={`bg-blue-500 text-[${getBgPrimary(
            isDarkTheme
          )}] text-sm rounded-full hover:scale-110 py-2 px-1 active:scale-95 transform transition focus:outline-none shadow-lg`}
          style={{ color: light_secondary }}
          onClick={onNextClick}
          disabled={currentPage === pageCount || currentPage === 0 || loading}
        >
          <BiSolidRightArrow />
        </Button>
      </div>
    </footer>
  );
};

export default Footer;
