# Session: 2026-06-28 — Mejoras TUI BRM

## Estado actual
- Logo ASCII cambiado de BBM → BRM
- Agregado Footer con keybindings en todas las pantallas (estilo Opencode)
- Navegación mejorada: F1-F7 para acceso directo a cada pantalla desde Home
- Keybindings consistentes: `H` → Home, `Esc` → Home, `Ctrl+Q` → Salir
- Nueva pantalla **Dashboard** (F1): métricas del workspace (repos, PRs abiertos, activos, stale)
- 7 tarjetas en Home: Dashboard, Repos, Permisos, PRs, Migración, Archive, Deps
- Target: devs y líderes técnicos

## Atajos globales
| Tecla | Acción |
|-------|--------|
| `H` / `Esc` | Home |
| `Ctrl+Q` | Salir |
| `D` | Dashboard |
| `R` | Repos |
| `P` | Permisos |
| `U` | PRs |
| `M` | Migración |
| `A` | Archive |
| `S` | Dependencias |

## Files
`src/bbm/tui/dashboard_screen.py` — nueva pantalla de métricas
