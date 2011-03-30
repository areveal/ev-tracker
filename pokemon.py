

import pokedex


class EvSet(object):
    
    STATS = ['HP', 'Attack', 'Defense', 'Special Attack', 'Special Defense', 'Speed']
    
    MAX_STAT = 255
    MAX_EV = 510
    
    def __init__(self, evs={}):
        self.evs = {}
        for stat, ev in evs.items():
            if stat in EvSet.STATS and int(ev) > 0:
                self.evs[stat] = int(ev)
    
    def __add__(self, other):
        evs = dict(self.evs)  # clone
        for stat, ev in other.evs:
            evs[stat] = ev[stat] + ev
        return EvSet(evs)
    
    def __str__(self):
        ev_string = ['+%d %s' % (ev, stat) for stat, ev in self.evs.items()]
        return ', '.join(ev_string)
    
    def verbose(self):
        ev_string = ['%s: %d' % (stat, ev) for stat, ev in self.evs.items()]
        if not len(ev_string):
            return 'No EVs'
        return '\n'.join(ev_string)
    
    def to_dict(self):
        return self.evs


class Species(object):
    
    def __init__(self, id, name, evs=None):
        self.id = int(id)
        self.name = name
        self.evs = EvSet() if evs is None else evs
    
    def __str__(self):
        return '#%03d %-10s %s' % (self.id, self.name, self.evs)


class Pokemon(object):
    
    @classmethod
    def from_dict(cls, dict):
        dict['species'] = pokedex.fetch(id=dict['species'])
        dict['evs'] = EvSet.from_dict(dict['evs'])
        return cls(**dict)

    def __init__(self, species, name=None, item=None, pokerus=False, evs=None, id=None):
        self.id = id
        self.species = species
        self._name = name
        self.item = item
        self.pokerus = pokerus
        self.evs = EvSet() if evs is None else evs
    
    @property
    def name(self):
        return self.species.name if self._name is None else self._name
    
    def __str__(self):
        name = self.name
        if self._name is not None:
            name = '%s (%s)' % (name, self.species.name)
        if self.id is None:
            return name
        else:
            return '%d %s' % (self.id, name)

    def status(self):
        status = [str(self)]
        if self.pokerus:
            status.append('Pokerus')
        if self.item:
            status.append(self.item)
        status.append(self.evs.verbose())
        return '\n'.join(status)

    def listing(self, active):
        padding = '* ' if self is active else '  '
        return '%s%s' % (padding, self)

    def to_dict(self):
        return {'species': self.species.id, 'name': self._name,
                'pokerus': self.pokerus, 'item': self.item,
                'evs': self.evs.to_dict()}
