// routes/health.js
// Health check endpoint — DevOps and monitoring tools ping this
// If this returns 200, the server is alive

const express = require("express");
const router = express.Router();

router.get("/", (req, res) => {
  res.status(200).json({
    status: "healthy",
    uptime: process.uptime(),           // how long server has been running
    timestamp: new Date().toISOString(),
    environment: process.env.NODE_ENV || "development",
  });
});

module.exports = router;