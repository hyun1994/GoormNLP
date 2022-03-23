# 구름 AI 자연어처리 전문가 과정 

📌 소개
--
영어문장 데이터 긍부정 분류 프로젝트 구현


🗓 개발기간
--
2021년 10월 25일 ~ 2021년 11월 01일 (07일)


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
* Seaborn
* Anaconda
* Jupyter Notebook
* Google Colab pro



💡 프로젝트에서 맡은 역할
--
* Overfitting 발생하게 하는 코드 수정
* Optimizer를 Adafactor로 변경을 통해 성능개선
* Learning rate를 변경해서 성능개선
* lr_scheduler를 LambdaLR로 변경하여 성능개선


💡 자체 평가 및 보완 
--
* 성능이 가장 좋았던 모델이 Optimizer를 Adafactor로 변경했던 모델이 98.7%로 좋았음
* 각 모델의 긍/부정 예측 결과가 크게 차이나지 않아서 Hard Voting 앙상블을 적용해도 성능 개선
