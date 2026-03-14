import React, { useContext, useEffect, useState } from "react";
import { Context } from "context/Context";
import { useWordPositions } from "hooks/useWordPositions";
import useCurrentPageData from "hooks/useCurrentPageData";
import { calculateScaledPositions } from "utils/functions";

const DEBUG_SHOW_BOXES = false;

const WordBoxesOverlay: React.FC = () => {
    const { currentPage, userSettingsUi, file, scrollTop, scrollLeft } = useContext(Context);
    const { wordPositions } = useWordPositions();

    const showBoxes = userSettingsUi.showBoxes ?? DEBUG_SHOW_BOXES;

    const currentPageData = useCurrentPageData(wordPositions, currentPage);

    const [boxes, setBoxes] = useState<
        { id: string; word: string; x: number; y: number; w: number; h: number }[]
    >([]);

    useEffect(() => {
        if (!currentPageData || !currentPageData.data) {
            setBoxes([]);
            return;
        }

        const pageSize = {
            width: currentPageData.width,
            height: currentPageData.height,
        };

        // Use the same scaled coordinates that feed translation/eye-tracking so the
        // debug overlay reflects the exact bounding boxes the app consumes.
        const mappedBoxes = currentPageData.data.map((item: any, index: number) => {
            const { xPrime, yPrime, wPrime, hPrime } = calculateScaledPositions(
                item.box,
                currentPage,
                pageSize
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

        setBoxes(mappedBoxes);
    }, [currentPageData, currentPage, scrollLeft, scrollTop]);

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
