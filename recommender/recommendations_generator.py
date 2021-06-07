import pandas as pd
import numpy as np

def get_recommendations_list(neo_db, id_list):
	recomendations = pd.DataFrame(columns=['MovieId', 'Score',])
	for i in range(len(id_list)):
		recomendations = recomendations.append({'MovieId': id_list[i], 'Score': len(id_list)-i}, ignore_index = True)
		rec = neo_db.get_recomendations(id_list[i])
		j = 0
		for recommendation in rec:
			if recommendation['idMovies']['id'] not in id_list:
				if j > 0:
					recomendations = recomendations.append({'MovieId': recommendation['idMovies']['id'], 'Score': 0}, ignore_index = True)
				else:
					recomendations = recomendations.append({'MovieId': recommendation['idMovies']['id'], 'Score': len(id_list)-i+0.5}, ignore_index = True)
			j += 1
	recomendations = recomendations.sort_values(by='Score')
	recomendations.drop_duplicates(inplace = True)
	return recomendations

def filtered_recommendations(neo_db, prev_list, banned_list):
	recoms_df = get_recommendations_list(neo_db, prev_list)
	recoms_df = recoms_df[np.isin(recoms_df['MovieId'], banned_list, invert=True)]
	recom_ids = map(lambda x: str(int(x)), list(recoms_df['MovieId']))
	return list(recom_ids)