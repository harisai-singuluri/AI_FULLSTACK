// middleware/logger.js
// In real companies, every request is logged for debugging

function logger(req, res, next) {
  const timestamp = new Date().toISOString();
  const method = req.method;
  const url = req.url;

  console.log(`[${timestamp}] ${method} ${url}`);

  next(); // CRITICAL: must call next() or the request hangs forever
}

module.exports = logger;