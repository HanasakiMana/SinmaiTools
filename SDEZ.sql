CREATE TABLE musicInfo(
    musicId         TEXT,
    title           TEXT,
    artist          TEXT,
    genre           TEXT,
    bpm             INTEGER,
    addVersion      TEXT,
    isNew           INTEGER,
    stdChartId      TEXT,
    dxChartId       TEXT
);

CREATE TABLE chartInfo(
    chartId         TEXT,
    chartType       TEXT,
    musicId         TEXT,
    diff            TEXT,
    chartLevel      TEXT,
    chartDs         REAL,
    charter         TEXT,
    tapCount        INTEGER,
    holdCount       INTEGER,
    slideCount      INTEGER,
    touchCount      INTEGER,
    breakCount      INTEGER
   
);

CREATE TABLE dbInfo(
    updateTime  TEXT
);

CREATE TABLE dataVersion(
    ver     TEXT
);

CREATE TABLE DBVersion(
    ver     TEXT
);

INSERT INTO DBVersion VALUES('101')