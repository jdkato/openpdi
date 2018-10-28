# Use of Force (`uof`)

> The use of force can generally be defined as the means of compelling
> compliance or overcoming resistance to an officer’s command(s) in
> order to protect life or property or to take a person into custody.
>
> *-- [Police Data Initiative](https://www.policedatainitiative.org/datasets/use-of-force/)*

## Description of standardized data

Each row in the standardized data contains information for single
officer-subject *Use of Force* incident. If multiple officers or subjects were
involved, there will be multiple rows for the given incident.

| Column name  | Column meaning                                                  | Example value              |
|--------------|-----------------------------------------------------------------|----------------------------|
| date         | The date of the incident in YYYY-MM-DD format.                  | 2015-12-31                 |
| state        | The two-letter code for the state in which the stop occurred.   | TX                         |
| address      | The street address of the incident.                             | 1511 FARO DR               |
| city         | The city of the incident.                                       | AUSTIN                     |
| latitude     | The latitudinal position of the incident.                       | 37.3860517                 |
| longitude    | The longitudinal position of the incident.                      | -122.0838511               |
| service      | The service being performed by the involved officer.            | TRAFFIC STOP               |
| force_type   | A label indicating the type of force used (see Classification). | VERBAL                     |
| force_raw    | The original data value from which we compute `force_type`.     | HAND STRIKE                |
| reason_type  | A label indicating the reason for force (see Definitions).      | PA                         |
| disposition  | The final ruling of whether or not the UoF was justified.       | AUTHORIZED or UNAUTHORIZED |

## Definitions

### `reason_type`

## Classification

### `force_type`
