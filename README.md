# README
I'm building a **modular Age of Sigmar toolkit**.

## Short term:

* Build a **TUI-based army roster builder** that lets you
    - Create, update, and delete models / units
    - Browse units that exist
    - Assemble a roster
        - Include specifying wargear options
        - Include artifacts etc.
    - Save the roster for future use
* Use `textual` for the TUI
* Don't worry about enforcing rules right now
    - Summing the total points, counting number of models etc. is fine
    - Allow filtering units by the selected faction and by unit type

## Long term:

* Add additional tools (e.g., a game assistant for playing matches).
* Possibly replace the TUI with a full GUI.
* Play full games of Age of Sigmar with a friend

## Architecturally:

* Hexagonal Architecture (ports & adapters)
* Core logic (services + domain) is separate from UI and database code.
* SQLite + SQLAlchemy handle persistence.
* UI calls a service layer, which talks to repositories via interfaces.
* Each tool can run independently but share the same core and data.

In one sentence:

> A reusable, modular AoS system that starts as a TUI roster builder and evolves into a full game assistant, with clean separation between UI, logic, and persistence.
