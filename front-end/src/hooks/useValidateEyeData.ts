import { useMemo } from "react";
import { GazeData } from "types/AppTypes";
import { getGazePointCoordinates } from "utils/eyeTracking";

const useValidateEyeData = (
  eyeData: GazeData[],
  bounds: {
    left: number;
    top: number;
    right: number;
    bottom: number;
  }
) => {
  return useMemo(() => {
    const { left, top, right, bottom } = bounds;
    for (const data of eyeData) {
      const { pointX, pointY } = getGazePointCoordinates(data);
      if (pointX < left || pointX > right || pointY < top || pointY > bottom)
        return false;
    }
    return true;
  }, [eyeData, bounds]);
};
export default useValidateEyeData;
