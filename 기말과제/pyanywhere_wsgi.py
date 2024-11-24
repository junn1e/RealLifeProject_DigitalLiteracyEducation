import sys

# 프로젝트 디렉토리 경로 추가
sys.path.insert(0, '/home/ehdwns7f')

# 프로젝트 폴더 경로 설정
project_home = '/home/ehdwns7f/mysite'
if project_home not in sys.path:
    sys.path = [project_home] + sys.path

from weather_app import app as application
