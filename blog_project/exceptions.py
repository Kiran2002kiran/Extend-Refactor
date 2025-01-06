########code1
from rest_framework.response import Response  
from rest_framework import status
from rest_framework.views import exception_handler   
def custom_exception_handler(exc, context):    
    # Call DRF's default exception handler to get the standard error response.
    response = exception_handler(exc, context)

    # If a response exists, modify it.
    if response is not None:
        response.data['status'] = 'error'
        response.data['error_code'] = exc.__class__.__name__.upper()  # Use exception class name as error code
        response.data['message'] = response.data.get('detail', 'An error occurred.')
        response.data.pop('detail', None)  # Remove 'detail' field if it exists

    # If no response exists (e.g., server error), create a custom response.
    else:
        response = Response(
            {
                'status': 'error',
                'error_code': 'SERVER_ERROR',
                'message': 'An internal server error occurred.',
            },
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )

    return response

