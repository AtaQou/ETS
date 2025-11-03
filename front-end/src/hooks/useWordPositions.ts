import { WordPositionsContext } from "context/WordPositionsContext";
import { useContext } from "react";

export const useWordPositions = () => {
  const context = useContext(WordPositionsContext);
  if (!context) {
    throw new Error(
      "useWordPositions must be used within a WordPositionsProvider"
    );
  }
  return context;
};
