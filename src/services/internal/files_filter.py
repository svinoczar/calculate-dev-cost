

import re
from data.github_api_response.commits_response_entity import SingleCommitEntity
from util.logger import logger


class FilesFilter:
    def __init__ (self):
        pass
    
    def filter(self, commit_objects: list[SingleCommitEntity]):
        c=1
        with open('.dcoignore', 'r', encoding='utf-8') as f:
            ignore_files = [line.strip() for line in f if line.strip() and not line.startswith('#')]
            logger.info(f'{ignore_files=}')

        for obj in commit_objects:
            logger.info(c)
            logger.info(f'{obj.commit.author.name=}')
            logger.info(f'BEFORE {[f.filename for f in obj.files]}')
            # obj.files = filter(not str.endswith(any(ignore_files)), obj.files)

            obj.files = [
                f for f in obj.files 
                if not re.sub(r'.*\/', '', f.filename).startswith('.')  # Игнорировать скрытые файлы
                and not any(re.sub(r'.*\/', '', f.filename).endswith(ext) for ext in ignore_files)  # Игнорировать по расширениям
            ]
                        
            logger.info(f'AFTER {[f.filename for f in obj.files]}')
            c+=1
            # file_path = file.filename
            
            # fname = re.sub(r'.*\/', '', file_path)
            # if fname.endswith(any())
            
    # def process_dcoignore():
        