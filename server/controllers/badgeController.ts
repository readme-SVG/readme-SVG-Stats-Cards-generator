/**
 * Badge Controller
 * Handles HTTP requests for badge generation, icon listing, and icon upload.
 * Follows DenverCoder1/custom-icon-badges controller pattern.
 */

import { Request, Response } from "express";
import {
  generateBadge,
  BadgeParams,
  PRESETS,
  getAvailableStyles,
  getAvailableThemes,
  getAvailableIcons,
  getAvailableSizes,
} from "../services/badgeRenderer";
import { listIcons, addCustomIcon, resolveIcon } from "../services/iconService";

/**
 * GET /badge
 * Generate a badge SVG from query parameters.
 *
 * Query params: label, value, icon, style, theme, size, scale,
 *   labelBg, valueBg, labelColor, valueColor, borderColor,
 *   borderRadius, gradient, uppercase, compact, iconData
 */
export function getBadge(req: Request, res: Response): void {
  try {
    const q = req.query;

    // Resolve preset if specified
    let base: BadgeParams = {};
    if (typeof q.preset === "string" && PRESETS[q.preset]) {
      const p = PRESETS[q.preset];
      base = { label: p.label, value: p.value, icon: p.icon, style: p.style, theme: p.theme, size: p.size };
    }

    // Resolve icon — if an icon slug maps to a custom icon, inject as iconData
    let iconData = typeof q.iconData === "string" ? q.iconData : undefined;
    const iconSlug = typeof q.icon === "string" ? q.icon : base.icon;
    if (iconSlug && !iconData) {
      const resolved = resolveIcon(iconSlug);
      if (resolved?.type === "custom") {
        iconData = resolved.data;
      }
    }

    const params: BadgeParams = {
      ...base,
      label:        typeof q.label        === "string" ? q.label        : base.label,
      value:        typeof q.value        === "string" ? q.value        : base.value,
      icon:         typeof q.icon         === "string" ? q.icon         : base.icon,
      iconData,
      style:        typeof q.style        === "string" ? q.style        : base.style,
      theme:        typeof q.theme        === "string" ? q.theme        : base.theme,
      size:         typeof q.size         === "string" ? q.size         : base.size,
      scale:        typeof q.scale        === "string" ? parseFloat(q.scale) : undefined,
      labelBg:      typeof q.labelBg      === "string" ? q.labelBg      : undefined,
      valueBg:      typeof q.valueBg      === "string" ? q.valueBg      : undefined,
      labelColor:   typeof q.labelColor   === "string" ? q.labelColor   : undefined,
      valueColor:   typeof q.valueColor   === "string" ? q.valueColor   : undefined,
      borderColor:  typeof q.borderColor  === "string" ? q.borderColor  : undefined,
      borderRadius: typeof q.borderRadius === "string" ? parseInt(q.borderRadius, 10) : null,
      gradient:     q.gradient  === "true" || q.gradient  === "1",
      uppercase:    q.uppercase === "true" || q.uppercase === "1",
      compact:      q.compact   === "true" || q.compact   === "1",
    };

    const svg = generateBadge(params);

    res.setHeader("Content-Type", "image/svg+xml");
    res.setHeader("Cache-Control", "public, max-age=300");
    res.send(svg);
  } catch (err) {
    const errorSvg = generateBadge({ label: "error", value: "badge generation failed", theme: "dark", style: "flat" });
    res.status(500).setHeader("Content-Type", "image/svg+xml").send(errorSvg);
  }
}

/**
 * GET /badge/:label-:value
 * Shields.io-compatible URL format.
 * e.g., /badge/build-passing?style=flat&theme=terminal
 */
export function getBadgeByPath(req: Request, res: Response): void {
  const pathSegment = req.params[0] || "";
  const lastDash = pathSegment.lastIndexOf("-");

  let label: string;
  let value: string;
  if (lastDash > 0) {
    label = pathSegment.slice(0, lastDash);
    value = pathSegment.slice(lastDash + 1);
  } else {
    label = pathSegment || "label";
    value = "value";
  }

  // Decode URL-encoded spaces (use __ or %20 for spaces)
  label = label.replace(/__/g, " ");
  value = value.replace(/__/g, " ");

  req.query.label = label;
  req.query.value = value;
  getBadge(req, res);
}

/**
 * GET /list.json
 * Returns available icons, styles, themes, and presets.
 */
export function listIconsJSON(_req: Request, res: Response): void {
  const icons = listIcons();
  res.json({
    icons,
    styles: getAvailableStyles(),
    themes: getAvailableThemes(),
    sizes: getAvailableSizes(),
    presets: PRESETS,
  });
}

/**
 * POST /icon
 * Upload a custom icon.
 * Body: { slug: string, type: string, data: string }
 */
export function postIcon(req: Request, res: Response): void {
  const { slug, type, data } = req.body || {};

  if (!slug || !type || !data) {
    res.status(400).json({ error: "Missing required fields: slug, type, data" });
    return;
  }

  if (data.length > 200_000) {
    res.status(414).json({ error: "Icon data too large" });
    return;
  }

  const result = addCustomIcon(slug, type, data);
  if (!result.success) {
    res.status(409).json({ error: result.error });
    return;
  }

  res.status(201).json({ message: `Icon "${slug}" added successfully` });
}
