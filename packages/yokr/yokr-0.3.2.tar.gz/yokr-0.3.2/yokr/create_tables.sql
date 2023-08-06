CREATE TABLE IF NOT EXISTS InfoCompany (
    HashInfoKey     TEXT,
    HashKey         TEXT,
    Name            TEXT,
    NameAlias       TEXT,
    Description     TEXT,
    UUID            TEXT,
    StartDate       NUM,
    ContactPersonId TEXT
);

CREATE TABLE IF NOT EXISTS InfoApp (
    HashInfoKey        TEXT,
    HashKey            TEXT,
    CompanyHashInfoKey TEXT,
    Name               TEXT,
    NameAlias          TEXT,
    Description        TEXT,
    UUID               TEXT,
    ContactPersonId    TEXT,
    StartDate          NUM
);

CREATE TABLE IF NOT EXISTS InfoInstance (
    HashInfoKey     TEXT,
    HashKey         TEXT,
    AppHashInfoKey  TEXT,
    Name            TEXT,
    NameAlias       TEXT,
    Description     TEXT,
    UUID            TEXT,
    ContactPersonId TEXT,
    StartDate       NUM
);

CREATE TABLE IF NOT EXISTS InfoEntity (
    HashKey         TEXT,
    LibVerHashKey   TEXT,
    EntityType      TEXT,
    Entity          TEXT,
    Version         TEXT,
    Title           TEXT,
    Description     TEXT,
    License         TEXT,
    Url             TEXT,
    BugReports      TEXT,
    Build           TEXT,
    PublicationDate NUM,
    AddedDate       NUM,
    AuxT1           TEXT,
    AuxT2           TEXT,
    AuxR1           REAL,
    AuxR2           REAL,
    AuxD1           NUM,
    AuxD2           NUM
);

CREATE TABLE IF NOT EXISTS InstanceData (
    InstHashInfoKey TEXT,
    TimeStamp       NUM,
    ParamName       TEXT,
    Value           REAL,
    Uploaded        INTEGER(1)
);

CREATE TABLE IF NOT EXISTS InstanceDataAgg (
    InstHashInfoKey TEXT,
    TimeStamp       TEXT,
    ParamName       TEXT,
    StartTime       TEXT,
    EndTime         TEXT,
    ValNum          NUM,
    ValSum          REAL,
    ValMax          REAL,
    ValMin          REAL,
    ValAvg          REAL,
    ValVar          REAL,
    Uploaded        INTEGER(1)
);

CREATE TABLE IF NOT EXISTS Uploads (
    Date   DATETIME,
    Status VARCHAR(10)
);

CREATE TABLE IF NOT EXISTS UsedEntities (
    HashInfoKey     TEXT,
    InstHashInfoKey TEXT,
    EntityHashKey   TEXT,
    StartDate       NUM,
    LastDate        NUM
);
