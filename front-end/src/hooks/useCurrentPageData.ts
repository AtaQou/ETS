import { useMemo } from "react";
import { IWordPositions } from "types/AppTypes";

const useCurrentPageData = (
  wordPositions: {
    data: IWordPositions[];
    page: number;
  }[],
  currentPage: number
) => {
  return useMemo(() => {
    return wordPositions && wordPositions.length
      ? wordPositions[currentPage - 1]
      : null;
  }, [wordPositions, currentPage]);
};

export default useCurrentPageData;
