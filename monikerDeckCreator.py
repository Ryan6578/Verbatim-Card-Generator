import sys
import os
from PIL import Image, ImageFont, ImageDraw
import datetime
import re
import math

# Cache
arc = {}
charSizes = {}
fonts = {}

def size_text(bounds, image, text, font, fontSize):
    width, height = bounds

    result = ''

    textEdit = ImageDraw.Draw(image)

    fontKey = font + str(fontSize)
    if fontKey in fonts:
        currentFont = fonts[fontKey]
    else:
        currentFont = ImageFont.truetype(font, encoding='unic', size=fontSize)
        fonts[fontKey] = currentFont

    size = 0

    for word in text.split():
        wordSize = 0
        for char in word:
            charKey = font + str(fontSize) + char
            if charKey in charSizes:
                # Cached value found - use that
                charW, charH = charSizes[charKey]
                size += charW
                wordSize += charW
            else:
                charW, charH = textEdit.textsize(char, font=currentFont)
                charSizes[charKey] = (charW, charH)
                size += charW
                wordSize += charW

        # Account for the space needed
        if result != '':
            spaceKey = font + str(fontSize) + ' '
            if spaceKey in charSizes:
                charW, charH = charSizes[spaceKey]
                size += charW
            else:
                charW, charH = textEdit.textsize(' ', font=currentFont)
                charSizes[spaceKey] = (charW, charH)
                size += charW

        if size > width:
            # Need a newline
            result += ('\n' + word)
            size = wordSize
        else:
            # Don't need a newline
            if result != '':
                result += (' ' + word)
            else:
                result += word

    return currentFont, result

startTime = datetime.datetime.now()

# Check to see that we have one argument (other than the script name)
if len(sys.argv) != 2:
    print('You need to specify a file name as an argument.')
    sys.exit()

# Make sure the file exists
if not os.path.isfile(sys.argv[1]):
    print('Input file does not exist.')
    sys.exit()

# Make sure the file is readable
if not os.access(sys.argv[1], os.R_OK):
    print('Input is not readable.')
    sys.exit()

# Font files
titleFont = './assets/proxima-nova-soft-bold.otf'
descriptionFont = './assets/proxima-nova-soft-regular.otf'
categoryFont = './assets/proxima-nova-soft-regular.otf'
pointFont = './assets/proxima-nova-soft-regular.otf'
pointTextFont = './assets/gotham-rounded-bold.otf'

sheetNumber = 1
column = 1
row = 1
cards = []
cardsLeft = 0

with open(sys.argv[1], 'r', encoding='UTF-8') as data:
    for line in data:
        line = line.replace('\n', '').strip()

        # Skip any empty lines
        if line == '':
            continue

        cardDetails = line.split('|')

        # Make sure we have five fields
        if len(cardDetails) != 5:
            continue

        # Make sure the color is a valid color
        if not re.match(r'^#([A-Fa-f0-9]){6}$', cardDetails[4]):
            continue

        cards.append(cardDetails)
        cardsLeft += 1

# Create each card
for cardDetails in cards:

    # Load new card image
    cardImage = Image.open('./assets/card.png')

    # Get the card dimensions
    cardWidth, cardHeight = cardImage.size

    # Create a new card sheet - if necessary
    if column == 1 and row == 1:
        if cardsLeft >= 70:
            currentSheet = Image.new('RGBA', (10 * cardWidth, 7 * cardHeight))
            cardsLeft -= 70
        else:
            # Handle columns
            if cardsLeft >= 10:
                newColumns = 10
            else:
                newColumns = cardsLeft

            newRows = math.ceil(cardsLeft / 10)

            currentSheet = Image.new('RGBA', (newColumns * cardWidth, newRows * cardHeight))

    # Get the card's color information
    hexColor = cardDetails[4].replace('#', '')
    red = int(hex((int(hexColor, 16) & 0xFF0000) >> 16), 16)
    green = int(hex((int(hexColor, 16) & 0x00FF00) >> 8), 16)
    blue = int(hex(int(hexColor, 16) & 0x0000FF), 16)

    # Draw the point circle
    if cardDetails[4] not in arc:
        arcImage = Image.new('RGBA', (2400, 2400), color=(0, 0, 0, 0))
        edit = ImageDraw.Draw(arcImage, mode='RGBA')
        edit.ellipse([(200, 200), (2200, 2200)], fill=(red, green, blue, 255), width=1)
        edit.rectangle([(200, 1000), (2200, 2200)], fill=(red, green, blue, 255), width=1)
        arcImageResized = arcImage.resize((200, 200), resample=Image.LANCZOS)
        finalArc = arcImageResized.crop((18, 10, 182, 180))
        arc[cardDetails[4]] = finalArc
    else:
        finalArc = arc[cardDetails[4]]
    arcW, arcH = finalArc.size
    cardImage.paste(finalArc, box=(332 - round(arcW/2), cardHeight - arcH), mask=finalArc)

    # Edits
    edit = ImageDraw.Draw(cardImage)

    # Title
    font, title = size_text((603, 100), cardImage, cardDetails[0], './assets/proxima-nova-soft-bold.otf', 45)
    editW, editH = edit.textsize(title, font=font)
    edit.text((332 - (editW/2), 100 - (editH/2)), title, fill=(0, 0, 0, 255), font=font, align='center')

    # Description
    font, description = size_text((543, 100), cardImage, cardDetails[1], './assets/proxima-nova-soft-regular.otf', 30)
    editW, editH = edit.textsize(description, font=font)
    edit.text((60, 300), description, fill=(0, 0, 0, 255), font=font, align='left')

    # Category
    font, category = size_text((600, 100), cardImage, cardDetails[2], './assets/proxima-nova-soft-regular.otf', 35)
    editW, editH = edit.textsize(category, font=font)
    edit.text((332 - (editW/2), 778 - (editH/2)), category, fill=(red, green, blue, 255), font=font, align='center')

    # Point Value
    font, points = size_text((300, 100), cardImage, cardDetails[3], './assets/proxima-nova-soft-regular.otf', 55)
    editW, editH = edit.textsize(points, font=font)
    edit.text((332 - (editW/2), 895 - (editH/2)), points, fill=(255, 255, 255, 255), font=font, align='center')

    # Point Text
    font, pointText = size_text((300, 100), cardImage, 'POINTS', './assets/gotham-rounded-bold.otf', 20)
    editW, editH = edit.textsize(pointText, font=font)
    edit.text((332 - (editW/2), 945 - (editH/2)), pointText, fill=(255, 255, 255, 255), font=font, align='center')


    # Paste at the offset
    currentSheet.paste(cardImage, ((cardWidth * column) - cardWidth, (cardHeight * row) - cardHeight))

    # Increment the column
    column += 1

    if column > 10 and row < 7:
        column = 1
        row += 1

    if column > 10 and row == 7:
        # Save the current sheet
        currentSheet.save(str(sheetNumber) + '.png', 'PNG', compress_level=1)

        # Increment the sheet number
        sheetNumber += 1

        # Reset the column/row
        column = 1
        row = 1

    # TODO: Debugging messages - remove once complete
    print('      Title: ' + cardDetails[0])
    print('Description: ' + cardDetails[1])
    print('   Category: ' + cardDetails[2])
    print('Point Value: ' + cardDetails[3])
    print('      Color: ' + cardDetails[4])
    print()

currentSheet.save(str(sheetNumber) + '.png', 'PNG')

endTime = datetime.datetime.now()
duration = endTime - startTime
print('Elapsed time: ' + str(duration.total_seconds()))
