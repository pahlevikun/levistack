# Screen anatomy

How to build one screen so it answers its question, holds its states and fits the platform.

## Contents
- Page or working screen
- Name the one question and the one finding
- Block list
- The shell
- Lists, tables and KPIs
- Charts
- All the states
- The phone and other widths
- Tells of generated screens

## Page or working screen

- A **page** is read and scrolled (landing, marketing, portfolio). Optimize for first impression and one memorable idea. Keep the argument visible: show the thing working.
- A **working screen** is used every day (dashboard, inbox, queue, settings, wallet, editor). Optimize for clarity, density and speed. It does not inherit page hero sizes, image quotas or invented metrics.
- A product site that shows its app is a page. The app fragments on it follow working-screen rules inside.

## Name the one question and the one finding

Every screen answers one question first: "Did today's sales come in?", "Which deploy broke?", "Who is waiting for a reply?" Write it in one line. It decides three things:

- **What is biggest.** The largest block carries the question.
- **What comes first** in reading order.
- **What is left out.** A few numbers can say what a chart would.

Then name the **one finding**: the fact in today's data that most needs attention ("9 no-shows while 8 people waited"). Put it where it is read first, next to the action it drives. A finding in a small caption at the bottom makes the screen read flat.

## Block list

List the screen's blocks as answers to its next questions, one line each. A block with no question is deleted. This avoids the stock order of KPI row, big chart, two small charts, table.

- Everything the brief names shows on the first screen (header plus first rows or the figure).
- The most frequent job is one tap away: a primary button in the title row, an action on the row that needs it.
- Put time-sensitive blocks (bills due, a failed deploy) before long tables.
- Cap long lists at 4 to 6 rows with "View all".
- Show the evidence beside the answer: one line on the event that matters beats a second chart.

Do not rebuild a studied screen. If your product is the same kind as a famous screen, copying its arrangement is the trap. Take structure from your product's own things.

## The shell

- **Navigation is designed before screens.** Choose the container by this tree:
  1. Top-level destination the user returns to, with its own state: **tab**.
  2. Drill-down with a clear parent: **push**.
  3. Self-contained create or edit task that returns when done: **modal** (page sheet on iOS).
  4. Parent must stay visible, lightweight choice, less than one screen, no inner navigation: **bottom sheet**. If it needs its own back stack, it should have been a modal.
  5. Immersive or blocking (camera, media, paywall, onboarding, sign-in): **full-screen modal** or a route group.
- Tabs: three to five, labels always visible, one word each. Two destinations need no tab bar. Six means the structure is wrong.
- No Settings tab and no Logout tab. Settings sits behind the profile.
- A center action button only when creation is the core action, and then four tabs or fewer.
- No nested tab bars. No double headers. One header owns the title.
- System back always works. Never trap the user.
- Every modal has an explicit close.
- Every detail screen is deep-linkable and lands with a sane back stack.
- A drawer is for a large secondary catalog, not for four destinations that should be tabs.
- A screen that opens more than two kinds of sheet is hiding structure in sheets.
- Write a **route tree** before code. Include sheets, deep links, Android back behavior and the number of taps to reach any core screen (two or fewer).

## Lists, tables and KPIs

- Consistent row heights. `numberOfLines` or the equivalent on every dynamic text. Virtualize past about 20 items.
- Right-align numbers and use tabular figures with fixed decimals. Units in a quieter color.
- Status marks inside rows are small pale pills with dark text of the same hue. A saturated chip with white text on every row is noise.
- Row actions: one action where it is needed, or one trailing menu. A filled bulk action for the list beats five grey buttons.
- KPI values at 24 to 40, not 48 or more. One container split by dividers reads better than four cards with icons in tinted circles.
- A delta needs its window ("+4 this week"). Zero change is grey. Do not color a zero.
- Do not put a sparkline on every number. Give the trend its own chart or leave it out.
- Counts follow the view and recompute when the filter changes.

## Charts

- Pick the chart by the question: change over time (line), compare (bar), part of whole (a few numbers or a thin ring), distribution (histogram).
- One question, one series. Use one hue per chart and neutrals for the rest.
- Three to five faint grid lines, no axis line, round ticks, no legend for a single series.
- Direct labels. Do not rely on color alone.
- An empty chart is drawn: the zero line, missing bars for empty periods. No illustration.

## All the states

A screen owes these states. Put each where it belongs.

| State | Rule |
|---|---|
| Zero | Printed in the normal style ("0", "$0") |
| Missing or not applicable | A quiet dash, never a dash at full value size |
| Loading | The final layout with each value replaced by a flat bar at real size, no layout shift. For a refresh, keep old values and update the freshness stamp |
| Empty section | Keep the frame and header. One sentence across the block and the action that fills it |
| First run | Keep the frame and title. Put the first action where the data will appear |
| Error | Inside the block that failed. One sentence on what failed and when data was last good, plus Retry. Not a full-screen banner |
| Stale | A freshness stamp with a refresh button |
| Offline | A banner and cached content, when a network layer exists |
| Limits | A bar at the true ratio, both ends labeled |

Red is a signal, not a texture. One red mark per object at most, on the failing fact.

## The phone and other widths

- Margins 16 to 20. Targets at least 44 pt on iOS and 48 dp on Android. Data at 14 or more, nothing below 11.
- **Navigation folds.** A sidebar becomes a top bar with a menu sheet, or a bottom bar of four or five destinations.
- **Tables become lists of two-line rows** below about 640 px: identity and the key number on line one, the other fields on line two in quiet type, the one action at the right. Fields move. They are never dropped.
- **Filters** collapse into one row of chips or a filter sheet. The first list row starts in the top 60 percent of the screen.
- **KPIs** become a two-column grid or a list with label left and value right. Never four squeezed columns.
- **Charts** go full width, 160 to 200 tall, three or four x labels.
- **A right rail** moves under the main column or into a tab. A rail that carries an action moves up as a one-line summary row.
- **Several panes** show one region at a time. Choosing a row pushes the detail. Back returns to the list at its scroll position.
- **Tablet and wide windows** restructure: rail or split view, master-detail, multi-column. Never stretch the phone layout. Multitasking can give a phone-width window on a tablet, so drive layout from size classes, never from the device model.
- Reading text keeps 45 to 75 characters per line.
- Keep content top-aligned. Center only empty states, sign-in and interstitials, or the screen jumps when content grows.

## Tells of generated screens

If a screen shows these, it was made on autopilot. Replace each with the thing in the right column.

| Tell | Instead |
|---|---|
| A dark tinted sidebar with a colored active pill | The sidebar on the page ground and a neutral selection |
| "Welcome back" with a wave emoji | A noun title |
| Four KPI cards each with an icon in a colored circle | One container split by dividers |
| A green delta pill on every KPI | A delta in words with its window, grey at zero |
| A gradient area chart with a dot on every point | A straight 2 px line without markers |
| A rainbow chart | One hue per chart |
| A fat donut with a total in the hole | A thin ring and a legend table |
| Zebra rows under uppercase tracked headers | Rules and alignment with quiet sentence-case headers |
| A top bar with search, a bell and an avatar on every screen | Only what the screen needs |
| Placeholder people, round vanity totals | The product's own data at real size, sums that close |
| An equal four-up grid whatever the data | A column count chosen by the item count |
| A coloured icon per category | One quiet icon set |

A screen with every tell removed and nothing in their place is a tidy template. What fills the space is the product: its own data at real size, the screen's one question answered by its biggest block.
