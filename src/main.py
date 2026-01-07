from data.github_api_response.commits_response_entity import SingleCommitEntity
from services.external.github_stats_manual import *
from services.internal.files_filter import FilesFilter
from util.mapper import JSONToGitCommitAuthorEntityList, JSONToSingleCommitEntity
from util.logger import logger
from services.internal.lang_detector import LanguageDetectorModel, BasicLanguageDetector

import json
import os
import re


detector = LanguageDetectorModel()
basic_detector = BasicLanguageDetector()

def process_repo(owner, repo):
    commits = get_commits_list(owner=owner, repo=repo)
    logger.info(f"Successfully retrieved {len(commits)} commits for {owner}/{repo}")
    
    contributors = get_contributors(owner=owner, repo=repo)
    dto_contributors = JSONToGitCommitAuthorEntityList(contributors)

    commits_dir = "user_commits"
    if not os.path.exists(commits_dir):
        os.makedirs(commits_dir)

    # Для каждого contributor'а собираем его коммиты
    for contributor in dto_contributors:
        contributor_login = contributor.login
        logger.info(f"Processing commits for: {contributor_login}")
        
        user_commits = []
        
        for commit in commits:
            if (commit.get('author') and 
                commit['author'].get('login') and 
                commit['author']['login'] == contributor_login):

                sha = commit['sha']
                try:
                    full_commit = get_commit(owner=owner, repo=repo, ref=sha)
                    # commit_dto = JSONToSingleCommitEntity(full_commit)
                    user_commits.append(full_commit)
                except Exception as e:
                    print(f"Error getting commit {sha}: {e}")
        
        if user_commits:
            filename = f"{commits_dir}/{contributor_login}_commits.json"
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(user_commits, f, ensure_ascii=False, indent=4)
            logger.info(f"Saved {len(user_commits)} commits to {filename}")
        else:
            logger.warn(f"No commits found for {contributor_login}")

    with open('contributors.json', 'w', encoding='utf-8') as f:
        json.dump(contributors, f, ensure_ascii=False, indent=4)
        
    with open('all_commits_meta.json', 'w', encoding='utf-8') as f:
        json.dump(commits, f, ensure_ascii=False, indent=4)

def preprocess_commits(filename: str):
    logger.info('Processing commits . . .')
    
    files_filter = FilesFilter()
    commit_objects: list[SingleCommitEntity] = []
    
    with open(filename, 'r', encoding='utf-8') as f:
        user_commits = json.load(f)
    
    for commit in user_commits:
        commit_objects.append(JSONToSingleCommitEntity(commit))
        
    print(len(commit_objects))
        
    files_filter.filter(commit_objects)
    
    return

    with open('TEST_COMMIT_DIFF.diff', 'w', encoding='utf-8') as out:
        c = f_idx = 1

        """ 
    
        [ filter cms ] -> 
            -> for cm in cms ->
                -> fs from cm ->
                    -> for f in fs -> 
                        -> [ lang detection ] -> [ objects generation ]

        
        """


        for commit in commit_objects:
            files = commit.files

            for file in files:
                file_path = file.filename
                fname = re.sub(r'.*\/', '', file_path)

                patch = file.patch
                if not patch:
                    continue

                # убираем @@ ... @@
                patch = re.sub(r'^@@.*?@@\n?', '', patch, flags=re.MULTILINE)
                if not patch.strip():
                    continue

                # 1. базовый анализ
                basic_lang, basic_conf = basic_detector.detect(fname, patch)

                # 2. ML-анализ
                ml_lang, ml_conf = detector.detect(patch)

                # 3. финальное решение
                if basic_conf >= 0.75:
                    lang, conf, classifier = basic_lang, basic_conf, 'manual classifier'
                elif ml_conf > basic_conf and ml_lang != 'Unknown':
                    lang, conf, classifier = ml_lang, ml_conf, 'ml classifier'
                else:
                    lang, conf = basic_lang, basic_conf
            
                if lang == 'Unknown':
                    logger.warning(f'{fname} | {lang} | {conf} | {classifier}')

                out.write(f'commit {c}, file {f_idx}\n')
                out.write(f'filename: {fname}\n')
                out.write(f'language: {lang}, accuracy: {conf:.3f}, classifier: {classifier}\n')
                out.write('=' * 25)
                out.write(f'\n{patch}\n')
                out.write('=' * 25)
                out.write('\n\n\n')

                f_idx += 1
            c += 1

    print("Done processing. . .")



if __name__ == '__main__':
    # process_repo('Nerds-International', 'nerd-code-frontend')

    preprocess_commits("user_commits/Demid0_commits.json")
