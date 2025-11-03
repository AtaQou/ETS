import { DebounceFn } from "types/AppTypes";
import {
  dark_primary,
  dark_secondary,
  light_primary,
  light_secondary,
} from "./consts";

// export const base64ToBlob = (base64, type = "") => {
//   const byteCharacters = atob(base64.split(",")[1]);
//   const byteNumbers = new Array(byteCharacters.length);
//   for (let i = 0; i < byteCharacters.length; i++) {
//     byteNumbers[i] = byteCharacters.charCodeAt(i);
//   }
//   const byteArray = new Uint8Array(byteNumbers);
//   return new Blob([byteArray], { type: type });
// };

// export const getFileFromStorage = () => {
//   const base64 = localStorage.getItem("pdfFile");
//   if (base64) {
//     const retrievedPdfBlob = base64ToBlob(base64, "application/pdf");
//     return retrievedPdfBlob;
//   }
//   return { size: 0 };
// };

// export const blobToBase64 = (blob) => {
//   return new Promise((resolve, reject) => {
//     const reader = new FileReader();
//     reader.onloadend = function () {
//       resolve(reader.result);
//     };
//     reader.onerror = reject;
//     reader.readAsDataURL(blob);
//   });
// };

export const debounce = (fn: DebounceFn, delay: number): DebounceFn => {
  let timeout: NodeJS.Timeout | null = null;

  return function (...args: any[]): void {
    if (timeout) {
      clearTimeout(timeout);
    }

    timeout = setTimeout(() => {
      fn(...args);
    }, delay);
  };
};

export const capitalize = (str: string) => {
  return str.charAt(0).toUpperCase() + str.slice(1);
};

export const getFontColorPrimary = (isDarkTheme: boolean) =>
  isDarkTheme ? light_primary : dark_primary;

export const getFontColorSecondary = (isDarkTheme: boolean) =>
  isDarkTheme ? light_secondary : dark_secondary;

export const getBgPrimary = (isDarkTheme: boolean) =>
  isDarkTheme ? dark_primary : light_primary;

export const getBgSecondary = (isDarkTheme: boolean) =>
  isDarkTheme ? dark_secondary : light_secondary;

export const getBgPrimaryReverse = (isDarkTheme: boolean) =>
  isDarkTheme ? light_primary : dark_primary;

export const getBgSecondaryReverse = (isDarkTheme: boolean) =>
  isDarkTheme ? light_secondary : dark_secondary;

export const getSize = () => {
  const element = document.getElementById("tooltip");
  if (element) {
    const { width, height } = element.getBoundingClientRect();
    return { width, height };
  }
  return { width: 0, height: 0 };
};

export const saveToFile = (data: Record<string, any>, filename: string) => {
  const serializedData = JSON.stringify(data, null, 1);
  const blob = new Blob([serializedData], { type: "text/plain" });
  const url = window.URL.createObjectURL(blob);
  const a = document.createElement("a");

  a.style.display = "none";
  a.href = url;
  a.download = filename;

  document.body.appendChild(a);
  a.click();

  window.URL.revokeObjectURL(url);
};

export const calculateScaledPositions = (
  box: number[],
  scrollTop: number,
  currentPage: number,
  scale: number
): { xPrime: number; yPrime: number; wPrime: number; hPrime: number } => {
  const [x, y, w, h] = box;
  const pdfContainer = document.getElementById("pdf-container");
  const element = document.getElementById("pdf-page");
  const header = document.getElementById("header");
  const footer = document.getElementById("footer");

  if (pdfContainer && element && header && footer) {
    const { width: canvasWidth, height: canvasHeight } =
      element.getBoundingClientRect();
    const { width: containerWidth } = pdfContainer.getBoundingClientRect();
    const { height: headerHeight } = header.getBoundingClientRect();

    console.log({ canvasWidth, canvasHeight });

    const cWidth = canvasWidth;

    const horizontalMargin = scale < 1 ? (containerWidth - cWidth) / 2 : 0;

    const yRelativeToPage = y + (currentPage - 1) * canvasHeight;

    const xPrime = x + horizontalMargin - 5;
    const yPrime = yRelativeToPage - scrollTop + headerHeight - 5;
    const wPrime = w + 10;
    const hPrime = h + 10;

    return { xPrime, yPrime, wPrime, hPrime };
  }
  return { xPrime: 0, yPrime: 0, wPrime: 0, hPrime: 0 };
};

const normalizeBounds = ({
  xPrime,
  yPrime,
  wPrime,
  hPrime,
}: {
  xPrime: number;
  yPrime: number;
  wPrime: number;
  hPrime: number;
}) => {
  const screenWidth = document.documentElement.scrollWidth;
  const screenHeight = document.documentElement.scrollHeight;

  const left = xPrime / screenWidth;
  const top = yPrime / screenHeight;
  const right = (xPrime + wPrime) / screenWidth;
  const bottom = (yPrime + hPrime) / screenHeight;

  return { left, top, right, bottom };
};
