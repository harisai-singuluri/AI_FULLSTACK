// // routes/ai.js
// // AI endpoint — React will call this, this calls OpenAI
// // This is the CORRECT pattern (API key never leaves the server)

// const express = require("express");
// const router = express.Router();
// const OpenAI = require("openai").default;

// const openai = new OpenAI({ apiKey: process.env.OPENAI_API_KEY });

// // Mock response when API not available
// function getMockResponse(question) {
//   return `[MOCK] Here is a simulated AI answer for: "${question}". In production, this would be a real GPT response.`;
// }

// // POST /api/ai/ask
// router.post("/ask", async (req, res) => {
//   const { question, context } = req.body;

//   // Input validation
//   if (!question || question.trim() === "") {
//     return res.status(400).json({
//       success: false,
//       error: "Question is required",
//     });
//   }

//   try {
//     const response = await openai.chat.completions.create({
//       model: "gpt-3.5-turbo",
//       messages: [
//         {
//           role: "system",
//           content: context || "You are a helpful assistant. Be concise and clear.",
//         },
//         {
//           role: "user",
//           content: question,
//         },
//       ],
//       max_tokens: 300,
//     });

//     const aiReply = response.choices[0].message.content;

//     res.json({
//       success: true,
//       question,
//       answer: aiReply,
//       model: response.model,
//       tokens_used: response.usage.total_tokens,
//     });

//   } catch (error) {
//     console.error("AI API Error:", error.message);

//     // Graceful fallback — server doesn't crash
//     if (error.status === 429 || error.code === "insufficient_quota") {
//       return res.json({
//         success: true,
//         question,
//         answer: getMockResponse(question),
//         mode: "mock",
//         note: "API quota exceeded — using mock response",
//       });
//     }

//     res.status(500).json({
//       success: false,
//       error: "AI service temporarily unavailable",
//     });
//   }
// });

// module.exports = router;


const express = require("express");

const router = express.Router();

function getMockResponse(question) {
  return `[MOCK AI RESPONSE] ${question}`;
}

router.post("/ask", (req, res) => {
  const { question } = req.body;

  if (!question) {
    return res.status(400).json({
      success: false,
      error: "Question is required",
    });
  }

  res.json({
    success: true,
    question,
    answer: getMockResponse(question),
  });
});

module.exports = router;