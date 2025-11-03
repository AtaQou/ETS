import { useContext } from "react";
import { SnackbarContext, SnackbarContextProps } from "../context/SnackbarContext";

export const useSnackbar = (): SnackbarContextProps => {
  const context = useContext<SnackbarContextProps | undefined>(SnackbarContext);

  if (!context) {
    throw new Error("useSnackbar must be used within a SnackbarProvider");
  }

  return context;
};
