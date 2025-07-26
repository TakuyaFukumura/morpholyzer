from django.test import TestCase, Client
from django.urls import reverse
import json
from .analyzer import MorphologicalAnalyzer
from .forms import TextAnalysisForm


class MorphologicalAnalyzerTestCase(TestCase):
    """形態素解析クラスのテスト"""
    
    def setUp(self):
        """テストセットアップ"""
        self.analyzer = MorphologicalAnalyzer()
    
    def test_basic_analysis(self):
        """基本的な形態素解析テスト"""
        text = "これは日本語のテストです。"
        result = self.analyzer.analyze(text)
        
        # 結果が空でないことを確認
        self.assertGreater(len(result), 0)
        
        # 最初の形態素が「これ」であることを確認
        self.assertEqual(result[0]['surface'], 'これ')
        self.assertEqual(result[0]['pos'], '名詞')
        
        # 必要なキーが全て含まれていることを確認
        required_keys = ['surface', 'pos', 'pos_detail1', 'pos_detail2', 
                        'pos_detail3', 'inflection_type', 'inflection_form', 
                        'base_form', 'reading', 'pronunciation']
        for key in required_keys:
            self.assertIn(key, result[0])
    
    def test_empty_text_analysis(self):
        """空文字列の解析テスト"""
        result = self.analyzer.analyze("")
        self.assertEqual(len(result), 0)
        
        result = self.analyzer.analyze("   ")
        self.assertEqual(len(result), 0)
    
    def test_pos_summary(self):
        """品詞統計テスト"""
        text = "私は学生です。"
        morphemes = self.analyzer.analyze(text)
        pos_summary = self.analyzer.get_pos_summary(morphemes)
        
        # 品詞統計が辞書形式で返されることを確認
        self.assertIsInstance(pos_summary, dict)
        
        # 名詞が含まれていることを確認
        self.assertIn('名詞', pos_summary)
    
    def test_special_characters(self):
        """特殊文字を含むテキストの解析テスト"""
        text = "Hello、世界！123"
        result = self.analyzer.analyze(text)
        
        # 何らかの結果が返されることを確認
        self.assertGreater(len(result), 0)


class TextAnalysisFormTestCase(TestCase):
    """フォームのテスト"""
    
    def test_valid_form(self):
        """有効なフォームデータのテスト"""
        form_data = {'text': 'これはテストです。'}
        form = TextAnalysisForm(data=form_data)
        self.assertTrue(form.is_valid())
    
    def test_empty_form(self):
        """空のフォームのテスト"""
        form_data = {'text': ''}
        form = TextAnalysisForm(data=form_data)
        self.assertFalse(form.is_valid())
    
    def test_max_length_validation(self):
        """文字数制限のテスト"""
        # 1000文字を超えるテキスト
        long_text = 'あ' * 1001
        form_data = {'text': long_text}
        form = TextAnalysisForm(data=form_data)
        self.assertFalse(form.is_valid())


class ViewsTestCase(TestCase):
    """ビューのテスト"""
    
    def setUp(self):
        """テストセットアップ"""
        self.client = Client()
    
    def test_index_view_get(self):
        """インデックスページのGETリクエストテスト"""
        response = self.client.get(reverse('morpholyzer:index'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, '形態素解析ツール')
        self.assertContains(response, 'form')
    
    def test_index_view_post_valid(self):
        """インデックスページの有効なPOSTリクエストテスト"""
        response = self.client.post(reverse('morpholyzer:index'), {
            'text': 'これはテストです。'
        })
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'これ')  # 解析結果が表示されているか
        self.assertContains(response, '名詞')  # 品詞が表示されているか
    
    def test_index_view_post_invalid(self):
        """インデックスページの無効なPOSTリクエストテスト"""
        response = self.client.post(reverse('morpholyzer:index'), {
            'text': ''
        })
        self.assertEqual(response.status_code, 200)
        # エラーメッセージやフォームエラーが表示されることを確認
        self.assertContains(response, 'form')
    
    def test_api_analyze_post_valid(self):
        """API解析エンドポイントの有効なPOSTリクエストテスト"""
        response = self.client.post(reverse('morpholyzer:api_analyze'), {
            'text': 'これはテストです。'
        })
        self.assertEqual(response.status_code, 200)
        
        # JSON形式の応答を確認
        data = json.loads(response.content)
        self.assertTrue(data['success'])
        self.assertIn('morphemes', data)
        self.assertIn('pos_summary', data)
        self.assertGreater(data['total_morphemes'], 0)
    
    def test_api_analyze_post_empty(self):
        """API解析エンドポイントの空テキストPOSTリクエストテスト"""
        response = self.client.post(reverse('morpholyzer:api_analyze'), {
            'text': ''
        })
        self.assertEqual(response.status_code, 400)
        
        data = json.loads(response.content)
        self.assertIn('error', data)
    
    def test_api_analyze_get_method(self):
        """API解析エンドポイントのGETリクエストテスト（エラー）"""
        response = self.client.get(reverse('morpholyzer:api_analyze'))
        self.assertEqual(response.status_code, 405)
        
        data = json.loads(response.content)
        self.assertIn('error', data)
