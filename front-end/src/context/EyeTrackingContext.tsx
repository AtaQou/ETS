import React, { createContext, useState, useContext, ReactNode } from "react";
import { GazeData } from "types/AppTypes";

interface EyeTrackingContextProps {
  eyeData: GazeData[];
  accumulateData: (newData: GazeData) => void;
}

const EyeTrackingContext = createContext<EyeTrackingContextProps | undefined>(
  undefined
);

interface EyeTrackingProviderProps {
  children: ReactNode;
}

export const EyeTrackingProvider: React.FC<EyeTrackingProviderProps> = ({
  children,
}) => {
  const [eyeData, setEyeData] = useState<GazeData[]>([]);

  const accumulateData = (newData: GazeData) => {
    setEyeData((prevData) => {
      const newEyeData = [...prevData, newData];
      if (newEyeData.length > 2100) {
        newEyeData.slice(1500);
      }
      return newEyeData;
    });
  };

  return (
    <EyeTrackingContext.Provider value={{ eyeData, accumulateData }}>
      {children}
    </EyeTrackingContext.Provider>
  );
};

export const useEyeTrackingData = (): EyeTrackingContextProps => {
  const context = useContext(EyeTrackingContext);
  if (!context) {
    throw new Error(
      "useEyeTrackingData must be used within an EyeTrackingProvider"
    );
  }
  return context;
};
