// // routes/users.js
// // Mock user data — same structure as if it came from a real database

// const express = require("express");
// const router = express.Router();

// // In real projects this comes from MongoDB/PostgreSQL
// // For now we simulate it — same logic applies
// const mockUsers = [
//   { id: 1, name: "Aura", role: "developer", skills: ["Java", "React"] },
//   { id: 2, name: "Riya", role: "designer", skills: ["Figma", "CSS"] },
//   { id: 3, name: "Arjun", role: "devops", skills: ["Docker", "AWS"] },
// ];

// // GET all users
// router.get("/", (req, res) => {
//   res.json({
//     success: true,
//     count: mockUsers.length,
//     data: mockUsers,
//   });
// });

// // GET single user by ID
// router.get("/:id", (req, res) => {
//   const userId = parseInt(req.params.id);
//   const user = mockUsers.find((u) => u.id === userId);

//   if (!user) {
//     return res.status(404).json({ success: false, error: "User not found" });
//   }

//   res.json({ success: true, data: user });
// });

// // POST create a user
// router.post("/", (req, res) => {
//   const { name, role, skills } = req.body;

//   // Basic validation — always validate input
//   if (!name || !role) {
//     return res.status(400).json({
//       success: false,
//       error: "Name and role are required",
//     });
//   }

//   const newUser = {
//     id: mockUsers.length + 1,
//     name,
//     role,
//     skills: skills || [],
//   };

//   mockUsers.push(newUser);

//   res.status(201).json({ success: true, data: newUser });
// });

// module.exports = router;



const express = require("express");

const router = express.Router();

const mockUsers = [
  {
    id: 1,
    name: "Aura",
    role: "developer",
  },
  {
    id: 2,
    name: "Riya",
    role: "designer",
  },
];

// GET all users
router.get("/", (req, res) => {
  res.json({
    success: true,
    data: mockUsers,
  });
});

module.exports = router;