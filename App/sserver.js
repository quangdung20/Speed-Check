const express = require('express');
const sqlite3 = require('sqlite3').verbose();
const cors = require('cors');

const app = express();
const port = 3000;

// Middleware
app.use(cors());
app.use(express.json());

// SQLite Connection
const db = new sqlite3.Database('speed_data.db');

// API Endpoint to get speed data
app.get('/api/speed_data', (req, res) => {
    const { start_time, end_time } = req.query;
    const query = `
        SELECT time, speed_real_right, speed_set_right, speed_real_left, speed_set_left
        FROM speed_data
        WHERE time BETWEEN ? AND ?
    `;
    db.all(query, [start_time, end_time], (err, rows) => {
        if (err) {
            res.status(500).json({ error: err.message });
            return;
        }
        res.json(rows);
    });
});

app.listen(port, () => {
    console.log(`Server running on http://localhost:${port}`);
});
