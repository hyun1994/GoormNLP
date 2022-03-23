# Neural Machine Translation

📌 소개
--
주어진 Train, Dev, Test1, Test2의 영어를 한국어로 번역하는 프로젝트 구현


🗓 개발기간
--
2021년 11월 17일 ~ 2021년 12월 01일 (15일)


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
* Pandas, Matplotlib, Nltk, Konlpy를 활용해서 주어진 데이터를 EDA를 통해 형태소별 빈도 수와 2gram 어절 분석 그리고 문장길이 분석을 하면서 Test2 데이터가 다른 데이터들에 비해 문장길이가 긴 문장들로 이루어진 데이터라는 것을 분석
* Batch size, Learning rate 등 Hyperparameter 변경을 통해 성능 개선
* 모델을 구성하는 Target Tokenizer의 Transformers인 monologg/koelectra-base-discriminator을 v3으로 변경
* MRC 프로젝트에서 멘토가 추천해준 대규모 데이터 학습후 주어진 데이터를 학습하는 방법을 적용하기 위해 Aihub 데이터에서 긴 문장위주로 가져와서 학습 후 주어진 데이터 학습을 통해 Harmonic Mean 14.52에서 19.88으로 성능 개선

💡 자체 평가 및 보완 
--
* MRC 프로젝트 멘토가 추천해준 방법이 성능이 가장 크게 발전했지만 프로젝트에서 제한하는 데이터라서 제출 제한
* Target Tokenizer의 Transformers를 DistilBertModel의 계열 Tokenizer로 학습해서 Tokenizer구성이 달라서 성능이 하락
