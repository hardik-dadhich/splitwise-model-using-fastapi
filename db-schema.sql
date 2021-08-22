CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

CREATE TABLE IF NOT EXISTS users (
    name text PRIMARY KEY,
    "createdAt" timestamp with time zone NOT NULL DEFAULT now(),
);

CREATE TABLE IF NOT EXISTS group (
    name text NOT NULL PRIMARY KEY,
    userlist text[],
);

CREATE TABLE IF NOT EXISTS expense (
    id uuid DEFAULT uuid_generate_v4() PRIMARY KEY,
    user_id uuid REFERENCES users(id) ON DELETE CASCADE ON UPDATE CASCADE,
);