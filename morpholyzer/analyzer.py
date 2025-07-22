import MeCab


class MorphologicalAnalyzer:
    """MeCabを使用した形態素解析クラス"""
    
    def __init__(self):
        """MeCabタガーを初期化"""
        try:
            # MeCabの設定ファイルを明示的に指定
            self.tagger = MeCab.Tagger('-r /etc/mecabrc')
        except Exception as e:
            # フォールバックとしてデフォルト設定を試行
            try:
                self.tagger = MeCab.Tagger()
            except Exception:
                raise Exception(f"MeCabの初期化に失敗しました: {e}")
    
    def analyze(self, text):
        """
        テキストを形態素解析する
        
        Args:
            text (str): 解析対象のテキスト
            
        Returns:
            list: 形態素解析結果のリスト。各要素は辞書形式で以下のキーを含む:
                - surface: 表層形
                - pos: 品詞
                - pos_detail1: 品詞細分類1
                - pos_detail2: 品詞細分類2
                - pos_detail3: 品詞細分類3
                - inflection_type: 活用型
                - inflection_form: 活用形
                - base_form: 原形
                - reading: 読み
                - pronunciation: 発音
        """
        if not text or not text.strip():
            return []
        
        # MeCabで解析実行
        result = self.tagger.parse(text)
        
        # 結果をパース
        morphemes = []
        lines = result.strip().split('\n')
        
        for line in lines:
            if line == 'EOS':  # End of Sentence
                break
                
            # タブで表層形と詳細情報を分割
            parts = line.split('\t')
            if len(parts) != 2:
                continue
                
            surface = parts[0]
            features = parts[1].split(',')
            
            # 特徴量が9個未満の場合はパディング
            while len(features) < 9:
                features.append('*')
            
            morpheme = {
                'surface': surface,
                'pos': features[0] if len(features) > 0 else '*',
                'pos_detail1': features[1] if len(features) > 1 else '*',
                'pos_detail2': features[2] if len(features) > 2 else '*',
                'pos_detail3': features[3] if len(features) > 3 else '*',
                'inflection_type': features[4] if len(features) > 4 else '*',
                'inflection_form': features[5] if len(features) > 5 else '*',
                'base_form': features[6] if len(features) > 6 else '*',
                'reading': features[7] if len(features) > 7 else '*',
                'pronunciation': features[8] if len(features) > 8 else '*',
            }
            
            morphemes.append(morpheme)
        
        return morphemes
    
    def get_pos_summary(self, morphemes):
        """
        品詞の統計情報を取得
        
        Args:
            morphemes (list): 形態素解析結果のリスト
            
        Returns:
            dict: 品詞ごとの出現回数
        """
        pos_count = {}
        for morpheme in morphemes:
            pos = morpheme['pos']
            pos_count[pos] = pos_count.get(pos, 0) + 1
        
        return pos_count