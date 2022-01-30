# Age of Empires II

## Analysis of public Age of Empires II games

A look into the players, matches, and civilizations that keep this 20+ year old game going

### Project Structure
#### Data Analysis
* `src/` contains all notebooks used for data analysis and python files to process scraping
#### Data
* `data/aoe2net/` has the match and players datasets from Kaggle
* `data/steamdb`
* &emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp; ↪ `/charts/` has player count data from steamdb.info
* &emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp; ↪ `/game-updates/` has game update data from steamdb.info
* `data/gen/` has generated game patch data and detailed game patch data for AoEII:DE
#### Graphs and CSVs
* `outputs/` stores the generated plots and CSVs from the data analysis notebooks
## Acknowledgements

Thanks to the below projects for providing the data for analysis:

- [aoe2.net](aoe2.net#api) - Reverse engineered game protocols to extract information from game replay files. Provided API for scraping data (used in the dataset by [aoe2stats.io](aoe2stats.io))
- [aoestats.io](aoestats.io) - @jerkeeler/Jeremy K for using aoe2.net to create `match` and `player` datasets as CSVs on [Kaggle.com](https://www.kaggle.com/jerkeeler/aoestats-io-example/data)
- [steamdb](https://steamdb.info/app/813780/graphs/) - For information around number of steam players
- Microsoft and Ensemble Studios for making the game along with supporting it with updates and new versions all these years
- The Age community
