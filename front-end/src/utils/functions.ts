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
  currentPage: number,
  pageSize?: { width?: number; height?: number }
): { xPrime: number; yPrime: number; wPrime: number; hPrime: number } => {
  const [x, y, w, h] = box;
  const pageWrapper = document.querySelector(
    `[data-page-number="${currentPage}"]`
  ) as HTMLElement | null;

  // Prefer the actual canvas to capture the rendered scale of the PDF page
  const pageCanvas = pageWrapper?.querySelector("canvas") as
    | HTMLCanvasElement
    | null;

  if (!pageWrapper) {
    return { xPrime: 0, yPrime: 0, wPrime: 0, hPrime: 0 };
  }

  const targetElement = (pageCanvas as HTMLElement) ?? pageWrapper;
  const { width: cssWidth, height: cssHeight, left, top } =
    targetElement.getBoundingClientRect();

  const naturalWidth = pageSize?.width ?? pageCanvas?.width ?? cssWidth;
  const naturalHeight = pageSize?.height ?? pageCanvas?.height ?? cssHeight;

  const scaleX = cssWidth / (naturalWidth || 1);
  const scaleY = cssHeight / (naturalHeight || 1);

  const xPrime = left + x * scaleX;
  const yPrime = top + y * scaleY;
  const wPrime = w * scaleX;
  const hPrime = h * scaleY;

  return { xPrime, yPrime, wPrime, hPrime };
};

