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

const createGazePointMapper = () => {
  const [screenWidth, screenHeight] = getScreenResolution();
  const { viewportLeftOnScreen, viewportTopOnScreen } =
    getViewportOffsetOnScreen();

  return (normalizedX: number, normalizedY: number) => {
    const absoluteScreenX = normalizedX * screenWidth;
    const absoluteScreenY = normalizedY * screenHeight;
    return clampToViewport(
      absoluteScreenX - viewportLeftOnScreen,
      absoluteScreenY - viewportTopOnScreen + gazeYOffsetPx
    );
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
  const mapToViewport = createGazePointMapper();
  return mapToViewport(normalized.x, normalized.y);
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
  const maxWordLength = wordPositions.reduce(
    (maxLen, wp) => Math.max(maxLen, wp.word?.length || 0),
    0
  );
  const gazePointsToConsider =
    baseGazePoints + Math.max(0, maxWordLength - 1) * additionalGazePointsPerLetter;
  const relevantEyeData = eyeData.slice(
    -Math.min(gazePointsToConsider, eyeData.length)
  );
  if (!relevantEyeData.length) {
    return { word: "", wordCoords: { left: 0, top: 0, width: 0, height: 0 } };
  }

  const mapToViewport = createGazePointMapper();
  const gazePoints: { x: number; y: number }[] = [];
  let avgGazeX = 0;
  let avgGazeY = 0;

  for (const rel of relevantEyeData) {
    const normalized = getNormalizedGazePoint(rel);
    if (!normalized) continue;
    const { pointX, pointY } = mapToViewport(normalized.x, normalized.y);
    gazePoints.push({ x: pointX, y: pointY });
    avgGazeX += pointX;
    avgGazeY += pointY;
  }

  if (!gazePoints.length) {
    return { word: "", wordCoords: { left: 0, top: 0, width: 0, height: 0 } };
  }

  avgGazeX /= gazePoints.length;
  avgGazeY /= gazePoints.length;

  const candidateLimit = 10;
  const coarseCandidates = wordPositions
    .map((wordData) => {
      const { left, top, width, height } = wordData.wordCoords;
      const edgeDistance = getDistanceFromPointToBox(avgGazeX, avgGazeY, {
        left,
        top,
        right: left + width,
        bottom: top + height,
      });
      return { wordData, edgeDistance };
    })
    .sort((a, b) => a.edgeDistance - b.edgeDistance)
    .slice(0, candidateLimit);

  for (const candidate of coarseCandidates) {
    const wordData = candidate.wordData;
    const { left, top, width, height } = wordData.wordCoords;

    let hitsInsideRadius = 0;
    let totalDistanceToBox = 0;

    for (const point of gazePoints) {
      const distanceToBox = getDistanceFromPointToBox(point.x, point.y, {
        left,
        top,
        right: left + width,
        bottom: top + height,
      });
      totalDistanceToBox += distanceToBox;
      if (distanceToBox <= gazeRadiusPx) {
        hitsInsideRadius += 1;
      }
    }

    const hitRatio = hitsInsideRadius / gazePoints.length;
    if (hitRatio < minHitRatio) continue;

    const avgDistanceToBox = totalDistanceToBox / gazePoints.length;
    const distanceToWordCenter = getDistanceFromPointToBoxCenter(avgGazeX, avgGazeY, {
      left,
      top,
      width,
      height,
    });

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
