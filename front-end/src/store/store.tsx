import { GazeData } from "types/AppTypes";
import create from "zustand";

interface EyeTrackingStore {
  eyeData: GazeData[];
  accumulateData: (newData: GazeData) => void;
}

const useEyeTrackingStore = create<EyeTrackingStore>((set) => ({
  eyeData: [],
  accumulateData: (newData: GazeData) =>
    set((state) => ({
      eyeData:
        state.eyeData.length > 2100
          ? [...state.eyeData.slice(1500), newData]
          : [...state.eyeData, newData],
    })),
}));

export default useEyeTrackingStore;
