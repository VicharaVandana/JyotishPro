import xml.etree.ElementTree as ET
import codecs
translations = {
  'Add': {'hi': 'जोड़ें', 'kn': 'ಸೇರಿಸಿ'},
  'Submit': {'hi': 'जमा करें', 'kn': 'ಸಲ್ಲಿಸಿ'},
  'English': {'hi': 'अंग्रेज़ी', 'kn': 'ಇಂಗ್ಲಿಷ್'},
  'Kannada': {'hi': 'कन्नड़', 'kn': 'ಕನ್ನಡ'},
  'Hindi': {'hi': 'हिंदी', 'kn': 'ಹಿಂದಿ'},
  'Language': {'hi': 'भाषा', 'kn': 'ಭಾಷೆ'},
  'Chart Style': {'hi': 'चार्ट शैली', 'kn': 'ಚಾರ್ಟ್ ಶೈಲಿ'},
  'North Indian': {'hi': 'उत्तर भारतीय', 'kn': 'ಉತ್ತರ ಭಾರತೀಯ'},
  'South Indian': {'hi': 'दक्षिण भारतीय', 'kn': 'ದಕ್ಷಿಣ ಭಾರತೀಯ'},
  'BirthChart': {'hi': 'जन्म कुंडली', 'kn': 'ಜನ್ಮ ಕುಂಡಲಿ'},
  'Mixed Charts': {'hi': 'मिश्रित कुंडली', 'kn': 'ಮಿಶ್ರ ಕುಂಡಲಿ'},
  'Astrological Charts': {'hi': 'ज्योतिष चार्ट', 'kn': 'ಜ್ಯೋತಿಷ್ಯ ಚಾರ್ಟ್'},
  'UserDetails': {'hi': 'विवरण', 'kn': 'ವಿವರಗಳು'},
  'PDF Report': {'hi': 'पीडीएफ रिपोर्ट', 'kn': 'ಪಿಡಿಎಫ್ ವರದಿ'},
  'Settings': {'hi': 'सेटिंग्स', 'kn': 'ಸೆಟ್ಟಿಂಗ್‌ಗಳು'},
  'Display Settings': {'hi': 'प्रदर्शन सेटिंग्स', 'kn': 'ಪ್ರದರ್ಶನ ಸೆಟ್ಟಿಂಗ್‌ಗಳು'},
  'File': {'hi': 'फ़ाइल', 'kn': 'ಫೈಲ್'},
  'Import': {'hi': 'आयात करें', 'kn': 'ಆಮದು ಮಾಡಿ'},
  'Export': {'hi': 'निर्यात करें', 'kn': 'ರಫ್ತು ಮಾಡಿ'},
  'Delete': {'hi': 'हटाएं', 'kn': 'ಅಳಿಸಿ'},
  'Fetch': {'hi': 'लाएं', 'kn': 'ತರಲು'},
  'Generate PDF Report': {'hi': 'पीडीएफ रिपोर्ट बनाएं', 'kn': 'ಪಿಡಿಎಫ್ ವರದಿ ರಚಿಸಿ'},
  'Name': {'hi': 'नाम', 'kn': 'ಹೆಸರು'},
  'Gender': {'hi': 'लिंग', 'kn': 'ಲಿಂಗ'},
  'Time of Birth': {'hi': 'जन्म समय', 'kn': 'ಜನನದ ಸಮಯ'},
  'Date of Birth': {'hi': 'जन्म तिथि', 'kn': 'ಜನನದ ದಿನಾಂಕ'},
  'Place of Birth': {'hi': 'जन्म स्थान', 'kn': 'ಜನನದ ಸ್ಥಳ'},
  'Longitude': {'hi': 'देशांतर', 'kn': 'ರೇಖಾಂಶ'},
  'Lattitude': {'hi': 'अक्षांश', 'kn': 'ಅಕ್ಷಾಂಶ'},
  'Timezone': {'hi': 'समय क्षेत्र', 'kn': 'ಸಮಯ ವಲಯ'},
  'Comments': {'hi': 'टिप्पणियाँ', 'kn': 'ಕಾಮೆಂಟ್‌ಗಳು'},
  'male': {'hi': 'पुरुष', 'kn': 'ಪುರುಷ'},
  'female': {'hi': 'महिला', 'kn': 'ಮಹಿಳೆ'},
  'other': {'hi': 'अन्य', 'kn': 'ಇತರೆ'},
  'Transit': {'hi': 'गोचर (Transit)', 'kn': 'ಗೋಚರ'},
  'Natal': {'hi': 'जन्म (Natal)', 'kn': 'ಜನ್ಮ'},
  'Outer Chart': {'hi': 'बाहरी चार्ट', 'kn': 'ಹೊರಗಿನ ಚಾರ್ಟ್'},
  'Inner Chart': {'hi': 'आंतरिक चार्ट', 'kn': 'ಒಳಗಿನ ಚಾರ್ಟ್'},
  'Sun': {'hi': 'सूर्य', 'kn': 'ಸೂರ್ಯ'},
  'Moon': {'hi': 'चंद्र', 'kn': 'ಚಂದ್ರ'},
  'Mars': {'hi': 'मंगल', 'kn': 'ಮಂಗಳ'},
  'Mercury': {'hi': 'बुध', 'kn': 'ಬುಧ'},
  'Jupiter': {'hi': 'गुरु', 'kn': 'ಗುರು'},
  'Venus': {'hi': 'शुक्र', 'kn': 'ಶುಕ್ರ'},
  'Saturn': {'hi': 'शनि', 'kn': 'ಶನಿ'},
  'Rahu': {'hi': 'राहु', 'kn': 'ರಾಹು'},
  'Ketu': {'hi': 'केतु', 'kn': 'ಕೇತು'},
  'Aries': {'hi': 'मेष', 'kn': 'ಮೇಷ'},
  'Taurus': {'hi': 'वृषभ', 'kn': 'ವೃಷಭ'},
  'Gemini': {'hi': 'मिथुन', 'kn': 'ಮಿಥುನ'},
  'Cancer': {'hi': 'कर्क', 'kn': 'ಕರ್ಕಾಟಕ'},
  'Leo': {'hi': 'सिंह', 'kn': 'ಸಿಂಹ'},
  'Virgo': {'hi': 'कन्या', 'kn': 'ಕನ್ಯಾ'},
  'Libra': {'hi': 'तुला', 'kn': 'ತುಲಾ'},
  'Scorpio': {'hi': 'वृश्चिक', 'kn': 'ವೃಶ್ಚಿಕ'},
  'Saggitarius': {'hi': 'धनु', 'kn': 'ಧನುಸ್ಸು'},
  'Capricorn': {'hi': 'मकर', 'kn': 'ಮಕರ'},
  'Aquarius': {'hi': 'कुंभ', 'kn': 'ಕುಂಭ'},
  'Pisces': {'hi': 'मीन', 'kn': 'ಮೀನ'}
}

def translate_file(filepath, lang):
    tree = ET.parse(filepath)
    root = tree.getroot()
    count = 0
    for message in root.iter('message'):
        source = message.find('source')
        translation = message.find('translation')
        if source is not None and translation is not None:
            text = source.text
            if text in translations:
                translation.text = translations[text][lang]
                translation.attrib.pop('type', None)
                count += 1
    tree.write(filepath, encoding='utf-8', xml_declaration=True)
    print(f'Translated {count} words in {filepath}')

translate_file('./translations/hindi.ts', 'hi')
translate_file('./translations/kannada.ts', 'kn')
