# Verbatim-Card-Generator
Card generator for Verbatim.

## Prerequisites
* [Python 3.7+](https://www.python.org/downloads/)
* [Pillow - PIL Fork](https://github.com/python-pillow/Pillow)

To install Pillow using pip:
``` pip install pillow```

## Input Data
The script uses a TSV (tab separated value) file to get the data for the cards it makes. You can do this in either Microsoft Excel or in Google Drive (with Google Sheets). Export your data as a .tsv file to use it with this script. In Google Sheets, this can be done by going to File > Download as > Tab-separated values (.tsv, current sheet).

Important information regarding spreadsheet formatting:
* The spreadsheet must have 5 columns (column A - column E)
  * Column A: Title
  * Column B: Description
  * Column C: Category (Geography, Historical, Fictional, Quote, ET Cetera, Political, Science, etc.)
  * Column D: Point Value (Typically between 1-4)
  * Column E: Color (hexadecimal values: 1 = #024716, 2 = #0f1a4f, 3 = #841215, 4 = #191717)
  
Example Spreadsheet:

Column A | Column B | Column C | Column D | Column E
-------- | -------- | -------- | -------- | --------
Cyndi Lauper | A "Girls just want to have fun" advocate who was a very prominent fashion idol during the 80s. With other famous songs like "Time After Time", "She Bop", and "All Through the Night". | CELEBRITY | 1 | #024716
André the Giant | A 7 ft 4 in (224 cm), 520 lb (236 kg) Frenchmen who was the first wrestler inducted into the WWE Hall of fame. He played the rhyming Turkish wrestler Fezzik in The Princess Bride. | CELEBRITY | 1 | #024716
Lollies | USA:Candies UK:Sweets | ET CETERA | 1 | #024716
Smokey the Bear | A mascot for the US Forest Service who wears a wide-brimmed brown hat and teaches about the dangers of wildfires. "Remember only YOU can prevent forest fires," circa 1947. | FICTIONAL | 2 | #0f1a4f
Ping An International Finance Centre | A 115-story megatall skyscraper in Shenzhen, Guangdong. The building was commissioned by an Insurance company and designed by the American architectural firm Kohn Pedersen Fox Associates. It was completed in 2017. | GEOGRAPHY | 3 | #841215

## How to Use
1. Install all the required dependencies listed above.
2. Download/clone this project and open the location in Windows Explorer.
3. Move your .tsv file into this same directory.
4. Open a command prompt at this location (type "cmd" in the address bar in Windows Explorer and hit enter).
5. Run the Python script (replace sheet.tsv with your .tsv file name):
```python verbatimDeckCreator.py sheet.tsv```
