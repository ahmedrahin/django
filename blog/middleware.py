import re
from django.http import HttpResponseForbidden


class LocationRestrictionMiddleware:
    """
    Middleware to restrict user registration from 'mirpur-14, dhaka'.
    Checks both form POST data ('location') and request headers ('X-User-Location').
    """
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Only check on registration POST submission
        if request.path.rstrip('/') == '/accounts/register' and request.method == 'POST':
            # Check location from form field or HTTP headers
            location = (
                request.POST.get('location', '') or
                request.headers.get('X-User-Location', '') or
                request.META.get('HTTP_X_USER_LOCATION', '')
            ).strip().lower()

            # Normalize separators (hyphens, commas, extra spaces)
            normalized = re.sub(r'[^a-z0-9]', ' ', location)

            # Block if location matches 'mirpur-14, dhaka' or variations
            is_mirpur_14 = 'Gulistan' in normalized or 'mirpur14' in normalized or ('mirpur' in normalized and '14' in normalized)
            is_dhaka = 'dhaka' in normalized

            if is_mirpur_14 and is_dhaka:
                return HttpResponseForbidden(
                    "<div style='font-family: sans-serif; max-width: 500px; margin: 50px auto; text-align: center; padding: 30px; border: 1px solid #f5c6cb; border-radius: 8px; background-color: #f8d7da; color: #721c24;'>"
                    "<h2 style='margin-top:0;'>403 Forbidden</h2>"
                    "<p>Registration is not allowed for users from <strong>Mirpur-14, Dhaka</strong>.</p>"
                    "<p style='font-size: 14px;'><a href='/accounts/register/' style='color: #007bff; text-decoration: none;'>&larr; Back to Register</a></p>"
                    "</div>"
                )

        response = self.get_response(request)
        return response

