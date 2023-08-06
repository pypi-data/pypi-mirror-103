from bs4 import BeautifulSoup, NavigableString
import statistics


class TextUnits:
  """
  TextUnits aims to find the EndNods with text using BeautifulSoup. TextUnits 
  class provides some basic functionalities: 
    1. easier retrieval of the end nodes results 
    2. basic numerical and statistics operation on the end nodes text

  Methods are grouped as follow: 
   1. tag_<method_name>: Methods that operate on the tags of TextUnits.units
   2. text_<method_name>: Methods that operate the text of TextUnits.units

  The default end_node_func returns only <p>, <div>, <li> text end nodes. 
  You could define a more sophiscated one in order find the end nodes 
  
  self.units -> [BS-end-nodes, ....]
  """
  def __init__(self, soup, end_node_func):
    self.units = soup(end_node_func)
    self.end_node_func = end_node_func 

  def tag_filter(self, tagname: str) -> list:
    if tagname == 'all':
      return self.units
    filtered = filter(lambda unit: unit.name == tagname, self.units)
    return list(filtered)
    
  def tag_count(self, tagname: str) -> int:
    filtered = self.tag_filter(tagname)
    return len(list(filtered))

  def text_counts(self, tagname: str) -> list:
    filtered = self.tag_filter(tagname)
    return [len(unit.text.split()) for unit in filtered]

  def text_total(self, tagname: str) -> list:
    return sum(self.text_counts(tagname))
  
  def text_stats(self, stats, tagname: str) -> float:
    return getattr(statistics, stats)(self.text_counts(tagname))



### below provide a default end-node locate function
def convert_regex_check_words(list_words):
  words = '|'.join(list_words)
  return '(' + words + ')'

def child_contains_navstr(children_tags):
  func = lambda child: isinstance(child.string, NavigableString)
  return map(func, children_tags)

def end_node_with_text(tag, 
                       incl_embed_navstr=True, 
                       end_nodes=['div', 'li', 'p']
                       ):
  
  # check of the endnode is of type
  if tag.name not in end_nodes:
    return False

  # check if the children nodes have deeper tag or 
  # when not being at <div>
  # just NavigableString, <em><b><strong> etc....
  nav_str_res = list(child_contains_navstr(tag.findChildren()))
  if (tag.name != 'div' and
      all(nav_str_res) and 
      nav_str_res):
    return True if incl_embed_navstr else False

  # check if there it is a empty text node
  if not ' '.join(tag.text.split()):
    return False

  # check if there are some other tag wrapping around 
  if len(tag(text=False)) > 0:
    return False
  
  # final node
  return True