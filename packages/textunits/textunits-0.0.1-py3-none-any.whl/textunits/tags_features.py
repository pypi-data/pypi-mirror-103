from textunits import TextUnits
import string

class TagFeaturesCreator:
  """
    TagFeaturesCreator is a Class Interface that generate dictionary-like features
    for TextUnits Object 

    To use TagFeaturesCreator: 
    1. Create an instance of `TagFeaturesCreator`: MyClass(TagFeaturesCreator)
    2. define super().__init__(*args, **kwargs) in that instance 
    3. Add methods that return a SINGLE value for a SINGLE TextUnits.units
      - name your method as 'unit_<feature_name>'
      - set your methods argument as (self, unit)
      - any variables should be defined within the method or the class instance

    4. After defining all the features methods, simply run .create_features()
    5. The results would be: {'feature_name': [feature_of_each_text_unit], ...}
  """

  def __init__(self, text_units: TextUnits):
    assert isinstance(text_units, TextUnits), "text_unit needs to be a TextUnits"
    # This function provide BS-bool to define end nodes with text
    self.text_units = text_units
    self.units = text_units.units

  @property
  def get_units(self):
    # this return the extracted text units
    return self.units

  def unit_get_text(self, unit):
    """Retrieve beautify text from a TextUnit"""
    text = ' '.join(unit.text.split())

    # remove punctuation
    return text.translate(text.maketrans('', '', string.punctuation))

  def __feature_methods__(self):

    methods_list = []
    for defined in dir(self):
      if defined.startswith('unit_'):
        methods_list.append(defined)
    return methods_list

  def create_features(self):
    """This method returns features of the units"""

    # extract all the text-units methods 
    feature_methods = self.__feature_methods__()
    units = self.get_units
    # features collection is a dictionary {'feature_name': [unit results]}
    features = {}

    for method in feature_methods:
      # print(method)
      # generate feature names and map the feature into a dict res
      feature_name = method.split('unit_')[-1]
      inclass_method_callback = lambda unit: getattr(self, method)(unit)
      res = list(map(inclass_method_callback, units))

      # input the results into the dictionary
      features[feature_name] = res

    return features  