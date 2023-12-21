const url = "http://localhost:443/backgroundDemo";

const decklist = `
Pokémon (19)
4 Arceus V BRS 122
3 Arceus VSTAR BRS 123
2 Bidoof CRZ 111
2 Bibarel BRS 121
1 Regigigas V CRZ 113
1 Regigigas VSTAR CRZ 114
1 Zacian V CEL 16
1 Radiant Alakazam SIT 59
1 Mew ex MEW 151
1 Skwovet SVI 151
1 Jirachi PAR 126
1 Spiritomb PAL 89

Trainer (28)
4 Iono PAL 185
4 Boss's Orders PAL 172
2 Cheren's Care BRS 134
1 Raihan CRZ 140
1 Avery CRE 130
4 Ultra Ball SVI 196
4 Nest Ball SVI 181
2 Lost Vacuum CRZ 135
1 Escape Rope BST 125
1 Box of Disaster LOR 154
1 Choice Belt PAL 176
3 Path to the Peak CRE 148

Energy (13)
7 Psychic Energy 5
4 Double Turbo Energy BRS 151
2 Jet Energy PAL 190
`;

fetch(url, {
    method: 'POST',
    headers: {
        'Content-Type': 'application/json'
    },
    body: JSON.stringify(decklist)
})
.then(response => response.json())
.then(data => console.log(data));
