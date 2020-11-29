# Customizing FilterableDropdown's search behavior


Out of the box, FilterableDropdown does a very simple 'startswith' style lookup to find candidates which match the user's input. However, this behavior can be customized using GooeyOptions to support all kinds of filtering strategies. 

For each example, we'll be starting with the following sample program. This uses just 4 choices to keep the different options easy to follow. However, `FilterableDropdown` is fully virtualized and can be used with 10s of thousands of choices. 


```python
from gooey import Gooey, GooeyParser, PrefixTokenizers

choices = [
    'Afghanistan Kabul',
    'Albania Tirana',
    'Japan Kyoto',
    'Japan Tokyo'
]

@Gooey(program_name='FilterableDropdown Demo', poll_external_updates=True)
def main():
    parser = GooeyParser(description="Example of the Filterable Dropdown")
    parser.add_argument(
        "-a",
        "--myargument",
        metavar='Country',
        help='Search for a country',
        choices=choices,
        widget='FilterableDropdown',
        gooey_options={
            'label_color': (255, 100, 100),
            'placeholder': 'Start typing to view suggestions'
        })
    args = parser.parse_args()
    print(args)
```






## Combining results 

## Suffix Trees
  

 
 

