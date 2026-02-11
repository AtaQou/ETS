import { GazeData, IScaledWordCoords, IWordPositions } from "types/AppTypes";

// export const normalizeCoordinates = (x, y) => {
//   const screenWidth = window.screen.width;
//   const screenHeight = window.screen.height;

//   const normalizedX = x / screenWidth;
//   const normalizedY = y / screenHeight;

//   return [normalizedX, normalizedY];
// };

// document.addEventListener("mousemove", (event) => {
//   const xPixel = event.clientX;
//   const yPixel = event.clientY;

//   const [xNormalized, yNormalized] = normalizeCoordinates(xPixel, yPixel);

//   console.log(`Clicked at pixel coordinates: (${xPixel}, ${yPixel})`);
//   console.log(`Normalized coordinates: (${xNormalized}, ${yNormalized})`);
// });

// export const createRedPoint = (
//   normalizedX: number,
//   normalizedY: number
// ): void => {
//   const screenWidth = window.screen.width;
//   const screenHeight = window.screen.height;

//   const actualX = normalizedX * document.documentElement.scrollWidth;
//   const actualY = normalizedY * document.documentElement.scrollHeight;

//   // Check if a red point already exists and remove it
//   const existingPoint = document.getElementById("eyeTrackingPoint");
//   if (existingPoint) {
//     existingPoint.remove();
//   }

//   const point = document.createElement("div");
//   point.id = "eyeTrackingPoint"; // Set an id for easy reference
//   point.style.position = "fixed";
//   point.style.left = `${actualX}px`;
//   point.style.top = `${actualY}px`;
//   point.style.border = "2px solid red";
//   point.style.borderRadius = "50%";
//   point.style.width = "20px";
//   point.style.height = "20px";
//   point.style.transform = "translateX(-50%) translateY(-50%)";
//   point.style.pointerEvents = "none";
//   point.style.transition = "all 300ms ease-out";
//   point.style.zIndex = "999";

//   document.body.appendChild(point);
// };

export const getGazePointCoordinates = (data: GazeData) => {
  const screenWidth = window.screen.width;
  const screenHeight = window.screen.height;
  const resolution = [screenWidth, screenHeight];
  let averageX = 0;
  let averageY = 0;

  if (data.left_gaze_point_validity && data.right_gaze_point_validity) {
    averageX = parseFloat(
      (
        (data.left_gaze_point_on_display_area[0] +
          data.right_gaze_point_on_display_area[0]) /
        2
      ).toFixed(2)
    );

    averageY = parseFloat(
      (
        (data.left_gaze_point_on_display_area[1] +
          data.right_gaze_point_on_display_area[1]) /
        2
      ).toFixed(2)
    );
  } else if (data.left_gaze_point_validity) {
    averageX = data.left_gaze_point_on_display_area[0];
    averageY = data.left_gaze_point_on_display_area[1];
  } else if (data.right_gaze_point_validity) {
    averageX = data.right_gaze_point_on_display_area[0];
    averageY = data.right_gaze_point_on_display_area[1];
  }

  if (data.left_gaze_point_validity || data.right_gaze_point_validity) {
    averageX = Math.min(
      Math.max(0, Math.round(averageX * resolution[0])),
      resolution[0]
    );
    averageY = Math.min(
      Math.max(0, Math.round(averageY * resolution[1])),
      resolution[1]
    );
  }

  return { pointX: averageX, pointY: averageY };
};
// This is for batches of gaze data and makes the circle smoother.
export const getAverageGazePointCoordinates2 = (dataArray: GazeData[]) => {
  let totalX = 0;
  let totalY = 0;
  let count = 0;

  const screenWidth = window.screen.width;
  const screenHeight = window.screen.height;
  const resolution = [screenWidth, screenHeight];

  dataArray.forEach((data) => {
    let averageX = 0;
    let averageY = 0;
    if (data.left_gaze_point_validity && data.right_gaze_point_validity) {
      averageX = parseFloat(
        (
          (data.left_gaze_point_on_display_area[0] +
            data.right_gaze_point_on_display_area[0]) /
          2
        ).toFixed(2)
      );

      averageY = parseFloat(
        (
          (data.left_gaze_point_on_display_area[1] +
            data.right_gaze_point_on_display_area[1]) /
          2
        ).toFixed(2)
      );
    } else if (data.left_gaze_point_validity) {
      averageX = data.left_gaze_point_on_display_area[0];
      averageY = data.left_gaze_point_on_display_area[1];
    } else if (data.right_gaze_point_validity) {
      averageX = data.right_gaze_point_on_display_area[0];
      averageY = data.right_gaze_point_on_display_area[1];
    }

    if (data.left_gaze_point_validity || data.right_gaze_point_validity) {
      averageX = Math.min(
        Math.max(0, Math.round(averageX * resolution[0])),
        resolution[0]
      );
      averageY = Math.min(
        Math.max(0, Math.round(averageY * resolution[1])),
        resolution[1]
      );
    }

    totalX += averageX;
    totalY += averageY;
    count++;
  });

  return count > 0
    ? { pointX: totalX / count, pointY: totalY / count }
    : { pointX: 0, pointY: 0 };
};

export const validateEyeData = (
  eyeData: GazeData[],
  bounds: {
    left: number;
    top: number;
    right: number;
    bottom: number;
  }
) => {
  const { left, top, right, bottom } = bounds;
  for (const dato of eyeData) {
    const { pointX, pointY } = getGazePointCoordinates(dato);
    console.log("Average gaze point", pointX, pointY);
    console.log("Tis leksis", left, top, right, bottom);
    // console.log('Average gaze point + 0.1', pointX + 0.1, pointY + 0.1)
    if (pointX < left || pointX > right || pointY < top || pointY > bottom)
      return false;
  }
  return true;
};

// left: left - wordPadding / 2,
//     top: top - wordPadding / 2,
//     right: left + width,
//     bottom: top + height,

const isPointInsideBox = (
  x: number,
  y: number,
  {
    left,
    top,
    right,
    bottom,
  }: { left: number; top: number; right: number; bottom: number }
) => {
  return x >= left && x <= right && y >= top && y <= bottom;
};

export const validateEyeData2 = (
  eyeData: GazeData[],
  wordPositions: IScaledWordCoords[],
  wordPadding = 10
) => {
  const baseGazePoints = 60;
  const additionalGazePointsPerLetter = 10;
  for (let wordData of wordPositions) {
    const { word, wordCoords } = wordData;
    const { left, top, width, height } = wordCoords;

    const gazePointsToConsider =
      baseGazePoints + (word.length - 1) * additionalGazePointsPerLetter;

    const relevantEyeData = eyeData.slice(
      -Math.min(gazePointsToConsider, eyeData.length)
    );

    const allPointsInside = relevantEyeData.every((rel) => {
      const { pointX, pointY } = getGazePointCoordinates(rel);
      return isPointInsideBox(pointX, pointY, {
        left: left,
        top: top,
        right: left + width,
        bottom: top + height,
      });
    });

    if (allPointsInside) {
      return wordData;
    }
  }
  return { word: "", wordCoords: { left: 0, top: 0, width: 0, height: 0 } };
};

export const validateHoldTranslation = (
  dimensions: DOMRect,
  data: GazeData[]
) => {
  const { left, top, width, height } = dimensions;
  return data.every((d) => {
    const { pointX, pointY } = getGazePointCoordinates(d);
    return isPointInsideBox(pointX, pointY, {
      left: left - 40,
      top: top - 40,
      right: left + width + 40,
      bottom: top + height + 40,
    });
  });
};
