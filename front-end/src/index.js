import React from "react";
import ReactDOM from "react-dom/client";
import App from "./App";
import "./index.css";
import { ContextProvider } from "./context/Context";
import { SnackbarProvider } from "./context/SnackbarContext";
import { WordPositionsProvider } from "./context/WordPositionsContext";

const root = ReactDOM.createRoot(document.getElementById("root"));
root.render(
  <ContextProvider>
    <SnackbarProvider>
      <WordPositionsProvider>
        <App />
      </WordPositionsProvider>
    </SnackbarProvider>
  </ContextProvider>
);
