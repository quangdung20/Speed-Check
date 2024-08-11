const sqlite3 = require('sqlite3').verbose();
const db = new sqlite3.Database('speed_data.db');

db.serialize(() => {
    db.run(`CREATE TABLE IF NOT EXISTS speed_data (
        time TIMESTAMP PRIMARY KEY,
        speed_real_right FLOAT,
        speed_set_right FLOAT,
        speed_real_left FLOAT,
        speed_set_left FLOAT
    )`);
});

db.close();
