# Age of Empires II content and balance analysis in the context of top RTS games

## Top RTS Games Comparison
Compare 11 RTS games, focusing on players over time and frequency of game updates

## Analysis of public Age of Empires II games

A look into the players, matches, and civilizations that keep this 20+ year old game going
* Focused analysis on game updates for AoEII:DE
* Focused analysis on civilization balance for AOEII:DE

### Project Structure
All code and presentation material available at [github.com/rishigoutam/aoe2](github.com/rishigoutam/aoe2)

#### Data Analysis
* `src/` contains all notebooks used for data analysis and python files to process scraping 

    - ↳ `rts_player_counts` analyzes top 11 RTS games in terms of frequency of game updates and player counts
    - ↳ `aoe_player_count_analysis` compares the AoE2:HD vs AoE2:DE game data
    - ↳ `aoe2de_analysis` looks into balance for matches played in AoE2:DE
    - ↳ `patch_scraper` scrapes game update data (patches) from steamdb.info

#### Data
* `data/aoe2net/` has the match and players datasets from Kaggle
* `data/steamdb`
  * ↳ `/charts/` has player count data from steamdb.info 
  * ↳ `/game-updates/` has game update data from steamdb.info
* `data/gen/` has notebook-generated game patch data and detailed game patch data for AoEII:DE

#### Graphs and CSVs
* `outputs/` stores the generated plots and CSVs from the data analysis notebooks

### Acknowledgements

Thanks to the below projects for providing the data for analysis:

- [aoe2.net](aoe2.net#api) - Reverse engineered game protocols to extract information from game replay files. Provided API for scraping data (used in the dataset by [aoe2stats.io](aoe2stats.io))
- [aoestats.io](aoestats.io) - @jerkeeler/Jeremy K for using aoe2.net to create `match` and `player` datasets as CSVs on [Kaggle.com](https://www.kaggle.com/jerkeeler/aoestats-io-example/data)
- [steamdb.info](https://steamdb.info/app/813780/graphs/) - For information around number of steam players
- [Steam Top RTS games](https://store.steampowered.com/tags/en/RTS/?flavor=contenthub_toprated)
- Microsoft for making the game along with supporting it with updates and new versions all these years
- The Age community for keeping this game alive
