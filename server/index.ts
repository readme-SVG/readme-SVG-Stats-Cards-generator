/**
 * Badge Forge — Server
 * Express server for URL-based badge generation.
 * Architecture inspired by DenverCoder1/custom-icon-badges.
 *
 * Features:
 *   - SVG badge generation via URL (query params or path-based)
 *   - Cache-Control headers for GET requests
 *   - Rate limiting for POST endpoints
 *   - Static file serving for the frontend app
 */

import express, { Request, Response, NextFunction } from "express";
import path from "path";
import rateLimit from "express-rate-limit";
import router from "./routes/routes";

const app = express();
const PORT = parseInt(process.env.PORT || "5000", 10);

// ── JSON body parsing ──
app.use(express.json({ limit: "256kb" }));

// ── Rate limiting for POST requests (icon uploads) ──
const postLimiter = rateLimit({
  windowMs: 5 * 60 * 1000, // 5 minutes
  max: 10,
  message: { error: "Too many requests, please try again later" },
  standardHeaders: true,
  legacyHeaders: false,
});
app.post("*", postLimiter);

// ── Cache-Control headers ──
app.use((req: Request, res: Response, next: NextFunction) => {
  if (req.method === "GET") {
    res.setHeader("Cache-Control", "public, max-age=300");
  } else {
    res.setHeader("Cache-Control", "no-store");
  }
  next();
});

// ── CORS headers ──
app.use((_req: Request, res: Response, next: NextFunction) => {
  res.setHeader("Access-Control-Allow-Origin", "*");
  res.setHeader("Access-Control-Allow-Methods", "GET, POST, OPTIONS");
  res.setHeader("Access-Control-Allow-Headers", "Content-Type");
  next();
});

// ── API routes ──
app.use("/", router);

// ── Static files — serve the frontend app ──
const staticRoot = path.resolve(__dirname, "..");
app.use(express.static(staticRoot, { extensions: ["html"] }));

// ── Fallback to index.html for SPA ──
app.get("*", (_req: Request, res: Response) => {
  res.sendFile(path.join(staticRoot, "index.html"));
});

// ── Start ──
app.listen(PORT, () => {
  console.log(`Badge Forge server running on http://localhost:${PORT}`);
  console.log(`Badge endpoint: http://localhost:${PORT}/badge?label=build&value=passing`);
  console.log(`Path endpoint:  http://localhost:${PORT}/badge/build-passing`);
  console.log(`Icon catalog:   http://localhost:${PORT}/list.json`);
});

export default app;
