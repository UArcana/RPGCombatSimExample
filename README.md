# Automated Combat Simulation & Balance Analyzer
A Python tool to simulate thousands of automated battles based on JSON-like weapons, skills, modifiers and such. 
Generates statistical reports to identify dominant strategies and balance issues in RPG combat systems.

## Features / Highlights
- Runs 10000+ simulated battles in minutes
- Outputs detailed reports for designers and developers
- Fully data-driven, using JSON-like input for easy iteration

## How to Run
1. Clone the repository:
   git clone https://github.com/UArcana/RPGCombatSimExample.git
2. Navigate to the project folder:
   cd RPGCombatSimExample
3. Run the simulation:
   python src/main.py

## What it Produces
- Summary of win rates for each weapon, skill combination with modifier details in Statistics folder.
- Early identification of broken or dominant strategies or gameplay issues
- Statistical reports for further analysis

## Why It Matters
- Supports system-level balancing without relying on manual play-testing
- Highlights potential design issues before content implementation
- Demonstrates proficiency in programming, data-driven design, and game systems analysis

## Other Settings and Modes
- Switching "STATISTICS_TEST_MODE" to false on main.py allows inspection of a single battle real-time.
- Test limitations can be set in TestStatistics.py
- AbilityDatabase.py contains the modifiable database for variables used in testing.