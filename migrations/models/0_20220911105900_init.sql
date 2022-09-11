-- upgrade --
CREATE TABLE IF NOT EXISTS "statsentry" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "created_on" TIMESTAMPTZ NOT NULL  DEFAULT CURRENT_TIMESTAMP,
    "manga_uuid" UUID NOT NULL,
    "chapter_num" DOUBLE PRECISION NOT NULL,
    "pages" SMALLINT NOT NULL,
    "bytes" INT NOT NULL
);
CREATE INDEX IF NOT EXISTS "idx_statsentry_manga_u_b25e32" ON "statsentry" ("manga_uuid");
COMMENT ON TABLE "statsentry" IS 'A single entry in the stats table.';
CREATE TABLE IF NOT EXISTS "aerich" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "version" VARCHAR(255) NOT NULL,
    "app" VARCHAR(100) NOT NULL,
    "content" JSONB NOT NULL
);
