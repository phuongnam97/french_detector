import re
import unicodedata

# importing sys
import sys
# adding Folder_2/subfolder to the system path
sys.path.insert(0, 'controller')
from dictionnary import check_exist_word 

def check_unexist_french_word(paragraph):
    words = convert_french_paper_content_to_list_of_words(paragraph)
    print(words)
    not_existed_words = []
    for word in words:
        if word == '': continue
        existed = check_exist_word(word)
        if not existed:
            not_existed_words.append(word)
    return not_existed_words


def convert_french_paper_content_to_list_of_words(paper_content):
  """Converts a French paper content to a list of words.

  Args:
    paper_content: The paper content as a string.

  Returns:
    The paper content as a list of words.
  """

  # Remove all punctuation from the paper content.
  newStr = paper_content.replace("l'", "").replace("\n", " ")
  paper_content = re.sub(r"[^\w\s]", "", newStr)

  # Convert the paper content to lowercase.
  paper_content = paper_content.lower()

  # Remove accents from the paper content.
  paper_content = unicodedata.normalize("NFD", paper_content)
  paper_content = "".join([c for c in paper_content if not unicodedata.combining(c)])
  paper_content = unicodedata.normalize("NFC", paper_content)

  # Split the paper content into words.
  words = paper_content.split(" ")

  # Return the list of words.
  return words

# word = "oller"
# print("Result: " + ("Exist word: " + word if check_exist_word(word) else "Not Exist word: " + word ))
content = """Ceci est un article sur l'utilisation de Python pour le traitement du langage naturel.
  Python est un langage puissant qui peut être utilisé pour une variété de tâches NLP,
  telles que la classification de texte, l'analyse de sentiment et la traduction automatique.
  Dans cet article, nous discuterons de la façon dont Python peut être utilisé pour implémenter ces tâches.
  Nous fournirons également des exemples de code Python qui peuvent être utilisés pour NLP."""
print(check_unexist_french_word(content))
