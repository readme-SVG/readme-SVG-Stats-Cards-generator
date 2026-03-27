# Badge Forge — SVG Custom Badge Generator

A zero-backend, production-ready badge generation toolkit for README-driven observability, release tracking, and developer workflow telemetry.

[![Vercel Deployment](https://img.shields.io/badge/Deploy-Vercel-000000?style=for-the-badge&logo=vercel)](https://readme-svg-custom-badge-generator.vercel.app)
[![Python](https://img.shields.io/badge/Python-3.10%2B-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![Flask](https://img.shields.io/badge/Flask-3.1.3-000000?style=for-the-badge&logo=flask)](https://pypi.org/project/Flask/)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue?style=for-the-badge)](LICENSE)
[![Status](https://img.shields.io/badge/Status-Client--Side%20Generator-7c3aed?style=for-the-badge)](#features)

> [!NOTE]
> This repository provides a browser-first badge generator, a TypeScript HTTP service, and Python tooling. There is no mandatory always-on backend for core usage.

# Example

<p align="center">
  <img src="https://readme-svg-custom-badge-generator.vercel.app/api/badge?label=coverage&value=98%25&style=plastic&theme=dark&size=md&icon=bolt&scale=1" alt="coverage: 98%">
  <img src="https://readme-svg-custom-badge-generator.vercel.app/api/badge?label=release&value=v2.0.0&style=outline&theme=sunset&size=lg&icon=rocket&scale=1&gradient=1" alt="release: v2.0.0">
  <img src="https://readme-svg-custom-badge-generator.vercel.app/api/badge?label=build&value=passing&style=soft&theme=terminal&size=md&icon=star&scale=1.15&borderRadius=50&gradient=1" alt="build: passing">
  <img src="https://readme-svg-custom-badge-generator.vercel.app/api/badge?label=quality&value=A%2B&style=social&theme=neon&size=lg&icon=none&scale=1.25&iconData=data%3Aimage%2Fpng%3Bbase64%2CiVBORw0KGgoAAAANSUhEUgAAACAAAAAgCAYAAABzenr0AAAFuElEQVR4AdRWe1CUVRT%2FfbursijQspDhK0cNWFF7WGM5kSjkAxEBWRVRTEVBQUFRlNeQj4xSI0V8m5oogSgoSlj2R%2BVU09Q0iVggJY8AFcRhBpDn0j03dodvv2F3malx2tn73XvPPefc3z333HOOzEY1tPtpNhme8u%2F%2FB0CttsfJYwdx5uQRnD11jPc0P5KeCrW9fb%2FtaZEFBltbY1nwYhRcyUFeTibGazTQaFzh6urCe5pTyzp%2FGpeyM7BksRYkYwkaswBmz%2FTClphorA0LhVqtxsCBA1FdU4trn1%2FH1YJC3hdev4G6%2BnrY2trCyckJq1e9g41REfCcPs0sBpkpjvA1K5EYHwvvOTMhCAKOnTiF7Tvfl7ZdREvBjl0pnGfIkCGYM3smNm%2FagOVLg0xtgT4B0ImXBQfBysoKbW1tSN1%2FEJ9mnEdB4Rcoul0sUXqr6Da3yNlzn2F%2F2iEMGjQIKpUKixYuMAlCAkAQBPj6eCOEISclpDhAG4zsnFx0dHRKNjYmdHZ2IuN8FnzmB%2BLevXLYM8ckEJ4zpnErGvNLANja2nCTy%2BVyNDU1ITYuid%2BvsaC5%2Bf0HD7EpNh6kx8bGBlNfnwJra6VETAIgfM0qvPLyS2htbUVa%2BlHU1z%2BSCFlKqK29j497rsNjmjv8fH0kohIA8%2BbOgU6nQ%2Frh48i7ctUgEBy0EPv3pRjmlg6ysi9yXUqlEgF%2B8yRiIgCOjg7cedrb29HQ0ICuri6DwHNDn8W4cWORfmCvgWbJgHziEdOlUChAV6G2V4nEZL1nh9JSuaNUVlaxt17Te4m%2Ffzs7Ozg6OELDApBo0cykquovVFfX8MPt3J4o4hYBUCjk6O7uRlHxHdz5rUTESIGn5ckTDBvmhLDVK%2FD8qJGidVOTX28VgV7TgAEDoJArRKwiADLZPwC6mQ%2BIuNjkVlExli4P5XHBxfkFjB49ilH795ezlyVnh%2BwtJQIgCAJfY0bgvfEnOXEbvyJy0k4LYoJInukWBIHL96aLAOhPLghCbx4%2BnjjRDc7s5ORU3%2F%2FwI376%2BRdOVyqt4DXDA297TWdtBh%2FTkxvKnJYz6D%2FsVARc16XTU3gvAtCl6%2BII3dxcmaM5cwb9h56nHUs2D1iAyb2cjzb2UmgtJno9EuK2IDkxDu8mxfFxTHQkwlevhA3LCcTz4qQJmMQage%2F9smhNBCB8XTTRMHLECAxjWY1Pej6EvLm5GQ%2Fr6lB85%2FceKuD%2B5lTuF0r2zilvUCNnKy%2BvQFt7G%2BcjfSOGDwc97%2FikHZym%2F4gAkHJCSDlApXqGh1E9Y0VlJUpKShEaFqkn8X7WXH%2B84e6JyVPceaPxbJ8AnMnIZBt2cB2ki8xPB6CYwAV7PrKe3tAVsDxPQSOMmdDHe5aBnpmVg%2FDIjYa5pYOFgf5YHxHOwLTjUl6%2BREwCIO3QUZSWloFy%2BprQFRg82FoiZCnBwUGNqPXreGz5%2BpubuHAxVyIqAdDY2MhzAN2jiuXz3TuT%2BR1LJM0QyCf2fvAeyJotLS349uZ3aG5ukUhJAOh03biYe5kVH5lc%2BLVXJyP3wjmWyeby%2B5RoMCJQsFmkDcCNwiuY4DaebdqMc5nZuP7lV9wSRux9V0QHDh7mhYXeEhsi12KBvy%2B8PD2g0bgY64HbeA2ofqTNozdEgOTo5FScnPjkjIRfT5BYQL9APYFI2fMRr2wok22MikRS%2FFYkbN2MuK0xhpawbTOSEmKRnBQH2lwQBJT98Sf2pR7A8ZOnSVWfzSQAksplnhsRFYPL%2Bde4Ca1Zie7i4sysMR%2BBAX689%2FfzxdgxY3gQo1PnsUAVyWTyrxWSCpPNLAAdS0wNDY%2Bxa%2FeHmPqWF7x9F6C8ogKVLMVSmqVGtd%2Fdu2WY56eFh5c3UvaksnriMS9sTO7OFs0CYDyif11dPbSLQxCgXQK%2FwCD4s14bFIIlIatY7dj%2F8q3fAERo%2FoXJfw7AHMa%2FAQAA%2F%2F%2F85%2BuRAAAABklEQVQDAKR2Lt85fDe3AAAAAElFTkSuQmCC&labelBg=%230d1117&valueBg=%23ff8080&labelColor=%23ff8080&valueColor=%23000000&borderColor=%23ffffff&borderRadius=0" alt="quality: A+">
  <img src="https://readme-svg-custom-badge-generator.vercel.app/api/badge?label=docs&value=stable&style=social&theme=light&size=md&icon=docs&scale=1" alt="docs: stable">
  <img src="https://readme-svg-custom-badge-generator.vercel.app/api/badge?label=docs&value=stable&style=social&theme=light&size=md&icon=none&scale=1&iconData=data%3Aimage%2Fpng%3Bbase64%2CiVBORw0KGgoAAAANSUhEUgAAACAAAAAgCAYAAABzenr0AAAFxklEQVR4AZRVC2xURRQ9b5d%2BQLpbEAJYY%2FioaaWR1g8FVrptsPz%2FjRhTEakQQ6RBUlMLjVihhSIfhWIUMEIgVSMBCyQgSIQtNFgxFAuxIMRiRSiyBZbWtnQ%2F49x5ffve7nu73W7mztzPmbnnzs7MMyGC36ODp7G8pJUsAmiPIRERcBaU49MRM3u8eCQTuidgsTNp%2BE2YDqcBlWeYkP1VDIMmMljT10WSJBwmNAGeeFV9I8OeUrBZNkgHq8XYNHk0YObTls8HViwuRNleBo4NlyRcjK8UFI7PiKcqi3%2FZi9VXGkVSLWJQTJTOh5WLtJAe6YEELPYO7C65V5z4BIov65PTLiirn7QlIymut2wWzjfLCu%2Bt6RO31CcyDM2I5VZgo52ypp%2FSOgMJADEUpOT5TyaQKqT5fgvQ1gG4WnDqzAUhFCgaaAUK50tc93ER7dXClmOWqAQUbG1uFw61k5iLckv8P1SdgQQeOCQsKNqAN4qwceRQkYgSDth%2BEGi8BdxyIrP6kn%2F26%2FOyKLnfJmXc7HYkWecg4Sk3As5G5RnflMoqXoSjD%2BEUCSRAXpejAJyI1M%2BeTWbjjX%2BBtV%2F%2BTLqQdTsnZY5PlUiEreliBqezZWmDUOPcJrx5n98TIxGxeDz4YY5dR1hPQJ4C3K86QEkWvDZJ4oTGouyrDBZtA1xVx2nBIKmlafvOJWNLzW1S0Vrv32mJbtKD3A%2BFP7gLTSAY6fMdIxerBWMOB4T89Q7Y3%2B%2BRnkL%2BhtafkDZgKcHQL3qYGBljPtT9AV6ErnoCdE%2FAYmdULU8YQxNGvr0ASOGvMkn8K4BlumpzwPmaO7h2Phr1ru9RvqQfpA1fA6tyDZNzOMISsL05mtGW8uTAqE7C4%2FfL18UY3G3a9h3o%2F9%2B88bgIuR9KYHTqS3YIO1QXmgCvfN77D8SiYrIUJQZHyhIxUtd0%2B67%2FpuS7XwQr3oWrMytw%2FsdYfNH%2FM6w9VIWOE6eB%2BEw74Y0kJAGqnCbE9uHbzRW6josP7cZLFvV6Dnl6LjLOWXHoSDVHqK36AH%2BgLjdgXH8LYqJ82HL2Fj0AKkCjGRIYPn6cnJUD15%2Fk15CPGX1TsfOT1VyTW%2Ba0d0XF3qJL2DxwKioungXpIpo1hq6uUP2dxd7s1zWKIYFlO%2B4KyMkK%2Bc3YGpuIlLeeFz7TmjGw9c0SuncDP91co8Q5q%2BfC3DYDWD4MniM2eNz5YndoLodQ609dsBgSCAaRnVvxH2gxkig46eohtn091k%2B%2Bjl5Rm4DHYyFZMwiqk9Z7JjyX1aHzkyMsgcycNsLohEjkVqfA4%2FNh5fjpoloCeVNL4e1zGL8tjYO5NBnNba3kxtGdj4iDKYygLiwBBeu80UtR%2FWPKhA6UTsiGd029SEaJTbMeg2nRMIza1gKpeCEqsucJfOrLD%2BkhMsyld%2FLrJ2ZpuouOaI0FOL6Vz0ZZ7T6YP0gSh2%2F7bPmwsgv3YS5JRu84%2BRx3dshvUFbeC%2F4vpnYxPYGu6M1r%2Bqq7QvB5Za3k6B3keLLFGfCs2iiqNs1JgPTRQpSdkAk1%2FSmvkzhGfsjkmWofksCVGrXq4LOgtdNmtEN5M2jcOmWq36Y0yg6QbiQmnZN%2FinW%2BCB3KtTWC03fByK8nwFH8TT%2BhrZK7RDNK0NQgb7EABHX0USLXrhVWOoTyYSCHRgwJ8E9nloJp%2FsesqLqxoS4aV3%2BNFl8%2FSuZ1qzn2fRznx7c2nlYDfq%2BsGBPgMb4LYuHqSv6uc5uadldEQg8wZATvKMhl6LNuMYdi3IyohSTAd0GwfmZsp27R%2FZvU6pQsTL51iukfXc7QKQgUNlqeUydIEJCEKiMxGfwrDXXy55pwJOLx4cqeZRcC1uCugBaWACGJBAnpioy08ZdNMbpG1x11KSc%2FN3Tqg%2Bd1QQMGdVaAW2%2FQgorXaAeUGOG%2BKaiVlL9Q8YcaIyZAC1JFlMDNn9cd%2BfEoz%2BttVZ5l2nIeqyWcNll3%2Bv8AAAD%2F%2F%2F3GH48AAAAGSURBVAMAcHIY3IdWcWoAAAAASUVORK5CYII%3D&labelBg=%238a8a8a&valueBg=%236da52e&valueColor=%23000000&borderRadius=6&gradient=1" alt="docs: stable">
  <img src="https://readme-svg-custom-badge-generator.vercel.app/api/badge?label=jira&value=readme&style=pill&theme=neon&size=sm&icon=none&scale=1.55&iconData=data%3Aimage%2Fpng%3Bbase64%2CiVBORw0KGgoAAAANSUhEUgAAACAAAAAgCAYAAABzenr0AAACWUlEQVR4AeyVz0sVURTHv848exYP%2BkHk86moIBIEtWoXuAlq17%2Fgrqe1aVW8CIqKJCKoRa1qF9SmRZugTSuhcCEqLvz944n6eIiiiD71vef9joz6ZubO3DujCOLAmblz77nnfObcc84YyfRo%2BTjFwDFfpwAnJwLJ8zFca4jjaiqulVWRIjD%2FuRW29HU340%2BmEX%2BfNe7N2Wt8lsveXJEAnEaNKm8nnC0dBUBd5xhtR5JIEagSX1zfNYaJ%2FDa2i4DkI30BIwHQMkPb%2FmIaN55M4mZmCikRFUJxTUWUABI1hmdiMbnmP7Vi5H0Lel814d%2FLZsyJxNSJhBLAWqEk%2FxhxDGfPGDgXNxAzoX0pATDbVzd8IBxuqe%2BYkr4qAXB326MJjOe2OFQSVQhlAHq99XwaLL1772aR%2BZ7H0x95fOtZ4ZJL6h%2BolagLYOBti5VITCaZfOxIoqP9Ai4lTPz8v%2BpyzglGoPZ%2BMIQLoPPLAkRe%2BUrT5Rja6qrx8M5FmD6JZwjrjFhK9ApTjAnmFNd0z%2FC6U0f6viGqY2FZdCCpxu4Co7E7ct9dAFRJpoNDR72iKPjx3CaHocUTgC2Wobv9OmsZFn4822yixgQ7Yf9MwdILc%2FMEsA0NzRasrGd7pQxmKx3Zf7%2B7b7IWiL1P5%2BkLEGSodOBw2f%2BviKP78HspaFvFuhbA8FzleVebrJd9e3zt%2FrW4P6Ew0gLo%2BppTMKmnogUgq2U9l5XaWgDcWpse5ePQRBvAEDXKzpZfKYbO%2FIP02gDczOS%2F%2FngSDYo%2FHO6RSSgAmbEw8ycfICgqOwAAAP%2F%2FF1JIRQAAAAZJREFUAwCoogOQP2MTDQAAAABJRU5ErkJggg%3D%3D&labelBg=%231868db&valueBg=%23000000&labelColor=%23000000&valueColor=%230a84ff&borderRadius=0" alt="jira: readme">
  <img src="https://readme-svg-custom-badge-generator.vercel.app/api/badge?label=Codex&value=+readme-SVG-custom-badge-generator&style=social&theme=neon&size=sm&icon=none&scale=1.55&iconData=data%3Aimage%2Fpng%3Bbase64%2CiVBORw0KGgoAAAANSUhEUgAAACAAAAAgCAYAAABzenr0AAADfUlEQVR4AdRWzSttURRfvyshA%2FmYSEmKJGOFfBViioEoI%2F4rRqKEgUwohHwMDIVCFCUDykBiwHt%2BS2vfs88919231%2Bv1Tnfttfb6%2FO119t7npn794ycl%2F%2Fj5%2FwB8fn7K0NCQFBQUSCqVUqI8ODgotOXb0FRowOTkpADQwuvr61rsa%2FsIiYU3NjbUBkAmJiYk9MkJ4P39XQvPzc15OQHo6tkFABJ9FhYWNObt7S2qTpR%2FBDA9PS3FxcUuEICcnJy4VX98fAiJHWAnTk9PtbAFlJSUCHPYPIlnBcCWz8zMuJjd3V1te0tLi9PFhebmZvU5ODhwJuaYmppy87iQCOD5%2BVmiLecKu7q64rFZ5%2B3t7QrEHGZnZ%2BX19dWmHk8EUF5e7pxYHPDfsTP%2BIADwQJSWliZ6ZwDo7%2B93jufn5947dYZAAYAcHh4677GxMSebkAFgc3NTbQCkqalJZQ53d3e66ynnQ21tbW4Ri4uLGaEeAO5k87i%2BvjZReW1tre5%2BHjtV5DGcnZ0572gNKj0AAwMD1CnV1dUpt6GsrExFJuDR00ngEO1kX1%2BfF%2BUB2N7e9ozRCU%2BGzQsLC00M5sD3Rt7Z2fFiPABcHa3Z2ry6ukqzvoqjoyOV8x2shsV5AEyZja%2BtrTlTQ0ODk%2F9E8AAA323i2Y8nJXLeatQDkKqqKopK9I%2BTGhIG4LuGmTwAPT09ps%2Fg%2FOSaMroJAehXkPYoAX4hLkC%2Bnu7u7q8x%2FfMA2B1A8%2B3tLZkjS1BUVOTONY2AX4g6EpDWX1xcUKW0tbWl3AYPAJAOih9DtpiXSvwTSz3BxYl6KxI9hkC6Bu0eACp6e3vJdKdfXl6qzAHwr1XqQuj4%2BFhz0Xd0dJTMowwA0bugsbHRBXtRgRN2pbW11XkvLS052YQMADQ8PT2RKfFOYCKd5DEwhrEW8vLyYqLHEwFUVFTIyMiIc2Siq6srN88l3NzceB%2Bu8fFxCf4cW%2FLl5WUZHh62qfDiIZD7%2B3uniwsPDw9auL6%2B3pmYY35%2B3s3jQmIHzGllZUWir4Ntramp0WNIMDz35CQAUl1d7e2Zx8dHYQ7Ll8R%2FBMAAvg4Wjv8lo45HjZxEX6OOjg4FUllZaaqsPCcAi%2BSfUhZiUYKxVQPQtnd2dupfMPrs7%2B9L6BMMwBICEILhdUwwJMp7e3v6aswvlOcNIDRxqN9fB5ALyG8AAAD%2F%2F9SJJzEAAAAGSURBVAMAJonq0P%2BdcjEAAAAASUVORK5CYII%3D&labelBg=%23ffffff&valueBg=%23000000&labelColor=%23000000&valueColor=%23ffffff&borderColor=%23ffffff&borderRadius=0" alt="Codex">
  <img src="https://readme-svg-custom-badge-generator.vercel.app/api/badge?label=observability&value=-on&style=outline&theme=dark&size=md&icon=rocket&scale=1&valueColor=%2303bcf1&compact=1" alt="observability: -on">
</p>

---

## Table of Contents
- [Features](#features)
- [Tech Stack & Architecture](#tech-stack--architecture)
  - [Core Stack](#core-stack)
  - [Project Structure](#project-structure)
  - [Key Design Decisions](#key-design-decisions)
- [Getting Started](#getting-started)
  - [Prerequisites](#prerequisites)
  - [Installation](#installation)
- [Testing](#testing)
- [Deployment](#deployment)
- [Usage](#usage)
  - [Basic Usage](#basic-usage)
- [Configuration](#configuration)
- [License](#license)
- [Support the Project](#support-the-project)

## Features

- Deterministic SVG rendering across JavaScript (`app.js`), TypeScript server (`server/services/badgeRenderer.ts`), and Python (`api/github_stats.py`).
- Multiple rendering profiles (`flat`, `flat-square`, `for-the-badge`, `plastic`, `social`, `rounded`, `pill`, `outline`, `soft`).
- Theme-aware palette model with overridable segment and text colors.
- Preset system optimized for common operational and release telemetry (`build`, `coverage`, `release`, `docs`, `quality`).
- Built-in icon registry plus custom icon upload/data URI support.
- Shields.io-compatible path endpoint (`/badge/<label>-<value>`) for URL-based embedding workflows.
- Query-based endpoint with rich parameterization (`/badge?...`) for runtime badge synthesis.
- Safe defaults and input guards (hex color validation, bounded scaling, icon payload limits).
- Optional gradient overlays, uppercase rendering, compact mode, and rounded geometry control.
- Static frontend delivery compatible with Vercel, plus optional Express service for API workflows.
- Local CLI utility (`process_event.py`) for scripted generation in CI/CD.
- Sample artifact regeneration workflow for reproducible visual baselines.

> [!TIP]
> Use the web app for interactive badge design, then promote stable output into versioned SVG artifacts in your repository.

## Tech Stack & Architecture

### Core Stack

- `JavaScript` + `HTML` + `CSS` for the browser rendering surface.
- `TypeScript` + `Express` for optional HTTP badge generation APIs.
- `Python 3.10+` for CLI and script-driven SVG generation.
- `Vercel` for static hosting/deployment.
- `GitHub Actions` for repository automation workflows.

### Project Structure

<details>
<summary>Expand file tree</summary>

```text
.
├── api/
│   ├── badge.js
│   ├── data_fetchers.py
│   └── github_stats.py
├── scripts/
│   └── refresh_sample_svgs.py
├── sample_svgs/
│   ├── sample_build.svg
│   ├── sample_coverage.svg
│   ├── sample_docs.svg
│   ├── sample_quality.svg
│   └── sample_release.svg
├── server/
│   ├── controllers/
│   │   └── badgeController.ts
│   ├── routes/
│   │   └── routes.ts
│   ├── services/
│   │   ├── badgeRenderer.ts
│   │   └── iconService.ts
│   ├── index.ts
│   ├── package.json
│   └── tsconfig.json
├── trigger action/
│   └── trigger_action.py
├── app.js
├── index.html
├── process_event.py
├── requirements.txt
├── styles.css
├── vercel.json
└── README.md
```

</details>

### Key Design Decisions

1. **Renderer parity over single-language lock-in**
   - Rendering logic is intentionally mirrored between browser JS, server TS, and Python to keep output stable across usage modes.
2. **Static-first default architecture**
   - Core user workflow requires only static assets; backend services are additive, not mandatory.
3. **Composable style system**
   - Style profile + theme palette + runtime overrides provide extensibility without engine rewrites.
4. **Operational safety controls**
   - Input constraints and icon payload limits reduce rendering abuse and oversized SVG outputs.

```mermaid
flowchart LR
    A[User Input: preset/label/value] --> B[Normalize Params]
    B --> C{Runtime Path}
    C -->|Browser| D[app.js Renderer]
    C -->|API| E[Express Controller]
    E --> F[badgeRenderer.ts]
    C -->|CLI| G[process_event.py]
    G --> H[github_stats.py]
    D --> I[SVG Output]
    F --> I
    H --> I
    I --> J[README Embed / CI Artifact / Download]
```

<details>
<summary>Architecture deep-dive: endpoint behavior and request lifecycle</summary>

- `GET /badge`: Consumes query parameters and returns `image/svg+xml`.
- `GET /badge/*`: Parses path format (`label-value`) and delegates to the same generation pipeline.
- `GET /list.json`: Returns runtime catalog (icons, styles, themes, sizes, presets).
- `POST /icon`: Registers custom icon payloads with request-rate limiting and size guards.
- GET responses are emitted with short caching headers (`max-age=300`) for predictable refresh behavior.

</details>

> [!IMPORTANT]
> For reproducibility, prefer pinned presets and checked-in SVG files over purely dynamic badge URLs.

## Getting Started

### Prerequisites

- `Node.js >= 18` (for TypeScript server mode).
- `npm` (for server dependencies/build).
- `Python >= 3.10` + `pip` (for CLI and script workflows).
- Modern browser for interactive UI usage.

### Installation

```bash
git clone https://github.com/OstinFCT/readme-SVG-custom-badge-generator.git
cd readme-SVG-custom-badge-generator
```

Install Python dependencies (optional but recommended):

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

Install server dependencies (optional API mode):

```bash
cd server
npm install
cd ..
```

Run static UI locally:

```bash
python -m http.server 8080
```

Open `http://localhost:8080`.

<details>
<summary>Troubleshooting and alternative setup paths</summary>

- If `python` resolves to Python 2, use `python3`.
- If `npm install` fails due to engine mismatch, verify `node -v` is `18+`.
- To run server mode in development:
  ```bash
  cd server
  npm run dev
  ```
- To run production server build:
  ```bash
  cd server
  npm run build
  npm start
  ```

</details>

## Testing

Run deterministic checks locally:

```bash
python -m py_compile api/github_stats.py api/data_fetchers.py process_event.py scripts/refresh_sample_svgs.py
python scripts/refresh_sample_svgs.py
python process_event.py --label build --value passing --style flat --theme terminal --output badge-smoke.svg
```

Run server build validation:

```bash
cd server
npm run build
cd ..
```

Optional style/lint checks:

```bash
black .
flake8 .
```

> [!WARNING]
> A full unit/integration test suite is not yet present; current validation is generation-oriented and compile/build oriented.

## Deployment

### Static Deployment (Recommended)

Use Vercel to publish the frontend artifact directly:

```bash
vercel
vercel --prod
```

### Server Deployment (Optional)

```bash
cd server
npm install
npm run build
npm start
```

Expose port `5000` (or set `PORT`) in your runtime environment.

### CI/CD Integration Guidance

- Add a Python compile + sample regeneration stage.
- Add TypeScript build checks for server integrity.
- Enforce clean working tree after artifact generation (`git diff --exit-code`).

> [!CAUTION]
> Dynamic badge endpoints are cacheable and externally consumable; review rate-limits and payload controls before public exposure.

## Usage

### Basic Usage

Generate a badge through the HTTP API:

```bash
curl "http://localhost:5000/badge?label=logging&value=healthy&style=flat&theme=terminal" -o logging-health.svg
```

Generate a badge through CLI:

```bash
python process_event.py \
  --label "logging" \
  --value "stable" \
  --icon "check" \
  --style "for-the-badge" \
  --theme "terminal" \
  --gradient \
  --output "logging-status.svg"
```

Embed in GitHub Markdown:

```markdown
![logging status](./logging-status.svg)
```

<details>
<summary>Advanced Usage: query parameters, custom formatters, and edge cases</summary>

### Query-driven customization

```bash
curl "http://localhost:5000/badge?label=logs&value=ingest%20ok&icon=rocket&style=pill&theme=neon&size=lg&uppercase=1&compact=1"
```

### Path format for Shields-style URLs

```bash
curl "http://localhost:5000/badge/logs-ingest__ok?style=flat-square&theme=dark"
```

### JavaScript integration example

```js
const svg = generateBadge({
  label: 'logging',
  value: 'rate limited',
  style: 'outline',
  theme: 'dark',
  borderColor: '#ef4444',
  compact: true,
});

console.log(svg);
```

### Edge-case guidance

- Keep label/value strings concise to avoid oversized visual output.
- Use hex colors only (`#RRGGBB`) for reliable fallback behavior.
- For custom icons, validate MIME and keep base64 payloads small.

</details>

## Configuration

Runtime controls can be applied via query params, CLI flags, and optional environment variables.

### Environment Variables

| Variable | Required | Scope | Purpose | Example |
|---|---|---|---|---|
| `PORT` | No | Server | Express listen port | `5000` |
| `PYTHONPATH` | No | Tooling | Import path extension for scripts | `./api` |

### Startup Flags (`process_event.py`)

| Flag | Type | Default | Description |
|---|---|---|---|
| `--label` | string | `build` | Left segment text |
| `--value` | string | `passing` | Right segment text |
| `--icon` | string | `check` | Icon key |
| `--style` | string | `flat` | Style profile |
| `--theme` | string | `dark` | Palette theme |
| `--output` | path | `badge.svg` | Output file |
| `--uppercase` | flag | `false` | Force uppercase output |
| `--compact` | flag | `false` | Condensed width layout |
| `--gradient` | flag | `false` | Gradient overlay |

<details>
<summary>Exhaustive HTTP configuration matrix</summary>

| Parameter | Type | Default | Allowed Values / Constraints | Notes |
|---|---|---|---|---|
| `preset` | string | none | `build`, `coverage`, `release`, `docs`, `quality` | Seeds baseline values |
| `label` | string | `build` | max ~40 chars | Left segment content |
| `value` | string | `passing` | max ~52 chars | Right segment content |
| `icon` | string | `none` | Built-in key or custom slug | Resolved via icon service |
| `iconData` | string | none | data URI, size-limited | Prefer validated payloads |
| `style` | string | `flat` | profile keys in renderer | Impacts height, radius, weight |
| `theme` | string | `dark` | theme keys in renderer | Provides fallback palette |
| `size` | string | `md` | `xs`,`sm`,`md`,`lg`,`xl` | Base scale multiplier |
| `scale` | float | `1.0` | clamped `0.7..2.0` | Additional width/height scaling |
| `labelBg` | hex color | theme-derived | `#RRGGBB` | Left background override |
| `valueBg` | hex color | theme-derived | `#RRGGBB` | Right background override |
| `labelColor` | hex color | theme-derived | `#RRGGBB` | Left text override |
| `valueColor` | hex color | theme-derived | `#RRGGBB` | Right text override |
| `borderColor` | hex color | theme-derived | `#RRGGBB` | Used by bordered styles |
| `borderRadius` | int | style-defined | clamped `0..999` | Optional custom radius |
| `gradient` | bool | `false` | `1/true` or `0/false` | Adds glossy overlay |
| `uppercase` | bool | `false` | `1/true` or `0/false` | Forces upper-case text |
| `compact` | bool | `false` | `1/true` or `0/false` | Reduces padding footprint |

</details>

## License

This project is licensed under the MIT License. See [`LICENSE`](LICENSE) for complete terms.

## Support the Project

[![Patreon](https://img.shields.io/badge/Patreon-OstinFCT-f96854?style=flat-square&logo=patreon)](https://www.patreon.com/OstinFCT)
[![Ko-fi](https://img.shields.io/badge/Ko--fi-fctostin-29abe0?style=flat-square&logo=ko-fi)](https://ko-fi.com/fctostin)
[![Boosty](https://img.shields.io/badge/Boosty-Support-f15f2c?style=flat-square)](https://boosty.to/ostinfct)
[![YouTube](https://img.shields.io/badge/YouTube-FCT--Ostin-red?style=flat-square&logo=youtube)](https://www.youtube.com/@FCT-Ostin)
[![Telegram](https://img.shields.io/badge/Telegram-FCTostin-2ca5e0?style=flat-square&logo=telegram)](https://t.me/FCTostin)

If you find this tool useful, consider leaving a star on GitHub or supporting the author directly.
