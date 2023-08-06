import json
import spacy
import pickle
nlp = spacy.load("en_core_web_md")
emoji_dict_path = "joji/data/emojis.json"
emoji_write_path = "joji/data/emoji_dict.p"
emoji_dict = open(emoji_dict_path)
emoji_dict_list = json.load(emoji_dict)["emojis"]

emoji_dict = {}

for data in emoji_dict_list:
    emoji_dict[data["name"]] = {
        "vector" : nlp(data["name"]),
        "emoji": data["emoji"],
        "unicode": data["unicode"]
    } 

file_ = open(emoji_write_path, "wb")
pickle.dump(emoji_dict, file_)
