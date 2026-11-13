# Lotus Boat

A calm pond game built from a viral motion video: a boat, a boatman, and lotus flowers that bounce when the boat passes.

## Status

Pre-build. Only the README exists. Reference video not uploaded yet.

## Reference video

- Planned location: `assets/reference/viral-video.mp4`
- Used to match lotus bounce motion, boat movement, and timing.

## Screens

### 1. Loading / start screen

- Pond with many lotus flowers.
- A boat with a boatman sits in the pond.
- One button only. Nothing else on screen.
  - Glass-morphic (frosted) style.
  - Label: "Start the game".
  - On tap: shows "Game coming soon". Game is not built yet.
- Animated guide hand loops a gesture showing how to draw a line.

## Gameplay

1. Player drags the boat or draws a path on the pond.
2. The boat follows that path.
3. Lotus flowers bounce when the boat touches them, matching the reference video.
4. The guide hand plays until the player first draws a line.

## Technical plan

- Single `index.html`. Vanilla JavaScript, HTML canvas.
- No build step, no framework.
- Glass button via CSS `backdrop-filter`.
- Path input via pointer events. Boat moves along the recorded path at constant speed.
- Lotus motion: simple spring per flower. Tune against the reference video.

## Out of scope for now

- Scoring, levels, win/lose rules.
- Real fluid physics.
- Asset pipeline.

## Known limits

- Lotus physics is a simple spring, not real collision. Upgrade to a physics library if the reference motion needs it.

## Open questions

- Game name (working name: Lotus Boat).
- Game rules for the "Game coming soon" build.
- Exact bounce height and timing: to be read from the reference video.
