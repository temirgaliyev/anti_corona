


def convert(langs_dict, csv_file, delim=';'):
	with open(csv_file, mode='r', encoding='UTF-8') as file:
		langs = [lang.strip().upper() for lang in next(file).split(delim)[1:]]
		for lang in langs:
			langs_dict[f"LANG_{lang}"] = {}
		
		for line in file:
			splitted = line.split(delim)
			var = splitted[0].strip()
			for lang, lang_val in zip(langs, splitted[1:]):
				langs_dict[f"LANG_{lang}"][var] = lang_val.strip()

