import pygtrie as trie
from fuzzywuzzy import process

class BasicDisplayOptions(object):
    pass

countries = ["Abkhazia -> Abkhazia", "Afghanistan",
             "Albania", "Algeria", "Andorra", "Angola", "Antigua and Barbuda", "Argentina",
             "Armenia", "Artsakh -> Artsakh", "Australia", "Austria", "Azerbaijan", "Bahamas, The",
             "Bahrain", "Bangladesh", "Barbados", "Belarus", "Belgium", "Belize", "Benin", "Bhutan",
             "Bolivia", "Bosnia and Herzegovina", "Botswana", "Brazil", "Brunei", "Bulgaria",
             "Burkina Faso[j]", "Burma -> Myanmar", "Burundi", "Cambodia", "Cameroon", "Canada[k]",
             "Cape Verde", "Central African Republic", "Chad", "Chile", "China",
             "China, Republic of -> Taiwan", "Colombia", "Comoros",
             "Congo, Democratic Republic of the[p]", "Congo, Republic of the",
             "Cook Islands -> Cook Islands", "Costa Rica", "Croatia", "Cuba", "Cyprus",
             "Czech Republic[r]", "Democratic People's Republic of Korea -> Korea, North",
             "Democratic Republic of the Congo -> Congo, Democratic Republic of the", "Denmark",
             "Djibouti", "Dominica", "Dominican Republic", "East Timor", "Ecuador", "Egypt",
             "El Salvador", "Equatorial Guinea", "Eritrea", "Estonia", "Eswatini -> Swaziland",
             "Ethiopia", "Fiji", "Finland", "France", "Gabon", "Gambia, The", "Georgia", "Germany",
             "Ghana", "Greece", "Grenada", "Guatemala", "Guinea", "Guinea", "Guyana", "Haiti",
             "Holy See -> Vatican City", "Honduras", "Hungary", "Iceland[v]", "India", "Indonesia",
             "Iran", "Iraq", "Ireland", "Israel", "Italy", "Ivory Coast", "Jamaica", "Japan",
             "Jordan", "Kazakhstan", "Kenya", "Kiribati", "Korea, North", "Korea, South",
             "Kosovo -> Kosovo", "Kuwait", "Kyrgyzstan", "Laos", "Latvia", "Lebanon", "Lesotho",
             "Liberia", "Libya", "Liechtenstein", "Lithuania", "Luxembourg", "Madagascar", "Malawi",
             "Malaysia", "Maldives", "Mali", "Malta", "Marshall Islands", "Mauritania", "Mauritius",
             "Mexico", "Micronesia", "Moldova", "Monaco", "Mongolia", "Montenegro", "Morocco",
             "Mozambique", "Myanmar", "Nagorno", "Namibia", "Nauru", "Nepal", "Netherlands",
             "New Zealand", "Nicaragua", "Niger", "Nigeria", "Niue -> Niue",
             "Northern Cyprus -> Northern Cyprus", "North Korea -> Korea, North", "North Macedonia",
             "Norway", "Oman", "Pakistan", "Palau", "Palestine", "Panama", "Papua New Guinea",
             "Paraguay", "Peru", "Philippines", "Poland", "Portugal",
             "Pridnestrovie -> Transnistria", "Qatar", "Republic of Korea -> Korea, South",
             "Republic of the Congo -> Congo, Republic of the", "Romania", "Russia", "Rwanda",
             "Sahrawi Arab Democratic Republic -> Sahrawi Arab Democratic Republic",
             "Saint Kitts and Nevis", "Saint Lucia", "Saint Vincent and the Grenadines", "Samoa",
             "San Marino", "São Tomé and Príncipe", "Saudi Arabia", "Senegal", "Serbia",
             "Seychelles", "Sierra Leone", "Singapore", "Slovakia", "Slovenia", "Solomon Islands",
             "Somalia", "Somaliland -> Somaliland", "South Africa", "South Korea -> Korea, South",
             "South Ossetia -> South Ossetia", "South Sudan", "Spain", "Sri Lanka", "Sudan",
             "Sudan, South -> South Sudan", "Suriname", "Swaziland", "Sweden", "Switzerland",
             "Syria", "Taiwan (Republic of China) -> Taiwan", "Tajikistan", "Tanzania", "Thailand",
             "The Bahamas -> Bahamas, The", "The Gambia -> Gambia, The", "Timor", "Togo", "Tonga",
             "Transnistria -> Transnistria", "Trinidad and Tobago", "Tunisia", "Turkey",
             "Turkmenistan", "Tuvalu", "Uganda", "Ukraine", "United Arab Emirates",
             "United Kingdom", "United States", "Uruguay", "Uzbekistan", "Vanuatu", "Vatican City",
             "Venezuela", "Vietnam", "Yemen", "Zambia", "Zimbabwe",
             "↑ UN member states and observer states ↑", "", "↓ Other states ↓", "Abkhazia",
             "Artsakh", "Cook Islands", "Kosovo", "Niue", "Northern Cyprus",
             "Sahrawi Arab Democratic Republic", "Somaliland", "South Ossetia", "Taiwan",
             "Transnistria", "↑ Other states ↑"]


us_states = ["Alabama", "Alaska", "Arizona", "Arkansas", "California", "Colorado",
                 "Connecticut", "Delaware", "Florida", "Georgia", "Hawaii", "Idaho", "Illinois",
                 "Indiana", "Iowa", "Kansas", "Kentucky[E]", "Louisiana", "Maine", "Maryland",
                 "Massachusetts", "Michigan", "Minnesota", "Mississippi", "Missouri", "Montana",
                 "Nebraska", "Nevada", "New Hampshire", "New Jersey", "New Mexico", "New York",
                 "North Carolina", "North Dakota", "Ohio", "Oklahoma", "Oregon", "Pennsylvania",
                 "Rhode Island", "South Carolina", "South Dakota", "Tennessee", "Texas", "Utah",
                 "Vermont", "Virginia", "Washington", "West Virginia", "Wisconsin", "Wyoming"]

x = trie.Trie()
output = {}
for country in countries:
    for i in country.split():
        if not x.has_key(i):
            x[i] = []
        x[i].append(country)


a = 10