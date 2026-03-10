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
import useEyeTracking from "../../hooks/useEyeTracking";
import usePrevious from "hooks/usePrevious";
import { apiURL } from "utils/consts";

const wordPadding = 20;
const apiKey = "AIzaSyCgaeL8Nfo0U4ZgQZ9xDRGCOH27-dkj3Sg";

type FocusSentenceResponse = {
  sentence: string;
  sentenceWithMarker?: string;
  matchedToken: string;
};

const escapeRegExp = (value: string) =>
  value.replace(/[.*+?^${}()|[\]\\]/g, "\\$&");

const createUniqueMarkers = () => {
  const markerId = `${Date.now()}${Math.random().toString(36).slice(2, 8)}`.toUpperCase();
  return {
    markerId,
    startMarker: `⟦${markerId}A⟧`,
    endMarker: `⟦${markerId}B⟧`,
  };
};

const injectMarkersInSentence = (
  sentence: string,
  startMarker: string,
  endMarker: string,
  primaryTarget: string,
  fallbackTarget: string
) => {
  const tryWrap = (target: string, useWordBoundary = false) => {
    const cleanedTarget = (target || "").trim();
    if (!cleanedTarget) return "";
    const escaped = escapeRegExp(cleanedTarget);
    const pattern = useWordBoundary ? `\\b${escaped}\\b` : escaped;
    const regex = new RegExp(pattern, "i");
    if (!regex.test(sentence)) return "";
    return sentence.replace(regex, `${startMarker} $& ${endMarker}`);
  };

  return (
    tryWrap(primaryTarget, true) ||
    tryWrap(primaryTarget) ||
    tryWrap(fallbackTarget, true) ||
    tryWrap(fallbackTarget) ||
    sentence
  );
};

const extractBetweenMarkers = (
  translatedText: string,
  startMarker: string,
  endMarker: string
) => {
  const startIndex = translatedText.indexOf(startMarker);
  const endIndex = translatedText.indexOf(endMarker);
  if (startIndex === -1 || endIndex === -1 || endIndex <= startIndex) {
    return "";
  }

  return translatedText
    .slice(startIndex + startMarker.length, endIndex)
    .replace(/\s+/g, " ")
    .trim();
};

const removeMarkers = (
  translatedText: string,
  startMarker: string,
  endMarker: string
) =>
  translatedText
    .replace(new RegExp(escapeRegExp(startMarker), "g"), "")
    .replace(new RegExp(escapeRegExp(endMarker), "g"), "")
    .replace(/\s+/g, " ")
    .trim();

const removeMarkerArtifacts = (translatedText: string, markerId: string) => {
  const markerRegex = new RegExp(
    `⟦\\s*${escapeRegExp(markerId)}\\s*[AB]\\s*⟧`,
    "gi"
  );

  return translatedText.replace(markerRegex, "").replace(/\s+/g, " ").trim();
};

const sanitizeWordOnlyTranslation = (value: string) => {
  const normalized = (value || "").replace(/\s+/g, " ").trim();
  if (!normalized) return "";

  // Avoid trailing sentence punctuation in word-only mode output.
  const withoutTrailingPunctuation = normalized
    .replace(/[.,!?;:]+$/g, "")
    .trim();

  return withoutTrailingPunctuation || "";
};

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

  useEyeTracking();
  // useMockData();

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
  const translationRequestIdRef = useRef(0);

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
        baseGazeSamples
      );
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
    userSettingsUi.hoverTranslateDebug,
    userSettingsUi.baseGazeSamples,
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
      focusBox?: number[],
      startMarker?: string,
      endMarker?: string
    ): Promise<FocusSentenceResponse> => {
      if (!focusBox || !docID || !userID) {
        return { sentence: "", sentenceWithMarker: "", matchedToken: "" };
      }
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
            startMarker,
            endMarker,
          }),
        });
        if (!response.ok) return { sentence: "", sentenceWithMarker: "", matchedToken: "" };
        const data = await response.json();
        return {
          sentence: data?.sentence || "",
          sentenceWithMarker: data?.sentenceWithMarker || "",
          matchedToken: data?.matchedToken || "",
        };
      } catch (error) {
        console.error("Error fetching sentence:", error);
        return { sentence: "", sentenceWithMarker: "", matchedToken: "" };
      }
    };

    const translateText = async (text: string) => {
      if (!text) return "";
      const targetLanguage = "el";
      try {
        const response = await fetch(
          `https://translation.googleapis.com/language/translate/v2?key=${apiKey}&source=en&target=${targetLanguage}&q=${encodeURIComponent(
            text
          )}`,
          {
            method: "GET",
            headers: {
              "Content-Type": "application/json",
              Accept: "application/json",
            },
          }
        );

        if (!response.ok) {
          const errorData = await response.json().catch(() => ({}));
          console.error(
            "Failed to fetch translation:",
            errorData?.error?.message || response.statusText
          );
          return "";
        }
        const data = await response.json();
        return data?.data?.translations?.[0]?.translatedText || "";
      } catch (error) {
        console.error("Error:", error);
        return "";
      }
    };

    const fetchTranslation = async () => {
      setTranslation("");
      if (currentWord && shouldTranslate) {
        translationRequestIdRef.current += 1;
        const requestId = translationRequestIdRef.current;
        const setTranslationIfLatest = (value: string) => {
          if (requestId === translationRequestIdRef.current) {
            setTranslation(value);
          }
        };

        const isSentenceMode = userSettingsUi.translationMode === "sentence";
        const sourceWord = currentWord.word;
        const { markerId, startMarker, endMarker } = createUniqueMarkers();
        const {
          sentence: sourceSentence,
          sentenceWithMarker,
          matchedToken,
        } =
          await getSentenceFromFocus(
            selectedDocID,
            userInfo.userID,
            currentPage,
            currentWord.sourceBox,
            isSentenceMode ? undefined : startMarker,
            isSentenceMode ? undefined : endMarker
          );

        // Keep UX useful even when sentence detection fails.
        if (!sourceSentence) {
          const fallbackWordTranslation = await translateText(sourceWord);
          setTranslationIfLatest(
            sanitizeWordOnlyTranslation(fallbackWordTranslation) || sourceWord || ""
          );
          return;
        }

        if (isSentenceMode) {
          const translatedSentence = await translateText(sourceSentence);
          setTranslationIfLatest(translatedSentence || sourceSentence || "");
          return;
        }

        const sentenceWithMarkers =
          sentenceWithMarker ||
          injectMarkersInSentence(
            sourceSentence,
            startMarker,
            endMarker,
            matchedToken,
            sourceWord
          );
        const markersWereInjected =
          sentenceWithMarkers.includes(startMarker) &&
          sentenceWithMarkers.includes(endMarker);

        const translatedSentence = await translateText(sentenceWithMarkers);
        if (!translatedSentence) {
          const fallbackWordTranslation = await translateText(sourceWord);
          setTranslationIfLatest(
            sanitizeWordOnlyTranslation(fallbackWordTranslation) || sourceWord || ""
          );
          return;
        }

        if (markersWereInjected) {
          const extractedWordTranslation = extractBetweenMarkers(
            translatedSentence,
            startMarker,
            endMarker
          );
          if (extractedWordTranslation) {
            setTranslationIfLatest(
              sanitizeWordOnlyTranslation(extractedWordTranslation) ||
                sourceWord ||
                ""
            );
            return;
          }
        }

        const cleanedSentenceFallback = removeMarkers(
          translatedSentence,
          startMarker,
          endMarker
        );
        const cleanedSentenceWithoutArtifacts = removeMarkerArtifacts(
          cleanedSentenceFallback,
          markerId
        );
        const fallbackWordTranslation = await translateText(sourceWord);

        // If markers were injected but extraction failed, prefer a clean word fallback.
        if (markersWereInjected && fallbackWordTranslation) {
          setTranslationIfLatest(
            sanitizeWordOnlyTranslation(fallbackWordTranslation) || sourceWord || ""
          );
          return;
        }

        setTranslationIfLatest(
          sanitizeWordOnlyTranslation(fallbackWordTranslation) ||
            cleanedSentenceWithoutArtifacts ||
            sourceWord ||
            ""
        );
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
