# WF2026: Software Factories & Keynotes ft. Microsoft, OpenAI, OpenClaw, Z.ai (GLM), MiniMax, HF

## Executive Summary
This is a longform local, model-assisted study note for **WF2026: Software Factories & Keynotes**. The 88,983-word transcript was processed in 40 local Ollama chunks with `qwen2.5:0.5b`, then assembled into a stable learning format. Treat it as an index into a keynote block, not as a substitute for watching the important segments.

The strongest thread is the shift from single coding assistants to software factories: persistent agent systems with memory, permissions, review loops, observability, and human steering. The keynote block moves across Microsoft Foundry and IQ, OpenAI Codex, GLM/Z.ai, Hugging Face model supply, browser and Slack-style agent work, Factory missions, agent teams, OpenClaw-style agent control, runtime experience for agents, and safety arguments around constrained agentic loops.

The practical lesson is that agent productivity depends less on one heroic model call and more on the surrounding factory floor: grounded context, task decomposition, reusable skills, deterministic checks, sandboxes, traces, review gates, and ways for humans to interrupt or redirect work.

## What To Learn
- How "software factory" expands coding agents into a full operating model for shipping software.
- Why long-running agents need memory, task state, permissions, traces, and review loops.
- How Microsoft Foundry/IQ frames grounding, model access, retrieval, and optimization for agents.
- How OpenAI Codex is presented as an agent loop that spans app, cloud, API, local tooling, and mobile surfaces.
- Why multi-agent work needs orchestration, ownership, validation contracts, and human steering instead of unmanaged swarms.
- How agent-first tooling changes interfaces: Slack, GitHub, CLIs, sandboxes, browser environments, and office tools become action surfaces.
- Where small demos can hide hard production problems: authorization, observability, regression control, data quality, and cost.

## Key Concepts
- Software factory: a system where agents, tools, tests, review, deployment, and monitoring form a repeatable production workflow.
- Agent grounding: connecting agents to private company context, documents, traces, tickets, data warehouses, and operational history.
- Agentic retrieval: retrieval designed for agents that must rank, inspect, and reason over context rather than just fetch keyword matches.
- Codex agent loop: a coding-agent workflow with chat, tasks, local/cloud execution, compaction, API access, and steering surfaces.
- Missions: long-running agent sessions that decompose work into subtasks and worker agents.
- Agent teams: orchestration patterns where a lead agent delegates to specialist subagents with different context or model choices.
- Agent readiness: preparing codebases, tools, docs, permissions, and validation checks so agents can work without constant babysitting.
- Runtime experience: giving production agents memory, evaluations, context updates, and feedback loops after deployment.

## Model-Assisted Observations
- Microsoft sections emphasize Foundry, Microsoft IQ, Foundry IQ, Web IQ, model catalogs, grounding, retrieval, observability, and agent optimization.
- OpenAI Codex sections frame agents as ambient workers that can be steered from app, API, Slack-like workflows, local environments, cloud tasks, and mobile clients.
- GLM/Z.ai and Hugging Face sections position open models and model supply chains as part of the agent stack, not just benchmark objects.
- Factory-oriented talks repeatedly argue that agents need smaller jobs, explicit validation, sandboxes, and persistent context.
- Several segments push against the idea that browser agents or UI agents only need better models; they also need better environments and action abstractions.
- The keynote block repeatedly returns to review debt: agent-written PRs, agent-created artifacts, and agent decisions still need measurable checks.
- The most reusable idea is to design the workflow around the agent's operating environment before optimizing prompts.

## Practical Takeaways
- Start a software-factory prototype with one workflow: triage, spec writing, implementation, review, or monitoring.
- Give every agent task an owner, input contract, output artifact, validation check, and rollback path.
- Prefer small specialist agents or skills over one large prompt that tries to own the whole workflow.
- Store decisions, traces, tool calls, and human corrections where future agents can retrieve them.
- Treat Slack, GitHub, docs, browser sessions, and office tools as agent interfaces only after permissions and audit trails are explicit.
- Use deterministic checks for anything that can be tested deterministically; reserve model judgment for ambiguity.
- Make interruption and steering first-class so a human can redirect a long-running agent before it compounds an error.
- Evaluate agent output by production impact: defects, cycle time, review burden, escaped failures, and recovery time.

## Implementation Sketch
Build a small local "software factory" around one repo issue. Use one agent or script to turn an issue into a short spec, one coding agent to produce a patch, one review step to run tests and inspect the diff, and one logging layer that records prompts, tool calls, files changed, checks run, and human corrections. The point is not maximum autonomy; it is to make the factory floor visible enough that you can improve it.

For a no-cost local version, keep the model calls behind Ollama, use repo-native tests as the deterministic gate, and store summaries rather than raw transcripts or private data. Add a second pass only after the first workflow has reliable traces and review outcomes.

## Failure Modes
- A software factory can produce more review debt than human-written code if it lacks good gates.
- Agents can inherit stale or wrong context when grounding data is uncurated.
- Multi-agent orchestration can hide responsibility unless every subtask has an owner and artifact.
- Browser/UI agents can waste time if the environment exposes pixels but not useful state or APIs.
- Long-running agents can drift from the original goal without checkpoints and human steering.
- Permission sprawl becomes a security issue when agents can read or act across Slack, GitHub, docs, email, and production systems.
- Small local models can compress nuance, especially over an 8.5-hour transcript; important claims should be checked against the video.

## Transcript Anchors
- Opening keynote: software factories, Microsoft Foundry, Microsoft IQ, Foundry IQ, Web IQ, model catalogs, retrieval, and agent optimization.
- OpenAI Codex segment: Codex app, Codex cloud, API, local tools, compaction, mobile, and steering agents from different surfaces.
- GLM/Z.ai and Hugging Face segment: open model capabilities, coding, agentic use cases, and model supply-chain questions.
- Factory/Missions segments: long-running agent missions, worker agents, validation contracts, agent readiness, and factory governance.
- Agent teams and OpenClaw-style segments: lead agents, subagents, trace visibility, sandboxes, deterministic interruption, and agent-to-agent protocols.
- Later safety and engineering segments: constrained agentic loops, provably safer workflows, runtime experience, and the role of human-agent collaboration.

## Watch Recommendation
Skim the full block first and deep-watch selected segments. Prioritize Microsoft Foundry/IQ if you care about enterprise grounding, Codex if you care about coding-agent workflows, Factory/Missions if you care about orchestration, and the safety/runtime segments if you care about production reliability.

## Review Questions
- What has to exist around a coding agent before it becomes part of a software factory?
- Which parts of a factory workflow should be deterministic checks rather than model judgment?
- How would you design permissions for an agent that reads Slack, GitHub, docs, and browser state?
- What evidence would prove that agent-written PRs reduce cycle time without increasing review debt?
- How should long-running missions expose state so humans can steer them before errors compound?
