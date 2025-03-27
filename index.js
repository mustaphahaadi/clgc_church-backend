import express from "express";
import sqlite3 from "sqlite3";
import { open } from "sqlite";
import cors from "cors";
import bodyParser from "body-parser";

const app = express();
const port = process.env.PORT || 3001;

// Middleware
app.use(cors());
app.use(bodyParser.json());

// Initialize database
async function initializeDatabase() {
  return open({
    filename: "./database.db",
    driver: sqlite3.Database,
  });
}

// Create tables
async function setupDatabase() {
  const db = await initializeDatabase();

  await db.exec(`
    CREATE TABLE IF NOT EXISTS members (
      id INTEGER PRIMARY KEY AUTOINCREMENT,
      date TEXT,
      firstName TEXT,
      lastName TEXT,
      email TEXT UNIQUE,
      phone TEXT,
      address TEXT,
      createdAt DATETIME DEFAULT CURRENT_TIMESTAMP
    );
    
    CREATE TABLE IF NOT EXISTS contacts (
      id INTEGER PRIMARY KEY AUTOINCREMENT,
      name TEXT,
      email TEXT,
      message TEXT,
      phone TEXT,
      subject TEXT,
      createdAt DATETIME DEFAULT CURRENT_TIMESTAMP
    );
  `);
}

// Routes
app.post("/api/members", async (req, res) => {
  const db = await initializeDatabase();
  const { date, firstName, lastName, email, phone, address } = req.body;

  try {
    const result = await db.run(
      `INSERT INTO members (date, firstName, lastName, email, phone, address) 
       VALUES (?, ?, ?, ?, ?, ?)`,
      [date, firstName, lastName, email, phone, address]
    );
    res.status(201).json({ id: result.lastID });
  } catch (error) {
    res.status(400).json({ error: error.message });
  }
});

app.post("/api/contacts", async (req, res) => {
  const db = await initializeDatabase();
  const { name, email, message, phone, subject } = req.body;

  try {
    const result = await db.run(
      `INSERT INTO contacts (name, email, message, phone, subject) 
       VALUES (?, ?, ?, ?, ?)`,
      [name, email, message, phone, subject]
    );
    res.status(201).json({ id: result.lastID });
  } catch (error) {
    res.status(400).json({ error: error.message });
  }
});

// Start server
setupDatabase().then(() => {
  app.listen(port, () => {
    console.log(`Server running on port ${port}`);
  });
});
