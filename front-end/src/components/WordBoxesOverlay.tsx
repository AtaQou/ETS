import React, { useContext, useMemo } from "react";
import { Context } from "context/Context";
import { useWordPositions } from "hooks/useWordPositions";
import useCurrentPageData from "hooks/useCurrentPageData";
import { calculateScaledPositions } from "utils/functions";

const DEBUG_SHOW_BOXES = false;

const WordBoxesOverlay: React.FC = () => {
    const { currentPage, scrollTop, userSettingsApi, userSettingsUi, file } =
        useContext(Context);
    const { zoom } = userSettingsApi;
    const { wordPositions } = useWordPositions();

    const showBoxes = userSettingsUi.showBoxes ?? DEBUG_SHOW_BOXES;

    const currentPageData = useCurrentPageData(wordPositions, currentPage);

    const boxes = useMemo(() => {
        if (!currentPageData || !currentPageData.data) return [];

        return currentPageData.data.map((item: any, index: number) => {
            const { xPrime, yPrime, wPrime, hPrime } = calculateScaledPositions(
                item.box,
                scrollTop,
                currentPage,
                1 // ΔΕΝ ξανα-σκέιλάρουμε με zoom στο front-end
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

    if (!showBoxes || !file || file.size === 0 || boxes.length === 0) {
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
