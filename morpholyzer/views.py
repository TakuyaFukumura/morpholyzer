from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .forms import TextAnalysisForm
from .analyzer import MorphologicalAnalyzer


def index(request):
    """メインページ"""
    form = TextAnalysisForm()
    morphemes = []
    pos_summary = {}
    original_text = ''
    error_message = ''
    
    if request.method == 'POST':
        form = TextAnalysisForm(request.POST)
        if form.is_valid():
            text = form.cleaned_data['text']
            original_text = text
            
            try:
                analyzer = MorphologicalAnalyzer()
                morphemes = analyzer.analyze(text)
                pos_summary = analyzer.get_pos_summary(morphemes)
            except Exception as e:
                error_message = f'形態素解析でエラーが発生しました: {str(e)}'
    
    context = {
        'form': form,
        'morphemes': morphemes,
        'pos_summary': pos_summary,
        'original_text': original_text,
        'error_message': error_message,
    }
    
    return render(request, 'morpholyzer/index.html', context)


@csrf_exempt
def api_analyze(request):
    """API エンドポイント（JSON形式での解析結果を返す）"""
    if request.method == 'POST':
        text = request.POST.get('text', '')
        
        if not text:
            return JsonResponse({'error': 'テキストが入力されていません。'}, status=400)
        
        try:
            analyzer = MorphologicalAnalyzer()
            morphemes = analyzer.analyze(text)
            pos_summary = analyzer.get_pos_summary(morphemes)
            
            return JsonResponse({
                'success': True,
                'original_text': text,
                'morphemes': morphemes,
                'pos_summary': pos_summary,
                'total_morphemes': len(morphemes)
            })
        
        except Exception as e:
            return JsonResponse({'error': f'形態素解析でエラーが発生しました: {str(e)}'}, status=500)
    
    return JsonResponse({'error': 'POSTメソッドのみサポートしています。'}, status=405)
