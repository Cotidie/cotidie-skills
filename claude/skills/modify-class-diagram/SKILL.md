---
name: modify-class-diagram
description: Update an existing UML class diagram (.drawio) so it better reflects a codebase's architecture. Use this skill when the user provides an existing .drawio or draw.io XML file along with a target codebase and asks to update / refresh / sync / refactor / fix / audit / review the diagram against the code, bring it in line with current implementation, or "diff the diagram against the codebase". Also trigger when the user uploads both a class diagram and source code and asks Claude to "make the diagram match" or "improve the diagram based on the code". Requires BOTH an existing `.drawio` (or draw.io XML) file AND a target codebase. Do NOT use this skill for creating a class diagram from scratch (use create-class-diagram instead), for modifying sequence/state/system diagrams, or for non-UML draw.io files.
trigger: /modify-class-diagram
---

# Modify UML Class Diagram (draw.io)

Updates an **existing** draw.io UML class diagram so it better represents the architecture of a target codebase. The output is a modified `.drawio` file, not a new one — the original file's structure, IDs, layout, and visual style are preserved as much as possible. The goal is **conservative, explainable changes** that improve architectural clarity, not a full regeneration.

**REQUIRED BACKGROUND:** This skill builds on `create-class-diagram`. All visual conventions — the two-arrow edge system, swimlane class shape, package containers, monochrome style, XML structure — are defined there and apply unchanged here. Read `create-class-diagram` if you don't already know the style; this skill only documents what's *different* about modifying an existing diagram.

## Required inputs

This skill cannot run without both:

1. **An existing `.drawio` file or draw.io XML** — must be uncompressed XML (plain `<mxfile>` / `<mxGraphModel>` / `<mxCell>`). If the file is the Base64-deflated form, decode it first or ask the user to re-export with "Compressed" turned off in draw.io.
2. **A target codebase** — a path on disk, a repository, or pasted source. You need enough of the code to see public classes, their public members, and how they refer to each other.

If either is missing, **stop and ask for it** before doing anything else. Don't infer the diagram from the codebase or vice versa — that's the `create-class-diagram` job, not this one.

## Core philosophy: minimum viable diff

The same lean philosophy from `create-class-diagram` applies — but with one extra rule on top:

**The default action when in doubt is leave it alone.**

The user has already made decisions about which classes to surface, how to name them, how to lay them out, which interfaces are worth showing, and which trivial types to inline. Most of those decisions are still correct even when the code has drifted. Don't relitigate them. Modify only what the codebase clearly contradicts.

A good edit is one you can explain in one sentence: "Renamed `RobotStatus` enum to `RobotMode` because the code uses `RobotMode`." A bad edit is "Reorganized the diagram." If you find yourself wanting to reorganize, stop — that's a sign you're treating this like `create-class-diagram`.

When in real doubt about whether a change is justified, **leave the diagram as-is and mention the discrepancy in your summary** instead. The user can decide.

## What counts as a justified change

| Change | Justified when… |
|---|---|
| **Rename a class / member** | The diagram name doesn't match the code's actual name and the entity is clearly the same thing |
| **Add a class** | The class is architecturally important (drives a layer, hosts the public API of a module, has multiple incoming dependencies) AND it's missing from the diagram |
| **Remove a class** | The class no longer exists in the code, OR the class is a trivial helper / private detail that adds noise without architectural value |
| **Add a relationship** | The dependency exists in the code AND both endpoints are already on the diagram AND the relationship is meaningful (not an incidental utility import) |
| **Remove a relationship** | The dependency no longer exists in the code, or it points to a class that was removed |
| **Update fields/methods** | Public API has changed: members were renamed, signatures changed, public members were added or removed |
| **Change package grouping** | The codebase's module structure has clearly shifted and the existing grouping is now misleading |

| Change | NOT justified |
|---|---|
| Re-laying out boxes for aesthetics | Layout is the user's decision; preserve it |
| Switching arrow styles globally | If the original used the two-arrow system, keep it; if it used full UML, keep that |
| Adding every private helper class | Architectural diagrams ignore implementation detail |
| Adding every transitive dependency | Show meaningful direct dependencies, not the import graph |
| Replacing concrete classes with interfaces "for OCP" | Same single-implementation rule as create-class-diagram |
| Inventing relationships you can't point at in the code | If you can't cite the file/line, don't draw the arrow |

## Public API focus

When inspecting code, look at the **public surface** of each class:

- public properties / fields
- public methods (and their signatures: parameter types, return type)
- public constructors (only show if non-trivial — a constructor with no params is usually noise)

**Ignore private members** unless one of these holds:

- The private member *is* the architectural point (e.g., a private singleton instance, a private dependency that's the whole reason the class exists).
- The private member is a field whose **type** reveals an important dependency that would otherwise be invisible (e.g., `_planner: PathPlanner` is the only thing tying the class to `PathPlanner`).

Language-specific note: Python uses leading-underscore convention rather than syntactic visibility. Treat `_name` as private and `name` as public unless context says otherwise. For a method like `_internal_helper`, ignore it. For a field like `self._planner: PathPlanner` that's clearly the class's main collaborator, surface the dependency as an arrow even though you don't list the field on the box.

## Workflow

### 1. Inspect the existing diagram

Parse the `.drawio` XML and inventory:

- **Classes** — for each box: id, name, stereotype (`<<interface>>`, `<<enumeration>>`, abstract), fields, methods, position (`x`, `y`, `width`, `height`), parent (top-level vs. inside a package).
- **Edges** — for each connector: id, source id, target id, style (which arrow type), and any waypoints.
- **Packages / groups** — id, label, geometry, which classes are children.
- **Title block / annotations** — preserve verbatim unless explicitly contradicted by the code.
- **Style fingerprint** — does the diagram use the lean two-arrow system or the full six-arrow set? Monochrome or does it use fill colors? `startSize=26` titles or `startSize=40`? Match what's there.

Build a mental map: `id → class object`. You'll use these ids when emitting the modified file.

### 2. Inspect the codebase

Walk the codebase and identify the architecturally meaningful units. You're looking for:

- **Public classes, abstract classes, interfaces, enums.**
- **Layer / module structure** — directories that correspond to subdomains (e.g. `planning/`, `robot/`, `safety/` in a ROS package).
- **Public collaborators** — which classes hold references to which, which classes call which, which classes appear as parameter or return types in public methods.
- **Inheritance / implementation** — `class Foo(Bar):`, `class Foo extends Bar`, `class Foo implements IBar`.
- **Important constructor arguments** — these often reveal the real dependencies.

Skip:
- Test files, fixtures, and mocks (unless the user is diagramming the test architecture itself).
- Generated code, vendored third-party code, build artifacts.
- Trivial value types (`Pose2D`, `Point`, `Vector3`) — these belong inline as field types, not as their own boxes.

### 3. Compare and decide

Produce a short mental diff. For each architecturally meaningful class in the codebase, mark it as: **already on diagram (matches)**, **already on diagram (drifted — needs update)**, or **missing from diagram (and worth adding?)**.

For each class on the diagram, mark it as: **still in code (matches)**, **still in code (drifted)**, **renamed**, or **deleted from code**.

For each edge on the diagram, verify the underlying dependency still exists in the code. Mark missing/added edges.

Then **prune the change list**:
- A class missing from the diagram but with no incoming dependencies is probably an implementation detail — leave it off.
- A class on the diagram with no real code analogue might still be useful as a conceptual placeholder if the user clearly placed it there intentionally — flag it in your summary instead of deleting.
- An "added" edge that just reflects an incidental utility import is noise — don't add it.

If the change list is empty after pruning, that's a fine outcome. Say so in your summary and emit the file unchanged (or skip emitting and tell the user nothing needs changing).

### 4. Apply changes to the XML

**Preserve everything you don't need to change.** This is the cardinal rule. Concretely:

- **Keep existing `mxCell` ids.** Never renumber. If a class is being renamed, change its `value` attribute but keep the id (`cls_executor` stays `cls_executor` even if the displayed name changes from `TurtleBot` to `TurtleBotExecutor`). Edges reference cells by id; renumbering breaks them.
- **Keep existing positions (`x`, `y`, `width`, `height`).** When updating fields/methods, the parent swimlane may need a new height — recompute it from the field/method block heights, but leave `x`/`y` alone.
- **Keep existing styles verbatim.** Copy the style string unchanged when editing a cell's value. If the diagram used a non-default style (custom font size, fill color, stroke width), don't normalize it.
- **Keep existing waypoints on edges.** If an edge has `<Array as="points">…</Array>` inside its geometry, preserve it.
- **Keep existing packages and parent relationships.** A class inside `pkg_world` stays inside `pkg_world` unless its module clearly moved.

**When adding new content:**

- New ids should follow the existing scheme. If the diagram uses `cls_*` for classes and `e_*` or auto-generated random ids for edges, match the local convention.
- Place new classes in empty space near the most-related existing class, with the same width as its neighbors. Don't squeeze a new box into a gap that's too small — extend the page if needed.
- Use the same arrow style as existing edges of the same logical kind. If existing "uses" edges are `endArrow=open;endFill=0;`, use the same string for new ones — even if it's not the canonical style from `create-class-diagram`.
- Inherit field/method block heights from neighbors (text blocks at ~14px per line is the draw.io default for the standard style).

**When removing content:**

- Remove the class swimlane AND its child cells (fields, separator, methods).
- Remove every edge whose `source` or `target` was on the deleted class — orphan edges render but point at nothing.
- If the deleted class was inside a package and was the only child, consider whether the package itself still earns its box.

**XML hygiene** — same rules as `create-class-diagram`:
- HTML-escape `<`, `>`, `&`, `"` inside `value` attributes.
- Use `&#10;` (or `&#xa;`, both valid) for line breaks in `value`. Some draw.io exports use `<br>` — that also works, but be consistent within a cell.
- Every edge cell must include `<mxGeometry relative="1" as="geometry"/>` (with or without a `<Array as="points">` child).
- Keep `<mxCell id="0"/>` and `<mxCell id="1" parent="0"/>` exactly as they are.

### 5. Output

Write the modified file back to the original path on disk when the user pointed at one; otherwise save it alongside the original as `<original-name>_updated.drawio`. Report the path in your reply.

Then write a **concise summary** in your reply, structured as:

```
**Changes**
- Renamed cls_executor display name from "TurtleBot" to "TurtleBotExecutor" — code class is `TurtleBotExecutor` in robot/turtlebot_node.py.
- Removed cls_motioncontroller — no class by that name in the codebase; closest match is the pure-function `compute_drive` in robot/motion.py.
- Added cls_pathfollower — drives waypoint advancement; held as a field on TurtleBotExecutor.
- Updated cls_pathserver methods to match action handler names in planning/path_server.py.

**Left unchanged**
- The `world` package grouping — still matches the codebase's planning/ subpackage.
- The two-arrow edge style — keeping the original lean convention.

**Uncertain**
- Whether `RobotState` should be an enum or a struct — the diagram shows it as a class but it's also published as a ROS msg, which is structurally similar to a record. Leaving as-is.
- The `User` actor box at the top — not a code class, but appears intentional as a stakeholder marker. Preserved.
```

The summary's job is to make every change auditable in 30 seconds. The user should be able to revert any individual edit without rebuilding the file.

## Style preservation cheat sheet

When in doubt, **mirror the existing diagram's style choices**, not the canonical conventions from `create-class-diagram`:

| If the existing diagram… | Do this in your edits |
|---|---|
| Uses `&lt;br&gt;` for newlines in values | Use `&lt;br&gt;` in new cells too |
| Uses `&#xa;` or `&#10;` for newlines | Match it |
| Uses random-string ids like `NCUIXoI1oaRRW0hac2T5-13` | Either reuse those for related cells, or create new readable ids — don't generate new long random ones |
| Uses `endArrow=none;endFill=0;dashed=1;` for "uses" | Match it; don't switch to the canonical `endArrow=open;endFill=0;` |
| Has classes outside any package | Put new top-level classes outside packages too |
| Has a title block | Preserve and update its description if architecture has shifted; don't replace |
| Has color-coded boxes | Keep colors on existing boxes; reuse the same colors for new boxes by analogy |
| Has empty `value=" "` (single space) on a class title | Probably an editing artifact — fill it in if you can identify the class, otherwise leave it |

## Common pitfalls

- **Treating this like `create-class-diagram`.** The temptation is to look at the codebase, mentally generate the "ideal" diagram, and replace the user's. Don't. Modify, don't regenerate.
- **Renumbering ids.** Edges silently break when their source/target ids no longer exist. If you must change an id (rare), update every edge that referenced it.
- **Deleting orphan edges by accident — or leaving them.** When removing a class, grep the XML for its id appearing as `source=` or `target=` and remove those edges too.
- **Adding every dependency you find in the code.** A diagram with 40 arrows is unreadable. Most "found" dependencies are imports of utility types, not architectural relationships. Keep the arrow count roughly the same as before unless the original was clearly missing major connections.
- **Replacing the title block's description.** The user wrote that description; only update specific factual claims that the code now contradicts (e.g., "2 robots" → "3 robots"). Don't rewrite the prose.
- **Normalizing styles.** If the original used a slightly nonstandard style string, copy it. Don't "clean it up" to the canonical form.
- **Forgetting that the existing arrow direction may differ.** If the original drew "uses" arrows from owner to dependency (correct) or from dependency to owner (backwards but consistent), preserve the convention used; if the convention is genuinely wrong, flag it in the summary instead of silently flipping all arrows.
- **Editing without first parsing.** Skimming the XML and editing by find-and-replace risks breaking ids and styles. Build the inventory first, then emit.
- **Modifying compressed `.drawio` files in place.** If the file is Base64-deflated, edits will silently fail to round-trip. Confirm the file is plain XML before starting.

## When the original diagram is unusable

Rare, but possible: the existing diagram is so out of date, broken, or low-quality that patching it would take more effort than starting over (e.g., wrong system entirely, file corrupted, empty diagram). In that case, **stop and tell the user** before regenerating. Offer to invoke `create-class-diagram` instead. Don't silently rewrite the file.

A diagram is "unusable" if:
- More than ~70% of its classes don't correspond to anything in the codebase.
- It diagrams a different system than the one in the codebase.
- The XML is structurally broken (missing root cells, mismatched parents) such that draw.io can't open it.

A diagram is **not** unusable just because:
- It's stylistically different from what `create-class-diagram` would produce.
- It has classes you'd choose to omit.
- It's laid out in a way you wouldn't choose.

## Brief commentary

End your reply with **2–4 sentences**: what the codebase looks like architecturally, the most interesting drift you found, and any uncertain interpretations the user should sanity-check. Don't restate the change list — they can read it above. Don't praise or critique the original diagram unless asked.
