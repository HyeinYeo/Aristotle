# 아리스토텔레스 수사학적 텍스트 분석기

이 프로그램은 텍스트 내 아리스토텔레스 수사학적 요소(파토스, 에토스, 로고스)를 분석하여 설득 전략 분석에 활용할 수 있는 도구입니다.

## 개요

이 분석기는 아리스토텔레스의 수사학 3요소를 기반으로 텍스트를 분석합니다:

- **파토스(Pathos)**: 감정에 호소하는 요소
- **에토스(Ethos)**: 화자의 신뢰성에 호소하는 요소
- **로고스(Logos)**: 논리와 이성에 호소하는 요소

텍스트 내에서 각 수사학적 요소와 관련된 단어와 특징(느낌표, 인용부호, 숫자 등)을 추출하여 정량적으로 분석합니다.

## 기능

- TSV 형식의 텍스트 데이터 로드
- KoNLPy의 Okt 형태소 분석기를 사용한 한국어 텍스트 분석
- 수사학적 요소별 단어사전 기반 분석
- 텍스트 길이 대비 정규화된 수사학적 점수 계산
- 분석 결과의 다양한 시각화
  - 전체 평균 수사학적 요소 점수
  - 라벨별 평균 수사학적 요소 점수
  - 라벨 내 개별 텍스트의 수사학적 요소 비교

## 설치 요구사항

```
pip install pandas matplotlib numpy konlpy
```

macOS의 경우 한글 폰트 설정을 위해 AppleGothic 폰트가 사용됩니다.

## 파일 구조

- `main.py`: 주 실행 파일
- `texts.tsv`: 분석할 텍스트 데이터 (탭으로 구분된 파일)
- `pathos.txt`: 파토스 관련 단어사전
- `ethos.txt`: 에토스 관련 단어사전
- `logos.txt`: 로고스 관련 단어사전

## 데이터 형식

### texts.tsv
텍스트 데이터는 다음과 같은 형식의 TSV 파일이어야 합니다:
```
title  content  label
제목1	텍스트 내용1	라벨1
제목2	텍스트 내용2	라벨2
...
```

## 사용 방법

1. `texts.tsv` 파일을 프로젝트 폴더에 위치시킵니다.
2. 각 수사학적 요소에 해당하는 단어사전 파일에 필요 단어를 추가합니다. (optional)
3. 다음 명령어로 프로그램을 실행합니다:

```
python main.py
```

## 분석 결과

프로그램은 다음과 같은 결과를 제공합니다:

1. 콘솔에 각 텍스트별 수사학적 요소 점수 출력
  
2. 시각화된 그래프:
   - 전체 텍스트의 평균 수사학적 요소 점수
   - 레이블별 평균 수사학적 요소 점수
   - 각 레이블 내 텍스트별 수사학적 요소 비교


## 주요 함수 설명

- `setup_fonts()`: 한글 폰트 설정
- `load_data()`: TSV 형식의 텍스트 데이터 로드
- `create_dictionary()`: 수사학적 요소별 단어사전 로드
- `analyze_words()`: 텍스트에서 단어사전에 포함된 단어 추출
- `analyze_pathos()`, `analyze_ethos()`, `analyze_logos()`: 각 수사학적 요소 분석
- `analyze_texts()`: 전체 텍스트 분석 수행
- `visualize_results()`: 분석 결과 시각화

## 분석 방법론

1. **파토스 분석**:
   - 파토스 단어사전 기반 단어 추출
     - 파토스 단어사전: [KNU 한국어 감성사전](https://raw.githubusercontent.com/park1200656/KnuSentiLex/master/SentiWord_Dict.txt)에서 추출
   - 느낌표(!), 물음표(?) 개수 계산

2. **에토스 분석**:
   - 에토스 단어사전 기반 단어 추출
   - 인용부호(") 개수 계산

3. **로고스 분석**:
   - 로고스 단어사전 기반 단어 추출
   - 숫자와 퍼센트(%) 기호 개수 계산

4. **정규화**:
   - 모든 점수는 텍스트 1000자당 출현 빈도로 정규화됨

## 주의사항

- KoNLPy 설치를 위해 Java 8 이상이 필요합니다.
- macOS에서 한글 폰트가 제대로 표시되지 않을 경우, 대체 폰트(DejaVu Sans)를 사용합니다.

## 확장 가능성

- 단어사전 확장 및 개선
- 복합어 탐지 문제 해결
- 기계학습 모델과 연동하여 분석 성능 향상
- 웹 인터페이스 구현

---
## AI 생성 허위정보 텍스트에 대한 분석 결과
1. 콘솔에 각 텍스트별 수사학적 요소 점수 출력
   ![image](https://github.com/user-attachments/assets/e9398960-ca9a-4dbc-8672-2c4cb5be63a5)
  
2. 시각화된 그래프:
   - 전체 텍스트의 평균 수사학적 요소 점수
     ![image](https://github.com/user-attachments/assets/6c0f0d0f-4377-4087-a97b-ee23161459a2)

   - 레이블별 평균 수사학적 요소 점수
     ![image](https://github.com/user-attachments/assets/0c0069a9-0327-4f0c-86d3-de66dddbfd7c)

   - 각 레이블 내 텍스트별 수사학적 요소 비교
      ![image](https://github.com/user-attachments/assets/31f4ba8a-1cda-4cc9-b844-f95fb9543960)
     ![image](https://github.com/user-attachments/assets/26d81ee4-6a60-4d0c-95c9-8fc3536fc632)
     ![image](https://github.com/user-attachments/assets/855cc76a-fa96-4987-b67e-a58a38b09af1)
     ![image](https://github.com/user-attachments/assets/b7ada448-fd62-49d4-811d-e611f6848127)
     ![image](https://github.com/user-attachments/assets/bfc23d91-ce7b-4ca7-b711-a57bf12baf2b)

