CREATE TABLE Pierwiastek (
    liczba_atom NUMERIC(3) PRIMARY KEY,
    liczba_mas NUMERIC(5, 2) NOT NULL
);

CREATE TABLE Atmosfera (
    id NUMERIC(6) PRIMARY KEY,
    cisnienie NUMERIC(9, 3) NOT NULL
);

CREATE TABLE Zawartosc (
    id NUMERIC(6) PRIMARY KEY,
    atmosfera NUMERIC(8) NOT NULL REFERENCES Atmosfera,
    stezenie NUMERIC(3, 2) NOT NULL,
    pierwiastek NUMERIC(8) NOT NULL REFERENCES Pierwiastek,
    CONSTRAINT stezenie_check CHECK ((0.00 <= stezenie) AND (stezenie <= 1.00))
);

CREATE FUNCTION zawartosc_check() RETURNS trigger AS $$
BEGIN
    IF NOT EXISTS (
        SELECT galaktyka
        FROM UkladGwiezdny
        WHERE NEW.id = galaktyka
    ) THEN
        RAISE EXCEPTION 'Galaktyka musi posiadać układ gwiezdny';
    ELSE
        RETURN NEW;
    END IF;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER zawartosc_check AFTER INSERT OR UPDATE ON Zawartosc
    EXECUTE PROCEDURE zawartosc_check();

CREATE TABLE Preferencje (
    id NUMERIC(6) PRIMARY KEY,
    temperatura NUMERIC(8) NOT NULL,
    przyspieszenie_graw NUMERIC(4, 2) NOT NULL,
    poziom_pustelnictwa NUMERIC(3, 2) NOT NULL,
    poziom_spokoju NUMERIC(8) NOT NULL,
    typ_planety VARCHAR(8) NOT NULL,
    CONSTRAINT typ_check CHECK (typ_planety IN ('skalista', 'gazowa')),
    CONSTRAINT poziom_check CHECK ((0.00 <= poziom_pustelnictwa) AND (poziom_pustelnictwa <= 1.00))
);

CREATE TABLE Rasa (
    nazwa VARCHAR(8) PRIMARY KEY,
    preferencje NUMERIC(6) NOT NULL REFERENCES Preferencje
);

CREATE TABLE Galaktyka (
    id NUMERIC(6) PRIMARY KEY,
    nazwa VARCHAR(8) NOT NULL,
    odleglosc NUMERIC(8) NOT NULL
);

CREATE FUNCTION obowiazkowy_uklad() RETURNS trigger AS $$
BEGIN
    IF NOT EXISTS (
        SELECT galaktyka
        FROM UkladGwiezdny
        WHERE NEW.id = galaktyka
    ) THEN
        RAISE EXCEPTION 'Galaktyka musi posiadać układ gwiezdny';
    ELSE
        RETURN NEW;
    END IF;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER obowiazkowy_uklad AFTER DELETE OR UPDATE ON Galaktyka
    FOR EACH ROW EXECUTE PROCEDURE obowiazkowy_uklad();

CREATE TABLE UkladGwiezdny (
    id NUMERIC(6) PRIMARY KEY,
    nazwa VARCHAR(8) NOT NULL,
    stabilnosc NUMERIC(3, 2) NOT NULL,
    galaktyka NUMERIC(6) NOT NULL REFERENCES Galaktyka,
    CONSTRAINT stabilnosc_check CHECK ((0.00 <= stabilnosc) AND (stabilnosc <= 1.00))
);

CREATE FUNCTION obowiazkowa_gwiazda() RETURNS trigger AS $$
BEGIN
    IF NOT EXISTS (
        SELECT uklad_gwiezdny
        FROM Gwiazda
        WHERE NEW.id = uklad_gwiezdny
    ) THEN
        RAISE EXCEPTION 'Układ gwiezdy musi posiadać gwiazdę';
    ELSE
        RETURN NEW;
    END IF;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER obowiazkowa_gwiazda AFTER DELETE OR UPDATE ON UkladGwiezdny
    FOR EACH ROW EXECUTE PROCEDURE obowiazkowa_gwiazda();

CREATE TABLE Gwiazda (
    id NUMERIC(6) PRIMARY KEY,
    nazwa VARCHAR(8) NOT NULL,
    jasnosc NUMERIC(9, 2) NOT NULL, -- wyrażona w jasnościach słonecznych
    masa NUMERIC(6, 4) NOT NULL, -- wyrażona w masach słońca
    uklad_gwiezdny NUMERIC(6) NOT NULL REFERENCES UkladGwiezdny
);

CREATE FUNCTION obowiazkowa_planeta() RETURNS trigger AS $$
BEGIN
    IF NOT EXISTS (
        SELECT gwiazda
        FROM Planeta
        WHERE NEW.id = gwiazda
    ) THEN
        RAISE EXCEPTION 'Gwiazda musi posiadać planetę';
    ELSE
        RETURN NEW;
    END IF;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER obowiazkowa_planeta AFTER DELETE OR UPDATE ON Gwiazda
    FOR EACH ROW EXECUTE PROCEDURE obowiazkowa_planeta();

CREATE TABLE Planeta (
    id NUMERIC(6) PRIMARY KEY,
    nazwa VARCHAR(16) NOT NULL,

    typ VARCHAR(16) NOT NULL,
    masa NUMERIC(6, 4) NOT NULL, -- wyrażona w masach Jowisza
    promien NUMERIC(6, 4) NOT NULL, -- wyrażona w promieniach Jowisza
    atmosfera NUMERIC(6) NOT NULL REFERENCES Atmosfera,

    gwiazda NUMERIC(6) NOT NULL REFERENCES Gwiazda,
    odleglosc_od_gwiazdy NUMERIC(8) NOT NULL,
    poziom_agresji_obcych NUMERIC(3, 2),
    -- null jeśli niezamieszkana
    CONSTRAINT typ_check CHECK (typ IN ('skalista', 'gazowa')),
    CONSTRAINT poziom_check CHECK ((0.00 <= poziom_agresji_obcych) AND (poziom_agresji_obcych <= 1.00))
);