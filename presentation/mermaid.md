``` mermaid
flowchart LR
    A{open-meteo} --> L((open-meteo API Requests))
    L --> B[London Dataframe]
    L --> C[Bangkok Dataframe]
    L --> D[ ... ]
    L --> E[Hong Kong Dataframe]
    G{top 20 cities website} -->|scraping| H(python list of 20 cities)
    I{OpenStreetMaps} --> J((OSM API request))
    H --> J
    J --> K(python list of dictionaries for coordinates of all cities)
    K --> L
    B --> M[Weather Dataframe:<br>each row is a time and city]
    C --> M
    D --> M
    E --> M
    M -.- F(save as .csv files)
    N{Google NGRAMS} --> S(json format)
    S -->|scraping| T(list of frequencies for each search)
    T --> U[NGRAMS Dataframe]
    U --> F
    M --> V[Final SQL Database]
    U --> V
    V -->|Data manipulation| O(London Visualisations)
    V -->|Data manipulation| Q(Descriptive Visualisations)
    V -->|Data manipulation| R(More Complex and Interactive Visualisations)
```
