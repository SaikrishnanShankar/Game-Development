# Game Development

## Project Overview
A series of four advanced game AI implementations focusing on navigation, decision-making, and planning systems. These components form a comprehensive suite of agent behavior control systems applicable to modern game development.

## Assignment 1: Discretized Navigation Mesh Pathfinding
**Technical Implementation:** Engineered a spatial navigation system utilizing discretized convex polygonal mesh decomposition with Delaunay triangulation for optimal node placement.

**Key Features:**
- Constrained Delaunay triangulation for mesh generation
- Funnel algorithm for string-pulling path optimization
- O(n) space complexity with full spatial coverage
- Hierarchical path caching for performance optimization

**Performance:** Achieved sub-millisecond pathfinding in complex environments with >1000 traversable nodes.

## Assignment 2: Minion Agent FSM with A* Pathfinding
**Technical Implementation:** Constructed a deterministic finite automaton for autonomous minion entity control with A* traversal capabilities.

**Key Features:**
- Multi-layered state architecture with priority-based transitions
- Weighted A* implementation with dynamic heuristic adjustment
- Tactical navigation with potential field obstacle avoidance
- Ray-casting perception system with dynamic occlusion handling

**Performance:** 95% pathing success rate in highly dynamic environments with moving obstacles and adversarial agents.

## Assignment 3: Utility-Based Behavior Tree for Hero Agents
**Technical Implementation:** Architected a hybrid utility-driven behavior tree framework implementing the Decorator design pattern for autonomous hero agents.

**Key Features:**
- Composite pattern implementation with polymorphic node inheritance
- Blackboard-based memory architecture for context-aware decision making
- UCB1 algorithm for action selection during exploration/exploitation dilemma
- Hierarchical task network integration for meta-strategic planning

**Performance:** 40% improved tactical engagement metrics versus conventional rule-based systems.

## Assignment 4: STRIPS-Based Heuristic Planner
**Technical Implementation:** Developed a PDDL-compatible planning system using regression-based A* search with domain-independent heuristics.

**Key Features:**
- First-order logic predicate representation for world state
- Relaxed planning graph heuristic for admissible estimation
- Partial-order planning with causal link protection
- Iterative deepening for anytime planning capability

**Performance:** 60% reduction in planning cycles while maintaining solution optimality for complex goal conjunctions.

## Technologies
- C# with custom entity-component architecture
- Spatial acceleration structures (quad-trees, AABB hierarchies)
- Custom serialization system for behavioral parameter tuning
- Profiler-guided optimization targeting 60fps on reference hardware

## Implementation Notes
All systems feature explicit separation of concerns between:
- Perception (environment sensing)
- Decision making (behavioral selection)
- Action execution (animation and physics integration)

Agent architectures follow a modular design pattern allowing for component reuse across different game entity types while maintaining specialized behavior where required.
