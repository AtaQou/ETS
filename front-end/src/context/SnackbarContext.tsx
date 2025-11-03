import React, { createContext, useState, ReactNode } from "react";

// Define the interfaces
interface SnackbarData {
  message: string;
  status: string;
  open: boolean;
}

export interface SnackbarContextProps {
  snackbarData: SnackbarData;
  triggerSnackbar: (newData: SnackbarData) => void;
  closeSnackbar: () => void;
}

export const SnackbarContext = createContext<SnackbarContextProps | undefined>(undefined);

interface SnackbarProviderProps {
  children: ReactNode;
}

export const SnackbarProvider: React.FC<SnackbarProviderProps> = ({ children }) => {
  const [snackbarData, setSnackbarData] = useState<SnackbarData>({
    message: "",
    status: "",
    open: false,
  });

  const closeSnackbar = () => {
    setSnackbarData((prevData) => ({ ...prevData, open: false }));
  };

  const triggerSnackbar = (newData: SnackbarData) => {
    closeSnackbar();
    setTimeout(() => {
      setSnackbarData({ ...newData, open: true });
    }, 100);
  };

  return (
    <SnackbarContext.Provider value={{ snackbarData, triggerSnackbar, closeSnackbar }}>
      {children}
    </SnackbarContext.Provider>
  );
};
