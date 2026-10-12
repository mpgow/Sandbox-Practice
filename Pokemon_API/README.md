# Pokemon API (PokeApi)

Find out your Pokemon Team Weaknesses (PTW)! Provided courtesy of [PokeApi](https://pokeapi.co/), check out their website for all sorts of free updated pokemon data from, "Pokémon to Berry Flavors."

* More REST API practice, but now with image loading and type weakness handling from querying the stored sqlite data of your team of 6 (or fewer) pokemon
* Search for pokemon via their id or name, replacing one of your choice if necessary. PokeApi will browser display the official artwork of each pokemon to confirm you've selected the right one
* Aggregates all of the pokemon types that would be (naively, compared individually) strong against your pokemon, and all of the types your pokemon are strong against (naively, assuming attack types match pokemon type)
* Identifies gaps of types that are strong against you without your own attack coverage, then randomly selects and displays a pokemon that has a type effective against your team!

Note:
This was not designed to save your team for prolonged use in a database, a file is created but not committed to; you can edit to commit pokemon but you'll also need to add voluntary deletion/team-wipe feature.

There's a small easter egg for those of you feeling lucky.