const express = require('express');
const sqlite3 = require('sqlite3').verbose();
const path = require('path');
const app = express();
const PORT = process.env.PORT || 3000;

// Connect to SQLite database
const db = new sqlite3.Database(path.join(__dirname, 'database', 'output.db'), (err) => {
  if (err) {
    console.error(err.message);
  }
  console.log('Connected to the stops database.');
});

// Set EJS as the templating engine
app.set('view engine', 'ejs');
app.set('views', path.join(__dirname, 'templates'));

// Serve static files from the public directory
app.use(express.static(path.join(__dirname, 'public')));

// list all views
app.get('/views', (req, res) => {
  res.send(app.get('views'));
});

// Route for index page
app.get('/', (req, res) => {
  res.render('index');
});

// Route for stop pages
app.get('/stop/:stopid', (req, res) => {
  const stopId = req.params.stopid;
  const date = new Date().toISOString().slice(0, 10);
  const sql = `
SELECT DISTINCT r.number, r.terminus
FROM route r
JOIN stop s ON r.number = s.route_id
WHERE s.point_id = ?  -- Replace with the specific point ID
ORDER BY s.time;
`;

  // db get all rows
  db.all(sql, [stopId], (err, rows) => {
    if (err) {
      console.error(err.message);
      res.status(500).send('Database error');
      return;
    }
    if (!rows) {
      res.status(404).send('Stop not found');
      return;
    }
    // respond with json
    res.json(rows);
    //res.render('template', { stop: row });
  });
});

// Start server
app.listen(PORT, () => {
  console.log(`Server is running on port ${PORT}`);
});
