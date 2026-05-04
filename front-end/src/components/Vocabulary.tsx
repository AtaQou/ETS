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
  docName?: string;
}

interface IExperimentUser {
  userID: number;
  username: string;
  sessionCount: number;
  translationCount: number;
}

interface IVocabularyResponse {
  word: IVocabularyEntry[];
  sentence: IVocabularyEntry[];
  documents: string[];
  effectiveUserID?: number;
}

const Vocabulary: FC = () => {
  const { userSettingsApi, userInfo } = useContext<IContextProps>(Context);
  const isDarkTheme = userSettingsApi.theme === "dark";
  const [selectedBranch, setSelectedBranch] = useState<TranslationBranch>("word");
  const [selectedDocName, setSelectedDocName] = useState("");
  const [users, setUsers] = useState<IExperimentUser[]>([]);
  const [selectedUserID, setSelectedUserID] = useState<string>("");
  const [vocabulary, setVocabulary] = useState<IVocabularyResponse>({
    word: [],
    sentence: [],
    documents: [],
  });
  const [loading, setLoading] = useState(false);
  const [loadingUsers, setLoadingUsers] = useState(false);
  const [errorMessage, setErrorMessage] = useState("");

  useEffect(() => {
    if (!userInfo.userID) {
      setUsers([]);
      setSelectedUserID("");
      return;
    }

    setLoadingUsers(true);
    axios
      .get(`${apiURL}/experiment/users`, {
        params: { requesterUserID: userInfo.userID },
      })
      .then((response) => {
        const fetchedUsers: IExperimentUser[] = response.data || [];
        setUsers(fetchedUsers);
        const currentUserId = String(userInfo.userID || "");
        if (fetchedUsers.some((user) => String(user.userID) === currentUserId)) {
          setSelectedUserID(currentUserId);
        } else if (fetchedUsers.length) {
          setSelectedUserID(String(fetchedUsers[0].userID));
        } else {
          setSelectedUserID("");
        }
      })
      .catch(() => {
        setErrorMessage("Failed to load users.");
      })
      .finally(() => {
        setLoadingUsers(false);
      });
  }, [userInfo.userID]);

  useEffect(() => {
    if (!userInfo.userID || !selectedUserID) {
      setVocabulary({ word: [], sentence: [], documents: [] });
      return;
    }

    setLoading(true);
    setErrorMessage("");
    axios
      .get(`${apiURL}/vocabulary`, {
        params: {
          userID: selectedUserID,
          requesterUserID: userInfo.userID,
          docName: selectedDocName || undefined,
        },
      })
      .then((response) => {
        const data = response.data || {};
        setVocabulary({
          word: Array.isArray(data.word) ? data.word : [],
          sentence: Array.isArray(data.sentence) ? data.sentence : [],
          documents: Array.isArray(data.documents) ? data.documents : [],
          effectiveUserID: data.effectiveUserID,
        });
      })
      .catch(() => {
        setErrorMessage("Failed to load vocabulary.");
      })
      .finally(() => {
        setLoading(false);
      });
  }, [selectedDocName, selectedUserID, userInfo.userID]);

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
      <div className='mb-4 grid grid-cols-2 gap-4'>
        <div>
          <label className='block mb-1 text-sm' style={{ color: getFontColorSecondary(isDarkTheme) }}>
            User
          </label>
          <select
            value={selectedUserID}
            onChange={(e) => setSelectedUserID(e.target.value)}
            className='w-full text-sm p-2 rounded border border-gray-300 text-gray-900'
            disabled={loadingUsers || users.length <= 1}
          >
            {!users.length && <option value=''>No users</option>}
            {users.map((user) => (
              <option key={user.userID} value={String(user.userID)}>
                {user.userID} - {user.username}
              </option>
            ))}
          </select>
        </div>
        <div>
          <label className='block mb-1 text-sm' style={{ color: getFontColorSecondary(isDarkTheme) }}>
            PDF File
          </label>
          <select
            value={selectedDocName}
            onChange={(e) => setSelectedDocName(e.target.value)}
            className='w-full text-sm p-2 rounded border border-gray-300 text-gray-900'
            disabled={loading || vocabulary.documents.length === 0}
          >
            <option value=''>All PDFs</option>
            {vocabulary.documents.map((docName) => (
              <option key={docName} value={docName}>
                {docName}
              </option>
            ))}
          </select>
        </div>
      </div>

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
              <div className='text-xs text-gray-500 mt-1'>
                PDF: {entry.docName || "-"}
              </div>
            </div>
          ))}
        </div>
      )}
      <div className='mt-3 text-xs text-gray-500' style={{ color: getFontColorSecondary(isDarkTheme) }}>
        Showing entries for user ID {vocabulary.effectiveUserID || selectedUserID || "-"}.
      </div>
    </div>
  );
};

export default Vocabulary;
