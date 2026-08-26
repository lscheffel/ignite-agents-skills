# Pre-Flight Checklist

Multi-Agent Orchestration Checklist before initialization.

## Decomposition
- [ ] Task decomposed into clear subtasks
- [ ] Dependencies between subtasks mapped
- [ ] Independent subtasks identified for parallelism

## Roles
- [ ] Role defined for each agent
- [ ] Role card filled in for each agent
- [ ] Responsibilities do not overlap

## Contracts
- [ ] I/O contract defined for each handoff
- [ ] Schemas consistent across agents
- [ ] Validation implemented for each contract
- [ ] Fallback defined for each contract

## Routing
- [ ] Model selected for each role
- [ ] Estimated cost documented
- [ ] Fallback model defined
- [ ] Adequate throughput

## Execution
- [ ] Fan-out configured for independent subtasks
- [ ] Fan-in configured for aggregation
- [ ] Synchronization gate defined
- [ ] Context window configured
- [ ] Logging configured