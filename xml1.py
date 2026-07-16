import xml.etree.ElementTree as ET

data = '''
<person>
  <name>Chuck</name>
  <phone type="intl">
    +1 734 303 4456
  </phone>
  <email hide="yes" />
</person>'''

tree = ET.fromstring(data)
print('Name:', tree.find('name').text)#tree.find, finds the tag named name and .text means it goes to the text and takes whats inside name
print('Attr:', tree.find('email').get('hide'))#finds the tag named email and then .get finds the content inside hide
