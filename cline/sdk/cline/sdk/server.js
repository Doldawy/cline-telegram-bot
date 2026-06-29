import express from "express";
import { Agent } from "@cline/sdk";

const app = express();
app.use(express.json());

const clineAgent = new Agent({
  model: "gpt-4o-mini",
  tools: [],
});

app.post("/run", async (req, res) => {
  const { prompt } = req.body;
  try {
    const result = await clineAgent.run(prompt);
    res.json({ ok: true, result });
  } catch (err) {
    res.json({ ok: false, error: err.message });
  }
});

app.listen(7070, () => {
  console.log("Cline SDK server running on port 7070");
});
