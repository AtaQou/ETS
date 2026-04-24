import React, { useContext, FC, useEffect, useMemo, useState } from "react";
import axios from "axios";
import { Context } from "../context/Context";
import { getFontColorSecondary } from "../utils/functions";
import { IContextProps } from "types/AppTypes";
import { apiURL } from "utils/consts";

type TranslationBranch = "word" | "sentence";

interface IVocabularyEntry {
  entryID: number;
  sourceText: string;
  translatedText: string;
  translationMode: TranslationBranch;
  firstTranslatedAt: string;
}

interface IVocabularyResponse {
  word: IVocabularyEntry[];
  sentence: IVocabularyEntry[];
}

const Vocabulary: FC = () => {
  const { userSettingsApi, userInfo } = useContext<IContextProps>(Context);
  const isDarkTheme = userSettingsApi.theme === "dark";
  const [selectedBranch, setSelectedBranch] = useState<TranslationBranch>("word");
  const [vocabulary, setVocabulary] = useState<IVocabularyResponse>({
    word: [],
    sentence: [],
  });
  const [loading, setLoading] = useState(false);
  const [errorMessage, setErrorMessage] = useState("");

  useEffect(() => {
    if (!userInfo.userID) {
      setVocabulary({ word: [], sentence: [] });
      return;
    }

    setLoading(true);
    setErrorMessage("");
    axios
      .get(`${apiURL}/vocabulary`, {
        params: { userID: userInfo.userID },
      })
      .then((response) => {
        const data = response.data || {};
        setVocabulary({
          word: Array.isArray(data.word) ? data.word : [],
          sentence: Array.isArray(data.sentence) ? data.sentence : [],
        });
      })
      .catch(() => {
        setErrorMessage("Failed to load vocabulary.");
      })
      .finally(() => {
        setLoading(false);
      });
  }, [userInfo.userID]);

  const activeEntries = useMemo(
    () => vocabulary[selectedBranch] || [],
    [selectedBranch, vocabulary]
  );

  const formatDateTime = (value: string) => {
    const date = new Date(value);
    if (Number.isNaN(date.getTime())) {
      return value;
    }
    return date.toLocaleString();
  };

  return (
    <div className='flex flex-col m-2 p-4'>
      <h1
        className='py-1 mb-4 text-xl font-bold text-gray-900 border-b border-gray-300'
        style={{ color: getFontColorSecondary(isDarkTheme) }}
      >
        Vocabulary
      </h1>
      <div className='mb-4 flex gap-2'>
        <button
          type='button'
          onClick={() => setSelectedBranch("word")}
          className='px-3 py-1 border rounded text-sm'
          style={{
            color: getFontColorSecondary(isDarkTheme),
            backgroundColor: selectedBranch === "word" ? "rgba(59,130,246,0.15)" : "transparent",
            borderColor: selectedBranch === "word" ? "rgb(59 130 246)" : "rgb(156 163 175)",
          }}
        >
          Words ({vocabulary.word.length})
        </button>
        <button
          type='button'
          onClick={() => setSelectedBranch("sentence")}
          className='px-3 py-1 border rounded text-sm'
          style={{
            color: getFontColorSecondary(isDarkTheme),
            backgroundColor: selectedBranch === "sentence" ? "rgba(59,130,246,0.15)" : "transparent",
            borderColor: selectedBranch === "sentence" ? "rgb(59 130 246)" : "rgb(156 163 175)",
          }}
        >
          Sentences ({vocabulary.sentence.length})
        </button>
      </div>
      {loading && (
        <div className='text-sm text-gray-500' style={{ color: getFontColorSecondary(isDarkTheme) }}>
          Loading vocabulary...
        </div>
      )}
      {!!errorMessage && (
        <div className='text-sm text-red-500 mb-2'>{errorMessage}</div>
      )}
      {!loading && !errorMessage && activeEntries.length === 0 && (
        <div className='text-sm text-gray-600' style={{ color: getFontColorSecondary(isDarkTheme) }}>
          No saved {selectedBranch === "word" ? "words" : "sentences"} yet.
        </div>
      )}
      {!loading && !errorMessage && activeEntries.length > 0 && (
        <div className='flex flex-col gap-2'>
          {activeEntries.map((entry) => (
            <div key={entry.entryID} className='border rounded p-3 text-sm'>
              <div className='font-semibold break-words'>{entry.sourceText}</div>
              <div className='break-words mt-1'>{entry.translatedText}</div>
              <div className='text-xs text-gray-500 mt-2'>
                First translated: {formatDateTime(entry.firstTranslatedAt)}
              </div>
            </div>
          ))}
        </div>
      )}
      <div className='mt-3 text-xs text-gray-500' style={{ color: getFontColorSecondary(isDarkTheme) }}>
        Showing entries for user ID {userInfo.userID || "-"}.
      </div>
    </div>
  );
};

export default Vocabulary;
