## DataBase Description

To perform our classification model we create a data base with the following description.

*Note: we create more temporary datasets to create the metadata with CritiScores, the description of these datasets it's in the end of each notebook.*

| Feature                 | Description                                                                                              |
| ----------------------- | -------------------------------------------------------------------------------------------------------- |
| username                | Username associated with the user's account                                                              |
| age                     | Age of the user (encoded as a numerical value)                                                           |
| gender                  | Gender of the user (M/F or other categorical values)                                                     |
| fav_entertainment       | Preferred types of entertainment (TV_shows, Books, Movies)                                               |
| least_fav_entertainment | Types of entertainment the user dislikes the most (TV_shows, Books, Movies)                              |
| likes                   | Genres or entertainment categories the user generally likes ('Animation', 'Classics', 'Fantasy', ...)    |
| dislikes                | Genres or entertainment categories the user generally dislikes ('Animation', 'Classics', 'Fantasy', ...) |
| movie_watching_freq     | Frequency of movie watching (Daily, Weekly, Monthly, Rarely, Never)                                      |
| show_watching_freq      | Frequency of TV show watching (Daily, Weekly, Monthly, Rarely, Never)                                    |
| reading_freq            | Frequency of reading activities (Daily, Weekly, Monthly, Rarely, Never)                                  |
| CritiPersonality        | Personality traits inferred from the user's entertainment preferences and viewing/reading habits         |
