import React, { useContext, useMemo } from "react";
import { Context } from "context/Context";
import { useWordPositions } from "hooks/useWordPositions";
import useCurrentPageData from "hooks/useCurrentPageData";
import { calculateScaledPositions } from "utils/functions";

const DEBUG_SHOW_BOXES = true;

const WordBoxesOverlay: React.FC = () => {
    const { currentPage, scrollTop, userSettingsApi, file } = useContext(Context);
    const { zoom } = userSettingsApi;
    const { wordPositions } = useWordPositions();

    const currentPageData = useCurrentPageData(wordPositions, currentPage);

    const boxes = useMemo(() => {
        if (!currentPageData || !currentPageData.data) return [];

        return currentPageData.data.map((item: any, index: number) => {
            //  ΠΡΙΝ: περνούσαμε το zoom που έχει ήδη χρησιμοποιηθεί στο back-end
            // const { xPrime, yPrime, wPrime, hPrime } = calculateScaledPositions(
            //   item.box,
            //   scrollTop,
            //   currentPage,
            //   zoom
            // );

            // ✅ ΤΩΡΑ: δεν κάνουμε άλλο scale με zoom στο front-end
            const { xPrime, yPrime, wPrime, hPrime } = calculateScaledPositions(
                item.box,
                scrollTop,
                currentPage,
                1 // χρησιμοποιούμε 1.0 για να μην ξανα-σκέιλάρουμε τα boxes
            );

            return {
                id: `${currentPage}-${index}`,
                word: item.word,
                x: xPrime,
                y: yPrime,
                w: wPrime,
                h: hPrime,
            };
        });
    }, [currentPageData, scrollTop, currentPage, zoom]);

    if (!DEBUG_SHOW_BOXES || !file || file.size === 0 || boxes.length === 0) {
        return null;
    }

    return (
        <div
            style={{
                position: "fixed",
                inset: 0,
                pointerEvents: "none",
                zIndex: 50,
            }}
        >
            {boxes.map((box) => (
                <div
                    key={box.id}
                    title={box.word}
                    style={{
                        position: "absolute",
                        left: `${box.x}px`,
                        top: `${box.y}px`,
                        width: `${box.w}px`,
                        height: `${box.h}px`,
                        border: "1px solid red",
                        boxSizing: "border-box",
                        backgroundColor: "rgba(255, 0, 0, 0.15)",
                        pointerEvents: "none",
                    }}
                />
            ))}
        </div>
    );
};

export default WordBoxesOverlay;
