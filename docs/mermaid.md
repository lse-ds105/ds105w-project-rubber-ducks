``` mermaid
flowchart TD
    A{open.meteo website} --> L((API Requests))
    L --> B[London Dataframe]
    L --> C[City 1 Dataframe]
    L --> D[City ... Dataframe]
    L --> E[City 19 Dataframe]
    B -.- F(save as .json/.csv file)
    C -.- F
    D -.- F
    E -.- F
    G{top 20 cities website} -->|css/xpath scraping| H(python list of 20 cities)
    I{coordinates website} -->|css/xpath scraping| J(python list of coordinates)
    J -->|merge lists| K(python list of cities and their coordinates)
    H -->|merge lists| K
    K --> L
    B --> M[Final Datframe: 
    rows = cities
    columns = weather + perception variables]
    C --> M
    D --> M
    E --> M
    N{perception wesbite} -->|merge?| M
    M -->|Data manipulation| O(London Visualisations)
    M -->|Data manipulation| Q(Descriptive Visualisations)
    M -->|Data manipulation| R(More Complex and Interactive Visualisations)
```


