import { GazeData, IScaledWordCoords } from "types/AppTypes";

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

const getViewportResolution = () => {
  const width =
    window.innerWidth ||
    document.documentElement.clientWidth ||
    window.visualViewport?.width ||
    window.screen.width;
  const height =
    window.innerHeight ||
    document.documentElement.clientHeight ||
    window.visualViewport?.height ||
    window.screen.height;

  return [Math.max(1, Math.round(width)), Math.max(1, Math.round(height))];
};

const clampGazeYOffsetPx = (value: number) =>
  Math.max(0, Math.min(100, Math.round(value)));

const readInitialGazeYOffsetPx = () => {
  if (typeof window === "undefined") return 8;
  try {
    const rawSettings = window.localStorage.getItem("userSettingsUi");
    if (!rawSettings) return 8;
    const parsed = JSON.parse(rawSettings);
    return clampGazeYOffsetPx(Number(parsed?.gazeYOffsetPx ?? 8));
  } catch (error) {
    return 8;
  }
};

let gazeYOffsetPx = readInitialGazeYOffsetPx();

export const setGazeYOffsetPx = (value: number) => {
  gazeYOffsetPx = clampGazeYOffsetPx(value);
};

export const getGazeYOffsetPx = () => gazeYOffsetPx;

const getScreenResolution = () => {
  const width = window.screen.width || window.innerWidth || 1;
  const height = window.screen.height || window.innerHeight || 1;
  return [Math.max(1, Math.round(width)), Math.max(1, Math.round(height))];
};

const getViewportOffsetOnScreen = () => {
  const screenLeft =
    typeof window.screenX === "number"
      ? window.screenX
      : (window as any).screenLeft || 0;
  const screenTop =
    typeof window.screenY === "number"
      ? window.screenY
      : (window as any).screenTop || 0;

  const outerWidth = window.outerWidth || window.innerWidth || 0;
  const outerHeight = window.outerHeight || window.innerHeight || 0;
  const innerWidth = window.innerWidth || 0;
  const innerHeight = window.innerHeight || 0;

  // Approximate browser frame/chrome thickness so we can convert absolute
  // screen coordinates to viewport/client coordinates.
  const borderX = Math.max(0, (outerWidth - innerWidth) / 2);
  const verticalChrome = Math.max(0, outerHeight - innerHeight);
  const titleAndToolbarY = Math.max(0, verticalChrome - borderX);

  return {
    viewportLeftOnScreen: screenLeft + borderX,
    viewportTopOnScreen: screenTop + titleAndToolbarY,
  };
};

const clampToViewport = (x: number, y: number) => {
  const [viewportWidth, viewportHeight] = getViewportResolution();
  return {
    pointX: Math.min(Math.max(0, Math.round(x)), viewportWidth - 1),
    pointY: Math.min(Math.max(0, Math.round(y)), viewportHeight - 1),
  };
};

const getNormalizedGazePoint = (data: GazeData) => {
  if (data.left_gaze_point_validity && data.right_gaze_point_validity) {
    return {
      x:
        (data.left_gaze_point_on_display_area[0] +
          data.right_gaze_point_on_display_area[0]) /
        2,
      y:
        (data.left_gaze_point_on_display_area[1] +
          data.right_gaze_point_on_display_area[1]) /
        2,
    };
  }

  if (data.left_gaze_point_validity) {
    return {
      x: data.left_gaze_point_on_display_area[0],
      y: data.left_gaze_point_on_display_area[1],
    };
  }

  if (data.right_gaze_point_validity) {
    return {
      x: data.right_gaze_point_on_display_area[0],
      y: data.right_gaze_point_on_display_area[1],
    };
  }

  return null;
};

export const getGazePointCoordinates = (data: GazeData) => {
  const normalized = getNormalizedGazePoint(data);
  if (!normalized) {
    return { pointX: 0, pointY: 0 };
  }

  const [screenWidth, screenHeight] = getScreenResolution();
  const { viewportLeftOnScreen, viewportTopOnScreen } =
    getViewportOffsetOnScreen();

  // Tobii gives normalized points on the full display area [0,1].
  // Convert to absolute screen pixels first, then to viewport/client pixels.
  const absoluteScreenX = normalized.x * screenWidth;
  const absoluteScreenY = normalized.y * screenHeight;

  return clampToViewport(
    absoluteScreenX - viewportLeftOnScreen,
    absoluteScreenY - viewportTopOnScreen + gazeYOffsetPx
  );
};
// This is for batches of gaze data and makes the circle smoother.
export const getAverageGazePointCoordinates2 = (dataArray: GazeData[]) => {
  let totalX = 0;
  let totalY = 0;
  let count = 0;

  dataArray.forEach((data) => {
    const { pointX, pointY } = getGazePointCoordinates(data);
    if (!data.left_gaze_point_validity && !data.right_gaze_point_validity) return;
    totalX += pointX;
    totalY += pointY;
    count += 1;
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

const getDistanceFromPointToBox = (
  x: number,
  y: number,
  { left, top, right, bottom }: { left: number; top: number; right: number; bottom: number }
) => {
  const dx = Math.max(left - x, 0, x - right);
  const dy = Math.max(top - y, 0, y - bottom);
  return Math.hypot(dx, dy);
};

const getDistanceFromPointToBoxCenter = (
  x: number,
  y: number,
  { left, top, width, height }: { left: number; top: number; width: number; height: number }
) => {
  const centerX = left + width / 2;
  const centerY = top + height / 2;
  return Math.hypot(x - centerX, y - centerY);
};

type GazeMatchOptions = {
  gazeRadiusPx?: number;
  minHitRatio?: number;
};

export const validateEyeData2 = (
  eyeData: GazeData[],
  wordPositions: IScaledWordCoords[],
  baseGazePoints = 60,
  options?: GazeMatchOptions
) => {
  const additionalGazePointsPerLetter = 10;
  const gazeRadiusPx = Math.max(
    0,
    Math.min(100, Math.round(options?.gazeRadiusPx ?? 20))
  );
  const minHitRatio = Math.max(
    0,
    Math.min(1, options?.minHitRatio ?? 0.55)
  );
  let bestMatch:
    | {
        wordData: IScaledWordCoords;
        score: number;
      }
    | undefined;

  for (let wordData of wordPositions) {
    const { word, wordCoords } = wordData;
    const { left, top, width, height } = wordCoords;

    const gazePointsToConsider =
      baseGazePoints + (word.length - 1) * additionalGazePointsPerLetter;

    const relevantEyeData = eyeData.slice(
      -Math.min(gazePointsToConsider, eyeData.length)
    );
    if (!relevantEyeData.length) continue;

    let hitsInsideRadius = 0;
    let totalDistanceToBox = 0;
    let validPointsCount = 0;
    let gazeCenterX = 0;
    let gazeCenterY = 0;

    for (const rel of relevantEyeData) {
      if (!rel.left_gaze_point_validity && !rel.right_gaze_point_validity) {
        continue;
      }

      const { pointX, pointY } = getGazePointCoordinates(rel);
      const distanceToBox = getDistanceFromPointToBox(pointX, pointY, {
        left,
        top,
        right: left + width,
        bottom: top + height,
      });

      totalDistanceToBox += distanceToBox;
      gazeCenterX += pointX;
      gazeCenterY += pointY;
      validPointsCount += 1;

      if (distanceToBox <= gazeRadiusPx) {
        hitsInsideRadius += 1;
      }
    }

    if (!validPointsCount) continue;

    const hitRatio = hitsInsideRadius / validPointsCount;
    if (hitRatio < minHitRatio) continue;

    const avgDistanceToBox = totalDistanceToBox / validPointsCount;
    const avgGazeX = gazeCenterX / validPointsCount;
    const avgGazeY = gazeCenterY / validPointsCount;
    const distanceToWordCenter = getDistanceFromPointToBoxCenter(avgGazeX, avgGazeY, {
      left,
      top,
      width,
      height,
    });

    // Higher hit ratio is better, then prefer smaller edge/center distance.
    const score =
      (1 - hitRatio) * 100 + avgDistanceToBox * 0.7 + distanceToWordCenter * 0.3;

    if (!bestMatch || score < bestMatch.score) {
      bestMatch = { wordData, score };
    }
  }

  if (bestMatch) {
    return bestMatch.wordData;
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
