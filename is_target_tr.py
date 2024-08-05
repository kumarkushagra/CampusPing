from bs4 import BeautifulSoup

# Define a function to filter tr elements
def is_target_tr(tag):
    if tag.name != 'tr':
        return False
    # Check if the tr contains the specified structure
    first_td = tag.find('td', nowrap=True)
    second_td = tag.find('td', class_='list-data-focus')
    if first_td and second_td:
        font_tag = first_td.find('font', size='3')
        img_tag = first_td.find('img', src='images/newicon.gif')
        a_tag = second_td.find('a', href=True, title="NOTICES / CIRCULARS")
        font_tag_2 = a_tag.find('font', size='3') if a_tag else None
        return font_tag and img_tag and a_tag and font_tag_2
    return False
