import TranslationPopup from "components/TranslationPopup";
import { Context } from "context/Context";
// import { useEyeTrackingData } from "context/EyeTrackingContext";
import { useWordPositions } from "hooks/useWordPositions";
import React, { useContext, useEffect, useRef, useState } from "react";
import {
  IContextProps,
  ID,
  IScaledWordCoords,
  IWordPositions,
} from "types/AppTypes";
import { validateEyeData2, validateHoldTranslation } from "utils/eyeTracking";
import { calculateScaledPositions } from "utils/functions";
import useEyeTrackingStore from "store/store";
import usePrevious from "hooks/usePrevious";
import { apiURL } from "utils/consts";

const wordPadding = 20;
const apiKey = "AIzaSyCgaeL8Nfo0U4ZgQZ9xDRGCOH27-dkj3Sg";
const TextBox = () => {
  // const { eyeData } = useEyeTrackingData();
  const { eyeData } = useEyeTrackingStore();
  const {
    pageMounted,
    scrollTop,
    currentPage,
    selectedDocID,
    shouldTranslate,
    setShouldTranslate,
    userSettingsUi,
    userInfo,
  } = useContext<IContextProps>(Context);
  const prevScrollTop = usePrevious(scrollTop);

  const { wordPositions } = useWordPositions();

  const [currentPageData, setCurrentPageData] = useState<{
    data: IWordPositions[];
    tokensAll?: any[];
    page: number;
    width?: number;
    height?: number;
  }>();

  const [currentWord, setCurrentWord] = useState<IScaledWordCoords>();
  const [wordsScreenPositions, setWordsScreenPositions] =
    useState<IScaledWordCoords[]>();
  const [translation, setTranslation] = useState<string>("");
  const [coolDown, setCoolDown] = useState<boolean>(false);
  const lastDetectionRunAtRef = useRef<number>(0);

  useEffect(() => {
    if (wordPositions && wordPositions.length) {
      setCurrentPageData(wordPositions[currentPage - 1]);
    }
  }, [currentPage, wordPositions]);

  useEffect(() => {
    if (pageMounted && currentPageData && currentPageData?.data.length) {
      const pageSize = {
        width: currentPageData.width,
        height: currentPageData.height,
      };
      const screenPositions = currentPageData.data.map((w) => {
        const { box, word } = w;
        const { xPrime, yPrime, wPrime, hPrime } = calculateScaledPositions(
          box,
          currentPage,
          pageSize
        );
        return {
          word,
          sourceBox: box,
          wordCoords: {
            left: xPrime,
            top: yPrime,
            width: wPrime,
            height: hPrime,
          },
        };
      });
      setWordsScreenPositions(screenPositions);
      return;
    }

    setWordsScreenPositions([]);
  }, [currentPage, currentPageData, pageMounted, scrollTop]);

  useEffect(() => {
    if (coolDown || userSettingsUi.hoverTranslateDebug) return;
    if (shouldTranslate) return;

    const now = performance.now();
    if (now - lastDetectionRunAtRef.current < 45) return;
    lastDetectionRunAtRef.current = now;

    const baseGazeSamples = userSettingsUi.baseGazeSamples ?? 60;
    if (
      pageMounted &&
      wordsScreenPositions &&
      wordsScreenPositions.length &&
      eyeData.length >= baseGazeSamples
    ) {
      const detectedWord = validateEyeData2(
        eyeData,
        wordsScreenPositions,
        baseGazeSamples,
        {
          gazeRadiusPx: userSettingsUi.gazeHitRadiusPx ?? 20,
        }
      );

      if (detectedWord.word) {
        setCurrentWord(detectedWord);
        setShouldTranslate?.(true);
      }
    }
  }, [
    pageMounted,
    eyeData,
    currentPageData,
    wordsScreenPositions,
    setShouldTranslate,
    shouldTranslate,
    coolDown,
    userSettingsUi.hoverTranslateDebug,
    userSettingsUi.baseGazeSamples,
    userSettingsUi.gazeHitRadiusPx,
  ]);

  useEffect(() => {
    if (!userSettingsUi.hoverTranslateDebug) return;
    const handleHover = (event: globalThis.MouseEvent) => {
      if (!wordsScreenPositions || !wordsScreenPositions.length) return;
      const hoveredWord = wordsScreenPositions.find((position) => {
        const { left, top, width, height } = position.wordCoords;
        return (
          event.clientX >= left &&
          event.clientX <= left + width &&
          event.clientY >= top &&
          event.clientY <= top + height
        );
      });

      if (hoveredWord) {
        setCurrentWord(hoveredWord);
        setShouldTranslate?.(true);
      } else {
        setCurrentWord(undefined);
        setShouldTranslate?.(false);
      }
    };

    window.addEventListener("mousemove", handleHover);
    return () => {
      window.removeEventListener("mousemove", handleHover);
    };
  }, [setShouldTranslate, userSettingsUi.hoverTranslateDebug, wordsScreenPositions]);

  useEffect(() => {
    const getSentenceFromFocus = async (
      docID: ID,
      userID: string,
      page: number,
      focusBox?: number[]
    ): Promise<string> => {
      if (!focusBox || !docID || !userID) return "";
      try {
        const response = await fetch(`${apiURL}/sentence-from-focus`, {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
            Accept: "application/json",
          },
          body: JSON.stringify({
            docID,
            userID,
            page,
            focusBox,
          }),
        });
        if (!response.ok) return "";
        const data = await response.json();
        return data?.sentence || "";
      } catch (error) {
        console.error("Error fetching sentence:", error);
        return "";
      }
    };

    const fetchTranslation = async () => {
      setTranslation("");
      if (currentWord && shouldTranslate) {
        const isSentenceMode = userSettingsUi.translationMode === "sentence";
        const sourceWord = currentWord.word;
        let sourceSentence = "";
        if (isSentenceMode) {
          sourceSentence = await getSentenceFromFocus(
            selectedDocID,
            userInfo.userID,
            currentPage,
            currentWord.sourceBox
          );
        }
        const textToTranslate =
          isSentenceMode && sourceSentence ? sourceSentence : sourceWord;
        if (!textToTranslate) return;

        try {
          const targetLanguage = "el";
          const response = await fetch(
            `https://translation.googleapis.com/language/translate/v2?key=${apiKey}&source=en&target=${targetLanguage}&q=${encodeURIComponent(
              textToTranslate
            )}`,

            {
              method: "GET",
              headers: {
                "Content-Type": "application/json",
                Accept: "application/json",
              },
            }
          );

          if (response.ok) {
            const data = await response.json();
            const translatedText = data?.data?.translations?.[0]?.translatedText;
            setTranslation(translatedText || "");
          } else {
            const errorData = await response.json();
            console.error(
              "Failed to fetch translation:",
              errorData.error.message
            );
          }
        } catch (error) {
          console.error("Error:", error);
        }
      }
    };
    fetchTranslation();
  }, [
    currentWord,
    shouldTranslate,
    selectedDocID,
    userInfo.userID,
    currentPage,
    userSettingsUi.translationMode,
  ]);

  useEffect(() => {
    if (scrollTop && prevScrollTop !== scrollTop) {
      setShouldTranslate?.(false);
      setCoolDown(false);
    }
  }, [prevScrollTop, scrollTop, setShouldTranslate]);

  // THIS IS FOR MOCKING THE TRANSLATION POPUP
  // useEffect(() => {
  //   const wordForTransl = wordsScreenPositions?.find(
  //     (w) => w.word === testWord
  //   );
  //   setShouldTranslate?.(true);
  //   setCurrentWord(wordForTransl);
  // }, [setShouldTranslate, wordsScreenPositions]);

  useEffect(() => {
    const translationElement = document.getElementById("translation");
    if (translationElement) {
      const dimensions = translationElement.getBoundingClientRect();
      const shouldHoldTranslation = validateHoldTranslation(
        dimensions,
        eyeData.slice(-400)
      );
      if (shouldHoldTranslation) {
        setCoolDown(true);
      } else {
        setCoolDown(false);
      }
    }
  }, [eyeData]);

  return (
    <>
      {/* {wordsScreenPositions?.map((pos) => (
        <div
          style={{
            position: "absolute",
            left: pos?.wordCoords.left || 0,
            top: pos?.wordCoords.top || 0,
            width: pos?.wordCoords.width || 0,
            height: pos?.wordCoords.height || 0,
            border: "2px solid red",
            zIndex: 40,
          }}
        ></div>
      ))} */}
      <div
        style={{
          position: "absolute",
          left: currentWord?.wordCoords.left || 0,
          top: currentWord?.wordCoords.top || 0,
          width: currentWord?.wordCoords.width || 0,
          height: currentWord?.wordCoords.height || 0,
          zIndex: 40,
        }}
      >
        <div className='relative'>
          {shouldTranslate && (
            <TranslationPopup
              translation={translation}
              offset={(currentWord?.wordCoords.width || 0) + wordPadding}
              setShouldTranslate={setShouldTranslate}
            />
          )}
        </div>
      </div>
    </>
  );
};

export default TextBox;
