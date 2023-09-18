import json
import os

def print_with_indent(value, indent=0):
    indention = '\t' * indent
    print(indention + str(value))


class Entry:
    def __init__(self, title, entries=None, parent=None):
        if entries is None:
            self.entries = []
        self.title = title
        self.parent = parent

    def __str__(self):
        return self.title

    def add_entry(self, entry):
        self.entries.append(entry)
        entry.parent = self

    def print_entries(self, indent=0):
        print_with_indent(self, indent)
        for entry in self.entries:
            entry.print_entries(indent + 1)


    def to_dict_for_json(self):
        result = {
            'title': self.title,
            'entries': [x.to_dict_for_json() for x in self.entries]
        }
        # for entry in self.entries:
        #     if entry.entries:
        #         result['entries'].append(entry.to_dict_for_json())
        #     else:
        #         result['entries'].append(entry)
        return result

    @classmethod
    def from_json(cls, value: dict):
        new_entry = Entry(value['title'])
        for entry in value.get('entries', []):
            new_entry.add_entry(cls.from_json(entry))
        return new_entry

    def save(self, path):
        with open(os.path.join(path, f'{self.title}.json'), 'w', encoding='utf-8') as f:
            json.dump(self.to_dict_for_json(), f)

    @classmethod
    def load(cls, filename):
        with open(filename, 'r', encoding='utf-8') as f:
            return cls.from_json(json.load(f))


class EntryManager:
    def __init__(self, data_path):
        self.entries = []
        self.data_path = data_path

    def save(self):
        for entry in self.entries:
            entry.save(self.data_path)

    def load(self):
        for file in os.listdir(self.data_path):
            if file.endswith('.json'):
                entry = Entry.load(os.path.join(self.data_path, file))
                self.entries.append(entry)

    def add_entry(self, title: str):
        self.entries.append(Entry(title))





