/**
 * Routes
 * Maps HTTP endpoints to controller handlers.
 * Follows DenverCoder1/custom-icon-badges routing pattern.
 */

import { Router } from "express";
import { getBadge, getBadgeByPath, listIconsJSON, postIcon } from "../controllers/badgeController";

const router = Router();

// Icon catalog — JSON listing of all available icons, styles, themes, presets
router.get("/list.json", listIconsJSON);

// Badge generation via query parameters
// e.g., /badge?label=build&value=passing&style=flat&theme=terminal
router.get("/badge", getBadge);

// Badge generation via path (shields.io-compatible)
// e.g., /badge/build-passing?style=flat&theme=terminal
router.get("/badge/*", getBadgeByPath);

// Custom icon upload
router.post("/icon", postIcon);

export default router;
