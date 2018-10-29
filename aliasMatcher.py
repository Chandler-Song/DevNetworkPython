authors = set(list(commit.author.email for commit in repo.iter_commits()))
possibleAliases = dict()
authorUsedAsKey = []

lcs = MetricLCS()
expr = r'^([a-zA-Z0-9_.+-]+)'

for authorA in authors:
	
	skipFullMatch = False
	for authorB in possibleAliases.keys():
		
		localPartAMatches = re.findall(expr, authorA)
		localPartBMatches = re.findall(expr, authorB)
		
		distance = lcs.distance(localPartAMatches[0], localPartBMatches[0])
		
		if (distance < 0.5):
			skipFullMatch = True
			if (authorA not in possibleAliases[authorB]):
				possibleAliases[authorB].append(authorA)
	
	if (skipFullMatch):
		continue
	
	for authorB in authors:
		
		localPartAMatches = re.findall(expr, authorA)
		localPartBMatches = re.findall(expr, authorB)
		
		distance = lcs.distance(localPartAMatches[0], localPartBMatches[0])
		
		if (authorA != authorB and distance < 0.5):
			if (authorA in authorUsedAsKey):
				authorAliases = possibleAliases[authorA]
				
				if authorB not in authorAliases:
					authorAliases.append(authorB)
				
			elif (authorB in authorUsedAsKey):
				authorAliases = possibleAliases[authorB]
				
				if authorA not in authorAliases:
					authorAliases.append(authorA)
				
			else:
				authorAliases = possibleAliases.setdefault(authorA, [])
				authorAliases.append(authorB)
				authorUsedAsKey.append(authorA)