PRAGMA
foreign_keys = ON;
BEGIN
TRANSACTION;

CREATE TABLE test_points
(
    id INTEGER PRIMARY KEY NOT NULL,
    x  INTEGER             NOT NULL,
    y  INTEGER             NOT NULL
);

INSERT INTO test_points (id, x, y)
VALUES (0, 0, 0),
       (1, 1, 1),
       (2, -1, 0);

CREATE TABLE test_lines
(
    start_point_id INTEGER NOT NULL,
    end_point_id   INTEGER NOT NULL,

    FOREIGN KEY (start_point_id)
        REFERENCES test_points (id),
    FOREIGN KEY (end_point_id)
        REFERENCES test_points (id)
);

INSERT INTO test_lines (start_point_id, end_point_id)
VALUES (0, 1),
       (0, 2);

COMMIT;
