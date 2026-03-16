/**
 * Icon Service
 * Manages built-in and custom icon resolution.
 * Follows DenverCoder1/custom-icon-badges IconsService pattern.
 */

export interface IconEntry {
  slug: string;
  type: string;
  data: string;
}

// Built-in icon set — unicode characters used directly in SVG text
const BUILTIN_ICONS: Record<string, string> = {
  none: "", star: "\u2605", heart: "\u2764", check: "\u2713",
  fire: "\uD83D\uDD25", bolt: "\u26A1", rocket: "\uD83D\uDE80",
  code: "\u2318", build: "\u2699", docs: "\uD83D\uDCD8",
};

// In-memory store for custom uploaded icons (can be replaced with DB)
const customIcons: Map<string, IconEntry> = new Map();

export function getBuiltinIcon(slug: string): string | null {
  return BUILTIN_ICONS[slug] ?? null;
}

export function getCustomIcon(slug: string): IconEntry | null {
  return customIcons.get(slug) ?? null;
}

export function resolveIcon(slug: string): { type: "builtin"; char: string } | { type: "custom"; data: string } | null {
  const builtin = getBuiltinIcon(slug);
  if (builtin !== null) {
    return { type: "builtin", char: builtin };
  }

  const custom = getCustomIcon(slug);
  if (custom) {
    return { type: "custom", data: custom.data };
  }

  return null;
}

export function addCustomIcon(slug: string, type: string, data: string): { success: boolean; error?: string } {
  if (!slug || !type || !data) {
    return { success: false, error: "Missing required fields: slug, type, data" };
  }

  if (slug.length > 64) {
    return { success: false, error: "Slug too long (max 64 characters)" };
  }

  if (data.length > 200_000) {
    return { success: false, error: "Icon data too large (max 200KB)" };
  }

  // Check if slug is reserved by built-in icons
  if (slug in BUILTIN_ICONS) {
    return { success: false, error: `Slug "${slug}" is reserved by a built-in icon` };
  }

  if (customIcons.has(slug)) {
    return { success: false, error: `Slug "${slug}" already exists` };
  }

  customIcons.set(slug, { slug, type, data });
  return { success: true };
}

export function listIcons(): { builtin: string[]; custom: IconEntry[] } {
  return {
    builtin: Object.keys(BUILTIN_ICONS),
    custom: Array.from(customIcons.values()),
  };
}
