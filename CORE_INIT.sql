-- =====================================
-- Extensions (на будущее)
-- =====================================
CREATE EXTENSION IF NOT EXISTS pgcrypto;

-- =====================================
-- ENUMs
-- =====================================
DO $$
BEGIN
    IF NOT EXISTS (SELECT 1 FROM pg_type WHERE typname = 'vcs_provider') THEN
        CREATE TYPE vcs_provider AS ENUM (
            'github',
            'gitlab',
            'bitbucket',
            'svn'
        );
    END IF;
END$$;

-- =====================================
-- Repositories
-- =====================================
CREATE TABLE IF NOT EXISTS repositories (
    id              BIGSERIAL PRIMARY KEY,
    vcs_provider    vcs_provider NOT NULL,
    external_id     TEXT,
    owner           TEXT NOT NULL,
    name            TEXT NOT NULL,
    url             TEXT NOT NULL,
    default_branch  TEXT,
    created_at      TIMESTAMPTZ DEFAULT now(),
    updated_at      TIMESTAMPTZ DEFAULT now(),

    UNIQUE (vcs_provider, external_id)
);

-- =====================================
-- Contributors (accounts)
-- =====================================
CREATE TABLE IF NOT EXISTS contributors (
    id              BIGSERIAL PRIMARY KEY,
    vcs_provider    vcs_provider NOT NULL,
    external_id     TEXT NOT NULL,
    login           TEXT,
    display_name    TEXT,
    email           TEXT,
    profile_url     TEXT,
    created_at      TIMESTAMPTZ DEFAULT now(),
    updated_at      TIMESTAMPTZ DEFAULT now(),

    UNIQUE (vcs_provider, external_id)
);

-- =====================================
-- Persons (real people)
-- =====================================
CREATE TABLE IF NOT EXISTS persons (
    id          BIGSERIAL PRIMARY KEY,
    full_name   TEXT,
    created_at  TIMESTAMPTZ DEFAULT now(),
    updated_at  TIMESTAMPTZ DEFAULT now()
);

-- =====================================
-- Person <-> Contributor mapping
-- =====================================
CREATE TABLE IF NOT EXISTS person_contributors (
    person_id       BIGINT REFERENCES persons(id) ON DELETE CASCADE,
    contributor_id  BIGINT REFERENCES contributors(id) ON DELETE CASCADE,
    created_at      TIMESTAMPTZ DEFAULT now(),
    updated_at      TIMESTAMPTZ DEFAULT now(),

    PRIMARY KEY (person_id, contributor_id)
);

-- =====================================
-- Commits
-- =====================================
CREATE TABLE IF NOT EXISTS commits (
    id                      BIGSERIAL PRIMARY KEY,
    repository_id                 BIGINT NOT NULL REFERENCES repositories(id) ON DELETE CASCADE,
    contributor_id          BIGINT REFERENCES contributors(id),
    sha                     TEXT NOT NULL,
    message                 TEXT NOT NULL,
    authored_at             TIMESTAMPTZ,
    committed_at            TIMESTAMPTZ,
    author_name             TEXT,
    author_email            TEXT,
    additions               INTEGER,
    deletions               INTEGER,
    changes                 INTEGER,
    commit_type             TEXT,
    -- Conventional commits / semantic info
    is_conventional         BOOLEAN DEFAULT FALSE,
    conventional_type       TEXT,
    conventional_scope      TEXT,
    is_breaking_change      BOOLEAN DEFAULT FALSE,
    -- Commit kind flags
    is_merge_commit         BOOLEAN DEFAULT FALSE,
    is_pr_commit            BOOLEAN DEFAULT FALSE,
    -- Extra useful metadata
    parents_count           INTEGER,
    files_changed           INTEGER,
    is_revert_commit        BOOLEAN DEFAULT FALSE,
    created_at              TIMESTAMPTZ DEFAULT now(),
    updated_at              TIMESTAMPTZ DEFAULT now(),

    UNIQUE (repository_id, sha)
);

-- =====================================
-- Commit files (diffs)
-- =====================================
CREATE TABLE IF NOT EXISTS commit_files (
    id                  BIGSERIAL PRIMARY KEY,
    commit_id           BIGINT NOT NULL REFERENCES commits(id) ON DELETE CASCADE,
    file_path           TEXT NOT NULL,
    additions           INTEGER,
    deletions           INTEGER,
    changes             INTEGER,
    language            TEXT,
    patch               TEXT,
    created_at              TIMESTAMPTZ DEFAULT now(),
    updated_at              TIMESTAMPTZ DEFAULT now()

);

-- =====================================
-- File extensions
-- =====================================
CREATE TABLE IF NOT EXISTS file_extensions (
    id              SERIAL PRIMARY KEY,
    extension       TEXT NOT NULL,
    language        TEXT NOT NULL,
    is_system       BOOLEAN DEFAULT FALSE,
    user_id         BIGINT DEFAULT NULL,
    created_at      TIMESTAMP WITH TIME ZONE DEFAULT now(),
    updated_at      TIMESTAMP WITH TIME ZONE DEFAULT now()
);

INSERT INTO file_extensions (extension, language) VALUES
    ('py', 'Python', TRUE),
    ('js', 'JavaScript', TRUE),
    ('ts', 'TypeScript', TRUE),
    ('java', 'Java', TRUE),
    ('cpp', 'C++', TRUE),
    ('c', 'C', TRUE),
    ('go', 'Go', TRUE),
    ('rs', 'Rust', TRUE),
    ('Dockerfile', 'Docker', TRUE),
    ('yml', 'YAML', TRUE),
    ('yaml', 'YAML', TRUE)
ON CONFLICT DO NOTHING;

-- =====================================
-- Analysis settings (JSONB)
-- =====================================
CREATE TABLE IF NOT EXISTS analysis_settings (
    id              BIGSERIAL PRIMARY KEY,
    scope_type      TEXT NOT NULL, -- repo/team/org
    scope_id        BIGINT NOT NULL,
    settings        JSONB NOT NULL,
    created_at      TIMESTAMPTZ DEFAULT now(),
    updated_at      TIMESTAMPTZ DEFAULT now(),

    UNIQUE (scope_type, scope_id)
);


-- =====================================
-- Indexes
-- =====================================
CREATE INDEX IF NOT EXISTS idx_commits_repo
    ON commits(repository_id);

CREATE INDEX IF NOT EXISTS idx_commits_contributor
    ON commits(contributor_id);

CREATE INDEX IF NOT EXISTS idx_commit_files_commit
    ON commit_files(commit_id);

CREATE INDEX IF NOT EXISTS idx_contributors_provider
    ON contributors(vcs_provider, external_id);

CREATE INDEX IF NOT EXISTS idx_analysis_settings_scope
    ON analysis_settings(scope_type, scope_id);
