// ai-hello.js
// Day 1: First AI integration (future-ready + fallback safe)

// Load environment variables
require("dotenv").config();

// Import OpenAI SDK
const OpenAI = require("openai");

// Create OpenAI client
const openai = new OpenAI({
  apiKey: process.env.OPENAI_API_KEY,
});

// ------------------------------
// MOCK AI (fallback if API fails)
// ------------------------------
function mockAI(question) {
  console.log("\n⚠️ Running in MOCK MODE (no API usage)");

  console.log("\n📤 Sending to AI:", question);

  setTimeout(() => {
    console.log("\n🤖 AI Response (MOCK):");
    console.log("--------------------------------");
    console.log("1. Works on frontend (UI)");
    console.log("2. Works on backend (server & APIs)");
    console.log("3. Connects database and deploys applications");
    console.log("--------------------------------");
    console.log("✅ Completed successfully (mock response)");
  }, 1200);
}

// ------------------------------
// REAL AI CALL
// ------------------------------
async function askAI(question) {
  try {
    console.log("\n📤 Sending to AI:", question);

    const response = await openai.responses.create({
      model: "gpt-4.1-mini",
      input: question,
    });

    const aiReply = response.output_text;

    console.log("\n🤖 AI Response:");
    console.log("--------------------------------");
    console.log(aiReply);
    console.log("--------------------------------");

  } catch (error) {
    console.log("\n❌ OpenAI API failed:", error.message);

    // If quota error → fallback automatically
    if (error.status === 429 || error.code === "insufficient_quota") {
      mockAI(question);
    } else {
      console.log("⚠️ Unknown error occurred");
    }
  }
}

// ------------------------------
// TEST CALL
// ------------------------------
askAI("Summarize what a full-stack developer does in 3 bullet points.");