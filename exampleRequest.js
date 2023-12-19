const url = "https://cardsapi.onrender.com/Deck";

const decklist = `
3 Roaring Moon ex PAR 124
1 Squawkabilly ex PAL 169
1 Galarian Moltres V CRE 97
1 Brute Bonnet PAR 123
1 Radiant Greninja ASR 46
1 Morpeko PAR 121
1 Lumineon V BRS 40

4 Professor Sada's Vitality PAR 170
1 Iono PAL 185
1 Boss's Orders PAL 172
4 Battle VIP Pass FST 225
4 Dark Patch ASR 139
4 Cross Switcher FST 230
4 Earthen Vessel PAR 163
4 Energy Switch SVI 173
3 Ultra Ball SVI 196
2 Switch Cart ASR 154
1 Hisuian Heavy Ball ASR 146
1 Super Rod PAL 188
1 Pal Pad SVI 182
1 Canceling Cologne ASR 136
2 Ancient Booster Energy Capsule PAR 159
3 PokéStop PGO 68
1 Collapsed Stadium BRS 137

7 Darkness Energy 7
3 Water Energy 3
`;

fetch("https://cardsapi.onrender.com/")
    .then(response => {
        if (!response.ok) {
            return response.text().then(text => { throw new Error(text) });
        }
        return response.json();
    })
    .then(data => console.log(data))
    .catch(error => console.log('Error:', error));

fetch("https://cardsapi.onrender.com/Deck")
    .then(response => {
        if (!response.ok) {
            return response.text().then(text => { throw new Error(text) });
        }
        return response.json();
    })
    .then(data => console.log(data))
    .catch(error => console.log('Error:', error));

fetch(url, {
    method: 'POST',
    headers: {
        'Content-Type': 'application/json'
    },
    body: JSON.stringify(decklist)
})
.then(response => {
    if (!response.ok) {
        return response.text().then(text => { throw new Error(text) });
    }
    return response.json();
})
.then(data => console.log(data))
.catch(error => console.log('Error:', error));
