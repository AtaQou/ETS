import sqlite3


def initializeDatabase():
    conn = sqlite3.connect('ETSsqLiteDB')

    c = conn.cursor()
    c.execute('''
            CREATE TABLE IF NOT EXISTS users
            ([userID] INTEGER PRIMARY KEY AUTOINCREMENT, [username] TEXT, [password] TEXT)
            ''')

    c.execute('''
            CREATE TABLE IF NOT EXISTS user_settings
            ([userID] INTEGER, [Selected_language] TEXT, [theme] TEXT, [zoomLevel] INTEGER, [baseGazeSamples] INTEGER DEFAULT 60, [translationMode] TEXT DEFAULT 'word', [translationOutputMode] TEXT DEFAULT 'on',
            FOREIGN KEY(userID) REFERENCES users(userID))
            ''')

    c.execute('''
            CREATE TABLE IF NOT EXISTS vocabulary
            ([wordID] INTEGER PRIMARY KEY AUTOINCREMENT, [userID] INTEGER, [word] TEXT, 
            [usageCount] INTEGER, [synonyms] TEXT,
            FOREIGN KEY(userID) REFERENCES users(userID))
            ''')

    c.execute('''
            CREATE TABLE IF NOT EXISTS documents
            ([docID] INTEGER PRIMARY KEY AUTOINCREMENT, [userID] INTEGER, 
            [docName] TEXT, [docFile] BLOB, [uploadDate] DATETIME, [lastReadPage] INTEGER,
            FOREIGN KEY(userID) REFERENCES users(userID))
            ''')

    c.execute('''
            CREATE TABLE IF NOT EXISTS user_sessions
            ([sessionID] TEXT PRIMARY KEY, [userID] INTEGER, [trackerAddress] TEXT, [trackerName] TEXT,
            [startedAt] DATETIME, [endedAt] DATETIME, [startSettings] TEXT, [endReason] TEXT,
            FOREIGN KEY(userID) REFERENCES users(userID))
            ''')

    c.execute('''
            CREATE TABLE IF NOT EXISTS translation_events
            ([eventID] INTEGER PRIMARY KEY AUTOINCREMENT, [userID] INTEGER, [sessionID] TEXT,
            [docID] INTEGER, [page] INTEGER, [sourceText] TEXT, [translatedText] TEXT, [sourceLang] TEXT,
            [targetLang] TEXT, [translationMode] TEXT, [provider] TEXT, [translatedAt] DATETIME, [settingsSnapshot] TEXT, [translationOutputMode] TEXT DEFAULT 'on', [isUndesired] INTEGER DEFAULT 0,
            FOREIGN KEY(userID) REFERENCES users(userID), FOREIGN KEY(sessionID) REFERENCES user_sessions(sessionID))
            ''')

    c.execute('''
            CREATE TABLE IF NOT EXISTS translation_stats
            ([userID] INTEGER, [sessionID] TEXT, [sourceText] TEXT, [targetLang] TEXT, [translationMode] TEXT,
            [usageCount] INTEGER DEFAULT 1, [lastTranslation] TEXT, [lastTranslatedAt] DATETIME,
            PRIMARY KEY (userID, sessionID, sourceText, targetLang, translationMode),
            FOREIGN KEY(userID) REFERENCES users(userID), FOREIGN KEY(sessionID) REFERENCES user_sessions(sessionID))
            ''')

    c.execute('''
            CREATE TABLE IF NOT EXISTS settings_change_events
            ([changeID] INTEGER PRIMARY KEY AUTOINCREMENT, [userID] INTEGER, [sessionID] TEXT,
            [changedFields] TEXT, [oldSettings] TEXT, [newSettings] TEXT, [changedAt] DATETIME,
            FOREIGN KEY(userID) REFERENCES users(userID), FOREIGN KEY(sessionID) REFERENCES user_sessions(sessionID))
            ''')

    conn.commit()

    print('DB fine')

    conn.close()


def convert_to_binary(filename):
    with open(filename, 'rb') as file:
        blob_data = file.read()
    return blob_data


def print_db_tables(database):
    conn = sqlite3.connect(database)
    c = conn.cursor()

    c.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = c.fetchall()

    for table in tables:
        print(f"Table: {table[0]}")

        # Get and print column information for each table
        c.execute(f"PRAGMA table_info({table[0]})")
        columns = c.fetchall()
        for column in columns:
            print(
                f"Column ID: {column[0]}, Name: {column[1]}, Type: {column[2]}, NotNull: {column[3]}, Default Value: {column[4]}, Primary Key: {column[5]}")

        print("\n")

    conn.close()


def create_users(database):
    conn = sqlite3.connect(database)
    c = conn.cursor()

    users = [('Dimosthenis Minas', 'password1'),
             ('Theodosiou Eleanna', 'password2')]
    c.executemany('INSERT INTO users(username, password) VALUES (?,?)', users)

    conn.commit()
    conn.close()


def fetch_users(database):
    conn = sqlite3.connect(database)
    c = conn.cursor()

    c.execute('SELECT * FROM users')

    df = pd.DataFrame(c.fetchall(), columns=['id', 'price'])
    print(df)

    conn.close()
