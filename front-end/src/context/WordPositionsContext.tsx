import React, {
  createContext,
  useContext,
  useReducer,
  ReactNode,
  useEffect,
  useMemo,
} from "react";
import {
  IContextProps,
  IScaledWordCoords,
  IWordPositions,
  IWordPositionsAction,
  IWordPositionsState,
} from "types/AppTypes";
import { Context } from "./Context";
import usePrevious from "hooks/usePrevious";
import { apiURL } from "utils/consts";
import axios from "axios";

interface WordPositionsProviderProps {
  children: ReactNode;
}

const initialWordPositionsState: IWordPositionsState = {
  wordsLoading: false,
  wordPositions: [],
  wordsScreenPositions: [],
};

const wordPositionsReducer = (
  state: IWordPositionsState,
  action: IWordPositionsAction
): IWordPositionsState => {
  switch (action.type) {
    case "SET_WORD_LOADING":
      return {
        ...state,
        wordsLoading: action.payload,
      };
    case "SET_WORD_POSITIONS":
      return {
        ...state,
        wordPositions: action.payload,
      };
    case "SET_WORDS_SCREEN_POSITIONS":
      return {
        ...state,
        wordsScreenPositions: action.payload,
      };
    default:
      return state;
  }
};

export const WordPositionsContext = createContext(initialWordPositionsState);

export const WordPositionsProvider: React.FC<WordPositionsProviderProps> = ({
  children,
}) => {
  const [state, dispatch] = useReducer(
    wordPositionsReducer,
    initialWordPositionsState
  );

  const getEnumeratedWords = useMemo(() => {
    let currentIndex = 0;

    const words = state.wordPositions
      ?.map(({ data }) => {
        return data.map(({ word }) => {
          currentIndex++;
          return { [currentIndex]: word };
        });
      })
      .flat();

    return words.reduce((acc, value) => {
      return { ...acc, ...value };
    }, {});
  }, [state.wordPositions]);

  console.log({ wordState: state, getEnumeratedWords });

  const { userInfo, userSettingsApi, selectedDocID } =
    useContext<IContextProps>(Context);

  const prevZoom = usePrevious(userSettingsApi.zoom);
  const prevDoc = usePrevious(selectedDocID);
  const setWordsLoading = (wordsLoading: boolean) => {
    dispatch({ type: "SET_WORD_LOADING", payload: wordsLoading });
  };

  const setWordPositions = (
    wordPositions: { data: IWordPositions[]; page: number }[]
  ) => {
    dispatch({ type: "SET_WORD_POSITIONS", payload: wordPositions });
  };

  const setWordsScreenPositions = (
    wordsScreenPositions: IScaledWordCoords[]
  ) => {
    dispatch({
      type: "SET_WORDS_SCREEN_POSITIONS",
      payload: wordsScreenPositions,
    });
  };

  useEffect(() => {
    if (
      userInfo.userID &&
      prevZoom &&
      (selectedDocID !== prevDoc ||
        userSettingsApi.zoom !== prevZoom ||
        performance.navigation.type === performance.navigation.TYPE_RELOAD ||
        performance.navigation.type === performance.navigation.TYPE_NAVIGATE)
    ) {
      setWordsLoading(true);
      axios
        .get(`${apiURL}/words-positions`, {
          params: {
            docID: selectedDocID,
            userID: userInfo.userID,
          },
        })
        .then((response) => {
          setWordPositions(response.data.data);
        })
        .catch((error) => {
          alert("Failed to get words positions.");
        })
        .finally(() => {
          setWordsLoading(false);
        });
    }
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [prevDoc, prevZoom, userInfo.userID]);

  const contextValue = {
    wordsLoading: state.wordsLoading,
    wordPositions: state.wordPositions,
    wordsScreenPositions: state.wordsScreenPositions,
    setWordPositions,
    setWordsScreenPositions,
  };

  return (
    <WordPositionsContext.Provider value={contextValue}>
      {children}
    </WordPositionsContext.Provider>
  );
};
