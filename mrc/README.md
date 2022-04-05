# 구름 AI 자연어처리 전문가 과정

📌 소개
--
주어진 Train, Test의 한국어로 이뤄진 내용 요약하는 프로젝트 구현


🗓 개발기간
--
2021년 11월 02일 ~ 2021년 11월 14일 (12일)


🧙 멤버구성
--
:octocat: 최혁인

:octocat: 이한빈

:octocat: 채지현

:octocat: 김윤나


🛠 프로젝트 사용기술
--
* Python3
* PyTorch
* Pandas
* Numpy
* Transformers
* Scrapy
* Matplotlib
* Nltk
* Konlpy
* Seaborn
* Anaconda
* Jupyter Notebook
* Google Colab pro



💡 프로젝트에서 맡은 역할
--
* Baseline code는 Overfitting이 발생하도록 제작된 코드라서 Overfitting 방지하기 위해서 AiHub 데이터 추가함
* 주어진 Baseline이 Bert For Question Answering 모델을 간략하게 만든 모델에 구글에  모델을 참고하고 attention is all need 논문을 통해 보완으로 Score를 131에서 15까지 성능 개선
* Batch size, Learning rate, 등 Hyperparameter 변경을 통해 15에서 5.63까지 성능 개선

💡 자체 평가 및 보완 
--
* 프로젝트의 질문의 내용은 정답 근처에 분포한다고 생각하고 정답의 위치 기준으로 문장 단위로 데이터 전처리하는 방식으로 접근했던 부분을 조금 더 활용하지 못한 점이 아쉬움
* 멘토가 추천했던 AiHub에서 대용량 데이터로 한번 학습 후 원래 데이터를 학습하면 조금 더 성능이 개선할 가능성이 있다는 피드백을 적용하지 못한 점이 아쉬움
