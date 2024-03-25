``` mermaid
flowchart LR
    A{open.meteo website} --> L((API Requests))
    L --> B[London Dataframe]
    L --> C[City 1 Dataframe]
    L --> D[City ... Dataframe]
    L --> E[City 19 Dataframe]
    G{top 20 cities website} -->|scraping| H(python list of 20 cities)
    I{coordinates website} --> J((API request))
    H --> J
    J --> K(python list of dictionaries for coordinates of all cities)
    K --> L
    B --> M[Weather Dataframe: 
    each row is a time and city]
    C --> M
    D --> M
    E --> M
    M -.- F(save as json files)
    N{Google NGRAMS} --> S(json format)
    S --> |scraping| T[dataframe of appearance % for each query]
    T --> |sum by years| U[NGRAMS Dataframe]
    U -.- F
    M --> V[Final Database]
    U --> V
    V -->|Data manipulation| O(London Visualisations)
    V -->|Data manipulation| Q(Descriptive Visualisations)
    V -->|Data manipulation| R(More Complex and Interactive Visualisations)
```
