-- Initial schema for the Trip Planner database.
-- This runs automatically on first container start (mounted into
-- /docker-entrypoint-initdb.d/ by the official mysql image).

CREATE DATABASE IF NOT EXISTS tripdb;
USE tripdb;

CREATE TABLE IF NOT EXISTS trips (
    id INT AUTO_INCREMENT PRIMARY KEY,
    destination VARCHAR(255) NOT NULL,
    start_date DATE NOT NULL,
    end_date DATE NOT NULL,
    notes TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Some seed data so the app isn't empty on first run
INSERT INTO trips (destination, start_date, end_date, notes) VALUES
('Paris, France',   '2026-09-10', '2026-09-15', 'Eiffel Tower, Louvre, Seine cruise'),
('Tokyo, Japan',    '2026-11-01', '2026-11-08', 'Shibuya, Mt Fuji day trip, sushi'),
('Bali, Indonesia', '2026-12-20', '2026-12-28', 'Ubud, beaches, temples');

