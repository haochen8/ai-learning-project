# MCP Apps: Primitives, discovery, and the Future of Software - Pietro Zullo, Manufact, Inc

## Executive Summary
This is a local, model-assisted study note for **MCP Apps: Primitives, discovery, and the Future of Software**. The local LLM summarized transcript chunks, then this final note was assembled into a stable learning format to avoid small-model formatting drift.

The transcript signals repeated attention to: MCP Apps: Primitives, discovery, and the Future of Software, MCP Apps, Manufact, App, MCP, Any, App Tools, Concrete. Treat the note as a learning scaffold: use it to decide what to rewatch, what to prototype, and what needs verification against the original talk.

## What To Learn
- How MCP Apps: Primitives, discovery, and the Future of Software decomposes a larger AI engineering task into smaller reasoning or implementation steps
- Which named tools, models, or frameworks matter in the talk: MCP Apps: Primitives, discovery, and the Future of Software, MCP Apps, Manufact, App, MCP
- How to distinguish a convincing demo from a workflow that has been evaluated carefully
- Where context handling, intermediate assumptions, and orchestration can fail
- What smallest prototype would let you test the talk's main claim yourself

## Key Concepts
- MCP Apps: Primitives, discovery, and the Future of Software: recurring transcript signal to connect back to MCP Apps: Primitives, discovery, and the Future of Software.
- MCP Apps: recurring transcript signal to connect back to MCP Apps: Primitives, discovery, and the Future of Software.
- Manufact: recurring transcript signal to connect back to MCP Apps: Primitives, discovery, and the Future of Software.
- App: recurring transcript signal to connect back to MCP Apps: Primitives, discovery, and the Future of Software.
- MCP: recurring transcript signal to connect back to MCP Apps: Primitives, discovery, and the Future of Software.
- Any: recurring transcript signal to connect back to MCP Apps: Primitives, discovery, and the Future of Software.
- App Tools: recurring transcript signal to connect back to MCP Apps: Primitives, discovery, and the Future of Software.
- Concrete: recurring transcript signal to connect back to MCP Apps: Primitives, discovery, and the Future of Software.

## Model-Assisted Observations
- MCP Apps are a full interaction layer that bridges the gap between an app's UI and its model, enabling real-time communication and state management
- ui/update-model-context`: Push live state into the model's context window without user messages
- ui/message`: Talk back to the app in a prompt-less manner
- app-tools`: Model calls into the App's registered tool surface
- State flows between the model and the UI: Live context sharing, unprompted

## Practical Takeaways
- Map the talk's claims into a small prototype before treating MCP Apps: Primitives, discovery, and the Future of Software as a production pattern
- Separate what the speaker demonstrates from what still needs evaluation
- Track inputs, outputs, assumptions, and failure cases for each agent or model step
- Convert vague workflow ideas into tests, review checkpoints, and rollback paths
- Use the transcript anchors below as review targets when rewatching the talk

## Implementation Sketch
Build a small prototype inspired by **MCP Apps: Primitives, discovery, and the Future of Software**. Define one input task, one model or agent workflow, one observable output, and two evaluation checks. Log every intermediate step so you can compare model behavior against the speaker's claims instead of relying on impressions.

## Failure Modes
- The workflow may look convincing while hiding weak evaluation.
- Long-context or multi-step agent behavior can degrade when intermediate assumptions are wrong.
- Small local models may compress nuance; verify important claims against the transcript or video.
- A demo pattern may not transfer cleanly to production constraints such as latency, cost, privacy, and maintainability.

## Transcript Anchors
- X/Twitter: https://x.com/pietrozullo LinkedIn: https://www.linkedin.com/in/pietrozullo/ GitHub: https://github.com/pietrozullo
- **Why companies will need to move** Any product that is used by humans through a UI will need
- Everyone in this room knows what MCP is, but I am sure not many people know what MCP
- **The primitives that make them real.** `ui/update-model-context`, the App pushing live state into the model's context window without
- **Distribution and discovery.** How the stores work, how to submit, what the surface looks like across hosts, and

## Watch Recommendation
Watch if you are studying agent workflows, recursive decomposition, or AI engineering process design. Skim first if you only need the high-level idea, then return to the transcript anchors above for details.

## Review Questions
- What problem is MCP Apps: Primitives, discovery, and the Future of Software trying to solve?
- Which assumption in the talk would be riskiest in production?
- How would you evaluate whether MCP Apps: Primitives, discovery, and the Future of Software improves an AI engineering workflow?
- Which part should be prototyped first, and what is the smallest useful demo?
- How do these terms connect: MCP Apps: Primitives, discovery, and the Future of Software, MCP Apps, Manufact, App, MCP?
