# Your Agent Is Wasting Tokens and You Don't Know It - Erik Hanchett, AWS

## Executive Summary
This is a local, model-assisted study note for **Your Agent Is Wasting Tokens and You Don't Know It**. The local LLM summarized transcript chunks, then this final note was assembled into a stable learning format to avoid small-model formatting drift.

The transcript signals repeated attention to: Your Agent Is Wasting Tokens and You Don't Know It, APIs, AWS, Another, Cache, Claude Haiku, Claude Sonnet, Don. Treat the note as a learning scaffold: use it to decide what to rewatch, what to prototype, and what needs verification against the original talk.

## What To Learn
- How Your Agent Is Wasting Tokens and You Don't Know It decomposes a larger AI engineering task into smaller reasoning or implementation steps
- Which named tools, models, or frameworks matter in the talk: Your Agent Is Wasting Tokens and You Don't Know It, APIs, AWS, Another, Cache
- How to distinguish a convincing demo from a workflow that has been evaluated carefully
- Where context handling, intermediate assumptions, and orchestration can fail
- What smallest prototype would let you test the talk's main claim yourself

## Key Concepts
- Your Agent Is Wasting Tokens and You Don't Know It: recurring transcript signal to connect back to Your Agent Is Wasting Tokens and You Don't Know It.
- APIs: recurring transcript signal to connect back to Your Agent Is Wasting Tokens and You Don't Know It.
- AWS: recurring transcript signal to connect back to Your Agent Is Wasting Tokens and You Don't Know It.
- Another: recurring transcript signal to connect back to Your Agent Is Wasting Tokens and You Don't Know It.
- Cache: recurring transcript signal to connect back to Your Agent Is Wasting Tokens and You Don't Know It.
- Claude Haiku: recurring transcript signal to connect back to Your Agent Is Wasting Tokens and You Don't Know It.
- Claude Sonnet: recurring transcript signal to connect back to Your Agent Is Wasting Tokens and You Don't Know It.
- Don: recurring transcript signal to connect back to Your Agent Is Wasting Tokens and You Don't Know It.

## Model-Assisted Observations
- Reducing token costs in AI engineering involves caching system prompts, routing messages based on difficulty, offloading tool results, trimming the history, and summarizing large tool calls
- Caching System Prompt: Add `system_prompt` to your agent's prompt
- Routing Messages: Use a model that is more efficient for tasks with fewer steps or simpler models for tasks with more complex ones
- Offloading Tool Results: Route tool results inside the agent and use summarization techniques to reduce their impact on context usage
- Trimming History: Reduce

## Practical Takeaways
- Map the talk's claims into a small prototype before treating Your Agent Is Wasting Tokens and You Don't Know It as a production pattern
- Separate what the speaker demonstrates from what still needs evaluation
- Track inputs, outputs, assumptions, and failure cases for each agent or model step
- Convert vague workflow ideas into tests, review checkpoints, and rollback paths
- Use the transcript anchors below as review targets when rewatching the talk

## Implementation Sketch
Build a small prototype inspired by **Your Agent Is Wasting Tokens and You Don't Know It**. Define one input task, one model or agent workflow, one observable output, and two evaluation checks. Log every intermediate step so you can compare model behavior against the speaker's claims instead of relying on impressions.

## Failure Modes
- The workflow may look convincing while hiding weak evaluation.
- Long-context or multi-step agent behavior can degrade when intermediate assumptions are wrong.
- Small local models may compress nuance; verify important claims against the transcript or video.
- A demo pattern may not transfer cleanly to production constraints such as latency, cost, privacy, and maintainability.

## Transcript Anchors
- So if we're using a multi-turn agent and we are talking back and forth, you will find at
- So that way when it's being called over and over again, the tool result isn't added into the
- And what that'll do is on the first call of your agent, it will send the full system
- So if you can find any way that where you have this tool result that you don't necessarily
- A good thing you can do before you deploy your agent is to run some observability tools and

## Watch Recommendation
Watch if you are studying agent workflows, recursive decomposition, or AI engineering process design. Skim first if you only need the high-level idea, then return to the transcript anchors above for details.

## Review Questions
- What problem is Your Agent Is Wasting Tokens and You Don't Know It trying to solve?
- Which assumption in the talk would be riskiest in production?
- How would you evaluate whether Your Agent Is Wasting Tokens and You Don't Know It improves an AI engineering workflow?
- Which part should be prototyped first, and what is the smallest useful demo?
- How do these terms connect: Your Agent Is Wasting Tokens and You Don't Know It, APIs, AWS, Another, Cache?
