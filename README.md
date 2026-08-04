# To Cook Or Be Cooked 🍳

USYD WAM/EIHWAM academic planning tool.

## Data model

Upload a CSV containing these columns:

`Unit, Semester, Level, CP, Mark, Projected Mark, Status, Attempt, Degree`

- Use `Status=Completed` and enter the actual `Mark` for completed units.
- Use `Status=Remaining` and enter a `Projected Mark` for future units.
- The app uses actual marks for current WAM/EIHWAM and projected marks only for future projections.
- Uploaded records are kept in the current browser session; they are never written to a shared server file.

## Features

- WAM and EIHWAM calculators
- Future projections
- Target planning
- Analytics for completed units
