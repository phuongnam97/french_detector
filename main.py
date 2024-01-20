import re
import unicodedata
import docx2txt
import antiword

# importing sys
import sys
# adding Folder_2/subfolder to the system path
sys.path.insert(0, 'controller')
from dictionnary import check_exist_word 

def remove_numbers(text):
  """Removes all numbers from a string."""
  numbers = set(range(10))
  return ''.join(ch for ch in text if ch not in numbers)

def get_percent(number, total):
  """
  Gets a percent with 2 numbers after the dot character.

  Args:
    number: The number.
    total: The total.

  Returns:
    A string representing the percent.
  """

  percent = number / total * 100
  formatted_percent = "{:.2f}".format(percent)

  return formatted_percent

def check_unexist_french_word(paragraph):
    words, proper_nouns = convert_french_paper_content_to_list_of_words(paragraph)
    print(words)
    not_existed_words = []
    for index, word in enumerate(words):
        # print('Process: ==== ' + index / len(words) * 100 + "%")
        percent = get_percent(index, len(words))
        print("Processing: ==== " + str(percent) + "%")
        if word == '' or word == '-': continue
        if has_number(word): continue
        if (word_start_with_uppercase(word) and word in proper_nouns):
          print('Proper noun: ', word)
          continue
        # remove word accent
        new_word = remove_accents(word)
        existed = check_exist_word(new_word.lower())
        if not existed:
            not_existed_words.append(word)
    return not_existed_words

def remove_urls(text):
    """Removes all URLs from the given text."""
    return re.sub(r"https?://\S+|www\.\S+", "", text)

def remove_urls_without_www(text):
    """Removes URLs without 'www' from the given text."""
    return re.sub(r"\w+(\.)\w+", "", text)

def remove_emails(text):
    """Removes all email addresses from the given text."""
    email_pattern = r"[\w\.-]+@[\w\.-]+\.\w{2,}"  # Matches common email formats
    return re.sub(email_pattern, "", text)

def remove_special_character(text):
    """Removes all "-" from the given text."""
    # character_pattern = r"\s-\s"  # Matches common email formats
    # return re.sub(character_pattern, "", text)
    return "".join(c for c in text if c != "-" or not (c == "-" and c.isspace()))

def remove_accents(word):
    """Removes accents from characters in a word, excluding dashes.

    Args:
        word: The word to remove accents from.

    Returns:
        The word without accents, keeping dashes.
    """
    return ''.join(c if not unicodedata.combining(c) or c == '-' else unicodedata.normalize('NFD', c)[0] for c in word)

def remove_french_special_case(text):
   text = text.replace('J’', "").replace("j’","").replace("S’", "").replace("s’","").replace("L’", "").replace("l’", "").replace("N’", "").replace("n’", "").replace("D’", "").replace("d’", "").replace("C’", "").replace("c’", "c")
   text = text.replace("J'", "").replace("j'","").replace("S'", "").replace("s'","").replace("L'", "").replace("l'", "").replace("N'", "").replace("n'", "").replace("D'", "").replace("d'", "").replace("C'", "").replace("c'", "c")
   text = text.replace("\xa0", " ").replace("/", " ").replace("jusqu’a","").replace("jusqu'a","").replace("jusqu’à","").replace("jusqu'à","").replace("jusqu’aux","").replace("jusqu'aux","").replace("jusqu'en","").replace("jusqu'au","").replace("jusqu’en","").replace("jusqu’au","")
   text = text.replace("aujourd’hui", "aujourd-hui").replace("aujourd'hui", "aujourd-hui").replace("Aujourd’hui", "aujourd-hui").replace("Aujourd'hui", "aujourd-hui")
   text = text.replace("-t-il", "").replace("-t-elle", "")
   text = text.replace("\n", "")
   return text

def convert_french_paper_content_to_list_of_words(paper_content):
  """Converts a French paper content to a list of words.

  Args:
    paper_content: The paper content as a string.

  Returns:
    The paper content as a list of words.
  """

  # Remove all punctuation from the paper content.
  newStr = remove_french_special_case(paper_content)
  newStr = remove_emails(newStr)
  # newStr = paper_content.replace("\xa0", " ").replace("-t-il"," ").replace("-t-elle"," ").replace("/", " ").replace("jusqu’a","").replace("jusqu'a","").replace("jusqu’à","").replace("jusqu'à","").replace("jusqu’aux","").replace("jusqu'aux","").replace("jusqu'en","").replace("jusqu'au","").replace("jusqu’en","").replace("jusqu’au","").replace("aujourd’hui", "aujourd-hui").replace("aujourd'hui", "aujourd-hui").replace("J'", "").replace("j'", "").replace("S'", "").replace("L'", "").replace("l'", "").replace("s'", "").replace("n'", "").replace(" d'", " ").replace("c'", "").replace("S’", "").replace("L’", "").replace("s’", "").replace("l’", "").replace("n’", "").replace(" d’", " ").replace("c’", "").replace("\n", " ")
  newStr = remove_urls(newStr)
  newStr = remove_urls_without_www(newStr)
  # newStr = remove_emails(newStr)

  print("Nam newStr: ", newStr)

  # Remove accents from the paper content.
  # print('Nam normalize NFD: ', paper_content)
  newStr = unicodedata.normalize("NFD", newStr)
  # print('Nam normalize NFD: ', paper_content)
  newStr = "".join([c for c in newStr if not unicodedata.combining(c)])
  newStr = unicodedata.normalize("NFC", newStr)
  # print('Nam normalize NFC: ', paper_content)

  newStr, proper_nouns = get_proper_nouns(newStr)
  print("Proper Nouns: ", proper_nouns)
  
  paper_content = re.sub(r"[^\w\s-]", "", newStr)
  paper_content = remove_french_special_case(paper_content)

  # Convert the paper content to lowercase.
  # paper_content = paper_content.lower()

  # # Remove accents from the paper content.
  # # print('Nam normalize NFD: ', paper_content)
  # paper_content = unicodedata.normalize("NFD", paper_content)
  # # print('Nam normalize NFD: ', paper_content)
  # paper_content = "".join([c for c in paper_content if not unicodedata.combining(c)])
  # paper_content = unicodedata.normalize("NFC", paper_content)
  # print('Nam normalize NFC: ', paper_content)

  # Split the paper content into words.
  words = paper_content.split(" ")

  # Return the list of words.
  return words, proper_nouns

def detect_and_remove_uppercase_words(text):
  """Detects and removes all uppercase words in a string text if the word is in the phrase, not the beginning word of the phrase."""
  pattern = r'\b[A-Z]+\b'
  words = re.findall(pattern, text)
  for word in words:
    if word != text[0]:
      text = text.replace(word, '')
  return text


# word = "oller"
# print("Result: " + ("Exist word: " + word if check_exist_word(word) else "Not Exist word: " + word ))
# content = """Ceci est un article sur l'utilisation de Python pour le traitement du langage naturel.
#   Python est un langage puissant qui peut être utilisé pour une variété de tâches NLP,
#   telles que la classification de texte, l'analyse de sentiment et la traduction automatique.
#   Dans cet article, nous discuterons de la façon dont Python peut être utilisé pour implémenter ces tâches.
#   Nous fournirons également des exemples de code Python qui peuvent être utilisés pour NLP."""
# print(check_unexist_french_word(content))

def get_file_extension(filename):
  """Gets the file extension of a file."""
  last_dot_index = filename.rfind('.')
  if last_dot_index == -1:
    return None
  else:
    return filename[last_dot_index + 1:]

def get_content(file_path):
  extension = get_file_extension(file_path)

  if (extension == 'txt'):
    # Read file txt
    with open(file_path, mode='r') as f:
      content = f.read()
    return content
  
  if (extension == 'doc'):
    # Read file doc
    content = antiword.open(file_path).read()
    return content

  if (extension == 'docx'):
    # Read file docx
    content = docx2txt.process(file_path)
    return content

def get_proper_nouns(text):
    # Remove space between DOT character
    # Need to detect first word of the line
    textToDetect = text.replace(". ", ".")
    print("Nam textToDetect: ", textToDetect)
    names1 = re.findall(r"([A-Z][a-z]+\b)", textToDetect)
    names2 = re.findall(r"(\b[A-Z][a-z]+[A-Z][a-z]+\b)", textToDetect)
    names3 = re.findall(r"(\b[a-z]+[A-Z][a-z]+\b)", textToDetect)
    names4 = re.findall(r"(\b[A-Z]+\b)", textToDetect)

    names = names1 + names2 + names3 + names4
    # names = names1

    if names:
        print("The name is:", names)
    else:
        print("The name was not found.")

    for name in names:
        text = text.replace(name, "", 1)

    return text, names

def word_start_with_uppercase(word):
    match = re.search(r"[A-Z][A-Za-z]+", word)
    # print(match)
    if match and len(match.group()) == len(word): return True
    
    return False

def has_number(word):
  """
  Checks if a word has a number.

  Args:
    word: The word to check.

  Returns:
    True if the word has a number, False otherwise.
  """

  pattern = r"\d+"
  match = re.search(pattern, word)

  return match is not None

content = get_content("files\\test.docx")
content = remove_numbers(content)
# print(get_file_extension('test.txt'))
# print(content)
print(check_unexist_french_word(content))