---
name: create-class-diagram
description: Create UML class diagrams in draw.io XML format (.drawio files) that emphasize OOP structure, SOLID principles, and clear dependencies between classes. Use this skill whenever the user asks for a UML class diagram, an OOP class diagram, a "class diagram for [a system]", wants to model code structure with classes/interfaces/enumerations, asks to reverse-engineer a codebase or package into a diagram, or mentions draw.io / diagrams.net in a class-modeling context — even if they don't say the words "UML" or "class diagram" explicitly. Also trigger when the user uploads source code or a package layout and asks Claude to "diagram it" or "show the architecture in classes". Do NOT use for sequence diagrams, state machines, system/data-flow architecture diagrams, or non-OOP system diagrams.
trigger: /create-class-diagram
---

# UML Class Diagram (draw.io)

Produces UML class diagrams as `.drawio` XML files. The target style is the clean, monochrome, dependency-focused look used in academic and professional software-design documentation: thin black strokes, no fill colors, three-compartment classes, and standard UML arrowheads.

## Output

Always output a single `.drawio` file. The file must be **uncompressed XML** (plain `<mxfile>` / `<mxGraphModel>` / `<mxCell>`), not the Base64-deflated form, so the user can read and edit it. `Write` it to the working directory (or a path the user specified) and tell the user the file path so they can open it in draw.io.

Filename convention: `<context>_<subject>_drawio.drawio` — e.g. `2026-1_PaymentService_UML.drawio`. If the user gives no context, just use the subject.

## What this skill is for (and not for)

**Use it for:** static class structure — classes, abstract classes, enumerations (and interfaces, when justified — see below), and the relationships between them.

**Do not use it for:** sequence diagrams, state machines, activity diagrams, deployment diagrams, system architecture / data-flow diagrams, ER diagrams. Those are different skills.

## Core philosophy: minimum viable diagram

The diagram exists to make the design legible to a human in under a minute. Every class, every arrow, every package box has to earn its place. **The default action when in doubt is delete, not add.** Resist the temptation to model every type, every concrete adapter, every interface "for OCP". Most class diagrams are too crowded, not too sparse.

This skill leans hard toward the **lean** end of the spectrum:

- **Don't invent interfaces with one implementation.** If the only implementor is `AStarPlanner`, just draw `PathPlanner`. The `IPathPlanner` interface is noise — it doubles the box count without adding information. Add the interface only when there are multiple real implementations on the diagram, or when the user explicitly says they want to show the abstraction boundary.
- **Don't include trivial value types.** `Pose2D`, `Vector3`, `Color`, `Point` and similar plain-data structures are usually better shown inline as field types (`+ position: Pose2D`) than as their own boxes. Add a box only if the type has nontrivial behavior (methods worth showing) or appears in many relationships.
- **Don't show every concrete adapter.** If the user has `GazeboRobotInterface` and `HardwareRobotInterface` as alternative backends, you don't need both on the diagram — the design point is "there is a robot interface", not "there are two of them". Mention the alternatives in your reply, not on the canvas.
- **Don't package things that don't form a domain.** A package container is a claim that "these classes belong together as a unit." If the only reason you're drawing a box around three classes is "they're loosely related", drop the box. Use packages only for clearly cohesive domains (a graph world, a hardware abstraction layer with multiple peers, etc.).

When you've drafted a diagram, do one pruning pass: for each class, ask "what would the diagram lose if I deleted this?" If the answer is "not much", delete it.

## Edges: the simplified two-type system

Default to **two arrow types only**:

| Relationship | Style fragment | Meaning |
|---|---|---|
| **Uses** | `endArrow=open;endFill=0;` | A depends on B in any way: holds it as a field, calls its methods, takes it as a parameter, returns it, owns it, aggregates it. |
| **Inherits** | `endArrow=block;endFill=0;endSize=16;` | A is a subtype of B (extends a class or implements an interface). |

This is deliberately coarser than full UML. The rationale: most readers can't reliably distinguish hollow-diamond aggregation from filled-diamond composition from plain association anyway, and the visual noise of mixed arrowheads obscures the dependency flow. The "uses" arrow says everything a reader needs: A points at B, so A knows about B. Whether it's by-reference or by-value, owned or borrowed, is usually clear from context (the field type, the method signature) — and if it isn't, a one-line comment in the field compartment beats a special arrowhead.

**When the user explicitly asks for full UML semantics**, fall back to the full six-arrow set:

| Relationship | Style fragment | Arrow appearance |
|---|---|---|
| Inheritance | `endArrow=block;endFill=0;endSize=16;` | hollow triangle |
| Realization | `endArrow=block;endFill=0;endSize=16;dashed=1;` | hollow triangle, dashed |
| Association | `endArrow=open;endFill=0;` | open V |
| Aggregation | `startArrow=diamondThin;startFill=0;startSize=14;endArrow=open;endFill=0;` | hollow diamond at owner |
| Composition | `startArrow=diamondThin;startFill=1;startSize=14;endArrow=open;endFill=0;` | filled diamond at owner |
| Dependency | `endArrow=open;endFill=0;dashed=1;` | open V, dashed |

Default to two-type. Use six-type only if the user says "use full UML notation", "distinguish composition from aggregation", or similar.

Every edge always includes `edgeStyle=orthogonalEdgeStyle;rounded=0;html=1;` and the geometry child `<mxGeometry relative="1" as="geometry"/>`.

Direction matters:
- **Inherits:** arrow points from the child/implementor **to** the parent.
- **Uses:** arrow points from the user **to** the thing being used.

## Class shapes

The atomic unit is a class, not a function or a module. Every box on the canvas is one of:
- a concrete class
- an abstract class (italicized name)
- an `<<interface>>` (only when justified — see philosophy section)
- an `<<enumeration>>`

Free-floating notes, label boxes, or annotations are allowed but kept rare. If something would be a free function, model it as a static method on the class it belongs to, or omit it.

Show fields and methods with proper UML visibility:
- `+` public
- `-` private
- `#` protected
- `~` package-private (only if the language has it)

Type the members: `- name: string`, `+ getUser(id: int): User`. Keep types short — use the language's natural type name (`string`, not `java.lang.String`). For methods that return nothing or for simple getters, dropping the return type is fine (`+ activate()` rather than `+ activate(): void`).

### Concrete class

Use the standard draw.io UML swimlane: one parent `swimlane` cell, with stacked `text` cells for fields and methods, separated by a `line` cell.

```xml
<mxCell id="cls_user" value="User"
        style="swimlane;fontStyle=1;align=center;verticalAlign=top;childLayout=stackLayout;horizontal=1;startSize=26;horizontalStack=0;resizeParent=1;resizeParentMax=0;resizeLast=0;collapsible=0;marginBottom=0;html=1;"
        vertex="1" parent="1">
  <mxGeometry x="100" y="100" width="200" height="120" as="geometry"/>
</mxCell>
<mxCell id="cls_user_fields"
        value="- id: int&#10;- name: string&#10;- email: string"
        style="text;strokeColor=none;fillColor=none;align=left;verticalAlign=top;spacingLeft=4;spacingRight=4;overflow=hidden;rotatable=0;points=[[0,0.5],[1,0.5]];portConstraint=eastwest;html=1;"
        vertex="1" parent="cls_user">
  <mxGeometry y="26" width="200" height="54" as="geometry"/>
</mxCell>
<mxCell id="cls_user_sep" value=""
        style="line;strokeWidth=1;fillColor=none;align=left;verticalAlign=middle;spacingTop=-1;spacingLeft=3;spacingRight=3;rotatable=0;labelPosition=right;points=[];portConstraint=eastwest;"
        vertex="1" parent="cls_user">
  <mxGeometry y="80" width="200" height="8" as="geometry"/>
</mxCell>
<mxCell id="cls_user_methods"
        value="+ login(): bool&#10;+ logout()"
        style="text;strokeColor=none;fillColor=none;align=left;verticalAlign=top;spacingLeft=4;spacingRight=4;overflow=hidden;rotatable=0;points=[[0,0.5],[1,0.5]];portConstraint=eastwest;html=1;"
        vertex="1" parent="cls_user">
  <mxGeometry y="88" width="200" height="32" as="geometry"/>
</mxCell>
```

### Interface

Only draw an interface if at least one of these is true:
1. Two or more implementations of it appear on the diagram.
2. The user explicitly modeled an interface in their code and asked for it on the diagram.
3. The user is teaching/illustrating a design pattern (Strategy, Observer, etc.) where the abstraction is the point.

If none of those hold, draw the concrete class instead.

When an interface is justified:

```xml
<mxCell id="iface_repo" value="&lt;&lt;interface&gt;&gt;&#10;Repository"
        style="swimlane;fontStyle=1;align=center;verticalAlign=top;childLayout=stackLayout;horizontal=1;startSize=40;horizontalStack=0;resizeParent=1;resizeParentMax=0;resizeLast=0;collapsible=0;marginBottom=0;html=1;"
        vertex="1" parent="1">
  <mxGeometry x="400" y="100" width="200" height="80" as="geometry"/>
</mxCell>
```

Note `startSize=40` (instead of 26) to fit two lines in the title bar. Interfaces typically have only a methods compartment — no fields — so you can skip the fields cell and the separator line.

The stereotype goes in the title bar on the line *above* the name, encoded as `&lt;&lt;interface&gt;&gt;&#10;Name`. Not as a separate cell, and not as `IName` — UML uses the stereotype, not a Hungarian-style prefix. (If the user's source code uses an `I` prefix, drop it on the diagram and add the stereotype.)

### Abstract class

Same as concrete class, but italicize the name with `fontStyle=3` on the title (3 = bold + italic).

### Enumeration

```xml
<mxCell id="enum_state" value="&lt;&lt;enumeration&gt;&gt;&#10;VehicleState"
        style="swimlane;fontStyle=1;align=center;verticalAlign=top;childLayout=stackLayout;horizontal=1;startSize=40;horizontalStack=0;resizeParent=1;resizeParentMax=0;resizeLast=0;collapsible=0;marginBottom=0;html=1;"
        vertex="1" parent="1">
  <mxGeometry x="700" y="100" width="160" height="100" as="geometry"/>
</mxCell>
<mxCell id="enum_state_values" value="STOPPED&#10;MOVING&#10;FINISHED"
        style="text;strokeColor=none;fillColor=none;align=left;verticalAlign=top;spacingLeft=4;spacingRight=4;overflow=hidden;rotatable=0;points=[[0,0.5],[1,0.5]];portConstraint=eastwest;html=1;"
        vertex="1" parent="enum_state">
  <mxGeometry y="40" width="160" height="60" as="geometry"/>
</mxCell>
```

## XML structure

Every diagram follows this shell:

```xml
<mxfile host="app.diagrams.net">
  <diagram id="page1" name="Page-1">
    <mxGraphModel dx="1200" dy="800" grid="1" gridSize="10" guides="1"
                  tooltips="1" connect="1" arrows="1" fold="1" page="1"
                  pageScale="1" pageWidth="1600" pageHeight="1100" math="0" shadow="0">
      <root>
        <mxCell id="0"/>
        <mxCell id="1" parent="0"/>
        <!-- title block, packages, classes, edges go here -->
      </root>
    </mxGraphModel>
  </diagram>
</mxfile>
```

Mandatory rules (from draw.io itself, not style preference):

- `<mxCell id="0"/>` and `<mxCell id="1" parent="0"/>` must both exist. Every other cell has `parent="1"` (or the id of a container).
- `vertex="1"` for shapes, `edge="1"` for connectors. Never both.
- Every edge cell **must** contain `<mxGeometry relative="1" as="geometry"/>` — even with no waypoints. Self-closing edge cells render incorrectly.
- All ids must be unique strings.
- HTML-escape any `<`, `>`, `&`, `"` inside `value` attributes (e.g. `&lt;&lt;interface&gt;&gt;`).
- Use `&#10;` for line breaks inside `value` (not `<br>`, not literal newlines).

## Packages and grouping

Use packages **only when the grouping carries real semantic weight.** A package box is a claim: "these classes belong together as a coherent subdomain, and their boundary matters." Indicators that a group earns its package box:

- Three or more classes that all serve one bounded responsibility.
- A clear seam where most edges crossing the boundary are interesting cross-domain dependencies.
- The user has named the subsystem (e.g., "the world model", "the hardware layer") in conversation or code.

If you'd be drawing a box around two classes just to label them, don't — let them sit free.

When you do use a package, it's a rounded rectangle with a label header:

```xml
<mxCell id="pkg_world" value="world"
        style="rounded=1;whiteSpace=wrap;html=1;fillColor=none;strokeColor=#000000;verticalAlign=top;align=left;spacingLeft=10;spacingTop=4;fontStyle=0;"
        vertex="1" parent="1">
  <mxGeometry x="40" y="60" width="320" height="500" as="geometry"/>
</mxCell>
```

Then set `parent="pkg_world"` on the classes that belong inside it, and use **relative** coordinates (the child's `x`,`y` are measured from the package's top-left). This way, when the user drags the package, the contents move with it.

## Title block

For larger diagrams (~6+ classes), include a title block in the top-left: a plain text cell with the diagram title in larger bold font, plus a 2–4 line description. For small diagrams, skip it — the title would feel heavier than the diagram itself.

```xml
<mxCell id="title" value="&lt;b style=&quot;font-size:20px&quot;&gt;Diagram Title&lt;/b&gt;&#10;&#10;Short description of what this system does.&#10;Two or three lines is the right length."
        style="text;html=1;align=left;verticalAlign=top;whiteSpace=wrap;rounded=0;fillColor=none;strokeColor=none;"
        vertex="1" parent="1">
  <mxGeometry x="40" y="20" width="500" height="100" as="geometry"/>
</mxCell>
```

## Layout heuristics

The reader scans top-to-bottom, left-to-right, so:

1. **Place abstractions above their implementations.** If you've kept an interface or abstract class, put it higher on the canvas; concrete classes inherit upward. (Less relevant in the lean default style, but applies when interfaces appear.)
2. **Lay out by dependency flow.** The class that drives the system goes near the top or center; the things it depends on flow outward from it. Read the arrows like reading lines of code: if A → B → C, put A first.
3. **Cluster by package, when packages exist.** Cross-package edges should be the most interesting edges in the diagram.
4. **Group enumerations near where they're used,** not in a separate corner — an enum next to its consumer is easier to read than one in a far-away "Enum" container.
5. **Aim for arrow flow, not symmetry.** A symmetric diagram with crossing arrows is worse than an asymmetric one without. Move boxes to uncross arrows before adjusting for visual balance.
6. **Spacing.** 40–80px gutters between unrelated classes; 20–30px is fine within a tight cluster.
7. **Canvas size.** Start with `pageWidth=1600`, `pageHeight=1100` for medium diagrams. For dense ones (15+ classes), bump to 2400×1600. Place classes well inside the page bounds — leave 40px margin from the edges.
8. **Use orthogonal edges**, not curves. Set `edgeStyle=orthogonalEdgeStyle` on every connector.

## SOLID-aware structure

When the user is modeling a real design, the principles guide the structure (not the labels — never put "SRP" on the diagram):

- **SRP:** if a class has more than ~7 methods or methods that group into obviously different concerns, flag it in your reply and suggest splitting.
- **OCP:** extension points should appear as interfaces or abstract classes — but only if the diagram is large enough that the abstraction earns its box (see the lean philosophy).
- **LSP:** subclasses should not appear to "narrow" the parent — if the user's code does this (e.g. by throwing `NotImplementedException`), mention it.
- **ISP:** prefer multiple small interfaces over one fat one, and connect each consumer to only the interface it actually uses.
- **DIP:** high-level classes should depend on abstractions when those abstractions exist on the diagram. If you've collapsed the abstraction (lean style), DIP is invisible on the canvas — that's fine, just don't claim DIP is present in your reply.

You don't label these on the diagram. After producing it, you can call out one or two SOLID observations in your reply.

## Workflow

When the user asks for a class diagram:

1. **Clarify scope if needed.** If the request is "diagram my codebase", ask which package or module — a single diagram with 30+ classes becomes unreadable. One diagram per package is the default.
2. **Extract the model.** From source code, an interface description, or the user's prose, list out: classes, interfaces, enums, their members (with visibility and types), and their relationships. Do this thinking work *before* writing XML.
3. **Prune.** Apply the lean philosophy: drop single-implementation interfaces, drop trivial value types, drop redundant adapter classes, drop empty packages. The first draft is always too crowded.
4. **Plan the layout.** Decide which (remaining) classes go in which package container, where any interfaces sit relative to their implementations, the rough top-to-bottom dependency flow.
5. **Generate the XML.** Use unique, descriptive ids (`cls_user`, `cls_repo`, `e_uses_1`) — this makes the file editable by hand later.
6. **Save and present.** `Write` the file to the working directory (or a user-specified path) as `<name>.drawio`, then report the path in your reply.
7. **Brief commentary.** In your reply, give a 2–4 sentence summary: which abstractions you surfaced, what the dependency direction is, what you intentionally left off (and why). Don't restate the diagram — the user can see it.

## Common pitfalls

- **Forgetting the edge geometry child.** `<mxCell ... edge="1"/>` self-closed will render but lose its shape. Always include `<mxGeometry relative="1" as="geometry"/>`.
- **Wrong arrow direction on inheritance.** The arrow points from child to parent. Easy to get backwards.
- **Using fillColor on classes.** The reference style is monochrome. Don't add fill colors unless the user asks — they make the diagram look like a wireframe mockup, not a UML diagram.
- **Inventing interfaces.** Resist the reflex of "every class with one collaborator gets an interface." Single-implementation interfaces are the most common bloat in AI-generated UML.
- **Putting `<<interface>>` in the wrong place.** It goes inside the title bar, on the line above the class name, encoded as `&lt;&lt;interface&gt;&gt;&#10;Name`. Not as a separate cell, and not in the methods compartment.
- **Hungarian interface names on diagrams.** UML uses `<<interface>>` Repository, not `IRepository`. If the user's code uses `IFoo`, the diagram name is `Foo` with the stereotype.
- **Mixing diagram families.** If the user wants a system architecture diagram (servers, databases, message queues, deployment zones), this skill is the wrong tool — say so and offer to do it as a different diagram instead.

## Reference: full minimal example

See `references/example.drawio` for a complete working file with one interface (justified by two implementations), one abstract class, several concrete classes, an enumeration, a `world` package, and the two default arrow types. Read it whenever you need to copy-paste a known-good shape or edge style.
