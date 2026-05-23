// server.js
// Entry point for the backend — this is how real company servers start

require("dotenv").config();
const express = require("express");
const cors = require("cors");

// Import route files
const healthRoutes = require("./routes/health");
const userRoutes = require("./routes/users");
const aiRoutes = require("./routes/ai");

// Import middleware
const logger = require("./middleware/logger");

const app = express();
const PORT = process.env.PORT || 3001;

// ----------------------------------------
// MIDDLEWARE (runs on every single request)
// ----------------------------------------
app.use(cors());              // Allow cross-origin requests (React calling this server)
app.use(express.json());      // Parse JSON request bodies
app.use(logger);              // Our custom logger

// ----------------------------------------
// ROUTES
// ----------------------------------------
app.use("/api/health", healthRoutes);
app.use("/api/users", userRoutes);
//app.use("/api/ai", aiRoutes);

// ----------------------------------------
// ROOT
// ----------------------------------------
app.get("/", (req, res) => {
  res.json({
    message: "🚀 AI Fullstack API is running",
    version: "1.0.0",
    endpoints: ["/api/health", "/api/users", "/api/ai/ask"],
  });
});

// ----------------------------------------
// 404 HANDLER (always add this)
// ----------------------------------------
app.use((req, res) => {
  res.status(404).json({ error: "Route not found" });
});

// ----------------------------------------
// START SERVER
// ----------------------------------------
app.listen(PORT, () => {
  console.log(`✅ Server running on http://localhost:${PORT}`);
  console.log(`📌 Environment: ${process.env.NODE_ENV || "development"}`);
});

