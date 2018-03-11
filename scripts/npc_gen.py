from godot import exposed, export
from godot.bindings import *
from godot.array import Array
from godot.dictionary import Dictionary
import names
from random import randint
import bisect
import json
import os, sys

class CreateNpc:
  """
  This is a class which creates a new NPC, with a name, stats, and a backstory.
  """
  def __init__(self, gender, profession='peasent'):
    """
    When an object is created from this class, the object is filled with the character's name, their profession, their gender, their stats, their personality, and a couple of lines of backstory.  This can be accessed through the "full_stats" attribute.
    Note that the 'stats' array value is laid out like this: strength, intelligence, constitution, and luck.
      Args:
        gender (str): the gender of the NPC. Mandatory.
        profession (str): the profession/class of the NPC. Defaults to 'peasent'.
      Returns:
        CreateNpc object
      Usage:
        >>> npc = CreateNpc('male', 'farmer')
        >>> foo.getStats()
        {'profession': 'peasent', 'stats': [6, 9, 7, 6], 'name': u'Michelle Bradley', 'personality': 'average_person'}
    """
    # Ensure that the caller passes a gender
    if not gender in ('male','female'):
         raise ValueError("Only the values 'male' and 'female' may be passed.")
         return 1
    # Ensure that the caller passed a proper profession.
    if not profession in ('peasent','farmer','shopkeeper','knight','warrior','aristocrat'):
        raise ValueError("Please pass a proper profession.")
        return 2
    self.profession = profession
    self.gender = gender
    self.character = dict()
    # This contains the four stats (Strength, Intelligence, Constitution, and Luck) for the NPC.
    self.character['stats'] = self.__assignStats(self.profession)
    # This gives a name which is full unicode, e.g. u'John Smith'.
    self.character['name'] = names.get_full_name(gender=self.gender)
    # Assign the NPC's gender
    self.character['gender'] = self.gender
    # Assign the NPC's profession, i.e. their job.
    self.character['profession'] = self.profession
    # Set the NPC's personality.
    self.character['personality'] = self.__assignPersonality(self.character['stats'])

  def getStats(self):
    """
    Return the stats for the NPC. The returned dictionary is laid out like this:
    'name' = Full name of NPC
    'profession' = What the character does, or their social class
    'backstory' = A brief backstory of the NPC
    'stats' = The NPC's stats, as represented by an array. They are listed as follows:
        * Strength
        * Intelligence
        * Constitution
        * Luck
    'personality' = The personality of the NPC
    
    Returns:
        character (dict)
    
    Usage:
        >>> npc.getStats()
        {'profession': 'peasent', 'stats': [10, 8, 6, 4], 'name': u'Jay Murphy', 'personality': 'xenophobe'}
    """
    return Dictionary(self.character)

  def __assignStats(self, profession):
    """
    Stats in the list are as follows: Strength, Intelligence, Constitution, and Luck.
    Args:
      profession (str): the profession/class of the NPC
    Returns:
      List: four integers based on the profession/class of the NPC.
    """
    # This needs to have way more content for the different classes/professions that will be in the game. In fact, it may be better to have this detailed in a different file.
    stats = []
    if profession == "peasent":
            stats = [randint(6, 10), randint(6, 10), randint(6, 10), randint(4,8)]
    elif profession == "farmer":
            stats = [randint(8,12), randint(7,10), randint(8,12), randint(5,9)]
    elif profession == "shopkeeper":
            stats = [randint(7,11), randint(9, 12), randint(7,11), randint(7,11)]
    # Need to put this class in.
    elif profession == "knight":
            stats = [randint(10, 13) for i in range(4)]
    elif profession == "warrior":
        stats = [randint(9, 15) for i in range(4)]
    elif profession == "aristocrat":
        stats = [randint(8,11), randint(9, 15), randint(8,12), randint(8,15)]
    # This has to be wrapped in an Array() because Godot can't handle this sort of data type.
    return Array(stats)

  # TODO: This is assigning some weird values, even if they are weighted. May have to go with something that is a bit more arbitrary,
  # i.e. give ranges of values of stats and assign personalities based upon those values. So I may have someone who has a high
  # charisma, as well as high intelligence, and they may be assigned the personality of "over achiever".
  def __assignPersonality(self, stats):
    """
    A personality is assigned to the NPC based upon their stats.
    Args:
       stats (list): the list of the NPC's stats
    Returns:
       personality (str): the NPC's personality
    """
    # Was a list of stats actually passed?
    if not isinstance(stats, Array):
         raise ValueError   ("Please pass a list of stats.")
    list_of_personalitites = ['average_person','buffoon','brainiac','fancy_pants','good_guy','klutz','over_achiever','health_nut','sychophant','tree_hugger','xenophobe']
    # Pick out the individual stats
    strength = stats[0]
    intelligence = stats[1]
    constitution = stats[2]
    luck = stats[3]
    # All of the personalities with default assignments. These numbers are arbitray; no
    # research was made for these values.
    p = {
        'average_person' : 5,
        'buffoon' : 1,
        'brainiac': 1,
        'fancy_pants' : 1,
        'good_guy' : 1,
        'klutz': 1,
        'over_achiever' : 1,
        'health_nut' : 1,
        'sychophant' : 1,
        'tree_hugger' : 1,
        'xenophobe' : 1
       }
    # Under certain conditions, add a point for a specific personality.
    if 8 <= strength <= 10 and 9 <= intelligence <= 11 : p['over_achiever'] += 1
    if 9 <= strength <= 11 and 8 <= luck <= 10 and 9 <= intelligence <= 11 : p['good_guy'] += 1
    if 7 <= constitution <= 10 and  8 <= intelligence <= 10 : p['klutz'] += 1
    if 10 <= intelligence <= 12 and 8 <= constitution <= 10 : p['brainiac'] += 1
    if 9 <= luck <= 11 and 8 <= constitution <= 12 : p['tree_hugger'] += 1
    if 7 <= strength <= 9 and 7 <= constitution <= 10 : p['sychophant'] += 1
    if 8 <= intelligence <= 11 and  8 <= constitution <= 10: p['xenophobe'] += 1
    # This code was based upon the "Pre-calculated" sorting code found here:
    # https://www.electricmonk.nl/log/2009/12/23/weighted-random-distribution/
    total = 0
    weights = []
    for w in p.items():
        total += w[1]
        weights.append( (total,w[0]) )
    random_number = randint(0, total - 1)
    personality = weights[bisect.bisect(weights, ( random_number, str(None) ) ) ]
    return personality[1]

@exposed
class GenerateNpc(Node2D):
    def create_npc(self, gender, job='peasent'):
        npc = CreateNpc(gender, job).getStats()
        return npc
