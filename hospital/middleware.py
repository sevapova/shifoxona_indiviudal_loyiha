from django.utils import translation

class ForceLanguageMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # 1. Get language directly from cookie
        language = request.COOKIES.get('django_language', 'uz')
        if language not in ['uz', 'ru', 'en']:
            language = 'uz'
            
        # 2. FORCE activate this language
        translation.activate(language)
        request.LANGUAGE_CODE = language
        
        # 3. Save to session if available
        if hasattr(request, 'session'):
            request.session['django_language'] = language
            
        response = self.get_response(request)
        
        # 4. Ensure the response also carries the correct cookie
        response.set_cookie('django_language', language)
        return response
