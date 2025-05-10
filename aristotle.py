import pandas as pd
from konlpy.tag import Okt
import re
import matplotlib.pyplot as plt
import numpy as np

# 한글 폰트 설정(MacOS)
def setup_fonts():
    plt.rcParams['axes.unicode_minus'] = False  # 마이너스 기호 깨짐 방지
    plt.rc('font', family='AppleGothic')  # macOS 기본 한글 폰트

    # 폰트 설정이 안 될 경우 대체 방법
    try:
        plt.figure()
        plt.text(0.5, 0.5, '테스트')
        plt.close()
    except:
        # 폰트 설정이 안 되면 영어로 출력
        print("한글 폰트 설정 실패, 영어로 대체합니다.")
        plt.rc('font', family='DejaVu Sans')

# 생성형 AI 허위정보 텍스트 불러오기
def load_data(file_path='texts.tsv'):
    column = ['title', 'content', 'label']
    df = pd.read_csv(file_path, sep='\t', encoding='utf-8', names=column, header=None)
    df.rename(columns={'content': 'document_content'}, inplace=True)
    return df

# 단어사전
def create_dictionary():
    # 파토스
    pathos_dict = get_dictionary('pathos')

    # 에토스
    ethos_dict = get_dictionary('ethos')

    # 로고스
    logos_dict = get_dictionary('logos')

    return pathos_dict, ethos_dict, logos_dict

# 단어사전 불러오기
def get_dictionary(mode):
    column_names = ['word']
    
    fileName = f'{mode}.txt'
    words = pd.read_csv(fileName, sep='\t', encoding='utf-8', names=column_names, header=None)
    words_list = [word.strip() for word in words['word']]  # 양쪽 공백 제거

    return words_list

# 단어 분석 함수
def analyze_words(text, okt, dict):
    morphs = [word for word, _ in okt.pos(text, stem=True)]
    phrases = okt.phrases(text)

    mode_words = list()
    mode_phrases = list()

    # 형태소 형태 분석
    for word in morphs:
        if word in dict:
            mode_words.append(word)
    
    # 구문 형태 분석
    for phrase in phrases:
        if (phrase in dict) and phrase not in mode_words:
            mode_phrases.append(phrase)

    return mode_words, mode_phrases

# 파토스 분석 함수
def analyze_pathos(text, okt, dict):
    pathos_words, pathos_phrases = analyze_words(text, okt, dict)
    
    count = len(pathos_words + pathos_phrases)
    exclamation_count = text.count('!')
    question_count = text.count('?')
    
    return {
        'pathos_words': count,
        'exclamation': exclamation_count,
        'question': question_count,
        'total_pathos': count + exclamation_count + question_count,
    }

# 에토스 분석 함수
def analyze_ethos(text, okt, dict):
    ethos_words, ethos_phrases = analyze_words(text, okt, dict)
    
    count = len(ethos_words + ethos_phrases)
    quotation_count = text.count('"') / 2  # 쌍따옴표 개수
    
    return {
        'ethos_words': count,
        'quotation': quotation_count,
        'total_ethos': count + quotation_count,
    }

# 로고스 분석 함수
def analyze_logos(text, okt, dict):
    logos_words, logos_phrases = analyze_words(text, okt, dict)
    
    count = len(logos_words + logos_phrases)
    number_count = len(re.findall(r'\d+', text))  # 숫자 개수
    percent_count = text.count('%')  # 퍼센트 기호 개수
    
    return {
        'logos_words': count,
        'number': number_count,
        'percent': percent_count,
        'total_logos': count + number_count + percent_count,
    }

# 메인 분석 함수
def analyze_texts(df):
    # Konlpy Okt 형태소 분석기
    okt = Okt()

    # 단어사전 로드
    pathos_dict, ethos_dict, logos_dict = create_dictionary()

    results = []
    for idx, row in df.iterrows():
        text = row['document_content']
        title = row['title']
        label = row['label']
        
        # 텍스트 길이
        text_length = len(text)
        
        # 각 수사학적 요소 분석
        pathos_results = analyze_pathos(text, okt, pathos_dict)
        ethos_results = analyze_ethos(text, okt, ethos_dict)
        logos_results = analyze_logos(text, okt, logos_dict)
        
        # 정규화된 점수 계산 (텍스트 길이 1000자당)
        pathos_score = pathos_results['total_pathos'] / text_length * 1000
        ethos_score = ethos_results['total_ethos'] / text_length * 1000
        logos_score = logos_results['total_logos'] / text_length * 1000
        
        # 결과 통합
        result = {
            'title': title,
            'label': label,
            'text_length': text_length,
            'pathos_score': pathos_score,
            'ethos_score': ethos_score,
            'logos_score': logos_score,
            **pathos_results,
            **ethos_results,
            **logos_results
        }
        
        results.append(result)
    
    # 결과를 데이터프레임으로 변환
    results_df = pd.DataFrame(results)
    
    return results_df

# 결과 시각화 함수
def visualize_results(results_df):
    # 전체 평균 점수
    plt.figure(figsize=(10, 6))
    avg_scores = results_df[['pathos_score', 'ethos_score', 'logos_score']].mean()
    
    bars = plt.bar(['파토스', '에토스', '로고스'], 
                  avg_scores, 
                  color=['#FF9999', '#66B2FF', '#99CC99'])
    
    # 값 표시
    for bar in bars:
        height = bar.get_height()
        plt.text(
            bar.get_x() + bar.get_width()/2.,
            height + 0.5,
            f'{height:.2f}',
            ha='center', va='bottom'
        )
    
    plt.title('텍스트의 평균 수사학적 요소 점수')
    plt.ylabel('점수 (텍스트 1000자당)')
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    plt.show()
    
    # label별 평균 수사학적 요소 점수
    plt.figure(figsize=(12, 6))
    
    # label별 평균 계산
    label_avg = results_df.groupby('label')[['pathos_score', 'ethos_score', 'logos_score']].mean()
    
    # label 종류 확인
    labels = label_avg.index.tolist()
    
    # 그래프 위치 설정
    x = np.arange(len(labels))
    width = 0.25
    
    # 막대 그래프 생성
    bars1 = plt.bar(x - width, label_avg['pathos_score'], width, label='파토스', color='#FF9999')
    bars2 = plt.bar(x, label_avg['ethos_score'], width, label='에토스', color='#66B2FF')
    bars3 = plt.bar(x + width, label_avg['logos_score'], width, label='로고스', color='#99CC99')
    
    # 값 표시
    def add_labels(bars):
        for bar in bars:
            height = bar.get_height()
            plt.text(
                bar.get_x() + bar.get_width()/2.,
                height + 0.5,
                f'{height:.2f}',
                ha='center', va='bottom'
            )
    
    add_labels(bars1)
    add_labels(bars2)
    add_labels(bars3)
    
    plt.xlabel('label')
    plt.ylabel('점수 (텍스트 1000자당)')
    plt.title('label별 평균 수사학적 요소 점수')
    plt.xticks(x, labels)
    plt.legend()
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    plt.tight_layout()
    plt.show()
    
    # label별로 타이틀마다의 수사학적 요소 시각화
    # 각 label별로 별도의 그래프 생성
    unique_labels = results_df['label'].unique()
    
    for label in unique_labels:
        # 현재 label에 해당하는 데이터만 필터링
        label_data = results_df[results_df['label'] == label]
        
        plt.figure(figsize=(14, 8))
        
        # 그래프 데이터 준비
        titles = label_data['title']
        pathos = label_data['pathos_score']
        ethos = label_data['ethos_score']
        logos = label_data['logos_score']
        
        x = np.arange(len(titles))  # 타이틀 위치
        width = 0.25  # 막대 너비
        
        # 막대 그래프 생성
        plt.bar(x - width, pathos, width, label='파토스', color='#FF9999')
        plt.bar(x, ethos, width, label='에토스', color='#66B2FF')
        plt.bar(x + width, logos, width, label='로고스', color='#99CC99')
        
        plt.xlabel('텍스트')
        plt.ylabel('점수 (텍스트 1000자당)')
        plt.title(f'label "{label}"의 텍스트별 수사학적 요소 비교')
        
        # 타이틀이 너무 길면 자르기
        plt.xticks(x, [t[:10] + '...' if len(t) > 10 else t for t in titles], rotation=45, ha='right')
        plt.legend()
        plt.grid(axis='y', linestyle='--', alpha=0.7)
        
        plt.tight_layout()
        plt.show()
    
    return

def main():
    # 폰트 설정
    setup_fonts()
    
    # 데이터 로드
    df = load_data()
    
    # 텍스트 분석
    results_df = analyze_texts(df)
    
    # 결과 출력
    print("분석 결과:")
    print(results_df[['title', 'pathos_score', 'ethos_score', 'logos_score']].to_string(index=False))
    
    # 결과 시각화
    visualize_results(results_df)

if __name__ == "__main__":
    main()