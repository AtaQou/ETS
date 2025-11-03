import TranslationPopup from "components/TranslationPopup";
import { Context } from "context/Context";
// import { useEyeTrackingData } from "context/EyeTrackingContext";
import { useWordPositions } from "hooks/useWordPositions";
import React, { useContext, useEffect, useMemo, useRef, useState } from "react";
import {
  IContextProps,
  IScaledWordCoords,
  IWordPositions,
} from "types/AppTypes";
import { validateEyeData2, validateHoldTranslation } from "utils/eyeTracking";
import { calculateScaledPositions } from "utils/functions";
import useEyeTrackingStore from "store/store";
import useEyeTracking from "../../hooks/useEyeTracking";
import usePrevious from "hooks/usePrevious";

const wordPadding = 20;
const apiKey = "AIzaSyAX5ypZhaH0PNJfya3tSGVfQLN49_o3u3U";
const testWord = "pathological";

const TextBox = () => {
  // const { eyeData } = useEyeTrackingData();
  const { eyeData } = useEyeTrackingStore();
  const {
    pageMounted,
    scrollTop,
    currentPage,
    userSettingsApi,
    shouldTranslate,
    setShouldTranslate,
  } = useContext<IContextProps>(Context);
  const prevScrollTop = usePrevious(scrollTop);

  useEyeTracking();
  // useMockData();

  const { wordPositions } = useWordPositions();

  const [currentPageData, setCurrentPageData] = useState<{
    data: IWordPositions[];
    page: number;
  }>();

  const [currentWord, setCurrentWord] = useState<IScaledWordCoords>();
  const [wordsScreenPositions, setWordsScreenPositions] =
    useState<IScaledWordCoords[]>();
  const observerRef = useRef<MutationObserver | null>(null);
  const [translation, setTranslation] = useState<string>("");
  const [coolDown, setCoolDown] = useState<boolean>(false);

  useEffect(() => {
    if (wordPositions && wordPositions.length) {
      setCurrentPageData(wordPositions[currentPage - 1]);
    }
  }, [currentPage, wordPositions]);

  const finalPositions = useMemo(() => {
    if (pageMounted && currentPageData && currentPageData?.data.length) {
      const screenPositions = currentPageData.data.map((w) => {
        const { box, word } = w;
        const { xPrime, yPrime, wPrime, hPrime } = calculateScaledPositions(
          box,
          scrollTop,
          currentPage,
          userSettingsApi.zoom
        );
        return {
          word,
          wordCoords: {
            left: xPrime,
            top: yPrime,
            width: wPrime,
            height: hPrime,
          },
        };
      });
      return screenPositions;
    }
    return [];
  }, [
    currentPage,
    currentPageData,
    pageMounted,
    scrollTop,
    userSettingsApi.zoom,
  ]);

  useEffect(() => {
    if (finalPositions) setWordsScreenPositions(finalPositions);
  }, [finalPositions]);

  useEffect(() => {
    if (coolDown) return;
    if (
      pageMounted &&
      wordsScreenPositions &&
      wordsScreenPositions.length &&
      eyeData.length > 300
    ) {
      const detectedWord = validateEyeData2(eyeData, wordsScreenPositions);
      const currentTime = new Date();
      let milli = currentTime.getMilliseconds();
      let f_milli = String(milli).padStart(3, "0");
      console.log(
        "word detected",
        detectedWord.word,

        `${currentTime.getHours()}:${currentTime.getMinutes()}:${currentTime.getSeconds()}.${f_milli}`
      );
      console.log({ detectedWord: detectedWord.word });

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
  ]);

  useEffect(() => {
    const fetchTranslation = async () => {
      setTranslation("");
      if (currentWord && shouldTranslate) {
        try {
          const response = await fetch(
            `https://translation.googleapis.com/language/translate/v2?key=${apiKey}&source=en&target=el&q=${currentWord.word}`,

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
            setTranslation(data.data.translations[0].translatedText);
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
  }, [currentWord, shouldTranslate]);

  useEffect(() => {
    if (shouldTranslate) {
      const currentTime = new Date();
      let milli = currentTime.getMilliseconds();
      let f_milli = String(milli).padStart(3, "0");
      console.log(
        "translation pops",
        `${currentTime.getHours()}:${currentTime.getMinutes()}:${currentTime.getSeconds()}.${f_milli}`
      );
    }
  }, [setShouldTranslate, shouldTranslate]);

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

  console.log({ coolDown, shouldTranslate });

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
