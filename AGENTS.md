# Agent instructions

These instructions apply to every agent working in this repository. `CLAUDE.md`
imports this file.

## What Wyvro is

Wyvro is Alex's own name for a set of small tools for tabletop players:
Dungeons & Dragons and Magic: The Gathering. Every project lives in this one
repository. It was started on 26 November 2026 and has no application code yet.
The working slogan is "Tools for Nerds" (Alex, 27 November 2026).

It has two purposes, in this order:

1. **To build real things in React, TypeScript and Node.** Alex is a Ruby on
   Rails engineer of seven years and is learning this stack by directing the
   work, so the code should be the plain, conventional version of each idea.
2. **To be useful to players**, and perhaps earn a little later.

## The projects, in build order

0. **The site itself.** Before any tool: the Wyvro home page, built, tested
   and live, so that the layout of the repository, the libraries, the checks
   and the hosting are all settled on something small (Alex, 27 November
   2026). Its plan was agreed on 27 November 2026 and its tickets are in
   Linear, in the project "The Wyvro site".
1. **Character sheets.** A D&D character sheet you create by following a flow:
   the character's stats, colours, perhaps a font, and a picture, all editable
   afterwards. It is a rebuild of Alex's 2022 Rails app, which is public at
   `github.com/alexmiller64/character_sheets` (Rails 7.0, eleven
   ViewComponents, Tailwind, Turbo, one Stimulus controller, one `Character`
   model in Postgres). That app is static and shows one character. Keep it as
   the thing to compare against: clone it to read, do not copy it in here.
2. **Commander life counter** for Magic: The Gathering. Nothing decided yet. It
   can probably run entirely in the browser with no server.
3. **Card inventory** for Magic: The Gathering. Record the cards someone owns,
   filter them heavily (colour, type, set and more), and show each card's price
   and price trend from Cardmarket. Not yet checked: whether Cardmarket's own
   pricing service takes new users. Scryfall's free card database may carry
   Cardmarket's euro prices; confirm before designing around either.
4. **Office Box.** A pixel-art office for directing a team of AI agents.
   **Parked**: an open-source tool, Pixel Agents, already does it apart from
   the voices. Do not plan or build it unless Alex brings it back.

## Decided

- **The stack is React and TypeScript in the browser and Node on the server.**
  That choice is the point of the project and is not open.
- **One site, with a section for each tool**: `wyvro.com/sheets`,
  `wyvro.com/life`, `wyvro.com/cards` (Alex, 27 November 2026; this replaces
  the earlier idea of an address per tool). The tools then share one security
  policy and one browser storage area, so the card inventory's plan looks at
  this again.
- **The repository is public to read and closed to outside contributions**
  (27 November 2026): no pull requests or issues from outside, no licence on
  the code for now. An interviewer can read all of it.
- **Alex merges every pull request. No agent merges, ever.** The agents get a
  GitHub account of their own once the site is live, so that GitHub enforces
  this.
- **The name stays Wyvro** (27 November 2026). The site goes live without
  being announced. The name and the colours are each written in one place in
  the code, so a change of name stays a small change.
- **No analytics for now.** The site loads nothing from another address and
  sets no cookies.
- **Websites first, not app-store apps.** No store fees and no review.
  Store apps for Apple and Google may follow once the site is built out (Alex,
  27 November 2026), most likely by wrapping the same React code. So every
  plan keeps that door open: the pages run in the browser and talk to the
  server through an API, and a tool that makes sense at a table works without
  a connection.
- **Hosting should cost nothing to start.** The intent, to be confirmed against
  each service's current terms when it is set up: Cloudflare Pages for the web
  pages, Render for a Node server, Neon for Postgres. Not Vercel's free plan,
  which is for non-commercial use only.
- **Tickets live in Linear**, in the Wyvro workspace (ticket key `WYV`).
- **Security is built in from the start, in three layers** (agreed 27 November
  2026):
  1. Every plan has a section on what could go wrong, and a security reviewer
     reads the plan.
  2. GitHub's automatic checks are on from the first push: secret scanning
     that blocks a push, alerts for vulnerable packages, code scanning, a
     protected `main`. Confirm what is free for this repository when it is
     created.
  3. A security reviewer agent reads every pull request in a fresh context
     before Alex merges, and tours the staging site as an attacker on a QA
     day. A new package is a decision it checks: agents can mistype or invent
     package names, and attackers register those names.
- **The work is tested as it was on Alex's Rails projects**: unit tests, tests
  that drive a real browser, and screenshots on every pull request that
  changes what a page looks like. Which tools do this is in the list below.

## Not decided yet

The plan for the first project settles these. Do not assume an answer:

- How the repository is laid out for several projects, and what they share.
- Which libraries: the build tool, the server framework, the test runner, how
  styles are written.
- What the checks are before a change is merged, and who merges.
- For the character sheets: which edition of the rules, whether people sign
  in, and where pictures are stored.

## Rules that apply to every project

- **Wizards of the Coast owns both games.** Its Fan Content Policy allows
  adverts, sponsorship and donations, and does not allow selling fan content or
  putting Wizards' material behind a payment. Anything paid must be a feature
  of ours (storage, exports), never card images or rules text. Read the current
  policy before adding anything that earns money:
  `https://company.wizards.com/en/legal/fancontentpolicy`.
- **Never commit a secret.** Keys and tokens go in `.env` files, which are
  ignored.
- **Plan before code.** A project starts with a written plan that Alex has
  agreed, then tickets, then code.

## How Alex works with agents

- **Agents write the code.** Alex directs, reads and decides; he does not type
  it by hand.
- **Explain as you build.** Before a stage, say in plain English what is about
  to be built and why, using the Rails equivalent where there is one. After it,
  walk him through the files that matter.
- **Write to him in plain English**, with full URLs and commands he can paste.

## The QA and develop skills

`.agents/skills/qa` and `.agents/skills/develop` hold the method for a QA day
and a build day, and `.claude/hooks/` holds the scripts that read agents'
reports aloud. **They were copied from another project and have not been
rewritten for this one**: they still name that project's commands, its staging
site and its tickets, and the QA skill's reference file for hosts and logins
has no Wyvro version yet. Until they are rewritten they are kept out of git
(`.git/info/exclude`). Do not commit them, and do not remove that exclusion,
before the rewrite.

One file in `.claude/` is committed: `.claude/settings.json`. It makes Claude
Code refuse `gh pr merge` and any change to the branch rules, so an agent
cannot merge by mistake. Only Alex changes it.
