# `docs/tickets/`

Project tickets live here — one file per ticket, YAML frontmatter + markdown body.

## Convention

The ticket schema is inherited from praxis. It lives in the substrate:

- **Schema + status vocabulary + template:** `docs/agentic-ai/tickets/` (inherited from praxis `agentic-os/tickets/` at bootstrap).
- **CLI scripts:** `scripts/tickets/` — CRUD, board view, status transitions.
- **Locked status vocabulary:** see `VOCAB.md` §"Ticket status vocabulary" — 8 active states + 6 terminal states.

## Rules of thumb

- **One ticket = one actionable item.** Bugs that surface a class-of-bug still get one ticket; the class expansion happens inside the `/bug` pipeline, not by opening more tickets upfront.
- **Every code-touching pipeline anchors to a ticket ID.** If a change ships without a ticket, either the ticket wasn't created (fix intake) or the change is trivial ("just" / "quick" prefix).
- **Move to `shipped/` on close.** Terminal-state tickets move out of the active flat directory to keep the working set small.

## See also

- **Praxis abstract:** `docs/agentic-ai/tickets/` — schema, template, transitions
- **Praxis skills:** `/intake` creates tickets; `/bug` operates on them; `consolidate` sweeps them
- **Vocabulary:** `VOCAB.md` §7 — ticket status states
