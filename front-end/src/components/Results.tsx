import React, { FC, useContext, useEffect, useMemo, useState } from "react";
import axios from "axios";
import { Context } from "context/Context";
import { IContextProps } from "types/AppTypes";
import { apiURL } from "utils/consts";
import { getBgSecondary, getFontColorSecondary } from "utils/functions";

interface IExperimentUser {
  userID: number;
  username: string;
  sessionCount: number;
  translationCount: number;
}

interface ISessionRow {
  sessionID: string;
  userID: number;
  username: string;
  trackerAddress?: string;
  trackerName?: string;
  startedAt: string;
  endedAt?: string | null;
  endReason?: string | null;
  startSettings?: Record<string, any> | string | null;
  translationCount: number;
  settingsChangeCount: number;
}

interface ITranslationEvent {
  eventID: number;
  userID: number;
  sessionID: string;
  docID?: number;
  page?: number;
  sourceText: string;
  translatedText: string;
  sourceLang: string;
  targetLang: string;
  translationMode: string;
  provider: string;
  translatedAt: string;
}

interface ISettingsChangeEvent {
  changeID: number;
  userID: number;
  sessionID?: string;
  changedFields: string[] | string;
  oldSettings?: Record<string, any> | string | null;
  newSettings?: Record<string, any> | string | null;
  changedAt: string;
}

interface ITimelineRow {
  id: string;
  timestamp: string;
  type: "translation" | "settings_change";
  payload: ITranslationEvent | ISettingsChangeEvent;
}

const formatDate = (value?: string | null) => {
  if (!value) return "-";
  const parsed = new Date(value);
  if (Number.isNaN(parsed.getTime())) return value;
  return parsed.toLocaleString();
};

const stringifyValue = (value: any) => {
  if (value === null || value === undefined) return "-";
  if (typeof value === "object") {
    try {
      return JSON.stringify(value);
    } catch (_err) {
      return String(value);
    }
  }
  return String(value);
};

const toObject = (value: any) => {
  if (!value || typeof value !== "object" || Array.isArray(value)) return null;
  return value as Record<string, any>;
};

const Results: FC = () => {
  const { userSettingsApi, userInfo } = useContext<IContextProps>(Context);
  const isDarkTheme = userSettingsApi.theme === "dark";

  const [users, setUsers] = useState<IExperimentUser[]>([]);
  const [selectedUserID, setSelectedUserID] = useState<string>("");
  const [sessions, setSessions] = useState<ISessionRow[]>([]);
  const [selectedSessionID, setSelectedSessionID] = useState<string>("");
  const [translations, setTranslations] = useState<ITranslationEvent[]>([]);
  const [settingsChanges, setSettingsChanges] = useState<ISettingsChangeEvent[]>([]);
  const [loading, setLoading] = useState(false);
  const [loadingDetails, setLoadingDetails] = useState(false);
  const [error, setError] = useState<string>("");

  const selectedSession = useMemo(
    () => sessions.find((session) => session.sessionID === selectedSessionID),
    [sessions, selectedSessionID]
  );

  const timeline = useMemo<ITimelineRow[]>(() => {
    const translationRows: ITimelineRow[] = translations.map((item) => ({
      id: `translation-${item.eventID}`,
      timestamp: item.translatedAt,
      type: "translation",
      payload: item,
    }));

    const settingsRows: ITimelineRow[] = settingsChanges.map((item) => ({
      id: `settings-${item.changeID}`,
      timestamp: item.changedAt,
      type: "settings_change",
      payload: item,
    }));

    return [...translationRows, ...settingsRows].sort((a, b) => {
      const aTime = new Date(a.timestamp).getTime();
      const bTime = new Date(b.timestamp).getTime();
      if (Number.isNaN(aTime) && Number.isNaN(bTime)) return 0;
      if (Number.isNaN(aTime)) return 1;
      if (Number.isNaN(bTime)) return -1;
      return aTime - bTime;
    });
  }, [settingsChanges, translations]);

  useEffect(() => {
    setLoading(true);
    axios
      .get(`${apiURL}/experiment/users`)
      .then((response) => {
        const fetchedUsers: IExperimentUser[] = response.data || [];
        setUsers(fetchedUsers);
        const currentUserId = userInfo.userID ? String(userInfo.userID) : "";
        if (currentUserId && fetchedUsers.some((u) => String(u.userID) === currentUserId)) {
          setSelectedUserID(currentUserId);
        } else if (fetchedUsers.length) {
          setSelectedUserID(String(fetchedUsers[0].userID));
        }
      })
      .catch((err) => {
        setError(err?.response?.data?.message || "Failed to load users.");
      })
      .finally(() => {
        setLoading(false);
      });
  }, [userInfo.userID]);

  useEffect(() => {
    if (!selectedUserID) {
      setSessions([]);
      setSelectedSessionID("");
      return;
    }

    setLoading(true);
    setError("");
    axios
      .get(`${apiURL}/experiment/sessions`, {
        params: { userID: selectedUserID },
      })
      .then((response) => {
        const fetchedSessions: ISessionRow[] = response.data || [];
        setSessions(fetchedSessions);
        if (fetchedSessions.length) {
          setSelectedSessionID(fetchedSessions[0].sessionID);
        } else {
          setSelectedSessionID("");
        }
      })
      .catch((err) => {
        setError(err?.response?.data?.message || "Failed to load sessions.");
      })
      .finally(() => {
        setLoading(false);
      });
  }, [selectedUserID]);

  useEffect(() => {
    if (!selectedUserID || !selectedSessionID) {
      setTranslations([]);
      setSettingsChanges([]);
      return;
    }

    setLoadingDetails(true);
    setError("");
    Promise.all([
      axios.get(`${apiURL}/experiment/translations`, {
        params: { userID: selectedUserID, sessionID: selectedSessionID, limit: 10000 },
      }),
      axios.get(`${apiURL}/experiment/settings-changes`, {
        params: { userID: selectedUserID, sessionID: selectedSessionID },
      }),
    ])
      .then(([translationsResponse, settingsChangesResponse]) => {
        setTranslations(translationsResponse.data || []);
        setSettingsChanges(settingsChangesResponse.data || []);
      })
      .catch((err) => {
        setError(err?.response?.data?.message || "Failed to load session details.");
      })
      .finally(() => {
        setLoadingDetails(false);
      });
  }, [selectedSessionID, selectedUserID]);

  const renderStartSettings = () => {
    const settingsObject = toObject(selectedSession?.startSettings);
    if (!settingsObject) {
      return <div className='text-sm'>No captured start settings.</div>;
    }

    return (
      <div className='grid grid-cols-2 gap-2 text-sm'>
        {Object.entries(settingsObject).map(([key, value]) => (
          <div key={key} className='flex justify-between border-b border-gray-200 py-1'>
            <div className='font-semibold mr-4'>{key}</div>
            <div className='text-right'>{stringifyValue(value)}</div>
          </div>
        ))}
      </div>
    );
  };

  return (
    <div className='flex flex-col m-2 p-4'>
      <h1
        className='py-1 mb-4 text-xl font-bold border-b border-gray-300'
        style={{ color: getFontColorSecondary(isDarkTheme) }}
      >
        Results
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
          >
            {!users.length && <option value=''>No users</option>}
            {users.map((user) => (
              <option key={user.userID} value={String(user.userID)}>
                {user.userID} - {user.username} (sessions: {user.sessionCount}, translations: {user.translationCount})
              </option>
            ))}
          </select>
        </div>

        <div>
          <label className='block mb-1 text-sm' style={{ color: getFontColorSecondary(isDarkTheme) }}>
            Session
          </label>
          <select
            value={selectedSessionID}
            onChange={(e) => setSelectedSessionID(e.target.value)}
            className='w-full text-sm p-2 rounded border border-gray-300 text-gray-900'
            disabled={!sessions.length}
          >
            {!sessions.length && <option value=''>No sessions</option>}
            {sessions.map((session) => (
              <option key={session.sessionID} value={session.sessionID}>
                {session.sessionID.slice(0, 8)}... | {formatDate(session.startedAt)} | translations: {session.translationCount}
              </option>
            ))}
          </select>
        </div>
      </div>

      {loading && (
        <div style={{ color: getFontColorSecondary(isDarkTheme) }}>
          Loading results...
        </div>
      )}

      {error && <div className='text-red-700 mb-3'>{error}</div>}

      {selectedSession && (
        <div
          className='p-3 rounded border border-gray-300 mb-4'
          style={{ backgroundColor: getBgSecondary(isDarkTheme), color: getFontColorSecondary(isDarkTheme) }}
        >
          <div className='font-semibold mb-2'>Session Info</div>
          <div className='grid grid-cols-2 gap-2 text-sm mb-3'>
            <div>Session ID: {selectedSession.sessionID}</div>
            <div>User ID: {selectedSession.userID}</div>
            <div>Started: {formatDate(selectedSession.startedAt)}</div>
            <div>Ended: {formatDate(selectedSession.endedAt)}</div>
            <div>Tracker: {selectedSession.trackerName || "-"}</div>
            <div>Address: {selectedSession.trackerAddress || "-"}</div>
          </div>
          <div className='font-semibold mb-2'>Settings At Session Start</div>
          {renderStartSettings()}
        </div>
      )}

      {loadingDetails && (
        <div style={{ color: getFontColorSecondary(isDarkTheme) }}>
          Loading session timeline...
        </div>
      )}

      {!loadingDetails && selectedSessionID && (
        <div className='border border-gray-300 rounded overflow-hidden'>
          <div
            className='grid grid-cols-6 px-3 py-2 text-sm font-semibold border-b border-gray-300'
            style={{ backgroundColor: getBgSecondary(isDarkTheme), color: getFontColorSecondary(isDarkTheme) }}
          >
            <div className='col-span-2'>Timestamp</div>
            <div className='col-span-1'>Type</div>
            <div className='col-span-3'>Details</div>
          </div>
          <div className='max-h-[360px] overflow-y-auto'>
            {!timeline.length && (
              <div className='p-3 text-sm' style={{ color: getFontColorSecondary(isDarkTheme) }}>
                No events recorded for this session.
              </div>
            )}
            {timeline.map((item) => {
              if (item.type === "translation") {
                const translation = item.payload as ITranslationEvent;
                return (
                  <div
                    key={item.id}
                    className='grid grid-cols-6 px-3 py-2 text-sm border-b border-gray-200'
                    style={{ color: getFontColorSecondary(isDarkTheme) }}
                  >
                    <div className='col-span-2'>{formatDate(item.timestamp)}</div>
                    <div className='col-span-1'>translation</div>
                    <div className='col-span-3'>
                      "{translation.sourceText}" → "{translation.translatedText}" (mode: {translation.translationMode}, page: {translation.page || "-"})
                    </div>
                  </div>
                );
              }

              const settingChange = item.payload as ISettingsChangeEvent;
              const changedFields = Array.isArray(settingChange.changedFields)
                ? settingChange.changedFields.join(", ")
                : settingChange.changedFields;

              return (
                <div
                  key={item.id}
                  className='grid grid-cols-6 px-3 py-2 text-sm border-b border-gray-200'
                  style={{ color: getFontColorSecondary(isDarkTheme) }}
                >
                  <div className='col-span-2'>{formatDate(item.timestamp)}</div>
                  <div className='col-span-1'>settings</div>
                  <div className='col-span-3'>
                    Changed: {changedFields || "-"} | New: {stringifyValue(settingChange.newSettings)}
                  </div>
                </div>
              );
            })}
          </div>
        </div>
      )}
    </div>
  );
};

export default Results;
