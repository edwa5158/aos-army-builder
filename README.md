[![Quality Gate Status](https://sonarcloud.io/api/project_badges/measure?project=edwa5158_aos-army-builder&metric=alert_status)](https://sonarcloud.io/summary/new_code?id=edwa5158_aos-army-builder)

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