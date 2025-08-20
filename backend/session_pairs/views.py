from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST, require_GET
import json
from .models import SessionComparison, Session

@csrf_exempt
@require_POST
def add_comparison(request):
    try:
        data = json.loads(request.body)
        session_id_1 = data.get('session_id_1')
        session_id_2 = data.get('session_id_2')
        preferred = data.get('preferred')

        if preferred not in [1, 2]:
            return JsonResponse({'error': "The 'preferred' value must be either 1 or 2."}, status=400)

        comparison = SessionComparison.objects.create(
            session_id_1=session_id_1,
            session_id_2=session_id_2,
            preferred=preferred
        )

        return JsonResponse({'message': f'Successfully added comparison: {session_id_1} vs {session_id_2} -> Preferred: {preferred}'}, status=201)

    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON'}, status=400)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

@require_GET
def get_session_pair(request):
    try:
        # Get two random sessions from the database
        random_sessions = Session.objects.order_by('?').values('name', 'data')[:2]

        if len(random_sessions) < 2:
            return JsonResponse({
                'error': 'Not enough sessions in the database to form a pair. Run the populate_sessions command.'
            }, status=500)

        # Structure the data for the JSON response
        response_data = {
            'session_1': {
                'name': random_sessions[0]['name'],
                'data': random_sessions[0]['data']
            },
            'session_2': {
                'name': random_sessions[1]['name'],
                'data': random_sessions[1]['data']
            }
        }
        
        return JsonResponse(response_data, status=200)

    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)